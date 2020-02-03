import attr
from pathlib import Path
import re

from pylexibank import Lexeme, Language
from pylexibank.providers.clld import CLLD
from pylexibank.util import progressbar
from pylexibank import FormSpec

from clldutils.misc import slug


@attr.s
class CustomLexeme(Lexeme):
    Word_ID = attr.ib(default=None)
    word_source = attr.ib(default=None)
    Borrowed = attr.ib(default=None)
    Borrowed_score = attr.ib(default=None)
    comment_on_borrowed = attr.ib(default=None)
    comment_on_word_form = attr.ib(default=None)
    borrowed_base = attr.ib(default=None)
    other_comments = attr.ib(default=None)
    loan_history = attr.ib(default=None)
    Analyzability = attr.ib(default=None)
    Simplicity_score = attr.ib(default=None)
    reference = attr.ib(default=None)
    numeric_frequency = attr.ib(default=None)
    age_label = attr.ib(default=None)
    gloss = attr.ib(default=None)
    integration = attr.ib(default=None)
    salience = attr.ib(default=None)
    effect = attr.ib(default=None)
    contact_situation = attr.ib(default=None)
    original_script = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    Longitude = attr.ib(default=None)
    Latitude = attr.ib(default=None)
    ISO639P3code = attr.ib(default=None)
    WOLD_ID = attr.ib(default=None)


def normalize_text(text):
    text = text.replace("\n", " // ")
    text = re.sub(r"\s+", " ", text).strip()

    return text


class Dataset(CLLD):
    __cldf_url__ = "http://cdstar.shh.mpg.de/bitstreams/EAEA0-92F4-126F-089F-0/wold_dataset.cldf.zip"
    dir = Path(__file__).parent
    id = "wold"
    lexeme_class = CustomLexeme
    language_class = CustomLanguage
    form_spec = FormSpec(
        separators="~,",
        first_form_only=True,
        brackets={},  # each language is different, need to do manually
        replacements=[
            (" ", "_"),
            ("(1)", ""),
            ("(2)", ""),
            ("(2", ""),
            ("(3)", ""),
            ("(4)", ""),
            ("(5)", ""),
            ("(6)", ""),
            ("(f.)", ""),
        ],
    )

    def cmd_makecldf(self, args):
        # add the bibliographic sources
        args.writer.add_sources()

        # add the languages from the language file
        # NOTE: the source lists all languages, including proto-languages,
        # but the `forms` only include the first 41 in the list
        language_lookup = args.writer.add_languages(lookup_factory="WOLD_ID")

        # add concepts
        concept_lookup = {}
        for concept in self.conceptlists[0].concepts.values():
            concept_id = "%s_%s" % (concept.number, slug(concept.english))
            args.writer.add_concept(
                ID=concept_id,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            concept_lookup[concept.attributes["wold_id"]] = concept_id

        # As some concepts are missing from the concept list, we need to
        # collect them here and add them
        # TODO: Integrate to Concepticon
        for parameter in self.raw_dir.read_csv("parameters.csv", dicts=True):
            if parameter["ID"] not in concept_lookup:
                concept_id = "%s_%s" % (
                    parameter["ID"].replace("-", ""),
                    slug(parameter["Name"]),
                )
                args.writer.add_concept(ID=concept_id, Name=parameter["Name"])
                concept_lookup[parameter["ID"]] = concept_id

        # read raw form data
        lexemes_rows = self.raw_dir.read_csv("forms.csv", dicts=True)
        for row in progressbar(lexemes_rows):
            # Add information not in row, so we can pass to `add_form()`
            # with a single comprehension
            row["Language_ID"] = language_lookup[row["Language_ID"]]
            row["Parameter_ID"] = concept_lookup[row["Parameter_ID"]]

            row["Value"] = row["Form"]
            row["Loan"] = float(row["BorrowedScore"]) > 0.6
            row["original_script"] = normalize_text(row["original_script"])
            row["comment_on_borrowed"] = normalize_text(
                row["comment_on_borrowed"]
            )
            row.pop("Segments")

            # CHECK: Manually apply replacaments from `etc/lexemes.csv`
            row["Form"] = self.lexemes.get(row["Form"], row["Form"])

            # CHECK: Manually separate using `form_spec`
            # NOTE: We cannot separate over slashes in all languages because
            #       in a number of them the slash is actually an orthographic
            #       character
            for sep in self.form_spec.separators:
                row["Form"] = row["Form"].split(sep)[0].strip()
            if row["Language_ID"] in [
                "Oroqen",
                "Romanian",
                "SeychellesCreole",
                "LowerSorbian",
                "SeliceRomani",
                "OldHighGerman",
                "Kanuri",
                "Mapudungun",
            ]:
                row["Form"] = row["Form"].split("/")[0].strip()

            # CHECK: Manually apply replacements from `form_spec`
            for repl in sorted(
                self.form_spec.replacements,
                key=lambda r: len(r[0]),
                reverse=True,
            ):
                row["Form"] = row["Form"].replace(repl[0], repl[1]).strip()

            args.writer.add_form(
                **{
                    k: v
                    for k, v in row.items()
                    if k in self.lexeme_class.fieldnames()
                }
            )

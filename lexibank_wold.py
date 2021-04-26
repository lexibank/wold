import re
from pathlib import Path

import attr
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
    return re.sub(r"\s+", " ", text).strip()


def format_citation(contrib, numentries):
    authors = contrib["Contributors"]
    if " with " in authors:
        authors = authors.replace(" with ", " (with ") + ")"
    return (
        "{}. 2009. {} vocabulary. In: Haspelmath, Martin & Tadmor, Uri (eds.) "
        "World Loanword Database. Leipzig: Max Planck Institute for Evolutionary Anthropology, "
        "{} entries. (Available online at https://wold.clld.org/vocabulary/{})".format(
            authors, contrib["Name"], numentries, contrib["ID"]
        )
    )


class Dataset(CLLD):
    __cldf_url__ = (
        "http://cdstar.shh.mpg.de/bitstreams/EAEA0-92F4-126F-089F-0/wold_dataset.cldf.zip"
    )
    dir = Path(__file__).parent
    id = "wold"
    lexeme_class = CustomLexeme
    language_class = CustomLanguage
    form_spec = FormSpec(
        separators="~,",
        first_form_only=True,
        brackets={},  # each language is different, need to do manually
        replacements=[
            (" (1)", ""),
            (" (2)", ""),
            (" (3)", ""),
            (" (4)", ""),
            (" (5)", ""),
            (" (6)", ""),
            ("(f.)", ""),
            ("(1)", ""),
            ("(2)", ""),
            ("(3)", ""),
            ("(4)", ""),
            ("(5)", ""),
            ("(6)", ""),
            ("(2", ""),
            (" ", "_"),
        ],
    )

    def cmd_makecldf(self, args):
        args.writer.add_sources()

        # add the languages from the language file
        # NOTE: the source lists all languages, including proto-languages,
        # but the `forms` only include the first 41 in the list
        language_lookup = args.writer.add_languages(lookup_factory="WOLD_ID")
        t = args.writer.cldf.add_table(
            "vocabularies.csv",
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id",
                "dc:description": "The vocabulary ID number corresponds to the ordering to the"
                " chapters on the book <em>Loanwords in the World's Languages</em>. "
                "Languages are listed in rough geographical order from west to east, "
                "from Africa via Europe to Asia and the Americas, so that "
                "geographically adjacent languages are next to each other.",
            },
            {"name": "Name", "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#name"},
            {
                "name": "Citation",
                "dc:description": "Each vocabulary of WOLD is a separate electronic publication "
                "with a separate author or team of authors and should be cited as specified "
                "here.",
                "propertyUrl": "dc:bibliographicCitation",
            },
            {
                "name": "Authors",
                "dc:description": "The authors are experts of the language and its history. "
                "They also contributed a prose chapter on the borrowing situation in "
                "their language that was published in the book "
                "Loanwords in the World's Languages.",
                "propertyUrl": "dc:creator",
            },
            {
                "name": "Number_of_words",
                "datatype": "integer",
                "dc:description": "There would be 1814 words in each vocabulary, "
                "corresponding to the 1814 Loanword Typology meanings, if each meaning "
                "had exactly one counterpart, and if all the counterparts were "
                'different words. But many ("polysomous") words are counterparts of '
                "several meanings, many meanings have several word counterparts "
                '("synonyms", or "subcounterparts"), and many meanings have no '
                "counterparts at all, so the number of words in each database varies "
                "considerably.",
            },
            {
                "name": "Language_ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#languageReference",
            },
        )
        t.add_foreign_key("Language_ID", "languages.csv", "ID")

        numentries = {
            r["pk"]: int(r["count_words"])
            for r in self.raw_dir.joinpath("db").read_csv("vocabulary.csv", dicts=True)
        }
        for contrib in self.raw_dir.read_csv("contributions.csv", dicts=True):
            args.writer.objects["vocabularies.csv"].append(
                dict(
                    ID=contrib["ID"],
                    Name="{} vocabulary".format(contrib["Name"]),
                    Citation=format_citation(contrib, numentries[contrib["ID"]]),
                    Authors=contrib["Contributors"],
                    Number_of_words=numentries[contrib["ID"]],
                    Language_ID=language_lookup[contrib["ID"]],
                )
            )

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
                concept_id = "%s_%s" % (parameter["ID"].replace("-", ""), slug(parameter["Name"]))
                args.writer.add_concept(ID=concept_id, Name=parameter["Name"])
                concept_lookup[parameter["ID"]] = concept_id

        # read raw form data
        lexemes_rows = self.raw_dir.read_csv("forms.csv", dicts=True)
        for row in progressbar(lexemes_rows):
            # Add information not in row, so we can pass to `add_form()`
            # with a single comprehension
            row["Language_ID"] = language_lookup[row["Language_ID"]]
            row["Parameter_ID"] = concept_lookup[row["Parameter_ID"]]

            row["Value"] = row.pop("Form")
            row["Loan"] = float(row["BorrowedScore"]) > 0.6
            row["Borrowed_score"] = row["BorrowedScore"]
            row["original_script"] = normalize_text(row["original_script"])
            row["comment_on_borrowed"] = normalize_text(row["comment_on_borrowed"])
            row.pop("Segments")

            args.writer.add_forms_from_value(
                **{k: v for k, v in row.items() if k in self.lexeme_class.fieldnames()}
            )

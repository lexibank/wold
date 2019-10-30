import attr
from pathlib import Path
import re
import unicodedata

from pylexibank import Lexeme
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar
from segments import Tokenizer, Profile
from segments.tree import Tree


@attr.s
class WOLDLexeme(Lexeme):
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


def _replace_newlines(text):
    text = text.replace("\n", " // ")
    text = re.sub("\s+", " ", text)

    return text


class Dataset(BaseDataset):
    __cldf_url__ = "http://cdstar.shh.mpg.de/bitstreams/EAEA0-92F4-126F-089F-0/wold_dataset.cldf.zip"
    dir = Path(__file__).parent
    id = "wold"
    lexeme_class = WOLDLexeme

    def _build_tokenizer(self, language):
        # build a tokenizer for a given profile
        profile_file = "%s.profile.tsv" % language
        profile_path = str(self.dir / "etc" / profile_file)
        profile = Profile.from_file(profile_path, form="NFC")
        default_spec = list(next(iter(profile.graphemes.values())).keys())
        profile.tree = Tree(list(profile.graphemes.keys()))
        tokenizer = Tokenizer(
            profile=profile, errors_replace=lambda c: "<{0}>".format(c)
        )

        def _tokenizer(item, string, **kw):
            kw.setdefault("column", "IPA")
            kw.setdefault("separator", " + ")
            return tokenizer(
                unicodedata.normalize("NFC", "^%s$" % string), **kw
            ).split()

        return _tokenizer

    def cmd_makecldf(self, args):
        # add the bibliographic sources
        args.writer.add_sources()

        # add the languages from the language file
        # NOTE: the source lists all languages, including proto-languages,
        # but the `forms` only include the first 41 in the list
        languages = self.raw_dir.read_csv("languages.csv", dicts=True)
        for language in languages:
            args.writer.add_language(
                ID=language["ID"],
                Name=language["Name"],
                Glottocode=language["Glottocode"],
            )

        # Build the tokenizers for each language, mapping from the
        # language["ID"] to the tokenizer (which is built using the glottocode
        # for the language)
        tokenizer = {
            language["ID"]: self._build_tokenizer(language["Glottocode"])
            for language in languages[:41]
        }

        # add concepts
        # NOTE: need to read the data from parameters.csv as well,
        # as the IDs found in forms.csv are not in concept list...
        conceptlist = {
            concept.attributes["wold_id"]: {
                "id": concept.id,
                "concepticon_id": concept.concepticon_id,
                "concepticon_gloss": concept.concepticon_gloss,
            }
            for concept in self.conceptlist.concepts.values()
        }
        for parameter in self.raw_dir.read_csv("parameters.csv", dicts=True):
            args.writer.add_concept(
                ID=parameter["ID"],
                Concepticon_ID=conceptlist.get(parameter["ID"], {}).get(
                    "concepticon_id", None
                ),
                Concepticon_Gloss=conceptlist.get(parameter["ID"], {}).get(
                    "concepticon_gloss", None
                ),
                Name=parameter["Name"],
            )

        # read raw form data
        lexemes_rows = self.raw_dir.read_csv("forms.csv", dicts=True)
        for row in progressbar(lexemes_rows):
            # This is long, but better to keep it explicit
            # TODO: original script as value? sources?
            args.writer.add_form_with_segments(
                Language_ID=row["Language_ID"],
                Parameter_ID=row["Parameter_ID"],
                Form=row["Form"],
                Value=row["Form"],
                Source=row["Source"].split(";"),
                Segments=tokenizer[row["Language_ID"]]({}, row["Form"]),
                Loan=float(row["BorrowedScore"]) > 0.6,
                word_source=row["word_source"],
                Word_ID=row["Word_ID"],
                Borrowed=row["Borrowed"],
                Borrowed_score=row["BorrowedScore"],
                comment_on_borrowed=_replace_newlines(row["comment_on_borrowed"]),
                Analyzability=row["Analyzability"],
                Simplicity_score=row["SimplicityScore"],
                reference=row["reference"],
                age_label=row["age_label"],
                gloss=_replace_newlines(row["gloss"]),
                integration=row["integration"],
                salience=row["salience"],
                effect=row["effect"],
                contact_situation=row["ContactSituation"],
                original_script=row["original_script"],
                comment_on_word_form=_replace_newlines(row["comment_on_word_form"]),
                other_comments=_replace_newlines(row["other_comments"]),
                loan_history=_replace_newlines(row["loan_history"]),
                borrowed_base=_replace_newlines(row["borrowed_base"]),
            )

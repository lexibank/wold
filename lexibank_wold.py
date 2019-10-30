import attr
from pathlib import Path
import re

from pylexibank import Lexeme
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar


@attr.s
class WOLDLexeme(Lexeme):
    Word_ID = attr.ib(default=None)
    word_source = attr.ib(default=None)
    Borrowed = attr.ib(default=None)
    Borrowed_score = attr.ib(default=None)
    comment_on_borrowed = attr.ib(default=None)
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

    def cmd_makecldf(self, args):
        # add the bibliographic sources
        args.writer.add_sources()

        # add the languages from the language file
        languages = self.raw_dir.read_csv("languages.csv", dicts=True)
        for language in languages:
            args.writer.add_language(
                ID=language["ID"],
                Name=language["Name"],
                Glottocode=language["Glottocode"],
            )

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
            args.writer.add_form(
                Language_ID=row["Language_ID"],
                Parameter_ID=row["Parameter_ID"],
                Form=row["Form"],
                Value=row["Form"],
                Source=row["Source"].split(";"),
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
                gloss=row["gloss"],  # needed?
                integration=row["integration"],
                salience=row["salience"],
                effect=row["effect"],
                contact_situation=row["ContactSituation"],
                original_script=row["original_script"],
            )

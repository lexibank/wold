import attr
from pathlib import Path
import re

from pylexibank import FormSpec
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


def normalize_comments(text):
    text = text.replace("\n", " // ")
    text = re.sub("\s+", " ", text)

    return text


class Dataset(BaseDataset):
    __cldf_url__ = "http://cdstar.shh.mpg.de/bitstreams/EAEA0-92F4-126F-089F-0/wold_dataset.cldf.zip"
    dir = Path(__file__).parent
    id = "wold"
    lexeme_class = WOLDLexeme

    def cmd_download(self, args):
        if not self.raw_dir.exists():
            self.raw_dir.mkdir()

        files = ["borrowings.csv"]
        self.raw_dir.download_and_unpack(
            self.__cldf_url__, *[Path(f) for f in files]
        )

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
            # Add information not in row, so we can pass to `add_form()`
            # with a single comprehension
            row["Value"] = row["Form"]
            row["Loan"] = float(row["BorrowedScore"]) > 0.6
            row["comment_on_borrowed"] = normalize_comments(
                row["comment_on_borrowed"]
            )
            row.pop("Segments")

            args.writer.add_form(
                **{
                    k: v
                    for k, v in row.items()
                    if k in self.lexeme_class.fieldnames()
                }
            )

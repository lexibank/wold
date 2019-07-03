import attr
from clldutils.path import Path
from pylexibank.dataset import Lexeme
from pylexibank.providers import clld


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


class Dataset(clld.CLLD):
    __cldf_url__ = (
        "http://cdstar.shh.mpg.de/bitstreams/EAEA0-92F4-126F-089F-0/wold_dataset.cldf.zip"
    )
    dir = Path(__file__).parent
    id = "wold"
    lexeme_class = WOLDLexeme

    def cmd_install(self, **kw):
        ccode = {
            x.attributes["wold_id"]: x.concepticon_id for x in self.conceptlist.concepts.values()
        }

        fields = self.lexeme_class.fieldnames()
        with self.cldf as ds:
            vocab_ids = [v["ID"] for v in self.original_cldf["contributions.csv"]]

            self.add_sources(ds)

            for row in self.original_cldf["LanguageTable"]:
                gc, iso = row["Glottocode"], row["ISO639P3code"]
                if gc == "tzot1264":
                    gc, iso = "tzot1259", "tzo"
                if row["ID"] in vocab_ids:
                    ds.add_language(ID=row["ID"], Name=row["Name"], Glottocode=gc, ISO639P3code=iso)

            for row in self.original_cldf["ParameterTable"]:
                ds.add_concept(
                    ID=row["ID"], Name=row.pop("Name"), Concepticon_ID=ccode.get(row["ID"])
                )

            for row in self.original_cldf["FormTable"]:
                if row["Language_ID"] in vocab_ids:
                    del row["ID"]
                    row["Value"] = row.pop("Form")
                    # Note: We count words marked as "probably borrowed" as loans.
                    row["Loan"] = float(row["BorrowedScore"]) > 0.6
                    ds.add_lexemes(**{k: v for k, v in row.items() if k in fields})

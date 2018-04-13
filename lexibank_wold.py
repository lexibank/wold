# coding: utf8
from __future__ import unicode_literals, print_function, division

import attr
from clldutils.path import Path

from pylexibank.providers import clld
from pylexibank.dataset import Metadata, Lexeme


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


class Dataset(clld.CLLD):
    __cldf_url__ = "http://cdstar.shh.mpg.de/bitstreams/EAEA0-4F9C-34D7-78A3-0/wold_dataset.cldf.zip"
    dir = Path(__file__).parent
    lexeme_class = WOLDLexeme

    def cmd_install(self, **kw):
        fields = self.lexeme_class.fieldnames()
        with self.cldf as ds:
            self.add_sources(ds)
            for row in self.iteritems():
                if row['Language_ID'] == 'None':
                    row['Language_ID'] = None

                ds.add_language(
                    ID=row['Language_name'],
                    name=row['Language_name'],
                    glottocode=row['Language_ID'])
                row['Language_ID'] = row.pop('Language_name')

                ds.add_concept(
                    ID=row['WOLD_Meaning_ID'],
                    conceptset=row['Parameter_ID'])
                row['Parameter_ID'] = row.pop('WOLD_Meaning_ID')

                del row['ID']
                # Note: We count words marked as "probably borrowed" as loans.
                row['Loan'] = float(row['Borrowed_score']) > 0.6
                ds.add_lexemes(**{k: v for k, v in row.items() if k in fields})

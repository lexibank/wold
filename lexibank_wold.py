import re
import json
import decimal
import pathlib
import collections

from csvw.metadata import URITemplate
import attr
from pylexibank import Lexeme, Language, Concept, Dataset as Base
from pylexibank.util import progressbar
from pylexibank import FormSpec

from util import vocabulary_description


def valid_gloss(inst, attr, value):
    if value:
        if not (('analyzable ' in inst.Analyzability) or ('semi-analyzable' in inst.Analyzability)):
            raise ValueError('gloss for unanalyzable word! {}: {}: {}'.format(inst.Analyzability, inst.Form, value))
        if '[' not in value:
            print(value)
            return
        morphemes, gloss = value.split('[', maxsplit=1)
        if not gloss.endswith(']'):
            print(value)
            return
        gloss = gloss[:-1]
        morphemes = morphemes.strip().split()
        gloss = gloss.split()
        if len(gloss) != len(morphemes):
            print('{} :: {}'.format(morphemes, gloss))
            return
        for m, g in zip(morphemes, gloss):
            if len(m.split('-')) != len(g.split('-')):
                print('{} :: {}'.format(m, g))
                return


@attr.s
class WoldLexeme(Lexeme):
    Word_ID = attr.ib(
        default=None,
        metadata={
            'dc:description': 'ID of the corresponding word in the WOLD database.'
        }
    )
    original_script = attr.ib(
        default=None,
        metadata={
            'dc:description':
                "If the language has no conventional orthography, the contributor's own "
                "transcription is given as Value. In such cases, the word in the language's usual "
                "writing system is provided in this field."
        }
    )
    comment_on_word_form = attr.ib(default=None)
    Borrowed = attr.ib(
        default=None,
        metadata={
            'dc:description': """\
The likelihood of borrowing of a word was categorized as follows:

1. clearly borrowed.
2. probably borrowed.
3. perhaps borrowed.
4. very little evidence for borrowing.
5. no evidence for borrowing.
"""}
    )
    Borrowed_score = attr.ib(
        default=None,
        metadata={
            'datatype': {
                'base': 'decimal', 'minimum': decimal.Decimal('0.0'), 'maximum': decimal.Decimal('1.0')},
            'dc:description': """\
The following borrowed scores are assigned to words depending on the degree of likelihood of borrowing:

1. clearly borrowed:    1.00
2. probably borrowed:   0.75
3. perhaps borrowed:    0.50
4. very little evidence for borrowing:  0.25
5. no evidence for borrowing:   0.00
"""}
    )
    comment_on_borrowed = attr.ib(default=None)
    borrowed_base = attr.ib(
        default=None,
        metadata={
            'dc:description': "Indicates whether an analyzable word was derived from a loanword."}
    )
    loan_history = attr.ib(default=None)
    Analyzability = attr.ib(
        default=None,
        converter=lambda s: s or None,
        metadata={
            'datatype': {
                'base': 'string',
                'format': 'analyzable compound|analyzable derived|analyzable phrasal|semi-analyzable|unanalyzable'},
            'dc:description':
                "analyzable (compound or derived or phrasal), semi-analyzable or unanalyzable"
        }
    )
    gloss = attr.ib(
        default=None,
        metadata={
            'dc:description': "Morpheme-by-morpheme gloss for analyzable words."}
    )
    Simplicity_score = attr.ib(
        default=None,
        metadata={
            'datatype': {
                'base': 'decimal', 'minimum': decimal.Decimal('0.5'), 'maximum': decimal.Decimal('1.0')},
            'dc:description': """\
The following simplicity scores are assigned to words depending on their analyzability:

1. unanalyzable:    1.00
2. semi-analyzable: 0.75
3. analyzable:  0.50
""",
        }
    )
    reference = attr.ib(
        default=None,
        metadata={
            'dc:description': "Bibliographic references. For details refer to the vocabulary descriptions."}
    )
    relative_frequency = attr.ib(
        default=None,
        converter=lambda s: s or None,
        metadata={
            'datatype': {
                'base': 'string',
                'format': '1. Very common|2. Fairly common|3. Not common'},
            'dc:description': "Frequency information according to the contributor's intuition - in the absence of representative corpora.",
        }
    )
    numeric_frequency = attr.ib(
        default=None,
        converter=lambda s: float(s.replace(',', '.')) if s else None,
        metadata={
            'datatype': 'float',
            'dc:description': "Occurrences per million words - if significant representative corpora exist."}
    )
    Age = attr.ib(
        default=None,
        converter=lambda s: None if s.lower() == 'no information' or not s else s,
        metadata={
            'dc:description': "Short description of the age of the word. For details refer to the vocabulary descriptions."}
    )
    Age_score = attr.ib(
        default=None,
        metadata={
            'datatype': {
                'base': 'decimal', 'minimum': decimal.Decimal('0.5'), 'maximum': decimal.Decimal('1.0')},
            'dc:description':
                """The following age scores are assigned to words depending on the estimated age of their age class:

1. first attested or reconstructed earlier than 1000:   1.00
2. earlier than 1500:   0.90
3. earlier than 1800:   0.80
4. earlier than 1900:   0.70
5. earlier than 1950:   0.60
6. earlier than 2007:   0.50
"""
        }
    )
    integration = attr.ib(
        default=None,
        metadata={
            'dc:description': """\
1. Highly integrated: no structural properties that betray the foreign origin
2. Intermediate: some synchronic properties of the foreign language
3. Unintegrated: significant phonological and/or morphological properties of the donor language
"""},
    )
    salience = attr.ib(
        default=None,
        converter=lambda s: (s.lower() if s != '""' else None) if s else None,
        metadata={
            'dc:description': """\
Environmental salience of borrowed meanings

no information.
not applicable.
not present: Snow did not exist in Thailand either before or after introduction of the Sanskrit loanword for snow, which nevertheless is known and understood by speakers of Thai.
present in pre-contact environment: There were mountains in England even before the word "mountain" was borrowed from French.
present only since contact: Many South American languages borrowed the word for "horse" from the Spaniards, who introduced it to their environment.
"""},
    )
    effect = attr.ib(
        default=None,
        converter=lambda s: None if s.lower() == 'no information' or not s else s,
        metadata={
            'dc:description': """\
Effect of a loanword on the lexical stock of a recipient language.

Coexistence: the word may coexist with a native word with the same meaning.
Insertion: the word is inserted into the vocabulary as a completely new item.
Replacement: the word may replace an earlier word with the same meaning that falls out of use or changes its meaning.
"""},
    )
    register = attr.ib(
        default=None,
        metadata={
            'dc:description': "Textual description of the register a word is used in."},
    )
    contact_situation = attr.ib(
        default=None,
        metadata={
            'dc:description':
                "Short description of the contact situation that resulted in the loan. "
                "Detailed descriptions are given in the vocabulary description."},
    )
    calqued = attr.ib(
        default=None,
        metadata={
            'dc:description': """\
0. No evidence for calquing
1. Very little evidence for calquing
2. Perhaps calqued
3. Probably calqued
4. Clearly calqued
"""},
    )
    # Vocabulary-specific fields:
    grammatical_info = attr.ib(default=None)
    colonial_word = attr.ib(
        default=None,
        metadata={
            'dc:description': 'Only given for words in the Zinacantán Tzotzil vocabulary.'
        }
    )
    etymological_note = attr.ib(
        default=None,
        metadata={
            'dc:description': 'Only given for words in the Selice Romani vocabulary.'
        }
    )
    lexical_stratum = attr.ib(
        default=None,
        metadata={
            'dc:description': 'Only given for words in the Japanese vocabulary.'
        }
    )
    word_source = attr.ib(
        default=None,
        metadata={
            'dc:description': "Only given for words in the Q'eqchi' vocabulary."
        }
    )


@attr.s
class WoldLanguage(Language):
    WOLD_ID = attr.ib(default=None)


@attr.s
class WoldConcept(Concept):
    Core_list = attr.ib(
        default=None,
        metadata={
            'datatype': {'base': 'boolean', 'format': 'yes|no'},
            'dc:description': 'Indicates whether the concept is one of the 1460 core LWT meanings'}
    )
    Semantic_category = attr.ib(
        default=None,
        metadata={
            'dc:description': "Meanings were assigned to semantic categories with "
                "word-class-like labels: nouns, verbs, adjectives, adverbs, function "
                "words. No claim is made about the grammatical behavior of words "
                "corresponding to these meanings. The categories are intended to be "
                "purely semantic."
        }
    )
    Semantic_field = attr.ib(
        default=None,
        metadata={
            'dc:description': "The first 22 fields are the fields of the Intercontinental "
                "Dictionary Series meaning list, proposed by Mary Ritchie Key, and "
                "ultimately based on Carl Darling Buck's (1949) <i>Dictionary of selected"
                " synonyms in the principal Indo-European languages</i>. The other two "
                "fields were added for the Loanword Typology project."
        }
    )
    Borrowed_score = attr.ib(
        default=None,
        metadata={
            'datatype': 'float',
            'dc:description':
                "The average borrowed score of all words corresponding to this meaning."
        }
    )
    Age_score = attr.ib(
        default=None,
        metadata={
            'datatype': 'float',
            'dc:description': "The average age score of all words corresponding to this meaning."
        }
    )
    Simplicity_score = attr.ib(
        default=None,
        metadata={
            'datatype': 'float',
            'dc:description':
                "The average simplicity score of all words corresponding to this meaning."
        }
    )


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


class Dataset(Base):
    dir = pathlib.Path(__file__).parent
    id = "wold"
    lexeme_class = WoldLexeme
    language_class = WoldLanguage
    concept_class = WoldConcept
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
        self._schema(args)
        args.writer.add_sources()

        # add the languages from the language file
        # NOTE: the source lists all languages, including proto-languages,
        # but the `forms` only include the first 41 in the list
        language_lookup = args.writer.add_languages(lookup_factory="WOLD_ID")

        desc_dir = self.cldf_dir / 'descriptions'
        if not desc_dir.exists():
            desc_dir.mkdir()
        numentries = {
            r["pk"]: int(r["count_words"])
            for r in self.raw_dir.joinpath("db").read_csv("vocabulary.csv", dicts=True)
        }
        db_contribs = {
            r['id']: r
            for r in self.raw_dir.joinpath('db').read_csv('contribution.csv', dicts=True)}
        for contrib in self.raw_dir.read_csv("contributions.csv", dicts=True):
            db_contrib = db_contribs[contrib['ID']]
            args.writer.objects["ContributionTable"].append(
                dict(
                    ID=contrib["ID"],
                    Name="{} vocabulary".format(contrib["Name"]),
                    Citation=format_citation(contrib, numentries[contrib["ID"]]),
                    Contributor=contrib["Contributors"],
                    Number_of_words=numentries[contrib["ID"]],
                    Language_ID=language_lookup[contrib["ID"]],
                )
            )
            desc = vocabulary_description(
                contrib['Name'], contrib["Contributors"], json.loads(db_contrib['jsondata']))
            p = desc_dir.joinpath('vocabulary_{}.md'.format(contrib['ID']))
            p.write_text(desc, encoding='utf8')

        concepticon = {concept.attributes['wold_id']: concept for concept in self.conceptlists[0].concepts.values()}
        for parameter in self.raw_dir.read_csv("parameters.csv", dicts=True):
            concept = concepticon.get(parameter['ID'])
            args.writer.add_concept(
                ID=parameter['ID'],
                Name=concept.english if concept else parameter['Name'],
                Concepticon_ID=concept.concepticon_id if concept else None,
                Concepticon_Gloss=concept.concepticon_gloss if concept else None,
                Core_list=parameter['CoreList'] == 'true',
                Semantic_field=parameter['SemanticField'],
                Semantic_category=parameter['SemanticCategory'],
                Borrowed_score=float(parameter['BorrowedScore']),
                Age_score=float(parameter['AgeScore']) if parameter['AgeScore'] else None,
                Simplicity_score=float(parameter['SimplicityScore']),
            )

        form2lexeme = {}
        wid2fid = collections.defaultdict(set)
        lexemes_rows = self.raw_dir.read_csv("forms.csv", dicts=True)
        for row in progressbar(lexemes_rows):
            # Add information not in row, so we can pass to `add_form()`
            # with a single comprehension
            row["Language_ID"] = language_lookup[row["Language_ID"]]
            row["Parameter_ID"] = row["Parameter_ID"]
            row["Value"] = row.pop("Form")
            row["Loan"] = float(row["BorrowedScore"]) > 0.6
            row["Borrowed_score"] = row["BorrowedScore"]
            row["Simplicity_score"] = row["SimplicityScore"]
            row["original_script"] = normalize_text(row["original_script"])
            row["comment_on_borrowed"] = normalize_text(row["comment_on_borrowed"])
            row.pop("Segments")
            row['Age_score'] = decimal.Decimal(row.pop('AgeScore')) if row['AgeScore'] else None
            row['Age'] = row.pop('age_label')
            row['Local_ID'] = row['ID']
            row['contact_situation'] = row['ContactSituation']
            row['Comment'] = row.pop('other_comments')

            lexemes = args.writer.add_forms_from_value(
                **{k: v for k, v in row.items() if k in self.lexeme_class.fieldnames()}
            )
            assert len(lexemes) == 1
            form2lexeme[row['ID']] = lexemes[0]['ID']
            wid2fid[row['Word_ID']].add(lexemes[0]['ID'])

        words = {r['pk']: r for r in self.raw_dir.joinpath('db').read_csv('unit.csv', dicts=True)}
        languages = {r['pk']: r['name'] for r in self.raw_dir.joinpath('db').read_csv('language.csv', dicts=True)}
        codes = {r['pk']: r['name'] for r in self.raw_dir.joinpath('db').read_csv('identifier.csv', dicts=True) if r['type'] == 'glottolog'}
        glottocodes = {
            r['language_pk']: codes[r['identifier_pk']]
            for r in self.raw_dir.joinpath('db').read_csv('languageidentifier.csv', dicts=True)
            if r['identifier_pk'] in codes}

        wids = [w['id'] for w in words.values()]
        for wid in wid2fid:
            assert wid in wids

        count = 0
        for row in self.raw_dir.joinpath('db').read_csv('loan.csv', dicts=True):
            assert row['target_word_pk'] in words
            source_word = None
            if row ['source_word_pk']:
                assert row['source_word_pk'] in words
                source_word = words[row['source_word_pk']]
            twid = words[row['target_word_pk']]['id']
            for fid in wid2fid[twid]:
                # The meaning-differentiated borrowing events.
                count += 1
                args.writer.objects['BorrowingTable'].append(dict(
                    ID=str(count),
                    Target_Form_ID=fid,
                    Comment='Source word unidentifiable' if source_word['name'].lower() == 'unidentifiable' else None,
                    Source_word=None if source_word['name'].lower() == 'unidentifiable' else source_word['name'],
                    Source_meaning=source_word['description'] or None,
                    Source_languoid=languages[source_word['language_pk']],
                    Source_languoid_glottocode=glottocodes.get(source_word['language_pk']),
                    Source_relation=row['relation'],
                    Source_certain=row['certain'] == 't',
                ))

    def _schema(self, args):
        args.writer.cldf['FormTable'].common_props['dc:description'] = \
            "Word forms are listed as 'counterparts', i.e. as words with a specific meaning. " \
            "Thus, words with multiple meanings may appear more than once in this table."
        args.writer.cldf['FormTable', 'Comment'].common_props['dc:description'] = \
            "For more specific comments see 'comment_on_borrowed' and 'comment_on_word_form'"
        args.writer.cldf['FormTable', 'Word_ID'].valueUrl = URITemplate('https://wold.clld.org/word/{Word_ID}')
        args.writer.cldf.remove_columns('FormTable', 'Cognacy')

        t = args.writer.cldf.add_component(
            "ContributionTable",
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
                "dc:description": "References the language for which this contribution provides "
                                  "a vocabulary.",
            },
        )
        t.common_props['dc:description'] = \
            "WOLD contributions are vocabularies (mini-dictionaries of about 1000-2000 entries) " \
            "with comprehensive information about the loanword status of each word. " \
            "Descriptions of how these vocabularies coded the data can be found in the " \
            "[descriptions](descriptions/) directory."
        args.writer.cldf['ContributionTable', 'description'].valueUrl = URITemplate(
            './descriptions/vocabulary_{ID}.md')
        args.writer.cldf['ContributionTable', 'description'].common_props['dc:format'] = 'text/markdown'
        args.writer.cldf['ContributionTable', 'id'].common_props["dc:description"] = \
            "The vocabulary ID number corresponds to the ordering to the chapters on the book " \
            "Loanwords in the World's Languages. Languages are listed in rough geographical order " \
            "from west to east, from Africa via Europe to Asia and the Americas, so that " \
            "geographically adjacent languages are next to each other."
        args.writer.cldf['ContributionTable', 'citation'].common_props["dc:description"] = \
            "Each vocabulary of WOLD is a separate electronic publication with a separate author " \
            "or team of authors and should be cited as specified here."
        args.writer.cldf['ContributionTable', 'contributor'].common_props["dc:description"] = \
            "The authors are experts of the language and its history. They also contributed a " \
            "prose chapter on the borrowing situation in their language that was published in the " \
            "book Loanwords in the World's Languages."
        t.add_foreign_key("Language_ID", "languages.csv", "ID")

        t = args.writer.cldf.add_component(
            'BorrowingTable',
            {
                'name': 'Source_relation',
                'datatype': {'base': 'string', 'format': "immediate|earlier"},
                'dc:description':
                    "Whether a word was contributed directly (immediate) or indirectly (earlier), "
                    "i.e. via another, intermediate donor languoid, to the recipient language.",
            },
            'Source_word',
            'Source_meaning',
            {
                'name': 'Source_certain',
                'datatype': {'base': 'boolean', 'format': "yes|no"},
                'dc:description': "Certainty of the source identification",
            },
            {
                'name': 'Source_languoid',
                'dc:description': 'Donor languoid, specified as name of a language or language subgroup or family',
            },
            {
                'name': 'Source_languoid_glottocode',
                'dc:description': 'Glottocode of the source languid',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#glottocode',
            }
        )
        t.common_props['dc:description'] = \
            'While a lot of information about the borrowing status is attached to the borrowed ' \
            'forms, the BorrowingTable lists information about (potential) source words. Note ' \
            'that we list loan events per meaning; i.e. one loanword may result in multiple ' \
            'borrowings if the word has multiple meanings.'

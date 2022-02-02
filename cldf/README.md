<a name="ds-cldfmetadatajson"> </a>

# Wordlist CLDF dataset derived from Haspelmath and Tadmor's "World Loanword Database" from 2009

**CLDF Metadata**: [cldf-metadata.json](./cldf-metadata.json)

**Sources**: [sources.bib](./sources.bib)

property | value
 --- | ---
[dc:bibliographicCitation](http://purl.org/dc/terms/bibliographicCitation) | Haspelmath, Martin & Tadmor, Uri (eds.) 2009. World Loanword Database. Leipzig: Max Planck Institute for Evolutionary Anthropology. (Available online at http://wold.clld.org)
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF Wordlist](http://cldf.clld.org/v1.0/terms.rdf#Wordlist)
[dc:format](http://purl.org/dc/terms/format) | <ol><li>http://concepticon.clld.org/contributions/Haspelmath-2009-1460</li></ol>
[dc:identifier](http://purl.org/dc/terms/identifier) | http://wold.clld.org
[dc:license](http://purl.org/dc/terms/license) | https://creativecommons.org/licenses/by/4.0/
[dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) | https://github.com/lexibank/wold
[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="https://github.com/lexibank/wold/tree/094f05d">lexibank/wold v4.0-2-g094f05d</a></li><li><a href="https://github.com/glottolog/glottolog/tree/v4.4">Glottolog v4.4</a></li><li><a href="https://github.com/concepticon/concepticon-data/tree/v2.5.0">Concepticon v2.5.0</a></li><li><a href="https://github.com/cldf-clts/clts//tree/b12a7df">CLTS v2.1.0-26-gb12a7df</a></li></ol>
[prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy) | <ol><li><strong>lingpy-rcParams</strong>: <a href="./lingpy-rcParams.json">lingpy-rcParams.json</a></li><li><strong>python</strong>: 3.10.1</li><li><strong>python-packages</strong>: <a href="./requirements.txt">requirements.txt</a></li></ol>
[rdf:ID](http://www.w3.org/1999/02/22-rdf-syntax-ns#ID) | wold
[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution


## <a name="table-formscsv"></a>Table [forms.csv](./forms.csv)

Word forms are listed as 'counterparts', i.e. as words with a specific meaning. Thus, words with multiple meanings may appear more than once in this table.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF FormTable](http://cldf.clld.org/v1.0/terms.rdf#FormTable)
[dc:extent](http://purl.org/dc/terms/extent) | 64289


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Local_ID](http://purl.org/dc/terms/identifier) | `string` | 
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | References [languages.csv::ID](#table-languagescsv)
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | References [parameters.csv::ID](#table-parameterscsv)
[Value](http://cldf.clld.org/v1.0/terms.rdf#value) | `string` | 
[Form](http://cldf.clld.org/v1.0/terms.rdf#form) | `string` | 
[Segments](http://cldf.clld.org/v1.0/terms.rdf#segments) | list of `string` (separated by ` `) | 
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | For more specific comments see 'comment_on_borrowed' and 'comment_on_word_form'
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`Loan` | `boolean` | 
`Graphemes` | `string` | 
`Profile` | `string` | 
`Word_ID` | `string` | ID of the corresponding word in the WOLD database.
`original_script` | `string` | If the language has no conventional orthography, the contributor's own transcription is given as Value. In such cases, the word in the language's usual writing system is provided in this field.
`comment_on_word_form` | `string` | 
`Borrowed` | `string` | The likelihood of borrowing of a word was categorized as follows:  1. clearly borrowed. 2. probably borrowed. 3. perhaps borrowed. 4. very little evidence for borrowing. 5. no evidence for borrowing. 
`Borrowed_score` | `decimal` | The following borrowed scores are assigned to words depending on the degree of likelihood of borrowing:  1. clearly borrowed:    1.00 2. probably borrowed:   0.75 3. perhaps borrowed:    0.50 4. very little evidence for borrowing:  0.25 5. no evidence for borrowing:   0.00 
`comment_on_borrowed` | `string` | 
`borrowed_base` | `string` | Indicates whether an analyzable word was derived from a loanword.
`loan_history` | `string` | 
`Analyzability` | `string` | analyzable (compound or derived or phrasal), semi-analyzable or unanalyzable
`gloss` | `string` | Morpheme-by-morpheme gloss for analyzable words.
`Simplicity_score` | `decimal` | The following simplicity scores are assigned to words depending on their analyzability:  1. unanalyzable:    1.00 2. semi-analyzable: 0.75 3. analyzable:  0.50 
`reference` | `string` | Bibliographic references. For details refer to the vocabulary descriptions.
`relative_frequency` | `string` | Frequency information according to the contributor's intuition - in the absence of representative corpora.
`numeric_frequency` | `float` | Occurrences per million words - if significant representative corpora exist.
`Age` | `string` | Short description of the age of the word. For details refer to the vocabulary descriptions.
`Age_score` | `decimal` | The following age scores are assigned to words depending on the estimated age of their age class:  1. first attested or reconstructed earlier than 1000:   1.00 2. earlier than 1500:   0.90 3. earlier than 1800:   0.80 4. earlier than 1900:   0.70 5. earlier than 1950:   0.60 6. earlier than 2007:   0.50 
`integration` | `string` | 1. Highly integrated: no structural properties that betray the foreign origin 2. Intermediate: some synchronic properties of the foreign language 3. Unintegrated: significant phonological and/or morphological properties of the donor language 
`salience` | `string` | Environmental salience of borrowed meanings  no information. not applicable. not present: Snow did not exist in Thailand either before or after introduction of the Sanskrit loanword for snow, which nevertheless is known and understood by speakers of Thai. present in pre-contact environment: There were mountains in England even before the word "mountain" was borrowed from French. present only since contact: Many South American languages borrowed the word for "horse" from the Spaniards, who introduced it to their environment. 
`effect` | `string` | Effect of a loanword on the lexical stock of a recipient language.  Coexistence: the word may coexist with a native word with the same meaning. Insertion: the word is inserted into the vocabulary as a completely new item. Replacement: the word may replace an earlier word with the same meaning that falls out of use or changes its meaning. 
`register` | `string` | Textual description of the register a word is used in.
`contact_situation` | `string` | Short description of the contact situation that resulted in the loan. Detailed descriptions are given in the vocabulary description.
`calqued` | `string` | 0. No evidence for calquing 1. Very little evidence for calquing 2. Perhaps calqued 3. Probably calqued 4. Clearly calqued 
`grammatical_info` | `string` | 
`colonial_word` | `string` | Only given for words in the Zinacantán Tzotzil vocabulary.
`etymological_note` | `string` | Only given for words in the Selice Romani vocabulary.
`lexical_stratum` | `string` | Only given for words in the Japanese vocabulary.
`word_source` | `string` | Only given for words in the Q'eqchi' vocabulary.

## <a name="table-languagescsv"></a>Table [languages.csv](./languages.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF LanguageTable](http://cldf.clld.org/v1.0/terms.rdf#LanguageTable)
[dc:extent](http://purl.org/dc/terms/extent) | 41


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string` | 
`Glottolog_Name` | `string` | 
[ISO639P3code](http://cldf.clld.org/v1.0/terms.rdf#iso639P3code) | `string` | 
[Macroarea](http://cldf.clld.org/v1.0/terms.rdf#macroarea) | `string` | 
[Latitude](http://cldf.clld.org/v1.0/terms.rdf#latitude) | `decimal` | 
[Longitude](http://cldf.clld.org/v1.0/terms.rdf#longitude) | `decimal` | 
`Family` | `string` | 
`WOLD_ID` | `string` | 

## <a name="table-parameterscsv"></a>Table [parameters.csv](./parameters.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ParameterTable](http://cldf.clld.org/v1.0/terms.rdf#ParameterTable)
[dc:extent](http://purl.org/dc/terms/extent) | 1814


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Concepticon_ID](http://cldf.clld.org/v1.0/terms.rdf#concepticonReference) | `string` | 
`Concepticon_Gloss` | `string` | 
`Core_list` | `boolean` | Indicates whether the concept is one of the 1460 core LWT meanings
`Semantic_category` | `string` | Meanings were assigned to semantic categories with word-class-like labels: nouns, verbs, adjectives, adverbs, function words. No claim is made about the grammatical behavior of words corresponding to these meanings. The categories are intended to be purely semantic.
`Semantic_field` | `string` | The first 22 fields are the fields of the Intercontinental Dictionary Series meaning list, proposed by Mary Ritchie Key, and ultimately based on Carl Darling Buck's (1949) <i>Dictionary of selected synonyms in the principal Indo-European languages</i>. The other two fields were added for the Loanword Typology project.
`Borrowed_score` | `float` | The average borrowed score of all words corresponding to this meaning.
`Age_score` | `float` | The average age score of all words corresponding to this meaning.
`Simplicity_score` | `float` | The average simplicity score of all words corresponding to this meaning.

## <a name="table-contributionscsv"></a>Table [contributions.csv](./contributions.csv)

WOLD contributions are vocabularies (mini-dictionaries of about 1000-2000 entries) with comprehensive information about the loanword status of each word. Descriptions of how these vocabularies coded the data can be found in the [descriptions](descriptions/) directory.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ContributionTable](http://cldf.clld.org/v1.0/terms.rdf#ContributionTable)
[dc:extent](http://purl.org/dc/terms/extent) | 41


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | The vocabulary ID number corresponds to the ordering to the chapters on the book Loanwords in the World's Languages. Languages are listed in rough geographical order from west to east, from Africa via Europe to Asia and the Americas, so that geographically adjacent languages are next to each other.<br>Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 
[Contributor](http://cldf.clld.org/v1.0/terms.rdf#contributor) | `string` | The authors are experts of the language and its history. They also contributed a prose chapter on the borrowing situation in their language that was published in the book Loanwords in the World's Languages.
[Citation](http://cldf.clld.org/v1.0/terms.rdf#citation) | `string` | Each vocabulary of WOLD is a separate electronic publication with a separate author or team of authors and should be cited as specified here.
`Number_of_words` | `integer` | There would be 1814 words in each vocabulary, corresponding to the 1814 Loanword Typology meanings, if each meaning had exactly one counterpart, and if all the counterparts were different words. But many ("polysomous") words are counterparts of several meanings, many meanings have several word counterparts ("synonyms", or "subcounterparts"), and many meanings have no counterparts at all, so the number of words in each database varies considerably.
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | References the language for which this contribution provides a vocabulary.<br>References [languages.csv::ID](#table-languagescsv)

## <a name="table-borrowingscsv"></a>Table [borrowings.csv](./borrowings.csv)

While a lot of information about the borrowing status is attached to the borrowed forms, the BorrowingTable lists information about (potential) source words. Note that we list loan events per meaning; i.e. one loanword may result in multiple borrowings if the word has multiple meanings.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF BorrowingTable](http://cldf.clld.org/v1.0/terms.rdf#BorrowingTable)
[dc:extent](http://purl.org/dc/terms/extent) | 21624


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Target_Form_ID](http://cldf.clld.org/v1.0/terms.rdf#targetFormReference) | `string` | References the loanword, i.e. the form as borrowed into the target language<br>References [forms.csv::ID](#table-formscsv)
[Source_Form_ID](http://cldf.clld.org/v1.0/terms.rdf#sourceFormReference) | `string` | References the source word of a borrowing<br>References [forms.csv::ID](#table-formscsv)
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`Source_relation` | `string` | Whether a word was contributed directly (immediate) or indirectly (earlier), i.e. via another, intermediate donor languoid, to the recipient language.
`Source_word` | `string` | 
`Source_meaning` | `string` | 
`Source_certain` | `boolean` | Certainty of the source identification
`Source_languoid` | `string` | Donor languoid, specified as name of a language or language subgroup or family
[Source_languoid_glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string` | Glottocode of the source languid


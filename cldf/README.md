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
[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="https://github.com/lexibank/wold/tree/8e07eca">lexibank/wold v3.0-35-g8e07eca</a></li><li><a href="https://github.com/glottolog/glottolog/tree/ea763abd75">Glottolog v4.3-treedb-fixes-326-gea763abd75</a></li><li><a href="https://github.com/concepticon/concepticon-data/tree/acebe08">Concepticon v2.4.0-87-gacebe08</a></li><li><a href="https://github.com/cldf-clts/clts/tree/df0f44c">CLTS v2.0.0-2-gdf0f44c</a></li></ol>
[prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy) | <ol><li><strong>python</strong>: 3.8.5</li><li><strong>python-packages</strong>: <a href="./requirements.txt">requirements.txt</a></li></ol>
[rdf:ID](http://www.w3.org/1999/02/22-rdf-syntax-ns#ID) | wold
[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution


## <a name="table-formscsv"></a>Table [forms.csv](./forms.csv)

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
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`Cognacy` | `string` | 
`Loan` | `boolean` | 
`Graphemes` | `string` | 
`Profile` | `string` | 
`Word_ID` | `string` | 
`word_source` | `string` | 
`Borrowed` | `string` | 
`Borrowed_score` | `string` | 
`comment_on_borrowed` | `string` | 
`comment_on_word_form` | `string` | 
`borrowed_base` | `string` | 
`other_comments` | `string` | 
`loan_history` | `string` | 
`Analyzability` | `string` | 
`Simplicity_score` | `string` | 
`reference` | `string` | 
`numeric_frequency` | `string` | 
`age_label` | `string` | 
`gloss` | `string` | 
`integration` | `string` | 
`salience` | `string` | 
`effect` | `string` | 
`contact_situation` | `string` | 
`original_script` | `string` | 

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

## <a name="table-vocabulariescsv"></a>Table [vocabularies.csv](./vocabularies.csv)

property | value
 --- | ---
[dc:extent](http://purl.org/dc/terms/extent) | 41


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | The vocabulary ID number corresponds to the ordering to the chapters on the book <em>Loanwords in the World's Languages</em>. Languages are listed in rough geographical order from west to east, from Africa via Europe to Asia and the Americas, so that geographically adjacent languages are next to each other.<br>Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Citation](dc:bibliographicCitation) | `string` | Each vocabulary of WOLD is a separate electronic publication with a separate author or team of authors and should be cited as specified here.
[Authors](dc:creator) | `string` | The authors are experts of the language and its history. They also contributed a prose chapter on the borrowing situation in their language that was published in the book Loanwords in the World's Languages.
`Number_of_words` | `integer` | There would be 1814 words in each vocabulary, corresponding to the 1814 Loanword Typology meanings, if each meaning had exactly one counterpart, and if all the counterparts were different words. But many ("polysomous") words are counterparts of several meanings, many meanings have several word counterparts ("synonyms", or "subcounterparts"), and many meanings have no counterparts at all, so the number of words in each database varies considerably.
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | References [languages.csv::ID](#table-languagescsv)


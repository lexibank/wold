import re

from clldutils.source import Source

YEAR = re.compile(r'(\s+|\.|-)(?P<year>\(?[12][0-9]{3}\)?[abf]*((-|–)[0-9]{2,4})?(\s*\[[0-9]{4}])?)[.;:,\s+]')
IN_PRESS = re.compile(r'(?P<year>(I|i)n press(\s[ab])?)(\s|\.)')

CONVERTER = {
    'Analyzability': lambda s: s or None,
    'relative_frequency': lambda s: s or None,
    'numeric_frequency': lambda s: float(s.replace(",", ".")) if s else None,
    'Age': lambda s: None if s.lower() == "no information" or not s else s,
    'salience': lambda s: (s.lower() if s != '""' else None) if s else None,
    'effect': lambda s: None if s.lower() == "no information" or not s else s,

}

def source(line, id_):
    m = YEAR.search(line)
    if not m:
        m = IN_PRESS.search(line)
    if not m:
        return Source('misc', str(id_), note=line)
    return Source('misc', str(id_), author=line[:m.start()].strip(), year=m.group('year'), note=line[m.end():].strip())


def bibtex(text):
    no, refs = None, []
    header = re.compile('(?P<no>[0-9]{1,2}) .*')
    count = 0
    for line in text.split('\n'):
        line = line.strip().replace('\t', ' ')
        if not line:
            continue
        m = header.match(line)
        if m:
            if no:
                yield no, refs
            no, refs = m.group('no'), []
        else:
            count += 1
            refs.append(source(line, count))
    yield no, refs


def title(key):
    key = key.replace('fd_', '')
    return {
        'name': 'Word form',
        'meanings': 'LWT meaning(s)',
        'description': 'Word meaning',
        'comment_on_word_form': 'Comments on word',
        'comment_on_borrowed': 'Comments',
        'borrowed': 'Borrowed status',
        'calqued': 'Calqued status',
        'reference': 'Reference(s)',
        'early_romani_reconstruction': "Early Romani reconstruction",
        'boretzky_and_igla_etymology': "Boretzky & Igla's etymology",
        'manuss_et_al_etymology': "M\u0101nu\u0161s et al. etymology",
        'vekerdi_etymology': "Vekerdi's etymology",
        'turner_etymology': "Turner's etymology",
        'other_etymologies': "Other etymologies",
        'mayrhofer_etymology': "Mayrhofer's etymology",
        'comparison_with_mandarin': "Comparison with Mandarin",
        'comparison_with_korean': "Comparison with Korean",
    }.get(key, key.replace('_', ' ').capitalize())


def vocabulary_description(name, authors, md):
    res = []
    for fd in [
        'fd_form',
        'fd_original_script',
        'fd_free_meaning',
        'fd_grammatical_info',
        'fd_comment_on_word_form',
        'fd_analyzability',
        'fd_gloss',
        'fd_age',
        'fd_register',
        'fd_numeric_frequency',
        'fd_borrowed',
        'fd_calqued',
        'fd_borrowed_base',
        'fd_comment_on_borrowed',
        'fd_loan_history',
        'fd_reference',
        'fd_effect',
        'fd_integration',
        'fd_salience',
        'abbreviations',
        'other_information',
    ]:
        if md.get(fd):
            res.append('## {}\n'.format(title(fd)))
            text = md[fd]
            if fd in ['abbreviations', 'fd_reference']:
                text = '\n'.join('- {}'.format(line) for line in text.split('\n') if line.strip())
            res.append(text)
            res.append('')
    return """\
# {} vocabulary

by {}

{}
""".format(name,
               authors,  # raw/contributions.csv::Contributors
               '\n'.join(res))

    """
        ]:
        % endfor
        </tbody>
    </table>
    % if ctx.jsondata.get('abbreviations'):
    <h3>Abbreviations</h3>
    <div>
        ${h.text2html(ctx.jsondata['abbreviations'], mode='p')}
    </div>
    % endif
    % if ctx.jsondata.get('other_information'):
    <h3>Other information</h3>
    <div>
        ${h.text2html(ctx.jsondata['other_information'], mode='p')}
    </div>
    """

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
            if fd in ['abbrevirations', 'fd_reference']:
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

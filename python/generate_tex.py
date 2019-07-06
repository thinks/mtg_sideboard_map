"""
Copyright(C) 2019 Tommy Hinks <tommy.hinks@gmail.com>
This file is subject to the license terms in the LICENSE file
found in the top-level directory of this distribution.
"""

import argparse
import json
import subprocess
from verify import verify_decklist, verify_matchups


def _write_tex_begin(title_str, author_str, date_str, tex_file):
    tex_file.write('\\documentclass{article}\n')
    tex_file.write('\\usepackage[utf8]{inputenc}\n')
    tex_file.write('\\usepackage{multicol}\n')
    tex_file.write('\\usepackage[table]{xcolor}\n')
    tex_file.write('\\usepackage{geometry}\n')
    tex_file.write('\\usepackage{titletoc}\n')
    tex_file.write('\\geometry{a4paper, portrait, margin = 1 in}\n')
    tex_file.write('\\title{' + title_str + '}\n')
    tex_file.write('\\author{' + author_str + '}\n')
    tex_file.write('\\date{' + date_str + '}\n')
    tex_file.write('\\renewcommand *\\contentsname{Contents}')
    tex_file.write('\\begin{document}\n')
    tex_file.write('\\maketitle\n')
    tex_file.write('\\titlecontents{section}[0em]\n')
    tex_file.write('{\\vskip 0.5ex} %\n')
    tex_file.write('{\\scshape} % Numbered sections formatting\n')
    tex_file.write('{} % Unnumbered sections formatting\n')
    tex_file.write('{} %\n')
    tex_file.write('\\tableofcontents\n')


def _write_tex_decklist_section(decklist_json, sb_bg_color, tex_file):
    md_json = decklist_json['maindeck']
    sb_json = decklist_json['sideboard']

    tex_file.write('\\section*{Decklist}\n')
    tex_file.write('\\begin{center}\n')
    tex_file.write('\\begin{tabular}{| l | l |}\n')
    tex_file.write('\\hline\n')
    tex_file.write('\\multicolumn{2}{| c |}{\\textbf{Decklist}} \\\\\n')
    tex_file.write('\\hline\n')
    tex_file.write('\\textit{Maindeck}(' + str(sum(md_json.values())) + ') & \\textit{Sideboard}(' +
                   str(sum(sb_json.values())) + ') \\\\\n')
    tex_file.write('\\hline\n')

    # Ugly iteration hack!
    md_cards = list(md_json.keys())
    md_counts = list(md_json.values())
    sb_cards = list(sb_json.keys())
    sb_counts = list(sb_json.values())
    for i in range(max(len(md_json), len(sb_json))):
        md_str = ''
        if i < len(md_cards):
            md_str = '\\cellcolor[HTML]{FFFFFF}\\small{' + str(md_counts[i]) + ' ' + md_cards[i] + '}'

        sb_str = ''
        if i < len(sb_cards):
            sb_str = '\\cellcolor[HTML]{' + sb_bg_color + '}\\small{' + str(sb_counts[i]) + ' ' + sb_cards[i] + '}'

        tex_file.write(md_str + ' & ' + sb_str + '\\\\\n')

    tex_file.write('\\hline\n')
    tex_file.write('\\end{tabular}\n')
    tex_file.write('\\end{center}\n')


def _write_tex_matchup_lines_pd(play_draw_json, screen_names_json, sign_str, bg_color, tex_file):
    # Ugly iteration hack!
    play_draw_cards = list(play_draw_json.keys())
    play_draw_counts = list(play_draw_json.values())
    for i in range(len(play_draw_json)):
        card_name = play_draw_cards[i]
        if card_name in screen_names_json:
            card_name = screen_names_json[card_name]
        play_draw_str = '\\cellcolor[HTML]{' + bg_color + '}\\small{' + sign_str + str(play_draw_counts[i]) + ' ' + \
                        card_name + '}'
        tex_file.write(play_draw_str + '\\\\\n')


def _write_tex_matchup_lines(play_json, draw_json, screen_names_json, sign_str, bg_color, tex_file):
    # Ugly iteration hack!
    play_cards = list(play_json.keys())
    play_counts = list(play_json.values())
    draw_cards = list(draw_json.keys())
    draw_counts = list(draw_json.values())

    for i in range(max(len(play_json), len(draw_json))):
        play_str = ''
        if i < len(play_cards):
            card_name = play_cards[i]
            if card_name in screen_names_json:
                card_name = screen_names_json[card_name]
            play_str = '\\cellcolor[HTML]{' + bg_color + '}\\small{' + sign_str + str(play_counts[i]) + ' ' + \
                       card_name + '}'
        draw_str = ''
        if i < len(draw_cards):
            card_name = draw_cards[i]
            if card_name in screen_names_json:
                card_name = screen_names_json[card_name]
            draw_str = '\\cellcolor[HTML]{' + bg_color + '}\\small{' + sign_str + str(draw_counts[i]) + ' ' + \
                       card_name + '}'
        tex_file.write(play_str + ' & ' + draw_str + '\\\\\n')


def _write_tex_matchup(name, matchup_json, screen_names_json, in_bg_color, out_bg_color, tex_file):
    tex_file.write('\\subsection*{' + name + '}\n')
    tex_file.write(matchup_json['notes'])

    if 'play_and_draw' in matchup_json:
        play_json = matchup_json['play_and_draw']
        # draw_json = matchup_json['play_and_draw']

        tex_file.write('\\begin{center}\n')
        tex_file.write('\\begin{tabular}{| l |}\n')
        tex_file.write('\\hline\n')
        tex_file.write('\\textit{Play and Draw}(' + str(sum(play_json['in'].values())) + ') \\\\\n')
        tex_file.write('\\hline\n')

        _write_tex_matchup_lines_pd(play_json['in'], screen_names_json, '+',
                                    in_bg_color, tex_file)
        _write_tex_matchup_lines_pd(play_json['out'], screen_names_json, '-',
                                    out_bg_color, tex_file)

        tex_file.write('\\hline\n')
        tex_file.write('\\end{tabular}\n')
        tex_file.write('\\end{center}\n')
        tex_file.write('\\addcontentsline{toc}{section}{' + name + '}\n')
    else:
        play_json = matchup_json['play']
        draw_json = matchup_json['draw']

        tex_file.write('\\begin{center}\n')
        tex_file.write('\\begin{tabular}{| l | l |}\n')
        tex_file.write('\\hline\n')
        tex_file.write('\\textit{Play}(' + str(sum(play_json['in'].values())) + ') & \\textit{Draw}(' +
                       str(sum(draw_json['in'].values())) + ') \\\\\n')
        tex_file.write('\\hline\n')

        _write_tex_matchup_lines(play_json['in'], draw_json['in'], screen_names_json, '+',
                                 in_bg_color, tex_file)
        _write_tex_matchup_lines(play_json['out'], draw_json['out'], screen_names_json, '-',
                                 out_bg_color, tex_file)

        tex_file.write('\\hline\n')
        tex_file.write('\\end{tabular}\n')
        tex_file.write('\\end{center}\n')
        tex_file.write('\\addcontentsline{toc}{section}{' + name + '}\n')


def _write_tex_matchup_section(matchups_json, screen_names_json, in_bg_color, out_bg_color, tex_file):
    tex_file.write('\\section*{Matchups}\n')
    tex_file.write('\\begin{multicols}{2}\n')
    for name, matchup_json in matchups_json.items():
        _write_tex_matchup(name, matchup_json, screen_names_json, in_bg_color, out_bg_color, tex_file)

    tex_file.write('\\end{multicols}\n')


def _write_tex_end(tex_file):
    tex_file.write('\\end{document}')


def generate_tex(sb_map_json, sb_bg_color, in_bg_color, out_bg_color, tex_file):
    _write_tex_begin(sb_map_json['title'], sb_map_json['author'], sb_map_json['date'], tex_file)
    _write_tex_decklist_section(sb_map_json['decklist'], sb_bg_color, tex_file)
    _write_tex_matchup_section(sb_map_json['matchups'], sb_map_json['screen_names'],
                               in_bg_color, out_bg_color, tex_file)
    _write_tex_end(tex_file)


def main():
    parser = argparse.ArgumentParser(description='Generate markdown')
    parser.add_argument('-sb', '--sbmap', help='Sideboard map JSON file', required=True)
    parser.add_argument('-tex', '--tex_file', help='Output tex file', required=True)
    parser.add_argument('-pdf', '--pdf_directory', help='Output directory for pdf file', required=False,
                        default='.')
    # Note(thinks): In my case "C:/Users/tommy/AppData/Local/Programs/MiKTeX 2.9/miktex/bin/x64/pdflatex.exe"
    parser.add_argument('-pdflatex', '--pdflatex_exe', help='Path to pdflatex exectuable (empty to disable pdf '
                                                            'generation', required=False, default='')
    parser.add_argument('-sb_bg_color', '--sideboard_background_color',
                        help='Background color of sideboard cells in decklist', required=False, default='EEEEEE')
    parser.add_argument('-in_bg_color', '--in_background_color',
                        help='Background color of cells for cards to bring in', required=False, default='BBDDBB')
    parser.add_argument('-out_bg_color', '--out_background_color',
                        help='Background color of cells for cards to take out', required=False, default='DDBBBB')

    args = vars(parser.parse_args())
    with open(args['sbmap']) as sb_map_json_file, \
            open(args['tex_file'], 'w') as tex_file:
        sb_map_json = json.load(sb_map_json_file)
        verify_decklist(sb_map_json['decklist'])
        verify_matchups(sb_map_json['decklist'], sb_map_json['matchups'])
        generate_tex(sb_map_json, args['sideboard_background_color'], args['in_background_color'],
                     args['out_background_color'], tex_file)

    if args['pdflatex_exe']:
        proc_args = [args['pdflatex_exe'], '-output-directory=' + args['pdf_directory'], args['tex_file']]

        # Must run twice to get proper table of contents.
        subprocess.run(proc_args)
        subprocess.run(proc_args)


if __name__ == "__main__":
    main()

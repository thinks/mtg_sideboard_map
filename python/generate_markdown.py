"""
Copyright(C) 2019 Tommy Hinks <tommy.hinks@gmail.com>
This file is subject to the license terms in the LICENSE file
found in the top-level directory of this distribution.
"""

import argparse
import json
from verify import verify_decklist, verify_sideboard_map


def write_matchup_notes(notes, md_file):
    md_file.write(notes + '\n')
    md_file.write('\n')


def write_matchup_lines(play, draw, sign, md_file):
    # Ugly iteration hack!
    play_cards = list(play.keys())
    play_counts = list(play.values())
    draw_cards = list(draw.keys())
    draw_counts = list(draw.values())

    for i in range(max(len(play), len(draw))):
        play_string = ""
        if i < len(play):
            play_string = sign + ' ' + str(play_counts[i]) + ' **' + play_cards[i] + '**'
        draw_string = ""
        if i < len(draw):
            draw_string = sign + ' ' + str(draw_counts[i]) + ' **' + draw_cards[i] + '**'
        md_file.write('| ' + play_string + ' | ' + draw_string + ' |\n')


def write_matchup_sideboarding(mu_json, md_file):
    md_file.write('| Play (' + str(sum(mu_json["play"]["in"].values())) + ') | Draw ('
                  + str(sum(mu_json["draw"]["in"].values())) + ') |\n')
    md_file.write("| --- | --- |\n")

    write_matchup_lines(mu_json["play"]["in"], mu_json["draw"]["in"], '+', md_file)
    md_file.write("| --- | --- |\n")
    write_matchup_lines(mu_json["play"]["out"], mu_json["draw"]["out"], '-', md_file)


def write_matchup(mu_name, mu_json, md_file):
    md_file.write('## ' + mu_name + '\n')
    write_matchup_notes(mu_json["notes"], md_file)
    write_matchup_sideboarding(mu_json, md_file)
    md_file.write('\n')


def write_decklist(decklist_json, md_file):
    md_file.write('## Decklist\n')
    for card, count in decklist_json["maindeck"].items():
        md_file.write(str(count) + ' ' + card + '  \n')
    md_file.write('\n')
    for card, count in decklist_json["sideboard"].items():
        md_file.write(str(count) + ' ' + card + '  \n')
    md_file.write('\n')


def write_toc(matchups_json, md_file):
    md_file.write('## Table of Contents\n')
    for name in matchups_json:
        md_file.write('[' + name + '](#' + name.replace(' ', '-').lower() + ')  \n')


def generate_markdown(sb_map_json, md_file):
    write_decklist(sb_map_json["decklist"], md_file)
    write_toc(sb_map_json["matchups"], md_file)
    for mu_name, mu_json in sb_map_json["matchups"].items():
        write_matchup(mu_name, mu_json, md_file)


def main():
    parser = argparse.ArgumentParser(description='Generate markdown')
    parser.add_argument('-sb', '--sbmap', help='Sideboard map JSON file', required=True)
    parser.add_argument('-md', '--markdown', help='Output markdown file', required=True)
    args = vars(parser.parse_args())

    with open(args['sbmap']) as sb_map_json_file, \
            open(args['markdown'], 'w') as md_file:
        sb_map_json = json.load(sb_map_json_file)
        verify_decklist(sb_map_json["decklist"])
        verify_sideboard_map(sb_map_json)
        generate_markdown(sb_map_json, md_file)


if __name__ == "__main__":
    main()

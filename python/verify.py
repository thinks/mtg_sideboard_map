"""
Copyright(C) 2019 Tommy Hinks <tommy.hinks@gmail.com>
This file is subject to the license terms in the LICENSE file
found in the top-level directory of this distribution.
"""


def verify_decklist(decklist_json):
    if not sum(decklist_json['maindeck'].values()) >= 60:
        raise Exception("maindeck must have at least 60 cards")
    if not sum(decklist_json['sideboard'].values()) <= 15:
        raise Exception("sideboard must have 15 or less cards")


def verify_matchups(decklist_json, matchups_json):
    for matchup_name, matchup_json in matchups_json.items():
        if 'play_and_draw' in matchup_json:
            play_json = matchup_json['play_and_draw']
            draw_json = matchup_json['play_and_draw']
        else:
            play_json = matchup_json['play']
            draw_json = matchup_json['draw']

        _verify_in_out_with_decklist(decklist_json, play_json['in'], play_json['out'], matchup_name)
        _verify_in_out_with_decklist(decklist_json, draw_json['in'], draw_json['out'], matchup_name)
        _verify_in_out_zero_sum(play_json['in'], play_json['out'], matchup_name)
        _verify_in_out_zero_sum(draw_json['in'], draw_json['out'], matchup_name)


def _verify_in_out_with_decklist(decklist_json, in_json, out_json, matchup_name):
    maindeck_json = decklist_json['maindeck']
    sideboard_json = decklist_json['sideboard']
    for card, quantity in in_json.items():
        if card not in sideboard_json:
            raise Exception(matchup_name + ": '" + card + "' not in sideboard")
        if quantity > sideboard_json[card]:
            raise Exception(matchup_name + ": cannot board in " + str(quantity) + " '" + card + "' " +
                            "(" + str(sideboard_json[card]) + " in sideboard)")
    for card, quantity in out_json.items():
        if card not in maindeck_json:
            raise Exception(matchup_name + ": '" + card + "' not in maindeck")
        if quantity > maindeck_json[card]:
            raise Exception(matchup_name + ": cannot board out " + str(quantity) + " '" + card + "' " +
                            "(" + str(maindeck_json[card]) + " in maindeck)")


def _verify_in_out_zero_sum(in_json, out_json, matchup_name):
    if not sum(in_json.values()) == sum(out_json.values()):
        raise Exception(matchup_name + ': must board in/out same number of cards')

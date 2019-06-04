"""
Copyright(C) 2019 Tommy Hinks <tommy.hinks@gmail.com>
This file is subject to the license terms in the LICENSE file
found in the top-level directory of this distribution.
"""


def verify_decklist(decklist_json):
    assert sum(decklist_json['maindeck'].values()) == 60
    assert sum(decklist_json['sideboard'].values()) == 15


def verify_matchups(decklist_json, matchups_json):
    for matchup_json in matchups_json.values():
        if 'play,draw' in matchup_json:
            play_json = matchup_json['play,draw']
            draw_json = matchup_json['play,draw']
        else:
            play_json = matchup_json['play']
            draw_json = matchup_json['draw']

        _verify_in_out_with_decklist(decklist_json, play_json['in'], play_json['out'])
        _verify_in_out_with_decklist(decklist_json, draw_json['in'], draw_json['out'])
        _verify_in_out_zero_sum(play_json['in'], play_json['out'])
        _verify_in_out_zero_sum(draw_json['in'], draw_json['out'])


def _verify_in_out_with_decklist(decklist_json, in_json, out_json):
    maindeck_json = decklist_json['maindeck']
    sideboard_json = decklist_json['sideboard']
    for card, quantity in in_json.items():
        if card not in sideboard_json:
            raise Exception(card + ' not in sideboard')
        assert sideboard_json[card] >= quantity
    for card, quantity in out_json.items():
        assert card in maindeck_json
        assert quantity <= maindeck_json[card]


def _verify_in_out_zero_sum(in_json, out_json):
    assert sum(in_json.values()) == sum(out_json.values())

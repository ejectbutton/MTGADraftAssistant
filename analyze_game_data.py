from datetime import datetime
from enum import Enum
import os
from typing import OrderedDict
import json
import fileinput

opening_hand_dict = {"All": OrderedDict()}
drawn_dict = {"All": OrderedDict()}
tutored_dict = {"All": OrderedDict()}
deck_dict = {"All": OrderedDict()}
sideboard_dict = {"All": OrderedDict()}

class GameIndexArray(Enum):
    expansion = 0,
    event_type = 1,
    draft_id = 2,
    draft_time = 3,
    game_time = 4,
    build_index = 5,
    match_number = 6,
    game_number = 7,
    rank = 8,
    opp_rank = 9,
    main_colors = 10,
    splash_colors = 11,
    on_play = 12,
    num_mulligans = 13,
    opp_num_mulligans = 14,
    opp_colors = 15,
    num_turns = 16,
    won = 17,
    card = 18

def increment_dict(dict, color, card, value, victory):
    if value == 0: 
        return
    dict["All"][card][1] += value
    if color not in dict.keys():
        dict[color] = {card: [0.0, value]}
    elif card not in dict[color].keys():
        dict[color][card] = [0.0, value]
    else:
        dict[color][card][1] += value
    if victory.lower() == 'true':
        dict["All"][card][0] += value
        dict[color][card][0] += value

def process_header(line):
    split_joiner = ''
    line_split = line.split(',')
    for i in range(len(line_split)):
        if i < GameIndexArray.card.value:
            continue
        if line_split[i][0] == '"':
            split_joiner += line_split[i].lstrip('"')
            continue
        if split_joiner != '':
            if line_split[i][-1] == '"':
                split_joiner += "," + line_split[i].rstrip('"')
            else:
                split_joiner += "," + line_split[i]
                continue
        if split_joiner == '':
            split_joiner = line_split[i]
        if "opening_hand_" in split_joiner:
            for d in opening_hand_dict.values():
                d[split_joiner.lstrip("opening_hand_")] = [0,0]
            for d in drawn_dict.values():
                d[split_joiner.lstrip("opening_hand_")] = [0,0]
            for d in tutored_dict.values():
                d[split_joiner.lstrip("opening_hand_")] = [0,0]
            for d in deck_dict.values():
                d[split_joiner.lstrip("opening_hand_")] = [0,0]
            for d in sideboard_dict.values():
                d[split_joiner.lstrip("opening_hand_")] = [0,0]
        if split_joiner != '':
            split_joiner = ''

def analyze_path(path):
    started = False
    processed = 0
    finput = fileinput.input(path)
    for line in finput:
        if not started:
            process_header(line)
            started = True
            continue
        processed += 1
        if processed % 10000 == 0:
            print(f'{datetime.now()}: Processed {processed} entries!')
        line_split = line.split(',')
        
        color = line_split[GameIndexArray.main_colors.value[0]]
        victory = line_split[GameIndexArray.won.value[0]]
        card_idx = 0
        length = len(line_split)
        for i in range(GameIndexArray.card.value, length):       
            if card_idx == len(opening_hand_dict["All"].keys()):
                break
            card = list(opening_hand_dict["All"].keys())[card_idx]

            if i % 5 == 3:
                increment_dict(opening_hand_dict, color, card, float(line_split[i]), victory)
            if i % 5 == 4:
                increment_dict(drawn_dict, color, card, float(line_split[i]), victory)
            if i % 5 == 0:
                increment_dict(tutored_dict, color, card, float(line_split[i]), victory)
            if i % 5 == 1:
                increment_dict(deck_dict, color, card, float(line_split[i]), victory)
            if i % 5 == 2:
                increment_dict(sideboard_dict, color, card, float(line_split[i]), victory)
                card_idx += 1


    with open(f'data\\{set}\\{format}\\game_results.json', "w") as outfile: 
        json.dump([{"OpeningHand": opening_hand_dict}, 
                   {"Drawn": drawn_dict}, 
                   {"Tutored": tutored_dict},
                   {"Deck": deck_dict}, 
                   {"Sideboard": sideboard_dict}], outfile)
    finput.close()

sets = os.listdir('data')
for set in sets:
    formats = os.listdir(f'data\\{set}')
    for format in formats:
        path = f'data\\{set}\\{format}\\game_data.csv'
        if os.path.isfile(path):
            analyze_path(path)



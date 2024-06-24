from datetime import datetime
from enum import Enum
import os
import string
from typing import OrderedDict
import json
import fileinput


def get_csv_line_as_array(line):
    line = ''.join([str(char) for char in line if char in string.printable])
    return_array = []
    line.lstrip()
    line.rstrip()
    line_split = line.split('"')
    for i in range(1, len(line_split), 2):
        return_array.append(line_split[i])
    return return_array


def analyze_manual_download():
    set_name = 'MH3'
    path = f'data\\{set_name}\\manual_downloads'

    card_dict = {}
    for f in os.listdir(path):
        archetype = f.split('.')[-2]
        with open(f'{path}\\{f}') as working_file:
            header = True
            for line in working_file:
                if header:
                    header = False
                    continue
                line_split = get_csv_line_as_array(line)
                name = line_split[0]
                if line_split[15] == '':
                    gih_wr = 0
                else:
                    gih_wr = float(line_split[15].strip('%'))/100
                if name not in card_dict:
                    card_dict[name] = {archetype: gih_wr}
                else:
                    card_dict[name][archetype] = gih_wr

    print('Dictionary loaded & ready for analysis!')
    return card_dict






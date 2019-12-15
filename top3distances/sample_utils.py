#!/usr/bin/env python3

import json


def get_uniq_names(namelist_file):
    with open(namelist_file, 'r') as json_file:
        data = json.load(json_file)
        names_list = []
        for p in data:
            names_list.append(p['fullname'])

        return names_list

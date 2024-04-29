#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Simon Mille

import json
import codecs
import sys
import os
# The idea is simply to combine the entries that have the same ID in the original reference structuring file, so as to have a file with 1,408 inputs instead of 2,774 (the latter corresponds to one input per different ordering).

path_gold_structuring = sys.argv[1]
head, tail = os.path.split(path_gold_structuring)
# The json looks like this inside:
# [{"eid": "Id285", "category": "Airport", "size": "2", "source": ["<TRIPLE>", "Aarhus_Airport", "operatingOrganisation", "\"Aarhus_Lufthavn_A/S\"", "</TRIPLE>", "<TRIPLE>", "Aarhus_Airport", "runwayLength", "2777.0", "</TRIPLE>"], "targets": [{"lid": "Id1", "comment": "good", "output": ["<SNT>", "operatingOrganisation", "runwayLength", "</SNT>"]}, {"lid": "Id2", "comment": "good", "output": ["<SNT>", "operatingOrganisation", "runwayLength", "</SNT>"]}]}...]

contents_gold_struct = ''
with codecs.open(path_gold_structuring, 'r', 'utf-8') as json_file:
  contents_gold_struct = json.load(json_file)

grouped_contents_gold_struct = []
# We'll keep track in dico_id of all IDs we've seen so far
counter_new_inputs = 0
previous_id = ''
for datapoint in contents_gold_struct:
  # If the ID of the input has just been seen, add the info about structuring to the previous datapoint
  if datapoint['eid'] == previous_id:
    for new_target in datapoint['targets']:
      grouped_contents_gold_struct[counter_new_inputs-1]['targets'].append(new_target)
  # If the ID of the input is new, just copy the datapoint as such in the final datastructure
  else:
    grouped_contents_gold_struct.append(datapoint)
    counter_new_inputs += 1
  previous_id = datapoint['eid']

print(f'The created file has {len(grouped_contents_gold_struct)} data points.')

ordANDstruct_folder = None
exist_oANDs_folder = False
if head.rsplit('/', 1)[1] == 'structing':
  ordANDstruct_folder = os.path.join(head.rsplit('/', 1)[0], 'orderingANDstructing')
  if not os.path.exists(ordANDstruct_folder):
    os.makedirs(ordANDstruct_folder)
  exist_oANDs_folder = True

if exist_oANDs_folder == True:
  with open(os.path.join(ordANDstruct_folder, 'test.json'), 'w') as fp:
    json.dump(grouped_contents_gold_struct, fp)
    print(f'Created file in {ordANDstruct_folder}.')
else:
  with open(os.path.join(head, 'orderingANDstructuring_gold-test.json'), 'w') as fp:
    json.dump(grouped_contents_gold_struct, fp)
    print(f'Created file in {head}.')

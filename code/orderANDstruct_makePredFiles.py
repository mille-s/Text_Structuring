#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Simon Mille

import glob
import json
import os
import codecs
import re
import sys

# The original structuring files have 2,774 data points. I want the structuring prediction of Thiago's modules given each of the 1,408 WebNLG inputs (instead of for each possible ordering).
# For each predicted ordering, simply retrieve the corresponding predicted structuring

input_folder = sys.argv[1]
path_gold_structuring = os.path.join(input_folder, 'structuring_gold-test.json')
pred_files_paths = glob.glob(os.path.join(input_folder, '*.postprocessed'))

contents_gold_struct = ''
with codecs.open(path_gold_structuring, 'r', 'utf-8') as json_file:
  contents_gold_struct = json.load(json_file)

def extract_lines(filepath, task):
  pred_lines = []
  pred_ordering_lines_raw = codecs.open(pred_filepath, 'r', 'utf-8').readlines()
  for line_raw in pred_ordering_lines_raw:
    pred_lines.append(line_raw.strip())
  return pred_lines

def extract_properties_from_structuring(struct_predictions):
  struct_predictions_properties = re.subn('<SNT>', '', struct_predictions)[0]
  struct_predictions_properties = re.subn('</SNT>', '', struct_predictions_properties)[0]
  while re.search('  ', struct_predictions_properties):
    struct_predictions_properties = re.subn('  ', ' ', struct_predictions_properties)[0]
  struct_predictions_properties = struct_predictions_properties.strip()
  return struct_predictions_properties

pred_ordering_lines = None
pred_structuring_lines = None

filename_struct = None

# Read predicted files and store the contents into a list
for pred_filepath in sorted(pred_files_paths):
  task = pred_filepath.split('_', 1)[0].rsplit('/', 1)[1]
  filename = pred_filepath.split('_', 1)[1]
  # print(task, filename)
  if task == 'ordering':
    pred_ordering_lines = extract_lines(pred_filepath, task)
  elif task == 'structuring':
    pred_structuring_lines = extract_lines(pred_filepath, task)
    filename_struct = filename

# Build a list for predicted structurings aligned with the orderings list. This list this contains 1,408 elements; each element is 2 lists:
# 1 list of the possible structurings for each of the 1,408 inputs, and 1 list of the same info stripped of the <SNT> and </SNT> tags, to align with the orderings.
# The file contents_gold_struct (more precisely, the eid of the data points) is used as reference to know when to predicted structurings come from the same datapoint.
list_structuring_aligned_with_ordering = []
counter_new_inputs = 0
previous_id = None
for struct_predictions, struct_gold in zip(pred_structuring_lines, contents_gold_struct):
  # If the id of the data point was seen before, add info to the existing lists
  if struct_gold['eid'] == previous_id:
    # Add current prediction to the first list
    list_structuring_aligned_with_ordering[counter_new_inputs-1][0].append(struct_predictions)
    # Get the list of properties without the SNT tags
    struct_predictions_properties = extract_properties_from_structuring(struct_predictions)
    # Add list of properties to the second list
    list_structuring_aligned_with_ordering[counter_new_inputs-1][1].append(struct_predictions_properties)
  else:
    # If we have a new data point, create the two lists in list_structuring_aligned_with_ordering
    list_structuring_aligned_with_ordering.append([[], []])
    # Add current prediction to the first list
    list_structuring_aligned_with_ordering[counter_new_inputs][0].append(struct_predictions)
    # Get the list of properties without the SNT tags
    struct_predictions_properties = extract_properties_from_structuring(struct_predictions)
    # Add list of properties to the second list
    list_structuring_aligned_with_ordering[counter_new_inputs][1].append(struct_predictions_properties)
    counter_new_inputs += 1
  previous_id = struct_gold['eid']

# Now for each of the 1,408 datapoints, retrieve the structuring that corresponds to the predicted ordering.
list_structurings_one_per_WebNLG_input = []
for j, (pred_ordering, pred_structurings) in enumerate(zip(pred_ordering_lines, list_structuring_aligned_with_ordering)):
  if pred_ordering in pred_structurings[1]:
    index_matching_ordering = pred_structurings[1].index(pred_ordering)
    list_structurings_one_per_WebNLG_input.append(pred_structurings[0][index_matching_ordering])
  # If no predicted ordering matches a gold ordering (i.e there is no corresponding structuring), simply copy the ordering with initial-final <SNT>-</SNT> tags
  else:
    new_structuring = '<SNT> '+pred_ordering+' </SNT>'
    list_structurings_one_per_WebNLG_input.append(new_structuring)

print(f'Created file for {filename_struct} ({len(list_structuring_aligned_with_ordering)} data points).')

fo_name = 'orderANDstruct_'+filename_struct
with codecs.open(os.path.join(input_folder, fo_name), 'w', 'utf-8') as fo:
  for new_dtp in list_structurings_one_per_WebNLG_input:
    fo.write(new_dtp)
    fo.write('\n')
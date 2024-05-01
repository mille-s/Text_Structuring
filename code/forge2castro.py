#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Simon Mille
import sys
import codecs
import re
import os

mflens_data_folder = sys.argv[1]
forge_file_name = sys.argv[2]

path_forge_out = os.path.join(mflens_data_folder, forge_file_name)

class CoNLL_line:
  def __init__(self, conll_line):
    columns = conll_line.strip().split('\t')
    # I convert everything to str to make comparisons safer
    self.id = str(columns[0])
    self.form = str(columns[1])
    self.lemma = str(columns[2])
    self.pos = str(columns[3])
    self.cpos = str(columns[4])
    self.feats = str(columns[5])
    self.in_prop = None
    if re.search('\|', self.feats):
      feats_list = self.feats.split('|')
      for feat in feats_list:
        if re.search('in_prop=', feat):
          self.in_prop = feat.split('in_prop=')[1]
    else:
      if re.search('in_prop=', self.feats):
        self.in_prop = self.feats.split('in_prop=')[1]
    self.gov = str(columns[6])
    self.deprel = str(columns[7])
    self.pgov = str(columns[8])
    self.pdeprel = str(columns[9])
    # To mark when a line was used in the output
    self.used = False

forge_out_read = codecs.open(path_forge_out, 'r', 'utf-8').read().split('\n\n')

lines_forge_ordering = []
lines_forge_structuring = []
for j, conll_out in enumerate(forge_out_read):
  # Ignore the last structure which is empty
  if not conll_out == '':
    # print(f'Text #{j}')
    lines = conll_out.split('\n')
    # We'll store in list_line_objects one object of class CoNLL_line for each line
    list_line_objects = []
    for line in lines:
      # Skip lines with metadata
      if not line.startswith('#'):
        new_line_object = CoNLL_line(line)
        list_line_objects.append(new_line_object)
        # print(new_line_object.in_prop)
    line_ordering = ''
    line_structuring = '<SNT> '
    for i, line_object in enumerate(list_line_objects):
      # Everytime we find a dot as word form, insert sentence boundary tags
      if line_object.form == '.':
        if i < len(list_line_objects) - 1:
          line_structuring = line_structuring+'</SNT> <SNT> '
        # If it's the final dot, there is no sentence after it
        else:
          line_structuring = line_structuring+'</SNT>'
      # Otherwose, just write the peoperty name
      elif not line_object.in_prop == None:
        line_ordering = line_ordering+line_object.in_prop+' '
        line_structuring = line_structuring+line_object.in_prop+' '
    lines_forge_ordering.append(line_ordering)
    lines_forge_structuring.append(line_structuring)
    # print(line_ordering)
    # print(line_structuring)
  
with codecs.open(os.path.join(mflens_data_folder, 'ordering_forge-test.out.postprocessed'), 'w', 'utf-8') as fo_order:
  for line_forge_ordering in lines_forge_ordering:
    fo_order.write(line_forge_ordering)
    fo_order.write('\n')
  print(f'Created file ordering_forge-test.out.postprocessed in {mflens_data_folder}.')

with codecs.open(os.path.join(mflens_data_folder, 'structuring_forge-test.out.postprocessed'), 'w', 'utf-8') as fo_struct:
  for line_forge_structuring in lines_forge_structuring:
    fo_struct.write(line_forge_structuring)
    fo_struct.write('\n')
  print(f'Created file structuring_forge-test.out.postprocessed in {mflens_data_folder}.')
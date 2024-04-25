#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Simon Mille

import codecs
import re
import sys
import difflib
import sys

pathFile2process = sys.argv[1]
print_debug = sys.argv[2]
out_file_ord = sys.argv[3]
out_file_struct = sys.argv[4]

sent_delim = '</SNT> <SNT>'

conll_structures_file =  codecs.open(pathFile2process, 'r', 'utf-8').read()
# Get end of line delimiter and split input files into separate conll structures
eol = None
conll_structures = None
if re.search('\r\n', conll_structures_file):
  conll_structures = conll_structures_file.split('\r\n\r\n')
  eol = '\r\n'
elif re.search('\n', conll_structures_file):
  conll_structures = conll_structures_file.split('\n\n')
  eol = '\n'
else:
  print('End of line delimiter unknown.')
# Remove last structure if empty
if conll_structures[-1] == '':
  conll_structures = conll_structures[:-1]

print(f'{len(conll_structures)} CoNLL structures found.')

def getNextItem_intra(lists_ordered_properties, conll_as_lineObjects, list_gov_deprel, last_element_intra, index, print_debug, altID_ToRemov = None):
  if print_debug == True:
    if altID_ToRemov == None:
      print(f'  Found {str(last_element_intra[-index])}_intra!')
    else:
      print(f'  Found {str(altID_ToRemov)}_intra (altID)!')
  # Loop over the list of lines to find the line of the property that should follow
  for conll_line in conll_as_lineObjects:
    # if print_debug == True:
    #   print(f'  -----------\n  AltID_ToRemov: {altID_ToRemov}')
      # print(f'  Node gov in CoNLL: {conll_line.gov}')
      # print(f'  Node deprel in CoNLL: {conll_line.deprel}')
      # print(f'  Node used: {conll_line.used}')
      # if conll_line.gov == last_element_intra[-index]:
      #   print(f'  conll_line.gov check OK')
      # elif conll_line.gov == altID_ToRemov:
      #   print(f'  conll_line.gov check OK (altID)')
      # if conll_line.deprel == 'intra':
      #   print(f'  conll_line.deprel check OK')
      # if conll_line.used == False:
      #   print(f'  conll_line.used check OK')
    if (conll_line.gov == last_element_intra[-index] or conll_line.gov == altID_ToRemov) and conll_line.deprel == 'intra' and conll_line.used == False:
      # if print_debug == True:
      #   print(f'  altID_ToRemov: {altID_ToRemov}')
      conll_line.used = True
      lists_ordered_properties.append(conll_line.form)
      if print_debug == True:
        print(f'  ->Added {conll_line.form}!')
      # Remove the description of the last element from list_gov_deprel
      if altID_ToRemov == None:
        list_gov_deprel.remove(f'{str(last_element_intra[-index])}_intra')
        if print_debug == True:
          print(f'  ->Removed {str(last_element_intra[-index])}_intra')
      # Or remove the description of another element in case the last one from list_gov_deprel could not be used
      else:
        list_gov_deprel.remove(f'{str(altID_ToRemov)}_intra')
        if print_debug == True:
          print(f'  ->Removed {str(altID_ToRemov)}_intra')
      # Update the ID of the node that is now the last one for "intra"
      last_element_intra.append(conll_line.id)
  return list_gov_deprel, last_element_intra

def getNextItem_inter(lists_ordered_properties, conll_as_lineObjects, list_gov_deprel, last_element_intra, last_element_inter, index, print_debug, altID_ToRemov = None):
  if print_debug == True:
    if altID_ToRemov == None:
      print(f'  Found {str(last_element_inter[-index])}_inter!')
    else:
      print(f'  Found {str(altID_ToRemov)}_inter (altID)!')
  # Loop over the list of lines to find the line of the property that should follow
  for conll_line in conll_as_lineObjects:
    # if print_debug == True:
    #   print(f'  Node gov in CoNLL: {conll_line.gov}')
    if (conll_line.gov == last_element_inter[-index] or conll_line.gov == altID_ToRemov) and conll_line.deprel == 'inter' and conll_line.used == False:
      # if print_debug == True:
      #   print(f'  altID_ToRemov: {altID_ToRemov}')
      conll_line.used = True
      lists_ordered_properties.append(sent_delim)
      lists_ordered_properties.append(conll_line.form)
      if print_debug == True:
        print(f'  ->Added {conll_line.form}!')
      # Remove the description of the last element from list_gov_deprel
      if altID_ToRemov == None:
        list_gov_deprel.remove(f'{str(last_element_inter[-index])}_inter')
        if print_debug == True:
          print(f'  ->Removed {str(last_element_intra[-index])}_inter')
      # Or remove the description of another element in case the last one from list_gov_deprel could not be used
      else:
        list_gov_deprel.remove(f'{str(altID_ToRemov)}_inter')
        if print_debug == True:
          print(f'  ->Removed {str(altID_ToRemov)}_inter')
      # Update the IDs of the nodes that are now the last one for "intra" and "inter"
      last_element_intra.append(conll_line.id)
      last_element_inter.append(conll_line.id)
  return list_gov_deprel, last_element_intra, last_element_inter

class CoNLL_line:
  def __init__(self, conll_line):
    columns = conll_line.strip().split('\t')
    # for column in columns:
    #   if re.search('\ufeff', column):
    #     print('Found BOM!')
    # self.id = re.subn('\ufeff', '', columns[0])[0]
    # I convert everything to str to make comparisons safer
    self.id = str(columns[0])
    self.form = str(columns[1])
    self.lemma = str(columns[2])
    self.pos = str(columns[3])
    self.cpos = str(columns[4])
    self.feats = str(columns[5])
    self.gov = str(columns[6])
    self.deprel = str(columns[7])
    self.pgov = str(columns[8])
    self.pdeprel = str(columns[9])
    # To mark when a line was used in the output
    self.used = False

# Split each structure into lines, and create a CoNLL_line object for each line
# list_conlls_as_lineObjects thus is a list of lists of CoNLL_line objects
list_conlls_as_lineObjects = []
for conll_structure in conll_structures:
  conll_lines = conll_structure.split(eol)
  list_line_objects = [CoNLL_line(conll_line) for conll_line in conll_lines]
  list_conlls_as_lineObjects.append(list_line_objects)

# Store here the final output
lists_properties_ordered_struct = []
# Store here the info about when fallback nodes were used
fallback_node = {'0':[], '1':[], '2':[], '3':[], '4':[], '5':[], '6':[]}
for i, conll_as_lineObjects in enumerate(list_conlls_as_lineObjects):
  if print_debug == True:
    print(f'\nProcessing input #{i}')
  lists_properties_ordered_struct.append([])
  # Save last element used to attach the next one to
  last_element_intra = []
  last_element_inter = []
  # Store here the info of all the nodes regarding their respective governor IDs and deprels
  list_gov_deprel = []
  # Get the first node, and list all combinations of gov/deprel in the structure
  for conll_line0 in conll_as_lineObjects:
    list_gov_deprel.append(f'{conll_line0.gov}_{conll_line0.deprel}')
    if conll_line0.deprel == 'ROOT':
      lists_properties_ordered_struct[i].append(conll_line0.form)
      if print_debug == True:
        print(f'  ->Added {conll_line0.form}!')
      last_element_intra.append(conll_line0.id)
      last_element_inter.append(conll_line0.id)
      list_gov_deprel.remove('0_ROOT')
  if print_debug == True:
    print(list_gov_deprel)
  # A well-formed structure should only have unique gov_deprel pairs (a node can have at most on inter and at most one intra relations below it) 
  # if not len(list_gov_deprel) == len(set(list_gov_deprel)):
  #   sys.exit(f'Duplicate linear order in {i}')

  # Each time we'll find and use a gov_deprel, it will be removed from the list
  counter = 0
  while len(list_gov_deprel) > 0:
    if print_debug == True:
      print(f'Intra: {last_element_intra}, Inter: {last_element_inter}')
    # Index to use to retrieve the right preceding node
    index = 1
    # If the current (last to date) node has other "intra" dependents
    if f'{str(last_element_intra[-1])}_intra' in list_gov_deprel:
      list_gov_deprel, last_element_intra = getNextItem_intra(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, index, print_debug)
    # Once the intra nodes are checked, check if the current node has an "inter" dependent
    elif f'{str(last_element_inter[-index])}_inter' in list_gov_deprel:
      list_gov_deprel, last_element_intra, last_element_inter = getNextItem_inter(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, last_element_inter, index, print_debug)
    # For "intra" dependents, if no next node can be found after the last one, check if it can be found after the previous nodes in the list (it happens if there are several nodes with the same gov_deprel combination)
    elif len(last_element_intra) > 1 and f'{str(last_element_intra[-2])}_intra' in list_gov_deprel:
      index = 2
      list_gov_deprel, last_element_intra = getNextItem_intra(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, index, print_debug)
      fallback_node[str(index)].append('intra_'+str(i))
    elif len(last_element_intra) > 2 and f'{str(last_element_intra[-3])}_intra' in list_gov_deprel:
      index = 3
      list_gov_deprel, last_element_intra = getNextItem_intra(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, index, print_debug)
      fallback_node[str(index)].append('intra_'+str(i))
    elif len(last_element_intra) > 3 and f'{str(last_element_intra[-4])}_intra' in list_gov_deprel:
      index = 4
      list_gov_deprel, last_element_intra = getNextItem_intra(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, index, print_debug)
      fallback_node[str(index)].append('intra_'+str(i))
    elif len(last_element_intra) > 4 and f'{str(last_element_intra[-5])}_intra' in list_gov_deprel:
      index = 5
      list_gov_deprel, last_element_intra = getNextItem_intra(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, index, print_debug)
      fallback_node[str(index)].append('intra_'+str(i))
    elif len(last_element_intra) > 5 and f'{str(last_element_intra[-6])}_intra' in list_gov_deprel:
      index = 6
      list_gov_deprel, last_element_intra = getNextItem_intra(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, index, print_debug)
      fallback_node[str(index)].append('intra_'+str(i))
    # For "inter" dependents, if the gorvernor does not appear in the list of potential last "inter" nodes, check in the "intra" list for a gov and place the new "inter" after the last property (index=1)
    elif len(last_element_intra) > 1 and f'{str(last_element_intra[-2])}_inter' in list_gov_deprel:
      index = 1
      list_gov_deprel, last_element_intra, last_element_inter = getNextItem_inter(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, last_element_inter, index, print_debug, altID_ToRemov=str(last_element_intra[-2]))
      fallback_node[str(index)].append('inter_'+str(i))
    elif len(last_element_intra) > 2 and f'{str(last_element_intra[-3])}_inter' in list_gov_deprel:
      index = 1
      list_gov_deprel, last_element_intra, last_element_inter = getNextItem_inter(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, last_element_inter, index, print_debug, altID_ToRemov=str(last_element_intra[-3]))
      fallback_node[str(index)].append('inter_'+str(i))
    elif len(last_element_intra) > 3 and f'{str(last_element_intra[-4])}_inter' in list_gov_deprel:
      index = 1
      list_gov_deprel, last_element_intra, last_element_inter = getNextItem_inter(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, last_element_inter, index, print_debug, altID_ToRemov=str(last_element_intra[-4]))
      fallback_node[str(index)].append('inter_'+str(i))
    elif len(last_element_intra) > 4 and f'{str(last_element_intra[-5])}_inter' in list_gov_deprel:
      index = 1
      list_gov_deprel, last_element_intra, last_element_inter = getNextItem_inter(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, last_element_inter, index, print_debug, altID_ToRemov=str(last_element_intra[-5]))
      fallback_node[str(index)].append('inter_'+str(i))
    elif len(last_element_intra) > 5 and f'{str(last_element_intra[-6])}_inter' in list_gov_deprel:
      index = 1
      list_gov_deprel, last_element_intra, last_element_inter = getNextItem_inter(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, last_element_inter, index, print_debug, altID_ToRemov=str(last_element_intra[-6]))
      fallback_node[str(index)].append('inter_'+str(i))
    # Sometimes the parser retuns things like "0 intra" or "0 inter". Use the ID of the root to use as an anchor in case of bad parsing, and order immediately after the last available node.
    elif f'0_intra' in list_gov_deprel:
      list_gov_deprel, last_element_intra = getNextItem_intra(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, index, print_debug, altID_ToRemov='0')
      fallback_node['0'].append('intra_'+str(i))
    # Once the intra nodes are checked, check if the current node has an "inter" dependent
    elif f'0_inter' in list_gov_deprel:
      list_gov_deprel, last_element_intra, last_element_inter = getNextItem_inter(lists_properties_ordered_struct[i], conll_as_lineObjects, list_gov_deprel, last_element_intra, last_element_inter, index, print_debug, altID_ToRemov='0') 
      fallback_node['0'].append('inter_'+str(i))
    else:
      sys.exit(f'Uncovered configuration in #{i}')

  if print_debug == True:
    print(f'----------------\nPredicted order: {lists_properties_ordered_struct[i]}')

print('\n====================================\n')
# Get a version of the output with only the order (no structuring)
lists_properties_ordered = []
for list_properties_wdelim in lists_properties_ordered_struct:
  list_propertiesOnly = [list_item for list_item in list_properties_wdelim if not list_item == sent_delim]
  lists_properties_ordered.append(list_propertiesOnly)

# Write ordering file and at the same time check that we didn't lose any property in the process
with codecs.open('ordering_MFleNS-test.out.postprocessed', 'w', 'utf-8') as fo_ord:
  count_mismatches = 0
  for id_ord, (input, output_ord) in enumerate(zip(list_conlls_as_lineObjects, lists_properties_ordered)):
    if not len(input) == len(output_ord):
      print(f'ERROR structure #{id_ord}')
      count_mismatches += 1
    fo_ord.write(' '.join(output_ord))
    if id_ord < len(lists_properties_ordered) - 1:
      fo_ord.write('\n')
  if count_mismatches == 0:
    print('The number of properties in the inputs looks good!')

# Write srtructuring file
with codecs.open('structuring_MFleNS-test.out.postprocessed', 'w', 'utf-8') as fo_struct:
  for id_struct, output_struct in enumerate(lists_properties_ordered_struct):
    fo_struct.write('<SNT> '+' '.join(output_struct)+' </SNT>')
    if id_struct < len(lists_properties_ordered_struct) - 1:
      fo_struct.write('\n')

print('Details of the structures on which fallback applied:')
total_fallbacks = 0
for key in fallback_node:
  print(f'  {key}: {fallback_node[key]}')
  total_fallbacks += len(fallback_node[key])
print(f'Fallback applied in {total_fallbacks} cases.')
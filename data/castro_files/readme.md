- ordering_gold-test.json:
  - 1,408 data points, 2,774 different orderings.
  - from Thiago’s GitHub
  - all possible orderings extracted from the WebNLG data given a WebNLG input.

- structuring_gold-test.json:
  - 2,774 data points, more possible structurings (haven’t counted them)
  - from Thiago’s GitHub
  - all possible structurings extracted from the WebNLG data given a WebNLG ordering.

- ordering_gold-SM-test.json:
  - output of me running Thiago’s code to get the reference ordering file; different order from the one used in the evals.

- orderingANDstructuring_gold-test.json:
  - 1,408 data points
  - created with [this code](https://github.com/mille-s/Text_Structuring/blob/main/code/orderANDstruct_makeRefFile.py); I just combined the outputs of the datatpoints that have the same ID in structuring_gold-test.json.
  - all possible orderings/structurings given a WebNLG input.

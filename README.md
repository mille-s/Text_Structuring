# Text_Structuring

This is the documentation of the repository that contains all the files used in the 2024 TextStructuring experiments.

## Experiment overall description

I extracted data from the Enhanced WebNLG dataset (Castro Ferreira et al., 2018) in the form of CoNLL-U trees in order to learn two early-stage generation subtasks: triple ordering and text structuring, in the sense of Castro Ferreira et al. (2019). Using syntactic parsing techniques, I try to learn how to order a set of input triples, package them into sentences, or both at the same time. As training data, I try a variety of data combinations in which the number of data points and their specifications can vary (see below for more details).

The CoNLL-U annotation is very simple; considering the following text plan: **\<SNT\> Prop1 Prop2 Prop3 \</SNT\> \<SNT\> Prop4 Prop5 \</SNT\>**.

Two consecutive properties in the same sentence are assigned a dependency edge 'intra': **Prop1 -intra-> Prop2, Prop2 -intra-> Prop3, Prop4 -intra-> Prop5**.
  
The first properties of two consecutive sentences are assigned the dependency ‘inter’: **Prop1 -inter-> Prop4**.

Example with 3 sentences:
- \[nationality, occupation, birthPlace\]S1 
- \[almaMater\]S2
- \[selectedByNasa, timeInSpace\]S3

![image](https://github.com/mille-s/Text_Structuring/blob/main/images/textStruct1.png)

In the CoNLL-U format:

![image](https://github.com/mille-s/Text_Structuring/blob/main/images/textStruct2.png)

## Experiment types
- Ordering only
  - 1.4K input/output pairs: there are 1.4K WebNLG inputs of size 2 and above (ordering and structuring are not relevant for size 1);
  - input = set of triples in random order;
  - output: set of triples in a predicted order.
- Structuring only
  - 2.7K input/output pairs: there are 2.7K different orderings for the 1.4K WebNLG inputs of size 2 and above, all of which are used to predict a specific structuring in Thiago’s original experiment;
  - input = set of triples in gold order;
  - output: set of triples in gold order with predicted sentence delimiters.
- Ordering + structuring
  - 1.4K input/output pairs: this was not part of Thiago’s experiments;
  - input = set of triples in random order;
  - output: set of triples in predicted order with predicted sentence delimiters.
 
## References

[Enriching the WebNLG corpus](https://aclanthology.org/W18-6521) (Castro Ferreira et al., INLG 2018)

[Neural data-to-text generation: A comparison between pipeline and end-to-end architectures](https://aclanthology.org/D19-1052) (Castro Ferreira et al., EMNLP-IJCNLP 2019)

# Repository contents

## ipynb files

### Thiago_Pipeline_Eal.ipynb
Code adapted from Castro et al's evaluation code. It replicates exactly their results, and allows for evaluating the modules created for the present experiments. 

## code
- conll2castro.py: to convert parser outputs to the format used in Castro et al's evaluation.
- forge2castro.py: to convert FORGe outputs to the format used in Castro et al's evaluation.
- orderANDstruct_makePredFiles.py: to build Castro et al's predicted files for both Ordering and Structuring.
- orderANDstruct_makeRefFile.py: to build the reference files for both Ordering and Structuring.

## data

### malt_feats
Contains all feature configuration files for the different parsers used in the experiments.

### webnlg
Contains the WebNLG dataset converted to CoNLL-U format for training parsers on it.

### castro_files
Contains files from the original Castro et al's experiments, and some files extracted from it.

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
  - created with this Colab: https://colab.research.google.com/drive/17eZyXCT3NyAqHGkynWt8kAqj9uI-cC_F?usp=sharing (Cell “Make reference file structuring grouped”); I just combined the outputs of the datatpoints that have the same ID in structuring_gold-test.json.
  - all possible orderings/structurings given a WebNLG input.

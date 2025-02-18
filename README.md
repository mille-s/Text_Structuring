# Introduction to the Text Structuring experiments

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

## Data description
I describe here the data that can be produced by the [WebNLG_TextStructuring.ipynb](https://github.com/mille-s/Text_Structuring/blob/main/WebNLG_TextStructuring.ipynb) code. Each produced train/dev/test file has an extension that keeps track of what is inside, e.g. train_2AO, dev_2TOcad1r2. Codes are explained below:
- Input Size (mandatory)
  - Description: the size of the inputs in the data.
  - Possible values/Codes: 2-7 (**2**), 3-7 (**3**).
  - Rationale: Thiago’s original experiments are carried out with inputs of size 2 to 7; excluding inputs of size 2 may result in cleaner data (inputs of size two will almost always be packaged in the same sentence independently of the properties). 
- Inputs kept (mandatory)
  - Description: which inputs are filtered out of the data.
  - Possible values/Codes: All (**A**), 1 input per original WebNLG input triple set (**T**), Only truly unique inputs (**U**).
  - Rationale: Since for each WebNLG input there are more than 1 possible outputs, and in parsing usually there is only one correct parse per input sentence (with the context, ambiguous trees should not be ambiguous any more; even though the context outside of each sentence is usually not available to the parsers), I want to experiment with only one possible output per WebNLG input (T); also, since some data points are incomplete, it is possible to find duplicate inputs that were not originally duplicates (e.g. one property is missing in a 5-triple input, and it now looks like an existing 4-triple input); I wanted to try and remove those as well (U).
- Property label (mandatory?)
  - Description: the label of the property used in the CoNLL-U.
  - Location: Column 2.
  - Possible values/Codes: Original (**O**), Split (**S**)
  - Rationale: not sure about this one yet, I supposed that splitting each property following the camel casing could allow for better modeling the semantics of each property, especially if we are going to use embeddings. TBD.
- Lemma (optional)
  - Description: a more generic form of the property label.
  - Location: Column 3.
  - Possible values/Codes: -, last element of the camel case splitting (**e1**), output of a lemmatiser (**e2**). “e” instead of “l” because it is more readable.
  - Rationale: it may help the parser to have access to some slightly more generic label for each property.
- PoS (optional)
  - Description: part-of-speech column, which can hold a much more abstract label for each property.
  - Location: Column 4.
  - Possible values/Codes: -, abstract class (**p1**).
  - Rationale: Since PoS doesn’t really make sense for this task, we can use this column for an equivalent to PoS, i.e. a generic label attached to the property; I think of a mapping of the Subject class to just a few categories such as Human, Location, Object, etc.
- CPoS (optional)
  - Description: an even more abstract label than PoS.
  - Location: Column 5.
  - Possible values/Codes: I don’t think we need this.
  - Rationale:
- Feat[domain] (optional)
  - Description: the category of the subject of the triple.
  - Location: Column 6.
  - Possible values/Codes: -, merged class (**d1**), abstract class (**d2**), original (**d3**).
  - Rationale: Using the category of the Subject should definitely help with predicting the order and structure.
- Feat[range] (optional)
  - Description: the category of the object of the triple.
  - Location: Column 6.
  - Possible values/Codes: -, merged class (**r1**), abstract class (**r2**), original (**r3**).
  - Rationale: Using the category of the Object could also help with predicting the order and structure.
- Feat[coref] (optional)
  - Description: an ID that indicates coreference between elements of the sentence.
  - Location: Column 6.
  - Possible values/Codes: -, subj_id (**c1**), obj_id (**c2**), subj&obj_id (**c3**).

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
 
## Evaluations
Several evaluations are carried out.
- labeled Attachment Score for ordering (and ordering+structuring since both edges are predicted by the parser)
  - Using the 1.4K test file that corresponds to the training file used for the evaluated model.
  - CoNLL-U train/dev/test (scrambled) files created with [WebNLG_TextStructuring.ipynb](https://github.com/mille-s/Text_Structuring/blob/main/WebNLG_TextStructuring.ipynb).
  - CoNLL-U predicted files are the output of the parser.
- Labeled Attachment Score for structuring only
  - Using the same 2.7K 2T test file for each model.
  - CoNLL-U train/dev (not scrambled) files are created as the ordering LAS, but without running the scrambling step.
  - CoNLL-U test (not scrambled) file that contains gold annotations was created with [WebNLG_TextStructuring.ipynb](https://github.com/mille-s/Text_Structuring/blob/main/WebNLG_TextStructuring.ipynb) (Cell _Convert gold structuring file into CoNLL for eval with LAS_).
  - CoNLL-U predicted files are the output of the parser.
- Castro’s code for ordering only
  - Using the 2T-1.4K file for all models (i.e. the test file used by Thiago for his experiments, with all inputs of size 2 and above, and with one input per WebNLG datapoint).
  - The predicted files are the CONLL-U predicted files from LAS-ordering converted using [this code](https://github.com/mille-s/Text_Structuring/blob/main/code/conll2castro.py).
- Castro’s code for structuring only
  - Using the 2T-2.7K file for all models (i.e. the test file used by Thiago for his experiments, with all inputs of size 2 and above, and with one input per possible ordering of the properties).
  - The predicted files are the CONLL-U predicted files from LAS-structuring converted using [this code](https://github.com/mille-s/Text_Structuring/blob/main/code/conll2castro.py).
- Ordering+Structuring (New)
  - Using the 2T-1.4K file for all models (i.e. files that I made myself to evaluate both tasks at the same time, with all inputs of size 2 and above, and one input per WebNLG datapoint).
  - The reference file was converted using [this code](https://github.com/mille-s/Text_Structuring/blob/main/code/orderANDstruct_makeRefFile.py).
  - The predicted files were converted using [this code](https://github.com/mille-s/Text_Structuring/blob/main/code/orderANDstruct_makePredFiles.py).
 
## References

[Enriching the WebNLG corpus](https://aclanthology.org/W18-6521) (Castro Ferreira et al., INLG 2018)

[Neural data-to-text generation: A comparison between pipeline and end-to-end architectures](https://aclanthology.org/D19-1052) (Castro Ferreira et al., EMNLP-IJCNLP 2019)

# Repository contents

## ipynb files

### WebNLG_TextStructuring.ipynb
Code to enrich (in particular with class information) and convert the WebNLG data to the CoNLL-U or CoNLL-09 format. CoNLL-U is used as training data for MaltParser (see below). User can choose what to put in the dataset and build a custom training data that varies according to the parameters described in the _Data description_ section above.

### Parsers_training.ipynb
Code for training, running and evaluating intrinsically MaltParser (LAS), and converting the output to the format needed for Castro's text structuring evaluation (see below).

### MaltOptimizer.ipynb
Code for running MaltOptimizer and finding optimal settings for MaltParser.

### Thiago_Pipeline_Eal.ipynb
Code adapted from Castro et al's evaluation code. It replicates exactly their results, and allows for evaluating the text structuring modules created for the present experiments. 

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
  - created with the [notebook in this repo](https://github.com/mille-s/Text_Structuring/blob/main/Parsers_training.ipynb): (Cell “Make reference file structuring grouped”); I just combined the outputs of the datatpoints that have the same ID in structuring_gold-test.json.
  - all possible orderings/structurings given a WebNLG input.

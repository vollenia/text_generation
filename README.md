# text_generation

## Summary
The goal of this project is to train a language model on a random text and generate new text by utilizing this language model.

To run the the code execute _main.py_ and follow the instructions. In this process you will be prompted to enter the name of the text file that you want to use for training, the type of language model you want to create from this text, how many new sentences you want to generate and wheather you would like to save these newly generated sentences.
Only built-in modules are used and the code was tested to run under Python 3.8.10.  
This is all you need to know to train language models and generate new text.  

## Modules Overview

In what follows, a more detailed overview over the functionality of the text generation system is provided.

### 1. Tokenizing the training data (corpus.py)
The goal of the function _tokenize_ is to take a _.txt_ document and split it's content into tokens. This is achieved by reading the document line by line while stripping lines with text of line breaks. This process also aims at identifying punctuation marks and tokenizing them as individual tokens. Identifying punctuatuion marks ,however, requires them to be split from the token they are trailng. This is achieved by using a dictionary where the keys represent punctuation mark and the values a whitespace plus the corresponding punctuation mark (e.g.: ‘.’ : ‘ .’). This modification enables the punctuation marks to be affected during tokanization when the string is split using _whitespace_ as a separator.
In addition to that, all capitalized tokens not in sentence initial position are assumed to be proper names.
Ultimately,the tokanization process returns a set of proper names as well as a list of lists where each list consists of tokens from the corresponding line.

### 2. Training the language model (lm.py)
The whole system revolves around the _LanguageModel_ class. It is instantiated with the integer variable _n_ as the parameter which determines the structure of the generated n-gram model.
The model is trained by taking the tokenized text and turning it into a dictionary containing the history of length n-1 of a word as key and a dictionary of all the words having this history with the corresponding counts as value. In order to process the data and create this dictionary, the tokenized text is split into overlapping tuples of length _n_. The overlap is defined as the shift by one item after the creation of a tuple. 

### 3. Generating new token sequences (lm.py)
After a language model has been trained its knowledge can be used to generate text. The function that is central to this process is _p_next_. The goal of this function is to search the model and return a dictionary of possible words and their probabilities of appearing in the given context / being the next generated word.

The first step that is implemented in order for the whole generation process to work is the creation of the history for
the initial history / search. This is done by creating "None"-Tokens for the length of n-1 as padding. This history is then used for the initial search.

For the cese of a specific history not being covered by the language model, a history reduction mechanism is implemented.
In order to still have a successful search, the history of n-1 items is at first turned into a history of n-2 items, thereby reducing the amount of words required.
Afterwards, the search for the new history is performed by, on the fly, creating n-2 version of n-1 histories in the trained language model.
The process of reducing the history is repeated until the history is matched and at least one output is found.
This approach is an easy solution which does not require re-training a model and backing off to a different n-gram architecture, ultimately reducing the amount of training data required in order to be able to generate text.

After a match has been found, the function _normalize_ is called on the search results. This function takes the
resulting dictionary of the search from p_next and while leaving its keys, turns its values into probabilities. These probabilities are then returned by p_next.
The funcion _generate_ then uses this normalized dictionary and feeds it to the function _sample_. _Sample_ is a function that indirectly
uses the output of p_next and selects one of the keys. This is done by implementing the built in random module while also taking the probabilities of the words into account.

The final step consists of _generate_ appending the output of _sample_ to a list. After one iteration of _generate_ is
completed, the new history of n-1 is taken as history for the next generation. _Generate_ is repeatedly called until a padding symbol is matched again.
Additionally, an artificial text size barrier is implemented. In case the length of the generated text exceeds the number of 500 tokens, the generation process is stopped after the next punctuation mark.

### 4. Detokenizing newly generated sequences (corpus.py)
The goal of the function _detokenize_ is to take the final output of _generate_ and turn it into a string.
The first step consists of re-capitalizing of words. In this process, words that follow specific punctuation marks, incorporating the first word in a sentence, are capitalized. In addition to that, all instances of I (I, I'd, I'll, I'm, I've) are capitalized as well. Lastly, the set of proper names collected during tokenization is used to match and re-capitalize tokens.  
In order to avoid whitespaces between words and punctuation marks uppon joining the tokens into a string, the punctuation marks are identified and appended to the preceeding token.

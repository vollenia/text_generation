# text_generation

## Summary
The goal of this project is to train a language model (LM) on a random text and generate new text by utilizing this LM.
To run the the code execute main.py and follow the instructions. In this process you will be prompted to enter the name of the text file that you want to use for training, the type oflanguage model you want to create from this text, how many new sentences you want to generate and wheather you would like to save these newly generated sentences.
This is all you need to know to train LMs and generate new text.  

In what follows, a more detailed overview over the functionality of the system is provided.

1. Tokenizing the training data (corpus.py)
The goal of the function tokenize is to take a .txt document and perform tokenization. In the context of this project, tokenize opens a document and reads it line by line, while stripping lines with text of line breaks. Ultimately, this function creates a list of lists where each list consists of tokens from the corresponding line.
The tokanization process includes identifying punctuation marks and tokenizing them as individual tokens. This is achieved by using a dictionary  where the keys represent punctuation mark and the values a whitespace plus the corresponding punctuation mark (e.g.: ‘.’ : ‘ .’).
This modification enables the punctuation marks being affected during tokanization when the string is split by using whitespace as a separator.

((((Another approach to improve the results of the whole system, in particular of the detokenization, was to try to identify proper names in the training data. In order to test whether this would be achievable, a simplified subset of the training data was created where each line consisted of only one sentence. The idea was to look only at those words that are capitalized despite not being in sentence initial position. This approach failed due to inconsistencies in the capitalization in the dataset (e.g.: … people Choose Caesar for … ; … weak words Have struck … ; … is it physical To walk unbraced …). For the sake of authenticity the code used has been left in tokenize.)))

2. Training the language model
he whole system revolves around the LanguageModel class. It is instantiated with the integer variable n as the parameter which determines the structure of the generated n-gram model.
The LM is trained by taking the tokenized text and turning it into a dictionary containing the history of length n-1 of a word as key and a dictionary of all the words having this history with the corresponding counts as value. In order to process the data and create this dictionary the tokenized text is first split into overlapping tuples of length n. The overlap is defined as the shift by one item after the creation of a tuple. 

2. Generating new token sequences
After a language model has been trained its knowledge can be used to generate text. One of the central
functions is p_next. The goal of this function is to search the dictionary containing the counts and return a dictionary of possible words and their probabilities of appearing in the given context / being the next generated word.

The first step that has been implemented in order for the whole generation process to work was to create the history for
the initial history / search. This was done by creating "None"-Tokens for the length of n-1 as DAP symbols. This history is then used for the initial search.

For cese of a specific history not being covered by the language model a history reduction mechanism was implemented.
In order to still have a successful search the history of n-1 items is at first turned into a history of n-2 items, thereby reducing the amount of words required as history.
Afterwards, the search for the new history is performed by on the fly creating n-2 version of n-1 histories in the
trained language model. This process of reducing the history and is repeated until the history is matched and at least one output is found. This is an easy solution which does not require re-training a model and backing off to a different n-gram architecture.

After a match has been found, normalize, is called on the search results. This function takes the
result dictionary (words and counts of these words appearing in context of the given history) of the search from p_next and while leaving its keys turns its values into probabilities. These probabilities are then returned by p_next.




Generate then uses this normalized dictionary and feeds it to the function sample. Sample is function that indirectly
uses the output of p_next and selects one of the keys. This is done by implementing the built in random module while
also taking the probabilities of the words into account.


The final step consists of generate appending the output of sample to a list. After one iteration of generate is
completed the new history of n-1 is taken as history for the next generation. Generate is repeatedly called until a
DAP symbol is matched.

((z(In this context the probability of an infinite generation loop is very unlikely but still
possible. Therefore a safety feature was implemented. It activates when the length of the generated text exceeds 500
items, waits for the next punctuation mark, marks the new end and break the generation process.)))

4. Detokenizing newly generated sequences (corpus.py)
The goal of this function is to take the final output of generate and turn it into a single string.
The first step consisted of re-capitalizing specific words. In this process, words that followed specific punctuation
marks were capitalized incorporating the capitalization of the first word in a sentence. In addition to that, all instances of I (I, I'd, I'll, I'm, I've) were capitalized as well.

Joining the list of tokens at this point resulted in whitespaces in front of every punctuation mark. Therefore, the
second improvement consisted of removing these whitespaces by identifying the position of the punctuation mark
adding the punctuation mark to the preceding item and deleting the original instance.

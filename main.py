from corpus import *
from lm import *

# Selecting text data for training
text = str(input('STEP 1/4 | Which text would you like to use as training data?'+'\n'+\
                       '           File name: '))
tokens, proper_names = (tokenize(text))

# Selecting the type of n-Gram model
ngram_type = int(input('STEP 2/4 | Which type of n-gram LM would you like to create?'+'\n'+\
                       '           Enter Nr: '))
ngram_lm = LanguageModel(ngram_type)
test_lm = ngram_lm.train(tokens)

# Generating text
nr_of_texts = int(input('STEP 3/4 | How many lines would you like to generate?'+'\n'+\
                       '           Enter Nr: '))
texts = []
for text in range(nr_of_texts):
    generated_text = ngram_lm.generate()
    fluent2 = (detokenize(generated_text, proper_names))
    texts.append(fluent2)
    texts.append('-'*10)   
final_texts = '\n'.join(texts)
print('Generated text:')
print(final_texts)

# Storing the generated text
store_texts = str(input('STEP 4/4 | Do you want to save the text?'+'\n'+\
                       '           [Texts will be written into the file: '\
                                   'generated_text.txt]'+'\n'+\
                       '           (y/n): '))
if store_texts == 'y':
    file = open('generated_text.txt', 'w' )
    file.write(final_texts)
    file.close()

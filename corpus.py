# Segmenting lines into tokens
def tokenize(text): # Input: .txt doc | Output: list of lists(lines) containing tokens
    punct = {'.':' .', ',':' ,', '!':' !', '?':' ?', ';':' ;', ':':' :'}
    end_punct = ['.', '!', '?']
    I = ['I', 'I\'ll', 'I\'m', 'I\'d', 'I\'ve']
    doc = open(text, 'r', encoding = 'utf8').readlines()
    token_sequences = []
    proper_names = set()
    
    # Removing \n, processing punctuation, converting to list
    for line in doc:
        if line != '\n':
            line = line.strip('\n')
            # Punctuation as intividual token
            for item in line:
                if item in punct.keys():
                    line = line.replace(item, punct[item])    
        line = line.split()
        
        # Identifying capitalized tokens not in sentence initial position --> proper names
        for i, item in enumerate(line):
            if i != 0 and item not in I:
                if item[0].isupper() and line[i-1] not in end_punct:
                    proper_names.add(item.lower())
            line[i] = item.lower()
        token_sequences.append(line)

    return(token_sequences, proper_names)

# Recreating lines from tokens
def detokenize(tokens, proper_names): # Input: list of tokens | Output: string ( + capitalizations + proper punct. represent.)
    I = ['i', 'i\'ll', 'i\'m', 'i\'d', 'i\'ve']
    end_punct = ['.', '!', '?', ':']
    punct = ['.', ',', '!', '?', ':', ';']
    detok = []

    #print(f'{proper_names=}')

    # Re-capitalization of senetence beginnings, I instances, proper names
    for i, item in enumerate(tokens):
        if i == 0 or item in I or item in proper_names:
            detok.append(item.capitalize())
        elif detok[-1] in end_punct:
            detok.append(item.capitalize())
        else:
            detok.append(item)
           
    # Removing whitespaces in front of punctuation marks
    for item in detok:
        position = detok.index(item)
        if item in punct:
            detok[position-1] = detok[position-1] + item
            del detok[position]
    detok = ' '.join(detok)
    
    return(detok)

#_____________TEST CASE: DETOKENIZE______________________________
#test, names = tokenize('names_test.txt')
#print(detokenize(test[0], names))

# Segmenting lines into tokens
def tokenize(text): # Input: .txt doc | Output: list of lists(lines) containing tokens
    punct = {'.':' .', ',':' ,', '!':' !', '?':' ?', ';':' ;', ':':' :'}
    doc = open(text, 'r', encoding = 'utf8').readlines()
    token_sequences = []
    
    #>>>>>>>>>>>>>>>>>>>>>>>>
    '''proper_names = set() # set containing found proper_names'''
    #>>>>>>>>>>>>>>>>>>>>>>>>
    
    for line in doc:
        if line != '\n':
            line = line.strip('\n')

            #>>>>>>>>>>>>>>>>>>>>>>>>
            # Identifying proper names --> FAILED due to inconsistent data
            '''line = line.split()
            for item in line[1:]:
                if item[0].isupper():
                    proper_names.add(item)'''
            #>>>>>>>>>>>>>>>>>>>>>>>>
            
            line = line.lower()
            # Punctuation as intividual token
            for item in line:
                if item in punct.keys():
                    line = line.replace(item, punct[item])            
        line = line.split()
        token_sequences.append(line)

        #>>>>>>>>>>>>>>>>>>>>>>>>
        '''print(proper_names)'''
        #>>>>>>>>>>>>>>>>>>>>>>>>
        
    return(token_sequences)

# Recreating lines from tokens
def detokenize(tokens): # Input: list of tokens | Output: string ( + capitalizations + proper punct. represent.)
    I = ['i', 'i\'ll', 'i\'m', 'i\'d', 'i\'ve']
    end_punct = ['.', '!', '?', ':']
    punct = ['.', ',', '!', '?', ':', ';']
    detok = []
    # Capitalization (I(list) + sentence beginnings) lowercase/uppercase binary switch
    uppercase_switch = True
    for item in tokens:
        if item in I:
            item = item.capitalize()
            detok.append(item)
            uppercase_switch = False
        elif uppercase_switch == False:
            detok.append(item)
        elif uppercase_switch == True:
            item = item.capitalize()
            detok.append(item)
            uppercase_switch = False
        if item[-1] in end_punct:
            uppercase_switch = True           
    # Eemoving whitespaces in front of punctuation marks
    for item in detok:
        position = detok.index(item)
        if item in punct:
            detok[position-1] = detok[position-1] + item
            del detok[position]
    
    detok = ' '.join(detok)
    
    return(detok)

#_____________TEST CASE: DETOKENIZE______________________________

#print(detokenize(['well', 'i\'ll','be','finished','in','time', '!', 'But', 'how', '?']))

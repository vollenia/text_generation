import random
def sample(distribution): # Input: dict(words + P) | Output: word (randomly selected according to P distrib)
        selected_word = random.choices(list(distribution.keys()), list(distribution.values()))
        
        return(selected_word[0])

def normalize(word_counts): # Input: dict(words + counts) | Output: dict(words + P)
        normalized_counts = {}
        total = sum(word_counts.values())
        for item in word_counts.keys():
                normalized_counts[item] = word_counts[item]/total
                
        return(normalized_counts)

def get_ngrams(tokens, n): # Input: list of lists(lines) containing tokens | Output: tuples of length n
        ngrams = []
        for line in tokens:
                for i in range(n-1):
                        line.insert(0, None)
                        line.append(None)
                first = 0
                last = n
                for element in range(len(line)):
                        ngram = line[first : last]
                        if len(ngram) != n:
                                break
                        else:
                                ngrams.append(tuple(ngram))
                                first += 1
                                last += 1
                                
        return(ngrams)

########## LANGUAGE MODEL OBJECT ##########

class LanguageModel(object):
        def __init__(self, n):
                self.n = n
                self.counts = {}
                self.vocabulary = set()
                
        def train(self, token_sequences): # Input: token_sequences | Output: LM as dict
                for line in token_sequences:
                        self.vocabulary.update(line)
                ngrams = get_ngrams(token_sequences, self.n)
                for item in ngrams:
                        word = item[-1]
                        counter = 1
                        dct_value = {}
                        dct_value[item[-1]] = counter
                        key = item[0:-1]
                        # If key(history) already in dict
                        if key in self.counts.keys():
                                # ... and word is the SAME
                                if word in self.counts[key].keys():
                                        self.counts[key][word] += 1        
                                # ... and word is NOT the SAME
                                else:
                                        self.counts[item[0:-1]][item[-1]] = counter                
                        # If this is the FIRST appearance of the key(history)              
                        else:
                                self.counts[(item[0:-1])] = dct_value
                
        def p_next(self, tokens): # Input: history as tokens | Output: dict of (next word + P)
                # If p_next input is zero --> beginning of a sentence
                if tokens == []:
                        for i in range(self.n-1):
                                tokens.append(None)
                history = tokens[-(self.n-1):]
                history = tuple(history)
                word_counts = {}
                
                # Look up history in counts / get word_counts
                if history in self.counts.keys():
                        word_counts = self.counts[history]
                        
                # If history does not exist in the LM
                else:
                        counter = 2
                        entry_found = False
                        while entry_found == False:
                                # ------ 1ST STEP ------ new history
                                # extract final n-2(history)
                                new_history = tokens[-(self.n-counter):]
                                new_history = tuple(new_history)
                                # ------ 2ND STEP ------ smaller counts
                                for item in self.counts.keys():
                                        new_count = item[-(self.n-counter):]
                                        if new_count == new_history:
                                                word_counts = self.counts[item]
                                                entry_found = True
                                                break       
                                # reduce window considered as 'history' further
                                else:
                                        counter += 1                       
                normalized_word_counts = normalize(word_counts)
                
                return(normalized_word_counts)
               
        def generate(self): # Input: (LM/Object) | Output: text (as list of tokens)
                stop = ['.', '!', '?', ',', ':', ';']
                new_text = []
                final_word = ()
                while final_word != None:
                        possible_words = self.p_next(new_text)
                        selected_word = sample(possible_words)
                        if selected_word == None:
                                break
                        # Artificial barriercin case of infinite loop (very unlikely but possible)
                        elif len(new_text) > 500 and selected_word in stop:
                                new_text.append(selected_word)
                                new_text.append('-- this is not the real end!!!')
                                break
                        else:
                                new_text.append(selected_word)
                del new_text[0 : self.n-1]
                
                return(new_text)

########## LM OBJECT - END ##########

#_____________TEST CASE: TRAIN___________________________________
        
#lm = LanguageModel(3)
#lm.train([['the', 'cat', 'runs', '!'],['the', 'dog', 'runs', '!']])

#_____________TEST CASE: P_NEXT___________________________________
        
#print(lm.p_next([]))
#print(lm.p_next([None, 'the']))
# ----> SPECIAL CASE (sort-of backoff (REPORT))
#print(lm.p_next(['UNKNOWN_WORD', 'the'])) # pritnts still an adequate result

#_____________TEST CASE: GENERATE_________________________________

#print(lm.generate())

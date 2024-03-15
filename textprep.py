"""
ML
Text preprocessing

"""

# import the necessary libraries 
# We will be using the NLTK (Natural Language Toolkit) library here.  

import nltk
import string
import re
import numpy as np
import heapq 


#  lowercase the text to reduce the size of the vocabulary of our text data.
def text_lowercase(text):
    return text.lower()
 

# Remove numbers
def remove_numbers(text):
    result = re.sub(r'\d+', '', text)
    return result

# convert the numbers into words. This can be done by using the inflect library.
# import the inflect library
import inflect
p = inflect.engine()

# convert number into words
def convert_number(text):
    # split string into list of words
    temp_str = text.split()
    # initialise empty list
    new_string = []
 
    for word in temp_str:
        # if word is a digit, convert the digit
        # to numbers and append into the new_string list
        if word.isdigit():
            temp = p.number_to_words(word)
            new_string.append(temp)
 
        # append the word as it is
        else:
            new_string.append(word)
 
    # join the words of new_string to form a string
    temp_str = ' '.join(new_string)
    return temp_str


# We remove punctuations so that we don’t have different forms of the same word. 
# If we don’t remove the punctuation, then been. been, been! will be treated separately.
# remove punctuation
def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

# remove whitespace from text
def remove_whitespace(text):
    return  " ".join(text.split())


# Remove default stopwords
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
 
# remove stopwords function
def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return filtered_text


# Stemming 
# Stemming is the process of getting the root form of a word. 
# Stem or root is the part to which inflectional affixes (-ed, -ize, -de, -s, etc.) are added. 
# The stem of a word is created by removing the prefix or suffix of a word. So, stemming a word may not result in actual words.
# books      --->    book
# looked     --->    look
# denied     --->    deni
# flies      --->    fli

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
stemmer = PorterStemmer()
 
# stem words in the list of tokenized words
def stem_words(text):
    word_tokens = word_tokenize(text)
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems


# Lemmatization
# Like stemming, lemmatization also converts a word to its root form. 
# The only difference is that lemmatization ensures that the root word belongs to the language. 
# We will get valid words if we use lemmatization. 
# In NLTK, we use the WordNetLemmatizer to get the lemmas of words. We also need to provide a context for the lemmatization.
# So, we add the part-of-speech as a parameter. 

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
stemmer = PorterStemmer()
 
# stem words in the list of tokenized words
def stem_words(text):
    word_tokens = word_tokenize(text)
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems


sentence = """At eight o'clock on Thursday morning
... Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
print(tokens)

# pos tag 
tagged = nltk.pos_tag(tokens)
print(tagged)

# Identify named entities:
entities = nltk.chunk.ne_chunk(tagged)
print(entities)

# Display a parse tree:
from nltk.corpus import treebank
t = treebank.parsed_sents('wsj_0001.mrg')[0]
# t = treebank.parsed_sents(tokens)[0]
t.draw()

# Creating BOW (Bag of words)
def bow_text(text):
    dataset = nltk.sent_tokenize(text) 
    for i in range(len(dataset)): 
        dataset[i] = dataset[i].lower() 
        dataset[i] = re.sub(r'\W', ' ', dataset[i]) 
        dataset[i] = re.sub(r'\s+', ' ', dataset[i]) 

    # Creating the Bag of Words model 
    word2count = {} 
    for data in dataset: 
        words = nltk.word_tokenize(data) 
        for word in words: 
            if word not in word2count.keys(): 
                word2count[word] = 1
            else: 
                word2count[word] += 1
    

    freq_words = heapq.nlargest(100, word2count, key=word2count.get)

    # In this step we construct a vector, which would tell us whether a word in each sentence is a frequent word or not. 
    # If a word in a sentence is a frequent word, we set it as 1, else we set it as 0.
    X = [] 
    for data in dataset: 
        vector = [] 
        for word in freq_words: 
            if word in nltk.word_tokenize(data): 
                vector.append(1) 
            else: 
                vector.append(0) 
        X.append(vector) 
    X = np.asarray(X)
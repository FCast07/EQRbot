import re
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from collections import Counter


#generate a set of english stopwords
stop_words = set(stopwords.words("english"))
#instantiate a lemmatizer object
normalizer = WordNetLemmatizer()


#function for lemmatize each word according to its grammar tag
def get_part_of_speech(word):
    probable_part_of_speech = wordnet.synsets(word)
    pos_counts = Counter()
    pos_counts["n"] = len(  [ item for item in probable_part_of_speech if item.pos()=="n"]  )
    pos_counts["v"] = len(  [ item for item in probable_part_of_speech if item.pos()=="v"]  )
    pos_counts["a"] = len(  [ item for item in probable_part_of_speech if item.pos()=="a"]  )
    pos_counts["r"] = len(  [ item for item in probable_part_of_speech if item.pos()=="r"]  )
    most_likely_part_of_speech = pos_counts.most_common(1)[0][0]
    return most_likely_part_of_speech


#function for preprocessing web_text
def preprocess_text(text):
    #with the exception of unicode words, every other character is deleted from input_sentence (i.e., as commas, dots, etc)
    cleaned = re.sub(r'\W+', ' ', text).lower()
    tokenized = word_tokenize(cleaned)
    tokenized_polished = [i for i in tokenized if not i in stop_words]
    #lemmatize each token according to the specific part of speech it represents
    normalized = " ".join([normalizer.lemmatize(token, get_part_of_speech(token)) for token in tokenized_polished])
    return normalized


#function for preprocessing eqr_input
def preprocess_eqr_input(input_sentence):
    #input_sentece is changed into lowercase characters
    input_sentence = input_sentence.lower()
    #with the exception of unicode words followed by a blank space, every other character is deleted from input_sentence (i.e., as commas, dots, etc)
    input_sentence = re.sub(r'[^\w\s]','',input_sentence)
    #divide input_sentence into list of single words
    tokens = word_tokenize(input_sentence)
    #remove common words useless for meaning detection
    input_sentence = [i for i in tokens if not i in stop_words]
    #lemmatize each token in input_sentence
    lemmatized_input_sentence = [normalizer.lemmatize(token, get_part_of_speech(token)) for token in input_sentence]
    return(lemmatized_input_sentence)


#function for preprocessing eqr_responses
def preprocess_eqr_responses(input_sentence):
    #input_sentece is changed into lowercase characters
    input_sentence = input_sentence.lower()
    #with the exception of unicode words followed by a blank space or separated by an underscore, every other character is deleted from input_sentence (i.e., as commas, dots, etc)
    input_sentence = re.sub(r'[^\w\s]','',input_sentence)
    #replace every _ character with a blank space
    input_sentence = input_sentence.replace("_", " ")
    #divide input_sentence into list of single words
    tokens = word_tokenize(input_sentence)
    #remove common words useless for meaning detection
    input_sentence = [i for i in tokens if not i in stop_words]
    return(input_sentence)


#function for lemmatize preprocessed eqr_response
def lemmatize_eqr_responses(responses):
    #initialise empty output_list
    lemmatized_responses = []
    #lemmatize word in each response, then append to unique list. This generates a list of lemmatized responses
    for response in responses:
        response = [normalizer.lemmatize(token, get_part_of_speech(token)) for token in response]
        lemmatized_responses.append(response)
    return lemmatized_responses


#function for preprocessing sentiment
def preprocess_sentiment(input_sentence):
    #input_sentece is changed into lowercase characters
    input_sentence = input_sentence.lower()
    #with the exception of unicode words followed by a blank space, every other string is deleted from input_sentence (i.e., as commas, dots, etc)
    input_sentence = re.sub(r'[^\w\s]','',input_sentence)
    #divide input_sentence into list of single words
    tokens = word_tokenize(input_sentence)
    return(tokens)

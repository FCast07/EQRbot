import re
from evalaf_expaf import computeAFaccepted, getSchemeDefs, prepareArgs, evalaf, expaf
import schemes # explanation schemes (templates)
from helpers import parse_extension # helper function
from collections import Counter
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))
import spacy
word2vec = spacy.load('en_core_web_md')

#function for preprocessing text
def preprocess(input_sentence):
    #input_sentece is changed into lowercase characters
    input_sentence = input_sentence.lower()
    #with the exception of unicode words followed by a blank space, every other character is deleted from input_sentence (i.e., as commas, dots, etc)
    input_sentence = re.sub(r'[^\w\s]','',input_sentence)
    #divide input_sentence into list of single words
    tokens = word_tokenize(input_sentence)
    #remove common words useless for meaning detection
    input_sentence = [i for i in tokens if not i in stop_words]
    #instantiate lemmatizer object
    lemmatizer = WordNetLemmatizer()
    #lemmatize each noun in input_sentence
    lemmatized_input_sentence = [lemmatizer.lemmatize(word, 'v') for word in input_sentence]
    return(lemmatized_input_sentence)

#function for preprocessing responses
def preprocess_responses(input_sentence):
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

#function for preprocessing sentiment
def preprocess_sentiment(input_sentence):
    #input_sentece is changed into lowercase characters
    input_sentence = input_sentence.lower()
    #with the exception of unicode words followed by a blank space, every other string is deleted from input_sentence (i.e., as commas, dots, etc)
    input_sentence = re.sub(r'[^\w\s]','',input_sentence)
    #divide input_sentence into list of single words
    tokens = word_tokenize(input_sentence)
    return(tokens)

#function for lemmatize response
def lemmatize_responses(responses):
    #instantiate lemmatizer object
    lemmatizer = WordNetLemmatizer()
    #initialise empty output_list
    lemmatized_responses = []
    #lemmatize each noun in each response, then append to unique list. This generates a list of lemmatized responses
    for response in responses:
        response = [lemmatizer.lemmatize(token, 'v') for token in response]
        lemmatized_responses.append(response)
    return lemmatized_responses

#function for comparing similar words count
def compare_overlap(words_count1, words_count2):
    similar_words = 0
    for token in words_count1:
        if token in words_count2:
              #similar_words += 1
              similar_words += words_count1[token]
    return similar_words

#function for comparing lists that have been compared by the compare_overlap function
def compare_similarity_list(list1, list2):
  union_list = []
  for i in range(len(list1)):
      union_list.append(list1[i] + list2[i])
  return union_list


positive_words = "great, good, fine, yes, love, best, happy, sure, nice, yeah"
exit_words = "leave, quit, exit, bye, goodbye, farewell, stop"
negative_words = "nope, no, nah, don't, never, dislike, can't, not, decline"
sentiments = [positive_words, exit_words, negative_words]


#function for establishing user's sentence sentiment
def sentiment_detection(input_sentence):
    #input_sentence is preprocessed but not lemmatized
    user_message = preprocess_sentiment(input_sentence)
    #remove common words useless for meaning detection
    lemmatizer = WordNetLemmatizer()
    #lemmatize each verb ('v') in user_message
    lemmatized_user_message = [lemmatizer.lemmatize(word, 'v') for word in user_message]
    #counting each word of lemmatized user_message list
    bow_lemmatized_user_message = Counter(lemmatized_user_message)
    #sentiments are preprocessed but not lemmatized (there is no need to lemmatize them)
    processed_sentiments = [preprocess_sentiment(sentiment) for sentiment in sentiments]
    #counting each word of lemmatized processed sentiments list
    bow_processed_sentiments = [Counter(sentiment) for sentiment in processed_sentiments]
    #compare similar words from bow_lemmatized_user_message and bow_processed_sentiments
    similarity_list_message_sentiment = [compare_overlap(s, bow_lemmatized_user_message) for s in bow_processed_sentiments]
    #find index of best suited sentiment based on similarity of words
    sentiment_index = similarity_list_message_sentiment.index(max(similarity_list_message_sentiment))
    return sentiment_index

# initialise the argumentation framework with eqr arguments.
exts = evalaf(['eqr'],S='preferred')
explanations = set()
for i,ext in enumerate(exts):
    acc_arg = ext[0]
    acc_att = ext[1]
    exp_arg,exp_att = expaf(acc_arg,acc_att)
    explanations = explanations.union(exp_arg)

responses = list(explanations)
#find the eqr scheme explanation (i.e., 'intro') that will be the initial provided recommendation
for r in responses:
    if "Given the patient's previous health record" in r:
        r_index = responses.index(r)
#clean the intro from useless characters
intro = responses[r_index].replace("_", " ")
#remove intro from possible responses
responses.pop(r_index)
class ChatBot:

    def find_intent_match(self, responses, context_message, user_message):
        #context_message is preprocessed and lemmatized (on 'v') before counting each of its word
        bow_context_message = Counter(preprocess(context_message))
        #user_message is preprocessed and lemmatized (on 'v') before counting each of its word
        bow_user_message = Counter(preprocess(user_message))
        #responses are preprocessed but not lemmatized
        processed_responses = [preprocess_responses(response) for response in responses]
        #processed responses are lemmatized (on 'v')
        lemmatized_processed_responses = lemmatize_responses(processed_responses)
        #counting each word of lemmatized processed responses list
        bow_lemmatized_processed_responses = [Counter(response) for response in lemmatized_processed_responses]
        #compare similar words from bow_context_message and bow_lemmatized_processed_responses
        similarity_list_context_responses = [compare_overlap(doc, bow_context_message) for doc in bow_lemmatized_processed_responses]
        #compare similar words from bow_user_message and bow_lemmatized_processed_responses
        similarity_list_user_responses = [compare_overlap(doc, bow_user_message) for doc in bow_lemmatized_processed_responses]
        #add results from each similarity lists into a unique list
        similarity_list_union = compare_similarity_list(similarity_list_context_responses, similarity_list_user_responses)
        #find index of best suited response based on similarity of words
        response_index = similarity_list_union.index(max(similarity_list_union))
        #provide the most likely response devoided of useless characters
        return responses[response_index].replace("\"", "").replace("\'", "").replace("_", " ")


    def respond(self, context_message, user_message):
        best_response = self.find_intent_match(responses, context_message, user_message)
        print(">>>>>>>>>>>>>")
        print(best_response)
        print(">>>>>>>>>>>>>")
        print("I hope I was able to help!")
        return self.chat()

    def chat(self):
        greetings = input(
"""

Hey! I'm an EQRbot! My advice to you is the following:

##################################################################

"""
+ intro +
"""

##################################################################

Would you like to know more? """)
        #if detected sentiment is non-positive
        if sentiment_detection(greetings) != 0:
                print("Have a good day, my friend!")
                print("Please, contact me if you need more assitance!")
                return True
        context_utterance = input("Would you please specify the context of your explanation request? ")
        user_request = input("What is the required explanation? ")
        return self.respond(context_utterance, user_request)


####################### MAIN PROGRAM #########################
EQRBot = ChatBot()
EQRBot.chat()

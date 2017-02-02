#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pablo Garay
# Description: Learns a Naive Bayes model parameters from a training set provided as command-line argument

from itertools import izip
import json
from math import log
import sys

import operator

from utils import *

# definitions
count_true = count_false = 0

# process command-line params
if len(sys.argv) != 3:
    print "Usage: python nblearn.py /path/to/text/file /path/to/label/file"
    exit(1)
file_text = sys.argv[1]
file_label = sys.argv[2]

data_text = []
data_labels = []

with open(file_text) as f_text, open(file_label) as f_labels:
    for line_ftext, line_flabels in izip(f_text, f_labels):
        # get rid of the id which for our purposes is useless. Make text lowercase
        text = line_ftext.strip().split(' ', 1)[1]
        data_text.append(text.lower())
        data_labels.append(line_flabels.strip().split(' ', 1)[1].lower())


size_data = len(data_text)
# print size_data

# for i in range(size_data):
#     print data_labels[i], data_text[i]
#     print

split_pct = int(0.75 * size_data)
# print split_pct

tr_text = data_text
tr_size = len(tr_text)
tr_labels = data_labels
# tr_text = data_text[:split_pct]
# tr_labels = data_labels[:split_pct]
# tr_size = len(tr_text)
# te_text = data_text[split_pct:]
# te_labels = data_labels[split_pct:]
# te_size = len(te_text)
# print tr_size, te_size

num_instances = {}
num_appearances = {}
class_instances = {"truthful": 0, "deceptive": 0, "positive": 0, "negative": 0}
# Create a table to replace all punctuation strings by white spaces (punctuation symbols usually act like separators)

for i in range(tr_size):
    veracity, sentiment = tr_labels[i].split() #get the 2 classes

    for word in tr_text[i].translate(translation_table, "'").split(): #delete ' character
        #for each word in the text description of a review
        word_length = len(word)

        if word_length > 2: # only consider words with more than 2 characters
            if word_length == 3: # ignore most common frequent 3-letter words in English that are not helpful - taken from Cryptography
                if word in li_freq_words:
                    continue

            if word not in num_instances:
                num_instances[word] = {"truthful":0,
                                       "deceptive":0,
                                       "positive":0,
                                       "negative":0}
                num_appearances[word] = 0
            num_instances[word][veracity] += 1
            num_instances[word][sentiment] += 1
            class_instances[veracity] += 1
            class_instances[sentiment] += 1
            num_appearances[word] += 1

# # print words in dictionary in alphabetical order
# for word in sorted(num_instances.keys()):
#     print word
num_words_found = len(num_instances.keys())
print "Number of different words found: ", num_words_found
print "Num lines: %d" %tr_size

# print num_instances
# print class_instances

# For testing purposes
# k_instances = {"truthful": 0, "deceptive": 0, "positive": 0, "negative": 0}
# for word, classes in num_instances.iteritems():
#     for k, num in classes.iteritems():
#         k_instances[k] += num
# print k_instances

# # Find average number of instances of a word across the different classes
# avg_instances = {}
# for word in num_instances:
#     avg_instances[word] = sum([num_instances[word][k] for k in rev_classes]) / float(len(rev_classes))
# # sorted_avg_instances = sorted(avg_instances.items(), key=operator.itemgetter(1), reverse=True)
# # print sorted_avg_instances
# sorted_num_appearances = sorted(num_appearances.items(), key=operator.itemgetter(1), reverse=True)
# print sorted_num_appearances

# Find conditional (posterior) probabilities of word occurrence given a class
posterior_prob = {}
# Apply Laplace (Add-One) Smoothing
for word in num_instances:
    if num_appearances[word] > 2: #feature selection
        posterior_prob[word] = {} # init
        for k in class_instances:
            posterior_prob[word][k] = float(num_instances[word][k] + 1) / float(class_instances[k] + num_words_found)
        # print probability[word]

print "Number of words after filtering selection: ", len(posterior_prob.keys())

# # Testing: check probabilities sum to 1
# suma = {"truthful": 0.0, "deceptive": 0.0, "positive": 0.0, "negative": 0.0}
# for word in num_instances:
#     for k in suma:
#         suma[k] += probability[word][k]
# print "suma", suma
# # print "class_instances", class_instances

prior_prob = {
    "truthful": float(class_instances["truthful"]) / float(class_instances["truthful"] + class_instances["deceptive"]),
    "deceptive": float(class_instances["deceptive"]) / float(class_instances["truthful"] + class_instances["deceptive"]),
    "positive": float(class_instances["positive"]) / float(class_instances["positive"] + class_instances["negative"]),
    "negative": float(class_instances["negative"]) / float(class_instances["positive"] + class_instances["negative"])
}
# print prior_prob

# save params of model in json file
prob = {
    "prior": prior_prob,
    "posterior": posterior_prob
}
json_prob = json.dumps(prob)
with open("nbmodel.txt", 'wb') as f_nb_params:
    json.dump(prob, f_nb_params)


# avg_prob = {}
# for word in posterior_prob:
#     avg_prob[word] = sum([posterior_prob[word][k] for k in rev_classes]) / len(rev_classes)
# sorted_avg_prob = sorted(avg_prob.items(), key=operator.itemgetter(1), reverse=True)
# print sorted_avg_prob



# veracity_correct_count = veracity_incorrect_count = sentiment_correct_count = sentiment_incorrect_count = 0
#
# f_out = open('nboutput.txt', 'wb')
#
# for review in range(te_size):
#     # In our calculations, it's imperative to use LOG so that we don't suffer from underflows
#     p_k_given_text = { #init val
#         "truthful" : log(prior_prob["truthful"]),
#         "deceptive": log(prior_prob["deceptive"]),
#         "positive": log(prior_prob["positive"]),
#         "negative": log(prior_prob["negative"])
#     }
#
#     for word in te_text[review].translate(translation_table, "'").split(): #delete ' character
#         #for each word in the text description of a review
#         word_length = len(word)
#
#         if word_length > 2: # only consider words with more than 2 characters
#             if word_length == 3: # ignore most common frequent 3-letter words in English that are not helpful - taken from Cryptography
#                 if word in li_freq_3_letter_words:
#                     continue
#
#             if word in posterior_prob: #only consider known tokens; ignore unknown tokens
#                 for k in rev_classes:
#                     p_k_given_text[k] += log(posterior_prob[word][k])
#
#     # print p_k_given_text
#     predict_veracity = "truthful" if p_k_given_text["truthful"] > p_k_given_text["deceptive"] else "deceptive"
#     predict_sentiment = "positive" if p_k_given_text["positive"] > p_k_given_text["negative"] else "negative"
#     (lbl_veracity, lbl_sentiment) = te_labels[review].split()
#     # print "Predicted:", predict_veracity, predict_sentiment
#     # print "Labels:", lbl_veracity, lbl_sentiment
#
#     if predict_veracity == lbl_veracity: veracity_correct_count += 1
#     else: veracity_incorrect_count += 1
#
#     if predict_sentiment == lbl_sentiment: sentiment_correct_count += 1
#     else: sentiment_incorrect_count += 1
#
#     f_out.write("%s %s\n" % (predict_veracity, predict_sentiment))
# f_out.close()
#
# print "veracity_correct_count: ", veracity_correct_count
# print "veracity_incorrect_count: ", veracity_incorrect_count
# print "veracity_acc: ", float(veracity_correct_count) / float(veracity_correct_count + veracity_incorrect_count) * 100
# print "sentiment_correct_count: ", sentiment_correct_count
# print "sentiment_incorrect_count: ", sentiment_incorrect_count
# print "sentiment_acc: ", float(sentiment_correct_count) / float(sentiment_correct_count + sentiment_incorrect_count) * 100



def report_summary(num_instances):
    # Summary for insight purposes
    count_freq_5_words = 0
    count_freq_10_words = 0
    count_freq_15_words = 0
    count_freq_25_words = 0
    count_freq_50_words = 0
    count_freq_100_words = 0
    count_freq_1000_words = 0

    for key, val in num_instances.iteritems():
        for k, v in val.iteritems():
            if v >= 5:
                count_freq_5_words += 1
            if v >= 10:
                count_freq_10_words += 1
            if v >= 15:
                count_freq_15_words += 1
            if v >= 25:
                count_freq_25_words += 1
            if v >= 50:
                count_freq_50_words += 1
            if v >= 100:
                count_freq_100_words += 1
            if v >= 1000:
                count_freq_1000_words += 1
                print "w: ", key, val, k, v

    print "#words with freq >= 5 : ", count_freq_5_words
    print "#words with freq >= 10: ", count_freq_10_words
    print "#words with freq >= 15: ", count_freq_15_words
    print "#words with freq >= 25: ", count_freq_25_words
    print "#words with freq >= 50: ", count_freq_50_words
    print "#words with freq >= 100: ", count_freq_100_words
    print "#words with freq >= 1000: ", count_freq_1000_words
# report_summary(num_instances)






# Testing: For testing purposes
# with open("te_labels.txt", "wb") as f:
#     for item in te_labels:
#         f.write("%s\n" % item)
#
# with open("data/test-data-labels.txt", "rb") as f1, open("other_te_labels.txt", "wb") as f2:
#     for line in f1:
#         # get rid of the id which for our purposes is useless. Make text lowercase
#         line = line.split(' ', 1)[1]
#         f2.write(line)













#         same_id, veracity, sentiment = line_flabels.strip().split(' ')
#         if id == same_id: count_true += 1
#         else: count_false += 1
#
#         print id, veracity, sentiment
#         print txt_review
#         print
#         print txt_review
#
#     print "count_true", count_true
#     print "count_false", count_false
#
# print "len(data)", len(data)
# for line in data:
#     print line


# with open("data/train-text.txt") as f_text:
#     text_data = f_text.read().splitlines()
#
# size_data = len(text_data)
#
# with open("data/train-labels.txt") as f_labels:
#     labels_data = f_labels.read().splitlines()
# rows_data = len(labels_data)
#
# split_pct = int(0.75 * size_data)
# # int(0.25 * size_data)
# print split_pct
#
# train_data_x = text_data[:split_pct]
# test_data_x = text_data[split_pct:]
#
# train_data_y = labels_data[:split_pct]
# test_data_y = labels_data[split_pct:]
#
# train_data_size = len(train_data_x)
# test_data_size = len(test_data_x)
# print len(train_data_x), len(test_data_x)
# print len(train_data_y), len(test_data_y)
#
#
# for row in izip(train_data_x, train_data_y):
#     print row


# for i in range(size_data):
#     text_data[]

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pablo Garay
# Description: Loads the HMM POS tagger parameters and classifies/predicts tags for input data

import json
import sys

import unicodedata

reload(sys)
sys.setdefaultencoding('utf8')

# parse command-line params
if len(sys.argv) != 2:
    print "Usage: python hmmdecode.py /path/to/input"
    exit(1)

# load HMM POS tagger parameters
with open('hmmmodel.txt', 'rb') as f_hmm_params:
    json_prob = json.load(f_hmm_params)

# load list of known words
known_words = set()
with open("wordlist.txt", "rb") as f_wordlist:
    for line in f_wordlist:
        word = line.strip()
        known_words.add(word)
print "num of words known:", len(known_words)

# print json_prob
transition_prob = json_prob["transition_prob"]
emission_prob = json_prob["emission_prob"]
states = json_prob["states"]
# print transition_prob
# print emission_prob
# print states

f_te_text = sys.argv[1]
# most_likely_paths = [["q0"] for state in range(len(states))]
# print most_likely_paths
# print len(most_likely_paths)


def emission_val(word, tag):
    # if unknown word, ignore emission probabilities
    # print known_words
    if word not in known_words:
        return 1
    else: # known word: return probability 0 if not seen in training set for specific tag/state
        return emission_prob[tag][word] if word in emission_prob[state] else 0



with open(f_te_text) as te_text:
    for line in te_text:
        line = unicodedata.normalize('NFD', unicode(line)).encode('ascii', 'ignore')
        words = line.strip().split(' ')

        probability = {}
        backpointer = {}

        for state in states:
            probability[state] = [None for t in range(len(words))]
            backpointer[state] = [None for t in range(len(words))]

        # for unknown tokens in the test data, ignore the emission probabilities
        word = words[0]

        for state in states:
            probability[state][0] = transition_prob["q0"][state] * emission_val(word, state)
            backpointer[state][0] = "q0"

        for (pos, word) in enumerate(words[1:], 1):
            emission_val(word, state)


# print len(probability["NC"])



        # prev_state = "q0"
        # for unit in line.strip().split(' '):


for (i, j) in enumerate(range(2,10), 3):
    print (i, j)




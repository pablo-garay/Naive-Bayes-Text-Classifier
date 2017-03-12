#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pablo Garay
# Description: Loads the HMM POS tagger parameters and classifies/predicts tags for input data

import json
from operator import itemgetter
from math import log
from time import time
from utils import *

import sys

reload(sys)
sys.setdefaultencoding('utf8')

# PARSE command-line params
if len(sys.argv) != 2:
    print "Usage: python hmmdecode.py /path/to/input"
    exit(1)
f_te_text = sys.argv[1]

# load HMM POS tagger parameters
with open('hmmmodel.txt', 'rb') as f_hmm_params:
    json_prob = json.load(f_hmm_params)
transition_prob = json_prob["transition_prob"]
emission_prob = json_prob["emission_prob"]
states = json_prob["states"]
# print transition_prob
# print emission_prob
# print states

# load list of known words
known_words = set()
with open("wordlist.txt", "rb") as f_wordlist:
    for line in f_wordlist:
        word = line.strip()
        known_words.add(word)
print "num of words known:", len(known_words)

def detect_proper_noun(raw_word, word_at_beginning_of_sentence = False):
    if word_at_beginning_of_sentence:
        if raw_word[0].isupper() and len(raw_word.split("_")) >= 2 and \
                        sum(1 for c in raw_word if c.isupper()) >= 2 and not any(char.isdigit() for char in raw_word):
            return True
    else: #word not at beginning of sentence
        if raw_word[0].isupper() and not any(char.isdigit() for char in raw_word):
            return True
    return False

# weighted log
def wt_log(num):
    """ Avoids computing log(0) by summing 1 to the input. Hence, when input = 0, log(input) = 0 """
    return log(num)

def emission_val(word, tag):
    # if unknown word, ignore emission probabilities
    if word not in known_words:
        return wt_log(1)
    else: # known word: return probability 0 if not seen in training set for specific tag/state
        if word in emission_prob[tag]:
            return emission_prob[tag][word]
        else:
            return wt_log(1e-100) # THIS IS KEY: value taken as best hyperparameter value found

start = time()
recursion_step_time = 0

# precompute weighted log of transition probabilities
for x in transition_prob.keys():
    for y in transition_prob[x].keys():
        transition_prob[x][y] = wt_log(transition_prob[x][y])

# precompute weighted log of emission probabilities
for x in emission_prob.keys():
    for y in emission_prob[x].keys():
        emission_prob[x][y] = wt_log(emission_prob[x][y])


with open(f_te_text) as te_text, open("hmmoutput.txt", "wb") as f_out:
    for line in te_text:
        # normalized_line = unicodedata.normalize('NFD', unicode(line)).encode('ascii', 'ignore')
        # normalized_line = line
        raw_words = line.strip().split(' ')
        words = [normalize_word(raw_word) for raw_word in raw_words]

        probability = {}
        backpointer = {}

        for state in states:
            probability[state] = [None for t in range(len(words))]
            backpointer[state] = [None for t in range(len(words))]

        # Viterbi Algorithm - INITIALIZATION STEP
        # for unknown tokens in the test data, ignore the emission probabilities
        word = words[0]

        for state in states:
            probability[state][0] = transition_prob["q0"][state] + emission_val(word, state)
            backpointer[state][0] = "q0"

        start_recursion = time()
        # RECURSION STEP FOR THE REMAINING POINTS
        for (pos, word) in enumerate(words[1:], 1):
            for state in states:
                computed_emission_val = emission_val(word, state)
                max_p = float("-inf")

                for prev_state in states:
                    # previous probability should not be log - ed (it was already calculated using log; negative number)
                    p = \
                        probability[prev_state][pos - 1] + \
                        transition_prob[prev_state][state] + \
                        computed_emission_val

                    if p > max_p:
                        max_p = p
                        probability[state][pos] = max_p
                        backpointer[state][pos] = prev_state

        recursion_step_time += (time() - start_recursion)







        # TERMINATION STEP
        max_prob = float("-inf")
        for state in states:
            if probability[state][pos] > max_prob:
                max_prob = probability[state][pos]
                most_likely_state = state

        # print most_likely_state
        path = [most_likely_state]
        for pos in range(pos, 0, -1):
            state = backpointer[state][pos]
            path.insert(0, state)
        # print words
        # print path

        # write output to text file in correct format
        if detect_proper_noun(raw_words[0], word_at_beginning_of_sentence=True):
            path[0] = "NP"
        f_out.write(raw_words[0] + "/" + path[0])
        try:
            for pos in range(1, len(raw_words)):
                # if position of word is not beginning of sentence (pos > 0) and word capitalized, tag as proper name: NP tag
                if detect_proper_noun(raw_words[pos], word_at_beginning_of_sentence=False):
                    path[pos] = "NP"
                f_out.write(" " + raw_words[pos] + "/" + path[pos])
            f_out.write("\n")
        except:
            print "Problem line:"
            print raw_words
            print path


print "Time to execute decoder: ", time() - start
print "Time spent in recursion step: ", recursion_step_time

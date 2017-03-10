#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pablo Garay
# Description: Loads the HMM POS tagger parameters and classifies/predicts tags for input data

import json
import unicodedata
from operator import itemgetter
from math import log

import sys

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
        if word in emission_prob[state]:
            return emission_prob[tag][word]
        else:
            return 0

# weighted log
def wt_log(num):
    """ Avoids computing log(0) by summing 1 to the input. Hence, when input = 0, log(input) = 0 """
    return log(1 + num)


with open(f_te_text) as te_text, open("hmmoutput.txt", "wb") as f_out:
    for line in te_text:
        # normalized_line = unicodedata.normalize('NFD', unicode(line)).encode('ascii', 'ignore')
        # normalized_line = line
        words = line.strip().split(' ')

        probability = {}
        backpointer = {}

        for state in states:
            probability[state] = [None for t in range(len(words))]
            backpointer[state] = [None for t in range(len(words))]

        # for unknown tokens in the test data, ignore the emission probabilities
        word = words[0]

        for state in states:
            probability[state][0] = wt_log(transition_prob["q0"][state]) + wt_log(emission_val(word, state))
            backpointer[state][0] = "q0"
            # # For debugging purposes
            # print "State:", state, ", ", "word:", word
            # print transition_prob["q0"][state], wt_log(transition_prob["q0"][state])
            # print emission_val(word, state), wt_log(emission_val(word, state))

        for (pos, word) in enumerate(words[1:], 1):
            for state in states:
                # init max and argmax values
                prev_state = states[0]
                max_p = probability[prev_state][pos - 1] + \
                        wt_log(transition_prob[prev_state][state]) + \
                        wt_log(emission_val(word, state))
                probability[state][pos] = max_p
                backpointer[state][pos] = prev_state

                for prev_state in states:
                    # print wt_log(emission_val(word, state))
                    # previous probability should not be log - ed (it was already calculated using log; negative number)
                    p = \
                        probability[prev_state][pos - 1] + \
                        wt_log(transition_prob[prev_state][state]) + \
                        wt_log(emission_val(word, state))

                    if p > max_p:
                        max_p = p
                        probability[state][pos] = max_p
                        backpointer[state][pos] = prev_state

        # print probability
        # print backpointer

        most_likely_state = states[0]
        max_prob = probability[most_likely_state][pos]
        for state in states:
            if probability[state][pos] > max_prob:
                max_prob = probability[state][pos]
                most_likely_state = state

        path = [state]
        for i in range(pos, 0, -1):
            state = backpointer[state][i]
            path.append(state)
        path.reverse()
        # print words
        # print path

        # write output to text file in correct format
        words = line.strip().split(' ')
        f_out.write(words[0] + "/" + path[0])

        try:
            for i in range(1, len(words)):
                f_out.write(" " + words[i] + "/" + path[i])
            f_out.write("\n")
        except:
            print "Problem line:"
            print words
            print path




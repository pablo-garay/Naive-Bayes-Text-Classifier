# -- coding: utf-8 --
# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pablo Garay
# Description: Learns a HMM POS tagger from a training set provided as command-line argument

import json
import unicodedata
import operator
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# process command-line params
if len(sys.argv) != 2:
    print "Usage: python hmmlearn.py /path/to/input"
    exit(1)
f_tr_text = sys.argv[1]

# possible_tags = set()
transition_prob = {}
emission_prob = {}
num_tag_ocurrences = {}
word_dict = {}

# Compute transition and emission probabilities from training file
with open(f_tr_text) as tr_text:
    for line in tr_text:
        prev_state = "q0" #initial state is "q0"
        for token in line.strip().split(' '):
            word = token[:-3].lower()
            # word = unicodedata.normalize('NFD', unicode(word)).encode('ascii','ignore')
            state = token[-2:]
            # print "word: " + word + " " + "tag: " + tag
            # possible_tags.add(tag)
            #add word to dictionary of known words
            if word not in word_dict: word_dict[word] = 1
            else: word_dict[word] += 1

            # for each tag, count its number of occurrences
            if state not in num_tag_ocurrences: num_tag_ocurrences[state] = 1
            else: num_tag_ocurrences[state] += 1

            # for emission probabilities
            if state not in emission_prob: emission_prob[state] = {}
            if word not in emission_prob[state]: emission_prob[state][word] = 1.0
            else: emission_prob[state][word] += 1.0

            # for transition probabilities
            if prev_state not in transition_prob: transition_prob[prev_state] = {}
            if state not in transition_prob[prev_state]: transition_prob[prev_state][state] = 1.0
            else: transition_prob[prev_state][state] += 1.0
            prev_state = state

possible_tags = num_tag_ocurrences.keys()
# print possible_tags

# Calculate transition probabilities: Divide by proper denominator (including use of Laplace (Add-One) Smoothing)
for prev_state in transition_prob:
    # Apply Laplace (Add-One) Smoothing
    total = sum([transition_prob[prev_state][next_state] for next_state in transition_prob[prev_state]])

    for state in possible_tags:
        if state not in transition_prob[prev_state]:
            transition_prob[prev_state][state] = 1.0 / float(total + len(possible_tags))
        else:
            transition_prob[prev_state][state] = (float(transition_prob[prev_state][state]) + 1) / float(total + len(possible_tags))
# print transition_prob

# Calculate emission probabilities: Divide by proper denominator
for state in emission_prob:
    num_ocurrences_tag = num_tag_ocurrences[state]
    for word in emission_prob[state]:
        emission_prob[state][word] = float(emission_prob[state][word]) / float(num_ocurrences_tag)

# save list of known words
included_words = 0
with open("wordlist.txt", "wb") as f_out, open("wordcount.txt", "wb") as fc_out:
    for w, c in sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True):
        fc_out.write("%s : %d\n" % (w, c))

    for w, c in sorted(word_dict.items(), key=operator.itemgetter(0)):
        if (c >= 5): #only include words appearing 10 times or more
            f_out.write("%s\n" % w)
            included_words += 1
print "total num of words: ", len(word_dict)
print "total num of words included (not discarded): ", included_words

# save params of model in json file
prob = {
    "transition_prob": transition_prob,
    "emission_prob": emission_prob,
    "states": possible_tags
}
with open("hmmmodel.txt", 'wb') as f_hmm_params:
    json.dump(prob, f_hmm_params)




# # For debug purposes: test if probabilities sum up to 1
# for prev_state in transition_prob:
#     tot_sum = sum([transition_prob[prev_state][tag] for tag in transition_prob[prev_state]])
#     print tot_sum
# print
# # For debug purposes: test if probabilities sum up to 1
# for tag in emission_prob:
#     tot_sum = sum([transition_prob[tag][word] for word in transition_prob[tag]])
#     print tot_sum

# print transition_prob
# print emission_prob

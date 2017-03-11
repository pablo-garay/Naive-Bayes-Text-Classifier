# -- coding: utf-8 --
# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pablo Garay
# Description: Learns a HMM POS tagger from a training set provided as command-line argument

import json
import unicodedata
import sys

import operator

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
        prev_state = "q0"
        for unit in line.strip().split(' '):
            word = unit[:-3].lower()
            # word = unicodedata.normalize('NFD', unicode(word)).encode('ascii','ignore')
            tag = unit[-2:]
            # print "word: " + word + " " + "tag: " + tag
            # possible_tags.add(tag)
            if word not in word_dict: word_dict[word] = 1
            else: word_dict[word] += 1

            # for each tag, count its number of occurrences
            if tag not in num_tag_ocurrences:
                num_tag_ocurrences[tag] = 1
            else:
                num_tag_ocurrences[tag] += 1

            # for transition probabilities
            if prev_state not in transition_prob:
                transition_prob[prev_state] = {}

            if tag not in transition_prob[prev_state]:
                transition_prob[prev_state][tag] = 1.0
            else:
                transition_prob[prev_state][tag] += 1.0

            prev_state = tag

            # for emission probabilities
            if tag not in emission_prob:
                emission_prob[tag] = {}

            if word not in emission_prob[tag]:
                emission_prob[tag][word] = 1.0
            else:
                emission_prob[tag][word] += 1.0
# print transition_prob

possible_tags = num_tag_ocurrences.keys()
# print possible_tags

# Calculate transition probabilities: Divide by proper denominator (including use of Laplace (Add-One) Smoothing)
for prev_state in transition_prob:
    # Apply Laplace (Add-One) Smoothing
    total = sum([transition_prob[prev_state][next_state] for next_state in transition_prob[prev_state]])
    # print total

    for tag in possible_tags:
        if tag not in transition_prob[prev_state]:
            transition_prob[prev_state][tag] = 1.0 / float(total + len(possible_tags))
        else:
            transition_prob[prev_state][tag] = (float(transition_prob[prev_state][tag]) + 1) / float(total + len(possible_tags))

print transition_prob

# # For debug purposes: test if probabilities sum up to 1
# for prev_state in transition_prob:
#     tot_sum = sum([transition_prob[prev_state][tag] for tag in transition_prob[prev_state]])
#     print tot_sum

# Calculate emission probabilities: Divide by proper denominator
for tag in emission_prob:
    num_ocurrences_tag = num_tag_ocurrences[tag]
    for word in emission_prob[tag]:
        emission_prob[tag][word] = float(emission_prob[tag][word]) / float(num_ocurrences_tag)

# print emission_prob

# # For debug purposes: test if probabilities sum up to 1
# for tag in emission_prob:
#     tot_sum = sum([transition_prob[tag][word] for word in transition_prob[tag]])
#     print tot_sum

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

# # For information purposes: print list of words with their count
# with open("wordcount.txt", "wb") as f_out:
#     for w, c in sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True):
#         f_out.write("%s : %d\n" %(w, c))
# print "total num of words: ", len(word_dict)



# save params of model in json file
prob = {
    "transition_prob": transition_prob,
    "emission_prob": emission_prob,
    "states": possible_tags
}
json_prob = json.dumps(prob)
with open("hmmmodel.txt", 'wb') as f_hmm_params:
    json.dump(prob, f_hmm_params)

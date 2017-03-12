#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pablo Garay
# Description: Measure accuracy of HMM POS tagger

from itertools import izip

correct = 0
incorrect = 0
num_lines = 0

with open("hmmoutput.txt", "rb") as f_predicted_tags, open("data/catalan_corpus_dev_tagged.txt", "rb") as f_dev_tagged:
    for line_predicted_tags, line_dev_tagged in izip(f_predicted_tags, f_dev_tagged):
        num_lines += 1
        tokens_predicted = line_predicted_tags.strip().split(' ')
        tags_predicted = [token[-2:] for token in tokens_predicted]

        tokens_tagged = line_dev_tagged.strip().split(' ')
        tags_tagged = [token[-2:] for token in tokens_tagged]

        if len(tags_predicted) != len(tags_tagged):
            print "Error: NOT SAME AMOUNT OF TAGS FOR THE SAME LINE"
            print "num_line: ", num_lines
            print tags_predicted
            print tags_tagged
            exit(1)
        else:
            for i in range(len(tags_predicted)):
                if tags_predicted[i] == tags_tagged[i]:
                    correct += 1
                else:
                    incorrect += 1
                    print "Predicted: ", tokens_predicted[i], "\t(Correct) Should be: ", tokens_tagged[i]

print "Total correct predictions: ", correct
print "Total incorrect predictions: ", incorrect
print "Total: ", correct + incorrect

print "Accuracy", float(correct) / float(correct + incorrect)

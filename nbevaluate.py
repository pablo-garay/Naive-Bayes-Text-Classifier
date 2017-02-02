#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pablo Garay
# Description: Evaluates the predictive results of classification with the test file

from itertools import izip

test_file_labels = "data/test-data-labels.txt"
veracity_correct_count = veracity_incorrect_count = sentiment_correct_count = sentiment_incorrect_count = 0

# count = 0
with open("nboutput.txt") as f_out_labels, open(test_file_labels) as f_te_labels:
    for line_out_labels, line_te_labels in izip(f_out_labels, f_te_labels):
        # get rid of the id which for our purposes is useless. Make text lowercase
        line_te_labels = line_te_labels.strip().split(' ', 1)[1].lower()
        lbl_veracity, lbl_sentiment = line_te_labels.split()

        # get rid of the id which for our purposes is useless. Make text lowercase
        line_out_labels = line_out_labels.strip().split(' ', 1)[1].lower()
        predicted_veracity, predicted_sentiment = line_out_labels.split()

        # count += 1
        # print count, "Predicted:", predicted_veracity, predicted_sentiment, "Labels:", lbl_veracity, lbl_sentiment

        if predicted_veracity == lbl_veracity: veracity_correct_count += 1
        else: veracity_incorrect_count += 1

        if predicted_sentiment == lbl_sentiment: sentiment_correct_count += 1
        else: sentiment_incorrect_count += 1

# Print some metrics as evaluation report
print "veracity_correct_count: ", veracity_correct_count
print "veracity_incorrect_count: ", veracity_incorrect_count
print "veracity_acc: ", float(veracity_correct_count) / float(veracity_correct_count + veracity_incorrect_count) * 100
print "sentiment_correct_count: ", sentiment_correct_count
print "sentiment_incorrect_count: ", sentiment_incorrect_count
print "sentiment_acc: ", float(sentiment_correct_count) / float(sentiment_correct_count + sentiment_incorrect_count) * 100
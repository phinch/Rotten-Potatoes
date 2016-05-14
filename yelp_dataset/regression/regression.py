#!/usr/bin/env python

from __future__ import division
import sys
import csv
import argparse
from collections import defaultdict

import util

import random
import math

import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import cross_validation
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

def load_file(file_path_ex, file_path_ch):

	labels = []
	features = []

	with open(file_path_ex, 'rb') as file_reader:
		reader = csv.reader(file_reader)
		reader.next()
		for row in reader:
			labels.append(1)

			toAppend = row[1:]
			toAppend = [float(x) for x in toAppend]

			features.append(toAppend)

	all_cheap_rest = []

	with open(file_path_ch, 'rb') as file_reader:
		reader = csv.reader(file_reader)
		reader.next()
		for row in reader:

			toAppend = row[1:]
			toAppend = [float(x) for x in toAppend]

			all_cheap_rest.append(toAppend)

	random.shuffle(all_cheap_rest)

	for i in range(1666):
		labels.append(0)
		features.append(all_cheap_rest[i])

	print len(labels)
	print len(features)

	return (labels, features)

def main():
	##### DO NOT MODIFY THESE OPTIONS ##########################
	parser = argparse.ArgumentParser()
	parser.add_argument('-training_expensive', required=True, help='Path to expensive training data')
	parser.add_argument('-training_cheap', required=True, help='Path to cheap training data')
	# parser.add_argument('-test', help='Path to test data')
	parser.add_argument('-c', '--classifier', default='nb', help='nb | log | svm')
	parser.add_argument('-top', type=int, help='Number of top features to show')
	parser.add_argument('-p', type=bool, default='', help='If true, prints out information')
	opts = parser.parse_args()
	############################################################
	# Note: anytime the print flag is set to '', you should not print anything out!

	##### BUILD TRAINING SET ###################################
	
	# Load training text and training labels
	(training_labels, training_features) = load_file(opts.training_expensive, opts.training_cheap)

	# print training_labels
	# print training_features

	# Transform training labels to numpy array (numpy.array)
	training_labels = numpy.array(training_labels)
	training_features = numpy.array(training_features)
	############################################################
	# TODO: Start modifiying the lines below here

	##### TRAIN THE MODEL ######################################
	# Initialize the corresponding type of the classifier and train it (using 'fit')
	if opts.classifier == 'nb':
		# TODO: Initialize Naive Bayes and train
		classifier = BernoulliNB(binarize=None)
		classifier.fit(training_features, training_labels)
	elif opts.classifier == 'log':
		# TODO: Initialize Logistic Regression and train
		classifier = LogisticRegression(penalty='l2')
		classifier.fit(training_features, training_labels)
	elif opts.classifier == 'svm':
		# TODO: Initialize SVM and train
		classifier = LinearSVC()
		classifier.fit(training_features, training_labels)
	else:
		raise Exception('Unrecognized classifier!')
	############################################################


	###### VALIDATE THE MODEL ##################################
	# TODO: print training mean accuracy using 'score'

	# TODO: Perform 10 fold cross validation (cross_validation.cross_val_score) with scoring='accuracy'
	# TODO: print get the mean score and std deviation

	############################################################
	if opts.p == True:
		print "training mean accuracy using score " + str(classifier.score(training_features, training_labels))

	est_scores = cross_validation.cross_val_score(classifier, training_features, training_labels, scoring='accuracy', cv=10)

	mean_est_scores = numpy.mean(est_scores)
	std_est_scores = numpy.std(est_scores)

	if opts.p == True:
		print "10 fold cross training mean accuracy " + str(mean_est_scores)
		print "10 fold cross training standard deviation " + str(std_est_scores)

	# ##### TEST THE MODEL #######################################
	# if opts.test is None:
	# 	# TODO: Test the classifier on one sample test tweet
	# 	# Tim Kraska 10:43 AM - 5 Feb 13
	# 	test_tweet = 'Water dripping from 3rd to 1st floor while the firealarm makes it hard to hear anything. BTW this is the 2nd leakage.  Love our new house'

	# 	# TODO: Print the predicted label of the test tweet

	# 	pred_label = classifier.predict(vectorizer.transform(test_tweet.split()))
	# 	if opts.p == True:
	# 		print "predicted label " + str(pred_label)

	# 	# TODO: Print the predicted probability of each label.
	# 	if opts.classifier != 'svm':
	# 		# Use predict_proba
		
	# 		pred_prob = classifier.predict_proba(vectorizer.transform(test_tweet.split()))
		


	# 		if opts.p == True:
	# 			print "predicted probability of each label " + str(pred_prob)

	# 	else:
	# 		#Use decision_funcion
	# 		pred_prob = classifier.decision_function(vectorizer.transform(test_tweet.split()))

	# 		if opts.p == True:
	# 			print "predicted probability of each label " + str(pred_prob)

	# else:
	# 	# TODO: Test the classifier on the given test set
	# 	# TODO: Extract features from the test set and transform it using vectorizer

	# 	# Load test text and test labels
	# 	(test_labels, test_texts) = load_file(opts.test)

	# 	# Get test features using vectorizer
	# 	test_features = vectorizer.transform(test_texts)

	# 	# Transform training labels to numpy array (numpy.array)
	# 	test_labels = numpy.array(test_labels)

	# 	# TODO: Print test mean accuracy

	# 	test_mean_accuracy = classifier.score(test_features, test_labels)

	# 	if opts.p == True:
	# 		print "Test mean accuracy " + str(test_mean_accuracy)

	# 	# TODO: Print the confusion matrix
	# 	c_matrix = confusion_matrix(test_labels, classifier.predict(test_features))
	# 	if opts.p == True:
	# 		print "Confusion matrix " + str(c_matrix)

	# 	# TODO: Write out the quantities to classifier.csv with the fields specified in the handout.
	# 	file_name = opts.classifier + "_classifier.csv"
	# 	csv_writer = csv.writer(open(file_name, 'wb'))
	# 	csv_writer.writerow(["classifier-name", "cross-val-score", "cross-val-stdev","test-score"])
	# 	csv_writer.writerow([opts.classifier, mean_est_scores, std_est_scores, test_mean_accuracy])


	############################################################


if __name__ == '__main__':
	main()

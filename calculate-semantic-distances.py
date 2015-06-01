import json

import numpy as np 
import matplotlib.pyplot as plt 

from awesome_print import ap 

semantic_axes = open('latent-topics').read().splitlines()

"""
  Each semantic axis is a row formatted as (sign) weight*word

"""

def extract_weights_word(aStr):
	aStr = [token.split('*') for token in aStr.split(' + ')]
	return [(float(weight),component.replace('"',"")) for weight,component in aStr]

def project(axis,document):
	axis = extract_weights_word(axis)
	if type(document) == str:
		document = document.split()

	_,aWords = zip(*axis)

	ans = sum([axis[aWords.index(word)][0] for word in set(aWords) & set(document)])
	return ans

documents = json.load(open('cleaned-corpus.json','w'))
import json
import re 

import numpy as np 
import matplotlib.pyplot as plt 

from awesome_print import ap 

semantic_axes = open('latent-topics').read().splitlines()

"""
  Each semantic axis is a row formatted as (sign) weight*word

"""


pattern = re.compile("(\S[A-Z])")
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

documents = json.load(open('cleansed-corpus.json','r'))
keys = documents.keys()

#make data.json

def make_name(aStr):
	aStr = aStr.replace('-',' ')
	aStr = aStr.replace('_',' ')
	aStr = aStr.replace('www.','')
	aStr = aStr.replace('.com','')
	aStr = aStr.replace('.org','')
	aStr = aStr.replace('.htm','')
	aStr = aStr.replace('.github.io','')
	aStr = aStr.replace('lab','')
	aStr = aStr.replace('-',' ')
	aStr = aStr.strip()
	if re.search("\S[A-Z]",aStr):
		aStr = re.sub('(\S)([A-Z])', r'\1 \2',aStr)
	elif aStr.endswith('.mssm.edu'):
		aStr = aStr[:-9]
	elif 'www.' in aStr:
		make_name(aStr.split('.')[1])
	elif '#bot' in aStr:
		aStr = aStr.replace('#bot','')
	else:
		aStr = aStr.capitalize()
	return aStr.strip().capitalize()

def find_institution(prof):
	institutions = ['rockefeller','nyu','sinai']
	list_of_faculty = {institution: open('%s-labs'%institution,'r').read().splitlines()
				for institution in institutions}
	return [institution for institution in institutions if any(prof in lab for lab in list_of_faculty[institution])].pop()

def fetch_keywords(aStr,axes,axis_count=2):
	aStr = aStr.split() if type(aStr) == str else aStr #Assumes delimiter is a space
	new_axes = [extract_weights_word(axes[i]) for i in xrange(axis_count)]
	return list(set(word for item in new_axes for _,word in item) & set(aStr))

def format_for_frontend(documents,axes):
	keys = documents.keys()

	answer = []

	for key in keys:
		item = {}
		item['x'] = project(axes[0],documents[key])
		item['y'] = project(axes[1],documents[key])
		item['r'] = project(axes[2],documents[key])

		item['description'] = {}
		item['description']['name'] = make_name(key.encode('ascii'))
		item['description']['keywords'] = fetch_keywords(documents[key],axes,axis_count=2)
		item['description']['institution'] = find_institution(key).capitalize()
		answer.append(item)
	return answer

for_frontend = format_for_frontend(documents,semantic_axes)
json.dump(for_frontend,open('data.json','w'))
'''
 Format of data.json 

   x : float
   y : float
   r : float
   description : 
     {
         name: ...
         institution: ...
         keywords: 
     }

'''
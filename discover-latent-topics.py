import nltk
import os 
import string
import json

from datetime import date
from awesome_print import ap 
from gensim import corpora, models, similarities
from nltk.stem.wordnet import WordNetLemmatizer


if not os.path.isfile(os.path.join(os.getcwd(),'cleansed-corpus.json')):
	#--- Assemble corpus
	directories = ["nyu","rockefeller","sinai"]

	filenames = [os.path.join(root,filename)
				 for root,subdirectory,filenames in os.walk(os.getcwd()) 
				 for filename in filenames 
				 if subdirectory == [] and '.git' not in root]
	#This walk assumes that all files are in terminal folders.
	lmtzr = WordNetLemmatizer()

	def fetch_cleansed_text(filename):	
		tokens =' '.join(line.strip().lower() for line in open(filename,'r').readlines())
		tokens = nltk.word_tokenize(''.join(ch for ch in tokens if ord(ch)<128)) #Preserve spaces 
		
		#Remove punctuation
		tokens = [token for token in tokens if all(ch in string.ascii_letters for ch in token)]

		#Remove stopwords
		text = [word for word in tokens if word not in nltk.corpus.stopwords.words('english')]
		text = [lmtzr.lemmatize(word) for word in text if word not in open('stopwords','r').read().splitlines() and len(word)>2]

		return text
		#Not standardizing abbreviations 

	corpus = {os.path.basename(os.path.normpath(filename)):fetch_cleansed_text(filename)
			  for filename in filenames}

	json.dump(corpus,open('cleansed-corpus-%s.json'%date.today(),'wb'))
	json.dump(corpus,open('cleansed-corpus.json','wb'))
else:
	corpus = json.load(open('cleansed-corpus.json','rb'))

keys = corpus.keys() #Create a way to iterate through dictionary, alt to ordered dict
texts = [corpus[key] for key in corpus]

dictionary = corpora.Dictionary(texts)
#dictionary.save('/texts.dict') # store the dictionary, for future reference
indexed_corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(indexed_corpus)
indexed_corpus_tfidf = tfidf[indexed_corpus]

lsi = models.LsiModel(indexed_corpus_tfidf,id2word=dictionary,num_topics=10)

with open('latent-topics-%s'%date.today(),'w') as f:
	for topic in lsi.show_topics(num_words=20,num_topics=100):
		print>>f,topic
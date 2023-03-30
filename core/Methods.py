import Constantes as cst

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import string
from tqdm import tqdm

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoConfig
# from transformers import TextClassificationPipeline
from transformers import pipeline
from scipy.special import softmax

# import spacy
# nlp = spacy.load("fr_core_news_sm")
# import re
# from gensim.models import Phrases
# from gensim.corpora import Dictionary
# from gensim.models import LdaModel

class Methods:
	""" Class Method : classe principale pour les méthodes fréquements utilisées. """
	
	def sort_by(list_, lmbd, reverse=True):
		return sorted(list_, key=lmbd, reverse=reverse)

	def take_argument_list_objects(list_object, lmbd):
		return [lmbd for l in list_object]

	def condition_count_time_response(participant, current_message, next_message):
		if participant == current_message.sender and current_message.sender != next_message.sender:
			time = next_message.date - current_message.date
			return time * (time < timedelta(hours=8)), 1 * (time < timedelta(hours=6))
		else: 
			return timedelta(0), 0

	def count_time_response(participants, conversation): 
		time = []
		average_time = []
		conversation.messages.reverse()
		for p in participants:
			nb = 0
			t = timedelta(0)
			for m in range(len(conversation.messages)-1):
				x, y = Methods.condition_count_time_response(p, conversation.messages[m], conversation.messages[m+1])
				# print("Sortie t : ", x)
				t += x
				nb += y
			
			if nb != 0:
				average_time.append(t / nb)
			else:
				average_time.append(timedelta(0))
			time.append(t)
		return time, average_time


#################### Sentiment analysis ####################

	
# Hugging face
	# def sentiment_analysis(message):

		
	# 	sentiment_classifier_1 = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment", tokenizer="cardiffnlp/twitter-xlm-roberta-base-sentiment")
	# 	sentiment_classifier_2 = pipeline('sentiment-analysis', model='cmarkea/distilcamembert-base-sentiment')
	# 	sentiment_classifier_3 = pipeline('sentiment-analysis', model='tblard/tf-allocine')

	# 	result_1 = sentiment_classifier_1(message)
	# 	result_2 = sentiment_classifier_2(message)
	# 	result_3 = sentiment_classifier_3(message)

	# 	# sentiment = result[0]['label']
	# 	# score = result[0]['score']

	# 	# print("Le sentiment est : ", sentiment, " avec un score de ", score)
	# 	print(message)
	# 	print("sentiment : ", result_1)
	# 	print("sentiment : ", result_2)
	# 	print("sentiment : ", result_3)
	# 	return result_3[0]


# XLM-roBERTa-base ~ trained on 198M de tweets
# https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment
	def sentiment_analysis_roberta(messages):
		# Preprocess text (username and link placeholders)
		# def preprocess(text):
		#     new_text = []
		#     for t in text.split(" "):
		#         t = '@user' if t.startswith('@') and len(t) > 1 else t
		#         t = 'http' if t.startswith('http') else t
		#         new_text.append(t)
		#     return " ".join(new_text)

		MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

		tokenizer = AutoTokenizer.from_pretrained(MODEL)
		config = AutoConfig.from_pretrained(MODEL)

		# PT
		model = AutoModelForSequenceClassification.from_pretrained(MODEL)
		# model.save_pretrained(MODEL)

		sentiments = []
		print("*"*10 + " sentiment_analysis_roberta " + "*"*10)
		for message in tqdm(messages):
			if message != "":
				encoded_input = tokenizer(message, return_tensors='pt')
				output = model(**encoded_input)
				scores = output[0][0].detach().numpy()
				scores = softmax(scores)

				# Print labels and scores
				ranking = np.argsort(scores)
				ranking = ranking[::-1]
				# for i in range(scores.shape[0]):
				#     l = config.id2label[ranking[i]]
				#     s = scores[ranking[i]]
				#     print(f"{i+1}) {l} {np.round(float(s), 4)}")
				sentiments.append({config.id2label[ranking[i]]:scores[ranking[i]] for i in range(scores.shape[0])})
			else:
				sentiments.append("")
		return sentiments

# distilcamembert-base-sentiment ~ 200.000 Amazon's shorts reviews and 235.000 Allocine's critics
# https://huggingface.co/cmarkea/distilcamembert-base-sentiment
	def sentiment_analysis_camembert(messages):
		analyzer = pipeline(
		    task='text-classification',
		    model="cmarkea/distilcamembert-base-sentiment",
		    tokenizer="cmarkea/distilcamembert-base-sentiment")
		
		print("*"*10 + " sentiment_analysis_camembert " + "*"*10)
		sentiments = [analyzer(message, top_k=None) if message != "" else "" for message in tqdm(messages)]

		return sentiments



#################### TOPIC MODELING ####################



# Flaubert topic classification : 10 classes 
# https://huggingface.co/lincoln/flaubert-mlsum-topic-classification
	# def topic_modeling2(message):
	# 	model_name = 'lincoln/flaubert-mlsum-topic-classification'

	# 	loaded_tokenizer = AutoTokenizer.from_pretrained(model_name)
	# 	loaded_model = AutoModelForSequenceClassification.from_pretrained(model_name)

	# 	topic_modeling = TextClassificationPipeline(model=loaded_model, tokenizer=loaded_tokenizer)
	# 	topics = topic_modeling(message, truncation=True)

	# 	return topics



	# def topic_modeling1(message):
	# 	import gensim
	# 	from gensim.utils import simple_preprocess
	# 	from gensim.models import TfidfModel, LdaModel
	# 	from gensim.corpora import Dictionary

	# 	# Préparer le corpus de phrases en français
	# 	phrases = ["Le chat noir dort sur le canapé", "Le chien aboie dans la cour", "Le chat et le chien sont amis"]

	# 	# Nettoyer et prétraiter les données
	# 	processed_phrases = [simple_preprocess(phrase, deacc=True) for phrase in phrases]

	# 	# Convertir les phrases en vecteurs
	# 	dictionary = Dictionary(processed_phrases)
	# 	corpus = [dictionary.doc2bow(phrase) for phrase in processed_phrases]
	# 	tfidf = TfidfModel(corpus)
	# 	corpus_tfidf = tfidf[corpus]

	# 	# Entraîner un modèle de topic modeling
	# 	lda_model = LdaModel(corpus_tfidf, id2word=dictionary, num_topics=2)

	# 	# Extraire les sujets des nouvelles phrases
	# 	new_phrases = [message]
	# 	for phrase in new_phrases:
	# 	    bow = dictionary.doc2bow(simple_preprocess(phrase, deacc=True))
	# 	    topics = lda_model[tfidf[bow]]
	# 	    print(f"La phrase '{phrase}' a été classée dans les sujets suivants : {topics}")

	# 	return topics



	# def topic_modeling3(message):

	# 	from transformers import CamembertModel, CamembertTokenizer
	# 	from sklearn.feature_extraction.text import CountVectorizer
	# 	from sklearn.decomposition import LatentDirichletAllocation

	# 	# Charger le modèle et le tokenizer Camembert pré-entraînés pour le français
	# 	model = CamembertModel.from_pretrained("camembert-base")
	# 	tokenizer = CamembertTokenizer.from_pretrained("camembert-base")


	# 	# Prétraiter la phrase en la tokenisant et en la transformant en vecteur de caractéristiques
	# 	phrase_tokens = tokenizer.encode(message, add_special_tokens=True)
	# 	phrase_vector = np.zeros((1, 768))
	# 	input_ids = torch.tensor([phrase_tokens])
	# 	with torch.no_grad():
	# 	    last_hidden_states = model(input_ids)[0]
	# 	phrase_vector[0, :] = last_hidden_states.mean(dim=1).squeeze().numpy()

	# 	# Charger les données pour la tâche de topic modeling
	# 	data = pd.read_csv("data_fr.csv", encoding="utf-8")

	# 	# Prétraiter les données en créant une matrice de documents-termes
	# 	docs = data["text"].tolist()
	# 	cv = CountVectorizer(max_df=0.95, min_df=2, stop_words="english")
	# 	dtm = cv.fit_transform(docs)

	# 	# Effectuer la tâche de topic modeling en utilisant LDA
	# 	lda = LatentDirichletAllocation(n_components=10, random_state=42)
	# 	lda.fit(dtm)

	# 	# Identifier les topics les plus pertinents pour la phrase donnée
	# 	phrase_topic_probabilities = lda.transform(phrase_vector)
	# 	top_topics = phrase_topic_probabilities.argsort()[:, -3:][:, ::-1].squeeze()
	# 	for topic in top_topics:
	# 	    print("Topic ", topic)
	# 	    print([(cv.get_feature_names()[i], lda.components_[topic][i])
	# 	          for i in lda.components_[topic].argsort()[:-10 - 1:-1]])
	# 	    print("\n")


	# def topic_modeling_conversation(messages):

	# 	# Nettoyage des données
	# 	spacy_docs = list(nlp.pipe([m for m in messages if m != ""]))

	# 	docs = []
	# 	print("*"*10 + " preprocessing_topic_modeling " + "*"*10)
	# 	for doc in tqdm(spacy_docs):
	# 	    tokens = []
	# 	    for token in doc:
	# 	        if len(token.orth_) > 3 and not token.is_stop: # supprimer tous les mots de moins de 3 caractères et supprimer tous les stop-words
	# 	            tokens.append( token.lemma_.lower() )  # lemmatiser les mots restants et mettre ces mots en minuscules
	# 	    docs.append(tokens)

	# 	print("Docs : ", docs)
	# 	bigram = Phrases(docs, min_count=10)
	# 	print("Bigrams : ", bigram)
	# 	for index in range(len(docs)):
	# 	    for token in bigram[docs[index]]:
	# 	        if '_' in token:  # les bigrammes peuvent être reconnus par "_" qui concatène les mots
	# 	            docs[index].append(token)

	# 	dictionary = Dictionary(docs)
	# 	print('Nombre de mots unique dans les documents initiaux :', len(dictionary))
	# 	# dictionary.filter_extremes(no_below=3, no_above=0.25)
	# 	print('Nombre de mots unique dans les documents après avoir enlevé les mots fréquents/peu fréquents :', len(dictionary))
	# 	print("Exemple : ", dictionary.doc2bow(docs[4]))

	# 	corpus = [dictionary.doc2bow(doc) for doc in docs]
	# 	print(corpus)

	# 	# Topic Modeling avec LDA
	# 	model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, chunksize=1000, passes=5, random_state=1)
	# 	for (topic, words) in model.print_topics():
	# 	    print("***********")
	# 	    print("* topic", topic+1, "*")
	# 	    print("***********")
	# 	    print(topic+1, ":", words)
	# 	    print()

	# 	return model.print_topics()[1]


	def topic_modeling(messages):
		classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")		
		classifier2 = pipeline(
			task="zero-shot-classification",
		    model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
		    tokenizer="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")


		candidate_labels = ["question", "réponse", "études", "travail", "vacances", "bar", "fête", "nourriture", "sport", "amis", "jeux", "rendez-vous", "lieux", "objets", "actions", "musique", "video", ""]
		
		print("*"*10 + " topic_modeling " + "*"*10)
		topics = [classifier2(message, candidate_labels, multi_label=True) if message != "" else "" for message in tqdm(messages)]
		
		return topics





# Détection de messages haineux
# https://huggingface.co/Hate-speech-CNERG/dehatebert-mono-french
	def hate_of_speech(messages):
		# tokenizer = AutoTokenizer.from_pretrained("Hate-speech-CNERG/dehatebert-mono-french")

		# model = AutoModelForSequenceClassification.from_pretrained("Hate-speech-CNERG/dehatebert-mono-french")
			
		hos = pipeline(
		    task='text-classification',
		    model="Hate-speech-CNERG/dehatebert-mono-french",
		    tokenizer="Hate-speech-CNERG/dehatebert-mono-french")

		# HOS = hos((messages))
		print("*"*10 + " hate_of_speech " + "*"*10)
		HOS = [hos(message) if message != "" else "" for message in tqdm(messages)]
		
		return HOS



# Détection d'entitées nommées
# https://huggingface.co/Jean-Baptiste/camembert-ner-with-dates
	def ner(messages):
		tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
		model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
		
		ner = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

		print("*"*10 + " ner " + "*"*10)
		topics = [ner(message) if message != "" else "" for message in tqdm(messages)]

		return topics
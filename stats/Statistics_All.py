import sys
sys.path.append('../core/')


from Message import Message
from Conversation import Conversation
from Preprocessing import Preprocessing

from Methods import Methods
import Constantes as cst
from Statistics_conversation import Statistics_conversation

import numpy as np
import pandas as pd
from collections import Counter
import statistics
from math import *

category_insta = {"nb_messages": "Nombre total de messages",
			"message": "Nombre de messages", 
			"audio": "Nombre d'audios", 
			"temporary_photo": "Nombre de contenus temporaires", 
			"photo": "Nombre de photos", 
			"video": "Nombre de videos", 
			"call": "Nombre d'appels", 
			"share": "Nombre de partages de contenu", 
			"error": "Nombre d'erreurs d'assimilation"}

index_insta = ["nb_messages", "message", "audio", "temporary_photo", "photo", "video", "call", "share", "error"]

category_fb = {"nb_messages": "Nombre total de messages",
			"message": "Nombre de messages", 
			"audio": "Nombre d'audios", 
			"gifs": "Nombre de gifs", 
			"photo": "Nombre de photos", 
			"video": "Nombre de videos", 
			"call": "Nombre d'appels", 
			"file": "Nombre de fichiers partagés", 
			"error": "Nombre d'erreurs d'assimilation"}

index_fb = ["nb_messages", "message", "audio", "gifs", "photo", "video", "call", "file", "error"]


class Statistics_All(object):
	""" Class Statistics_all_conversations : classe principale contenant les statistiques de toutes les conversations tel que la moyenne, le min et le max,\
	 	l'écart type et la variance. """

	def __init__(self, stats, social_network):
		if social_network == "insta":
			category = category_insta
			index = index_insta
			my_name = cst.my_name_insta
		else:
			category = category_fb
			index = index_fb
			my_name = cst.my_name_fb


		self.nb_conversations = len(stats)

		all_stats = []
		for f in category.keys():
			all_stats.append([s.df_statistics_conversation.loc[f, "value"] for s in stats])

		total = [sum(a) for a in all_stats]
		average = [int(np.mean(a)) for a in all_stats]
		min_nb = [min(a) for a in all_stats]
		max_nb = [max(a) for a in all_stats]
		standard_deviation = [statistics.pstdev(a) for a in all_stats]
		variance = [statistics.pvariance(a, m) for a, m in zip(all_stats, average)]

		self.total_messages_sent = sum([s.df_statistics_conversation.loc["nb_messages_by_participants", "value"][my_name] for s in stats])
		self.total_messages_received = total[0] - self.total_messages_sent

		self.df_statistics_all_conversations = pd.DataFrame({\
													"fields": category.values(),\
													"total": total,\
													"average": average,\
													"min": min_nb,\
													"max": max_nb,\
													"standart_deviation": standard_deviation,\
													"variance": variance}, index=index)

	def __repr__(self):
		return f"\n\
				Nombre de conversations \t\t: {self.nb_conversations}\n\
				Nombre total de messages envoyés \t: {self.total_messages_sent}\n\
				Nombre total de messages reçus \t: {self.total_messages_received}\n\
				\n\n{self.df_statistics_all_conversations}"

	def __str__(self):
		return f"\n\
				Nombre de conversations \t\t: {self.nb_conversations}\n\
				Nombre total de messages envoyés \t: {self.total_messages_sent}\n\
				Nombre total de messages reçus \t\t: {self.total_messages_received}\n\
				\n\n{self.df_statistics_all_conversations}"


if __name__ == "__main__":
	social_network = "insta"
	preprocessing = Preprocessing(social_network=social_network)
	
	stats = [Statistics_conversation(conv, social_network) for conv in preprocessing.list_conversations]
	all_stats = Statistics_All(stats, social_network)
	
	print(all_stats)

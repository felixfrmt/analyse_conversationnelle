import sys
sys.path.append('../core/')


from Message import Message
from Conversation import Conversation
from Preprocessing import Preprocessing

from Methods import Methods
import Constantes as cst
import statistics

import numpy as np
import pandas as pd
from collections import Counter
from tabulate import tabulate

category_insta = {"message": "Nombre de messages", 
			"audio": "Nombre d'audios", 
			"temporary_content": "Nombre de contenus temporaires", 
			"photo": "Nombre de photos", 
			"video": "Nombre de videos", 
			"call": "Nombre d'appels", 
			"share": "Nombre de partages de contenu", 
			"reaction": "Nombre de réactions à des messages",
			"error": "Nombre d'erreurs d'assimilation"}

index_insta = ["id", "nb_messages", "nb_messages_by_participants", "time", "average_time", "message", "audio", "temporary_photo", "photo", "video", "call", "share", "reaction", "error"]


category_fb = {"message": "Nombre de messages", 
			"audio": "Nombre d'audios", 
			"gifs": "Nombre de gifs", 
			"photo": "Nombre de photos", 
			"video": "Nombre de videos", 
			"call": "Nombre d'appels", 
			"file": "Nombre de fichiers partagés", 
			"error": "Nombre d'erreurs d'assimilation"}

index_fb = ["id", "nb_messages", "nb_messages_by_participants", "time", "average_time", "message", "audio", "gifs", "photo", "video", "call", "file", "error"]


class Statistics_conversation(object):
	""" Class Statistics_conversation : classe principale pour les statistiques d'une conversation représentée sous forme de dataframe. """

	def __init__(self, conversation, social_network):
		if social_network == "insta":
			category = category_insta
			index = index_insta
		else:
			category = category_fb
			index = index_fb


		participants = conversation.participants.copy()

		counter_sender = Counter([m.sender for m in conversation.messages])
		time, average_time = Methods.count_time_response(participants, conversation)
		counter_type = Counter([m.type_message for m in conversation.messages])

		stats = [("id", conversation.id_),
			   ("Nombre total de messages", len(conversation.messages)),
			   ("Nombre de messages par participants", dict([(p, counter_sender[p]) for p in participants])),
			   ("Temps total de réponse", dict([(p, str(t)) for p, t in zip(participants, time)])),
			   ("Temps moyen de réponse", dict([(p, str(avg_t)) for p, avg_t in zip(participants, average_time)]))]

		stats = stats + [(value, counter_type[key]) for key, value in category.items()]
		self.df_statistics_conversation = pd.DataFrame({"field": [x for x, y in stats], "value": [y for x, y in stats]}, index=index)





def classement(stats, field="nb_messages"):
	if field in ["time", "average_time"]:
		stats = Methods.sort_by(stats, lambda x: list(x.df_statistics_conversation.loc["average_time", "value"].values())[0].total_seconds(), reverse=True)
	elif field == "nb_messages_by_participants":
		stats = Methods.sort_by(stats, lambda x: list(x.df_statistics_conversation.loc[field, "value"].values())[0], reverse=True)
	else:
		stats = Methods.sort_by(stats, lambda x: x.df_statistics_conversation.loc[field, "value"], reverse=True)
	return stats



def stats_one_conv(conversations, name, social_network):
	one_conv = [conv for conv in conversations if name == conv.id_]
	print(f"Conversation : {one_conv}")
	if one_conv:
		stats = Statistics_conversation(one_conv[0], social_network)
		display(stats.df_statistics_conversation)
		return stats
	else:
		print("Liste des conversations avec cette personne vide")
		exit(0)


if __name__ == "__main__":
	social_network = "insta"
	preprocessing = Preprocessing(social_network=social_network)

	stats = [Statistics_conversation(conv, social_network) for conv in preprocessing.list_conversations]
	stats = classement(stats, "nb_messages")

	for x in stats[0:10]:
		print("\n")
		print(tabulate(x.df_statistics_conversation, headers = 'keys', tablefmt = 'psql'))

	# stats_one_conv(conversations, "eistigangpillypilly_2074961085862785", social_network)

	# stats = stats_one_conv("gauthierptj".encode('latin-1').decode('utf-8'))
	# print([stats[i].df_statistics_conversation for i in range(len(stats))])
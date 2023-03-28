from Preprocessing import Preprocessing
from NLP_Conversation import NLP_Conversation

if __name__ == "__main__":
	social_network = "insta"
	preprocessing = Preprocessing(social_network=social_network)
	

	conv_id = "yazz_1025307678869520" 
	list_conv = [conv for conv in preprocessing.list_conversations if conv.id_ == conv_id]

	if list_conv:
		conv = list_conv[0]
		conv = NLP_Conversation(conv.id_, conv.participants, conv.messages)
		print(conv)


	
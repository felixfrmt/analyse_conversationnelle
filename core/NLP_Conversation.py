import Constantes as cst
from NLP_Message import NLP_Message
from Conversation import Conversation
from Methods import Methods


class NLP_Conversation(Conversation):
    """ Class Conversation : classe principale pour les conversations contenant un id pour identifier le dossier, la liste des participants, et l'ensemble des messages. """

    def __init__(self, id_, participants, messages):
        contents = [m.content for m in messages]
        sentiment_1 = Methods.sentiment_analysis_roberta(contents)
        sentiment_1 = [list(sent) for sent in sentiment_1]
        sentiment_1 = [sent[0] if sent else "" for sent in sentiment_1]

        sentiment_2 = Methods.sentiment_analysis_camembert(contents)
        sentiment_2 = [sent[0]["label"] if sent else "" for sent in sentiment_2]
        
        hos = Methods.hate_of_speech(contents)
        hos = [h[0]["label"] if h else "" for h in hos]

        # topics = Methods.topic_modeling(contents)
        # topics = [top["labels"] for top in topics]
        # topics = [top[0:2] for top in topics]

        # print(topics)
        nlp_messages = [NLP_Message(m.sender, m.date, m.type_message, m.content, s1, s2, h) for m, s1, s2, h in zip(messages, sentiment_1, sentiment_2, hos)]
        
        super().__init__(id_, participants, nlp_messages)
        
        self.topics = "Methods.topic_modeling_conversation(contents)"


    def __repr__(self):
        return f"Id : {self.id_}\nParticipants : {self.participants}"

    def __str__(self):
        # return f"Id : {self.id_}\nParticipants : {self.participants}\nMessages : \n\t{self.messages[0:min(10, len(self.messages))]}\nTopics : {self.topics}"
        return f"Id : {self.id_}\nParticipants : {self.participants}\nMessages : \n\t{self.messages}\nTopics : {self.topics}"


if __name__ == "__main__":

    from datetime import datetime
    from Message import Message
    m1 = Message(cst.my_name_insta, datetime.fromtimestamp(1666004000000/1000), "message", "Coucou, tu vas bien ?")
    m2 = Message(cst.my_name_insta, datetime.fromtimestamp(1666005000000/1000), "message", "Non je suis allé chez le médecin")
    m3 = Message("Personne", datetime.fromtimestamp(1666006000000/1000), "message", "ah merde, il a dit quoi ?")



    m4 = Message("Personne", datetime.fromtimestamp(1669002000000/1000), "message", "Tu viens à quelle heure à l'école pour trzvailler ?")
    m5 = Message(cst.my_name_insta, datetime.fromtimestamp(1669002900000/1000), "message", "vers 14h")
    m6 = Message("Personne", datetime.fromtimestamp(1669002914000/1000), "message", "ça marche, tu vas kiffer la nouvelle mise à jour du code")


    conv = NLP_Conversation("Personne_1_dzzdzd", [cst.my_name_insta, "Personne"], [m1, m2, m3, m4, m5, m6])
    print(conv)

    conv2 = NLP_Conversation("Somebody_fejefnfekl", ["Somebody", cst.my_name_insta], [m4, m5, m6])
    print( conv2)
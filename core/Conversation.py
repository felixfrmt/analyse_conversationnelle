import Constantes as cst
import Message


class Conversation(object):
    """ Class Conversation : classe principale pour les conversations contenant un id pour identifier le dossier, la liste des participants, et l'ensemble des messages. """

    def __init__(self, id_, participants, messages):
        self.id_ = id_
        self.participants = participants
        self.messages = messages

    def __repr__(self):
        return f"\nId : {self.id_}\t\tParticipants : {self.participants}"

    def __str__(self):
        return f"\nId : {self.id_}\nParticipants : {self.participants}\nMessages : \n\t{self.messages[0:min(3, len(self.messages))]}"
        # return f"Id : {self.id_}\nParticipants : {self.participants}\nMessages : \n\t{self.messages}"





# if __name__ == "__main__":
#     from datetime import datetime

#     m1 = Message.Message(cst.my_name_insta, datetime.fromtimestamp(1666005000000/1000), "message", "Holaaaa")
#     m2 = Message.Message(cst.my_name_insta, datetime.fromtimestamp(1666004000000/1000), "audio", "")
#     m3 = Message.Message("Personne", datetime.fromtimestamp(1666003000000/1000), "message", "Bye")



#     m4 = Message.Message("Personne", datetime.fromtimestamp(1666002000000/1000), "audio", "")
#     m5 = Message.Message(cst.my_name_insta, datetime.fromtimestamp(1666001000000/1000), "video", "video.mp4")
#     m6 = Message.Message("Personne", datetime.fromtimestamp(1666000000000/1000), "message", "Byebye")


#     conv = Conversation("Personne 1_dzzdzd", [cst.my_name_insta, "Personne"], [m1, m2, m3, m4, m5, m6])
#     print(conv)

#     conv2 = Conversation("Somebody_fejefnfekl", ["Somebody", cst.my_name_insta], [m4, m5, m6])
#     print( conv2)


    # conversation.id_
    # conversation.participants
    # conversation.get_messages(messages where foreign_id_conversation = conversation.id_)
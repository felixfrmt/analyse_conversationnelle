import Constantes as cst
import datetime

class Message(object):
    """ Class Message : classe principale pour les messages contenant l'emetteur, le type de message, la date et son contenu. """
    
    def __init__(self, sender="", date=0, type_message="message", content=""):
        self.sender = sender        
        self.date = date
        self.type_message = type_message
        self.content = content        

    def __repr__(self):
        return f"\n\n\t{self.type_message} : \n\t\tDe : {self.sender}\n\t\tLe : {self.date}\n\t\tContent :\n\t\t\t{self.content}"

    def __str__(self):
        return f"\n\t{self.type_message} : \n\t\tDe : {self.sender}\n\t\tLe : {self.date}\n\t\tContent :\n\t\t\t{self.content}"

    # def __dict__(self):
    #     msg_dict = {
    #         "sender": self.sender,
    #         "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
    #         "type_message": self.type_message,
    #         "content": self.content,
    #     }
    #     return msg_dict



# if __name__ == "__main__":
#     m = Message("Félix", 0, "message", "Holaaaa")
#     m1 = Message("Abdel", 1, "audio", "Byee")

#     print(m)
#     print(m1)

#     print("Accès a la var sender : ", m.sender)

#     temp = m.date
#     m.date = 0

#     print(f"Sans modifications : {m}")
#     m.content = "BLaBLAAaa"
#     print(f"Avec modifications : {m}") 
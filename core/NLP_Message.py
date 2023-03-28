from Message import Message
from Methods import Methods


class NLP_Message(Message):
    """ Class NLP_Message : classe pour l'IA permettant l'analyse conversationnelle. Elle étend la classe Message en ajoutant le sentiment et le topic du message """
    
    def __init__(self, sender="", date=0, type_message="message", content="", sentiment_1="", sentiment_2="", hos="", topics=""):
        super().__init__(sender, date, type_message, content)
        if content != "":
            self.sentiment_1 = sentiment_1   
            self.sentiment_2 = sentiment_2      
            self.hos = hos
            self.topics = topics
        else:
            self.sentiment_1 = ""
            self.sentiment_2 = ""
            self.hos = ""
            self.topics = ""


    def __repr__(self):
        return f"\n\n\t{self.type_message} : \n\t\tDe : {self.sender}\n\t\tLe : {self.date}\n\t\tContent :\n\t\t\t{self.content}\
                        \n\t\tSentiment model roberta : {self.sentiment_1}\n\t\tSentiment model camembert : {self.sentiment_2}\
                        \n\t\tHate of speech : {self.hos}\n\t\tTopics : {self.topics}"

    def __str__(self):
        return f"\n\n\t{self.type_message} : \n\t\tDe : {self.sender}\n\t\tLe : {self.date}\n\t\tContent :\n\t\t\t{self.content}\
                        \n\t\tSentiment model roberta : {self.sentiment_1}\n\t\tSentiment model camembert : {self.sentiment_2}\
                        \n\t\tHate of speech : {self.hos}\n\t\tTopics : {self.topics}"

    # def __dict__(self):
    #     msg_dict = {
    #         "sender": self.sender,
    #         "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
    #         "type_message": self.type_message,
    #         "content": self.content,
    #         "sentiment_1" : self.sentiment_1,   
    #         "sentiment_2" : self.sentiment_2,      
    #         "hos" : self.hos,
    #         "topics" : self.topics,    
    #     }
    #     return msg_dict



if __name__ == "__main__":
    nlp_msg = NLP_Message(sender="Alice", date=123456, content="je t'aime")
    print(nlp_msg)
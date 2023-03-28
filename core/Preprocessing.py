import json
import os
from datetime import datetime

import Constantes as cst
from Message import Message
from Conversation import Conversation


class Preprocessing(object):


    def __init__(self, social_network="insta"):
        if social_network == "insta":
            path = "../core/messages_insta/inbox/"
        else:
            path="./messages_fb/inbox/"
        
        ids, files = self.explore_data(path=path, format='json')
        print("files : ", files)
        self.list_conversations = self.load_conversations(paths=files, ids=ids)


    def explore_data(self, path, format='json'):
        ids = []
        files = []
        print("path : ", path)
        for r, d, f in os.walk(path):
            json = []
            taken = False
            for file in f:
                if file.endswith(format) and not "nlp" in file:
                    print(file)
                    json.append(os.path.join(r, file))
                    if not taken:
                        taken = True
                        ids.append(r.split("/")[-1])
            if json:
                files.append(json)

        return ids, files



    def load_file_messages(self, path="", file=None):
        list_messages = []
        if file:
            file = json.load(file)
        else:    
            with open(path, 'r') as f:
                file = json.load(f)

        participants = [participant["name"].encode('latin-1').decode('utf-8') for participant in file["participants"] if participant["name"] != cst.encoded_name_insta]
        participants = [cst.my_name_insta] + participants


        for e in file["messages"]:
            sender = e["sender_name"].encode('latin-1').decode('utf-8')
            date = datetime.fromtimestamp(e["timestamp_ms"] / 1000)

            content = ""

            if len(e.keys()) == 2 :
                type_message = "temporary_content" 
            else:
            
                if "content" in e.keys():
                    if "started an audio call" in e["content"] or "call_duration" in e.keys():
                        type_message = "call"
                    else:
                        content = e["content"].encode('latin-1').decode('utf-8')
                        type_message = "message"

                elif "share" in e.keys():
                    type_message = "share"
                
                elif "audio_files" in e.keys():
                    type_message = "audio"

                elif "photos" in e.keys():
                    type_message = "photo"

                elif "videos" in e.keys():
                    type_message = "video"                    
                
                elif "reactions" in e.keys():
                    type_message = "reaction"

                else:                        
                    print("dict keys : ", e.keys())
                    type_message = "error"
                                   
            m = Message(sender, date, type_message, content)
            list_messages.append(m)
        return file, list_messages, participants



    def load_conversations(self, paths=[], ids="", format='json'):
        list_conversations = []
        paths = [sorted(p, reverse=False) for p in paths]

        for id_, files in zip(ids, paths):
            list_messages = []
            for f in files:
                opened_file, list_mes, participants = self.load_file_messages(f)
                list_messages = list_messages + list_mes
            # participants = [p["name"].encode('latin-1').decode('utf-8') for p in opened_file["participants"] if p["name"] != cst.encoded_name_insta]
            # participants = [cst.my_name_insta] + participants

            conversation = Conversation(id_, participants, list_messages)
            list_conversations.append(conversation)        
        
        return list_conversations




# if __name__ == "__main__":

#     preprocessing = Preprocessing(social_network="insta")
#     print("\n".join([str(conv) for conv in preprocessing.list_conversations]))
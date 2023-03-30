import sys
sys.path.append('../core/')
sys.path.append('../stats/')

from Preprocessing import Preprocessing
from Conversation import Conversation
from Statistics_conversation import Statistics_conversation
from Statistics_All import Statistics_All
from NLP_Conversation import NLP_Conversation


import os
import shutil
import json
from json import JSONEncoder
import datetime
from tqdm import tqdm

from typing import Annotated

from typing import Union, List, Dict, Optional
from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from collections import Counter


app = FastAPI(title="API Analyse conversationnelle", description="API permettant l'analyse des conversations d'Instagram", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}




@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    path = "../core/messages_insta/inbox/"
    
    for file in tqdm(files):
        repo = file.filename.split("/")[-2]
        name = file.filename.split("/")[-1]
        if name.endswith("json") and not "nlp" in name:
            if not os.path.exists(path+repo):
                os.makedirs(path+repo)
                print("enregistrement ici : ", "../core/messages_insta/inbox/"+name)
            contents = await file.read()
            with open(path+repo+"/"+name, "wb") as f:
                f.write(contents)
    
    global preprocessing
    preprocessing = Preprocessing()
    
    return "Good !"


@app.get("/all_stats/")
async def get_all_stats():
    social_network = "insta"
    global stats
    stats = [Statistics_conversation(conv, social_network) for conv in preprocessing.list_conversations]

    all_stats = Statistics_All(stats, social_network)

    # print(all_stats.__dict__)

    html_content =  """
                    <table class="table">
                        <tbody>
                          <tr>
                            <td>Nombre de conversations</td>
                            <td>Nombre total de messages envoyés</td>
                            <td>Nombre total de messages reçus</td>
                          </tr>
                          <tr>
                            <td>""" + str(all_stats.nb_conversations) + """</td>
                            <td>""" + str(all_stats.total_messages_sent) + """</td>
                            <td>""" + str(all_stats.total_messages_received) + """</td>
                          </tr>
                        </tbody>
                      </table>
                    """ + all_stats.df_statistics_all_conversations.to_html(index=False, classes="table", border="0")

    return HTMLResponse(content=html_content, status_code=200)



@app.get("/list_id_conversations/")
async def get_list_conversation():
    return {"list_id_conversations": [conv.id_ for conv in preprocessing.list_conversations]}


@app.get("/list_messages/{conv_id}")
async def get_list_messages(conv_id):
    list_conv = [conv for conv in preprocessing.list_conversations if conv.id_ == conv_id]
    global conv
    conv = list_conv[0]
    return {"conversation": conv}


class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return str(obj)



@app.get("/list_nlp_messages/{conv_id}")
async def get_list_nlp_messages(conv_id):
    global json_string
    if not os.path.isfile("../core/messages_insta/inbox/"+conv_id+"/nlp_message_1.json"):
        nlp_conv = NLP_Conversation(conv.id_, conv.participants, conv.messages)

        dict_messages = [{"sender": msg.sender,
                          "sentiment_1": msg.sentiment_1, 
                          "sentiment_2": msg.sentiment_2,
                          "hos": msg.hos } for msg in nlp_conv.messages]


        json_string = json.dumps({"participants": nlp_conv.participants, "messages": dict_messages}, indent=4)

        with open("../core/messages_insta/inbox/"+conv_id+"/nlp_message_1.json", 'w') as outfile:
            outfile.write(json_string)
        json_string = {"participants": nlp_conv.participants, "messages": dict_messages}
    else:
        with open("../core/messages_insta/inbox/"+conv_id+"/nlp_message_1.json", "r") as file:
            json_string = json.load(file)
            
    return json_string


@app.get("/stats_nlp_conversation/{conv_id}")
async def get_stats_nlp_conversation(conv_id):
    sentiments = [m["sentiment_1"] for m in json_string["messages"]]
    counter_sentiments = Counter(sentiments)
    
    hos = [h["hos"] for h in json_string["messages"]]
    counter_hos = Counter(hos)
    return {"sentiments": counter_sentiments, "hos": counter_hos}
 



@app.get("/stats_conversation/{conv_id}")
async def get_stats_conversation(conv_id):
    stats_conversation = [s for s in stats if s.id_ == conv_id]
    stats_conversation = stats_conversation[0].df_statistics_conversation
    stats_conversation = stats_conversation.set_index('field')
    stats_conversation.loc["Nombre de messages par participants", "value"] = str(stats_conversation.loc["Nombre de messages par participants", "value"]).strip("{}")
    stats_conversation.loc["Temps total de réponse", "value"] = str(stats_conversation.loc["Temps total de réponse", "value"]).strip("{'}")
    stats_conversation.loc["Temps moyen de réponse", "value"] = str(stats_conversation.loc["Temps moyen de réponse", "value"]).strip("{'}")
    # print([index for index, row in stats_conversation.iterrows()])
    # stats_conversation["value"] = [json.dumps(row["value"]) if str(index) == "Nombre de messages par participants" for index, row in stats_conversation.iterrows()]
    html_content = stats_conversation.to_html(index=True, header=False, classes="table", border="0")
    return HTMLResponse(content=html_content, status_code=200)




if __name__ == '__main__':
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

import json
import os
from datetime import datetime

HISTORY_DATA="history_data"

def init_memory():
    if not os.path.exists(HISTORY_DATA):
        os.makedirs(HISTORY_DATA)

def save_to_memory(url:str,platform:str,transcript:str,blueprint:str,psychology:str):
    init_memory()
    timestamp=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename=f"{HISTORY_DATA}/run_{timestamp}.json"
    data={
      "timestamp":datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
      "url":url,
      "platform":platform,
      "transcript":transcript,
      "blueprint":blueprint,
      "psychology":psychology
    }
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

def get_history_list():
    init_memory()
    files=[f for f in os.listdir(HISTORY_DATA) if f.endswith(".json")]
    return sorted(files,reverse=True)

def load_history_file(filename:str):
    init_memory()
    filepath=os.path.join(HISTORY_DATA,filename)
    with open(filepath,"r",encoding="utf-8") as f:
        return json.load(f)


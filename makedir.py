# create directory in accordance to the json file

import os
import json
from urllib.parse import unquote

json = json.load(open("TLMC.json", 'r', encoding='utf-8'))
folder = os.path.dirname(os.path.realpath(__file__))+"\\down\\"


def createDir(path:str):
    if not os.path.exists(path):
        os.makedirs(path)
        
def createFile(path:str, url:str):
    with open(path, 'w') as f:
        f.write(url)
        f.close()
    
    
def createStructure(json, folder):
    for level in json:
        if "dir" in level:
            dir = level["dir"]
            if dir.startswith("[") and dir.endswith("]"):
                dir = dir[1:-1:]
            createDir(folder+dir)
            createStructure(level["files"], folder+dir+"\\")
        else:
            createFile(folder+level["name"], level["url"])
            
createStructure(json, folder)
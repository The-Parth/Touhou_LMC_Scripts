# this script recursively searches for all the files in the Touhou Lossless Music Collection and indexes them to TLMC.json

import os
import json
from urllib.parse import unquote
import requests
import time
import re
import bs4

# The TLMC archive FTP server
baseurl = "http://151.80.40.155/tlmc/"
basepath = os.path.dirname(os.path.realpath(__file__))+"\\" # this is the path to the directory of this script

def getFiles(url:str):
    try:
        r = requests.get(url)
    except:
        print("Error: " + url)
        time.sleep(5)
        return getFiles(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    
    files = []
    
    for link in soup.find_all('a'):
        link : bs4.element.Tag
        hr = link.get('href')
        if hr == '../':
            continue
        if hr.endswith('/'):
            inner_dir = getFiles(url+hr)
            pfn = unquote(hr)[:-1:]
            files.append({"dir":pfn, "files":inner_dir})
            print("Done: " + pfn)
        else:
            files.append({"name":unquote(hr), "url":url+hr})
    return files

print("Getting files...")
files = getFiles(baseurl)
# save the files to a json file
with open(basepath+"TLMC.json", 'w', encoding='utf-8') as f:
    json.dump(files, f, indent=4, ensure_ascii=False)
print("Done getting files")
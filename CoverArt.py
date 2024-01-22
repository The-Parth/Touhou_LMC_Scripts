# Add cover art to the all the files of all types in the directory
# Query MusicBrainz for the cover art, and download it
# Add the cover art to the files
# use mutagen to add the cover art

"""
Fetch cover art and apply to file
"""

import os
import json
from urllib.parse import unquote
import requests
import time
import mutagen

basedir = "C:\\TOHO\\TLMC\\岸田教団&THE明星ロケッツ\\2017.05.07 [K2-0016] ANCIENT FLOWER [例大祭14]"
# Best song - Secret Philosophy 

def getMBID(artist:str, album:str):
    url = "https://musicbrainz.org/ws/2/release/?query=artist:%22" + artist + "%22%20AND%20release:%22" + album + "%22&fmt=json"
    r = requests.get(url)
    if r.status_code == 200:
        j = json.loads(r.text)
        if j["count"] == 0:
            return None
        else:
            print(j["releases"][0]["id"])
            return j["releases"][0]["id"]
    else:
        print("Error: " + str(r.status_code))
        return None
    
def getCoverArt(mbid:str):
    url = "http://coverartarchive.org/release/" + mbid
    r = requests.get(url)
    if r.status_code == 200:
        j = json.loads(r.text)
        if len(j["images"]) == 0:
            return None
        else:
            return j["images"][0]["image"]
    else:
        print("Error: " + str(r.status_code))
        return None
    

def addCoverArt(path:str, url:str):
    # Incomplete
    audio = mutagen.File(path)
    if audio is None:
        print("Error: " + path + " is not a valid audio file")
        return
    r = requests.get(url)
    if r.status_code == 200:
        audio.tags.add(mutagen.id3.APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=r.content))
        audio.save()
        print("Done: " + path)
    else:
        print("Error: " + str(r.status_code))
        return
    

img = getCoverArt(getMBID("ANCIENT FLOWER","KISIDA KYODAN & THE AKEBOSI ROCKETS"))

# save the image
with open("cover.jpg", "wb") as f:
    f.write(requests.get(img).content)



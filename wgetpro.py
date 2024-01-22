import os
import requests
import bs4
from urllib.parse import unquote

"""
Download files from a url with this python script
Made because don't want wget
"""

directory = "http://151.80.40.155/tlmc/%5BC.H.S%5D/2017.05.07%20%5BCHS-0029%5D%20t%26T.%20%28tpz%20And%20TOUHOU.%29%20from%202005%20%5B%E4%BE%8B%E5%A4%A7%E7%A5%AD14%5D/"


def downloader(directory:str):
    page = requests.get(directory, stream=True)
    # now, recursively download all files in the directory
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all('a'):
        link : bs4.element.Tag
        hr = link.get('href')
        if hr == '../':
            continue
        # hr is url encoded, so we need to decode it, all the way, not jusr %20
        hr_unquoted = unquote(hr)
        
        # download the file
        np = requests.get(directory + hr, stream=True)
        if np.status_code == 200:
            print("Downloading: " + hr)
        else:
            print("Error: " + str(np.status_code))
            continue
        
        # make down directory if it doesn't exist
        if not os.path.exists("down"):
            os.makedirs("down")
        
        with open("down/" + hr_unquoted, 'wb') as f:
            for chunk in np.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    
        print("Done: " + hr_unquoted)
                    

downloader(directory)

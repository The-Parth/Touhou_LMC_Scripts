# download all the songs required in a directory
import requests
import os
import time

basepath = "C:\\TOHO\\TLMC\\Liverne" # sample 

# this is the path to the directory of files to download

# download logic - all files opened as a text file, check if it's a url, if it is, download it, if not skip it
# if it's a directory, create it, and recursively download all the files in it

# complements my make dir script, can go as deep as needed recursively.

def downloadFile(path: str):
    with open(path, 'r') as f:
        try:
            url = f.read()
            f.close()
        except:
            url = "invalid"
    # check if it's a url
    if url.startswith("http"):
        error_count = 0
        while error_count < 2:
            # download the file
            try:
                np = requests.get(url, stream=True)
                if np.status_code == 200:
                    print("Downloading: " + url)
                else:
                    print("Error: " + str(np.status_code))
                    error_count += 1
                # replace the original file with the downloaded file, temp file is used to prevent corruption
                with open(path+".tmp", 'wb') as f:
                    for chunk in np.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                
                # if the file is downloaded successfully, delete the original file and rename the temp file
                os.remove(path)
                os.rename(path+".tmp", path)
                            
                print("Done: " + path)
                break
            except:
                print("Error: " + url)
                time.sleep(5)
    else:
        print("Skipping: " + path)
        return
    
def downloadDir(path: str):
    if not os.path.exists(path):
        print("Error: " + path + " does not exist")
        return
    for file in os.listdir(path):
        if os.path.isdir(path + "\\" + file):
            downloadDir(path + "\\" + file)
        else:
            downloadFile(path + "\\" + file)
            
if __name__ == "__main__":
    downloadDir(basepath)
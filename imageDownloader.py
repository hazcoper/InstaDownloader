import os
import shutil

def downloadImage(SHORTCODE, folderName=None):
    """
    Will download the given image to the given folder name
    """

    os.system(f"instaloader -l hazprinter --dirname-pattern output -- -{SHORTCODE}")

def downloadStory(code, folderName=None):
    pass


def cleanCache():
    """
    Cleans the files that where downloaded by instaloader
    """
    folderList = [x for x in os.listdir() if x == "output"]
    
    for folder in folderList:
        # os.rmdir(folder)
        shutil.rmtree(folder)


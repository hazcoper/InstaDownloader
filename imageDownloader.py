import os
import shutil

def login():
    """
    will login to a certain username and password
    """

def downloadImage(SHORTCODE, folderName=None):
    """
    Will download the given image to the given folder name
    """

    os.system(f"instaloader -l hazprinter --dirname-pattern output -- -{SHORTCODE}")

def cleanCache():
    folderList = [x for x in os.listdir() if x == "output"]
    
    for folder in folderList:
        # os.rmdir(folder)
        shutil.rmtree(folder)

# downloadImage(
#     "Cg52QVbsypo"
# )


/afs/.ist.utl.pt/users/8/4/ist196884/.local/bin/instaloader  --login newAgainPt --dirname-pattern output -- -Cg4bQEWLwUt


instaloader


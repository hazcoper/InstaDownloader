# Standard imports
import sys
import os
import time
import re

# Local imports
from imageDownloader import cleanCache, downloadImage
from telegramFunc import receive_bot_message, telegram_bot_sendtext, send_photo


# Global variables
responseList = []  # append and remove from the top. Will contain the userIds  to respond to
userID = None


# Function to validate URL
# using regular expression
def isValidURL(str):
    """
    Validate that a given string is a url using regex
    """
 
    # Regex to check valid URL
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
     
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty
    # return false
    if (str == None):
        return False
 
    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False


def sendImages(SHORTCODE, userID):
    """
    It will send all of the images and caption that have been downloaded from instagram
    """

    # send the photos
    path = f"output"
    imageList = [os.path.join(path, x) for x in os.listdir(path) if x.split(".")[-1] == "jpg"]
    
    for imagePath in imageList:
        send_photo(imagePath, userID)

    # send the caption
    captionFile = [os.path.join(path, x) for x in os.listdir(path) if x.split(".")[-1] == "txt"][0]
    
    with open(captionFile) as f:
        text = f.read()

    print("this is the caption: ", text)
    telegram_bot_sendtext(text, userID)

    # clean the folder
    cleanCache()


if __name__ == '__main__':

    print("[SERVER] - Program started")
    while True:
        
        mss = receive_bot_message(responseList)     #Grab the first message
        while mss == False:             #Wait for new messages to come in
            mss = receive_bot_message(responseList) 
            time.sleep(0.5)

        print(f"[SERVER] - Received the following message: {mss}")

        # select the correct user id
        userID = int(responseList[0])
        print(f"[SERVER] - Selected the following userID {userID}")

        # validade if message corresponds to a url
        if isValidURL(mss):

            try:
                # grab the shortcode
                mss = mss.split("/")
                p = mss.index("p")

                print(f"[SERVER] - Received valid link: {mss}")
                print(f"[SERVER] - Parsed the following shortcode: {mss[p+1]}")
            
                telegram_bot_sendtext(f"Downloading: {mss[p+1]}", userID)
                downloadImage(mss[p+1])
                sendImages(mss[p+1], userID)


            except Exception as e:
                telegram_bot_sendtext("Command has failed... (if the account is private you need to login)", userID)
                print("This was the error ", e)
    

        elif mss == "help":
            print("user has asked for help")
            telegram_bot_sendtext("just send the instagram link and I will return the photo", userID)
        
        else:
            print("Unrecognized command: ", mss)
            telegram_bot_sendtext("Unrecognized command...", userID)

        # remove the selected user id
        responseList = responseList[1:]


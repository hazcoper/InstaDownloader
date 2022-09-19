# Standard imports
import sys
import os
import time
import requests
import re

# Non standard imports
import telegram

# Local imports
from imageDownloader import cleanCache, downloadImage
from telegramFunc import receive_bot_message, telegram_bot_sendtext, send_photo

lastMessage = 119801179        #Used to check if  the message received hasent been read already
responseList = []  # append and remove from the top. Will contain the userIds  to respond to
userID = None

# Function to validate URL
# using regular expression
def isValidURL(str):
 
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


def parse_cred():
    """Gets the bottoken and chatid from the credential file"""
    file_name = "credential.txt"
    with open(file_name, "r", encoding="UTF-8") as file:
        lines = file.readlines()
    bot_token = lines[0][:-1]
    chatID = lines[1]

    return bot_token, chatID

def telegram_bot_sendtext(bot_message, userID):
    """Receives the message for the bot to send, and sends it to the bot specified below"""
    bot_token, bot_chatID = parse_cred()
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(userID) + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def receive_bot_message():
    """Receives the messages coming from the user and makes sure that messages are not read twice"""
    global lastMessage
    currentMessage = ''

    bot_token, bot_chatID = parse_cred()
    link = "https://api.telegram.org/bot" + bot_token + "/getUpdates"
    response = requests.get(link)    #get the json data from the link
    response = response.json()

    response = response['result']   #go to the result part of the dictionary
    if len(response) == 0:
        # means that I have not received a message in a long time
        return False
    response = response[-1]         #go to the last sent message

    currentMessage = response['update_id']  #get the message code to check if we are not repeating messages
    message = response['message']
    message = message['text']

    if not currentMessage == lastMessage:
        lastMessage = currentMessage
        responseList.append(response["message"]["chat"]["id"])
        return message
    else:
        return False


def send_photo(photo, userID):      #sends a photo and delets it afterwards
    token, chatID = parse_cred()
    bot = telegram.Bot(token=token)  # Start the telegram API
    bot.send_document(userID, document=open(photo, 'rb'))  # Send the image
    os.remove(photo)  # delete file

def sendImages(SHORTCODE, userID):
    """
    It will send all of the images that have been downloaded and will send the caption
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


print("program started")
while True:
    mss = receive_bot_message()     #Grab the first message
    while mss == False:             #Wait for new messages to come in
        mss = receive_bot_message()
        time.sleep(0.5)

    print("I have received this message: ", mss)

    # select the correct user id
    userID = int(responseList[0])
    print("THis is the userID", userID, type(userID))

    if isValidURL(mss):

        try:
            # grab the shortcode
            mss = mss.split("/")
            print(mss, type(mss))
            p = mss.index("p")

            print("have received the following link: ", mss, mss[p+1])
        
            telegram_bot_sendtext(f"Downloading: {mss[p+1]}", userID)
            imageDownloader.downloadImage(mss[p+1])
            sendImages(mss[p+1], userID)
            imageDownloader.cleanCache()


        except Exception as e:
            telegram_bot_sendtext("Command has failed...", userID)
            print("This was the error ", e)
 

    elif mss == "help":
        print("user has asked for help")
        telegram_bot_sendtext("just send the instagram link and I will return the photo", userID)
    
    else:
        print("Unrecognized command: ", mss)
        telegram_bot_sendtext("Unrecognized command...", userID)

    # remove the selected user id
    responseList = responseList[1:]


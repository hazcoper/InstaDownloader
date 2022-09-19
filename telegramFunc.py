# Standard imports
import requests
import os


# Non standard imports
import telegram

lastMessage = 119801179        #Used to check if  the message received hasent been read already


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

def receive_bot_message(responseList):
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


def send_photo(photo, userID):
    """
    Sends a photo and deletes it afterwards
    """
    token, chatID = parse_cred()
    bot = telegram.Bot(token=token)  # Start the telegram API
    bot.send_document(userID, document=open(photo, 'rb'))  # Send the image
    os.remove(photo)  # delete file




# TelegramBot Insta downloader


Simple telegram bot that will receive a link for a instagram post and will return the image of that post

Uses telegram bot api to create a chat bot that will deal with the user interaction and instaloader to download the posts

# Explanation

A fast and simple option to download instagram posts

# Usage

For more options refer to instaloader documentation

After dealing with the login, installing everything and creating your bot, using the project is really easy.
run the program using the following command:
```bash
python3 Main.py
```

## Login
It is not necessary for you to login with your account, however, if you desire to download images from a private account, you must login (and the login account should follow the account with the desired photo)
in order to login run the following command in the terminal
```bash
instaloader --login YOUR_USERNAME
```
After pressing enter it will ask for the password. Instaloader will then cache the username and password, meaning that only need to login once.

# Creating bot
open telegram, register your account with the bot and start sending links
  - to register your account with the bot, check the link that was given by the Bot Father when you created your bot
  - it will be necesasry to create a file called "credentials.txt.
    - add the http API token
    - add the user id
      - send a message to your bot, open https://api.telegram.org/botAPI_TOKEN/getUpdates and you should see the user id there


# Install
After cloning the repo, run the following command to install the dependencies
```bash
pip install -r requirements.txt
```
After that follow the usage instructions

# Create bot

# To do

    - see if it works with stories
    - test the code
    - support multiple users
      - have a way to identify them and each could have different permissiosn

# Done
    - separate code
    - make usage instructions
    - create the requirements file
    - make install instructions
      - needs to include the making of the bot


# Known limitations
    - all the text after a # in the description will not be sent

# Disclaimer
Please do not use this tool to steal content from other people, always remeber to give credit where credit's due
I am not responsible for any misuse of this tool
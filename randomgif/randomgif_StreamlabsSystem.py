import os
import json
import codecs

from datetime import datetime

ScriptName = "Radnom Gif Command"
Website = "http://www.dustydiamond.de/"
Description = "Chooses a suitable gif for the game you're streaming on twitch"
Creator = "DustyDiamond"
Version = "1.0.0"
Command = "!gif"

settings = {}
game = ""

def Init():
    global settings, GifDir

    work_dir = os.path.dirname(__file__)
    GifDir = os.path.join(work_dir, "Gifs")

    if not os.path.exists(GifDir):
        os.makedirs(GifDir)

    try:
        with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    
    except:
        settings = {
            "command": "!gif",
            "permission": "Everyone",
            "cooldown": 30,
            "bot_response": "Hier GIF einfuegen",
            "onCooldown": "$user, $command is still on cooldown for $cd seconds!",
	        "onUserCooldown": "$user, $command is still on user cooldown for $cd seconds! "
        }

    return

def log(message):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    Parent.Log("INFO:", ScriptName + ": " + dt_string + ": " + message)
    return

def send_message(message):
    Parent.SendStreamMessage(message)
    log("Message Sent")
    return

def Execute(data):
    global game, GifDir
    message = ""
    if data.IsChatMessage() and data.GetParam(0) == "!getgame" and Parent.HasPermission(data.User, "Moderator", ""):
        game = getGame("cogefee")
        game = replace(game, " ", "")
        message = "Current Game is: " + game
        
    if data.IsChatMessage() and data.GetParam(0) == settings["command"]:
        game = getGame("cogefee")
        game = game.replace(" ", "")
        location = GifDir

        
    send_message(message)
    return


def getGame(channel):
    global game, jsonData
    if channel == "":
        channel = Parent.GetChannelName()
    
    jsonData = json.loads(Parent.GetRequest("https://decapi.me/twitch/game/" + channel, {}))
    game = jsonData["response"]
    return game

def OpenGifDir():
    location = GifDir
    os.startfile(os.path.join(os.getcwd(), GifDir))

def ReloadSettings(jsonData):
    Init()
    return

def Tick():
    return

def Unload():
    return

# Define Helpers
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]
import os
import json
import codecs
import random
import time
import PIL
from shutil import copyfile

from datetime import datetime

ScriptName = "Random Gif Command"
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
            "folder": "",
            "permission": "Everyone",
            "cooldown": 30,
            "bot_response": "Hier GIF einfuegen",
            "onCooldown": "$user, $command is still on cooldown for $cd seconds!",
	        "onUserCooldown": "$user, $command is still on user cooldown for $cd seconds! ",
            "delay": 2,
            "gifsize": 600
        }

    return

def log(message):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    Parent.Log("INFO:" + dt_string + ": ", ScriptName + ": " + message)
    return

def send_message(message):
    Parent.SendStreamMessage(message)
    #log("Message Sent")
    return

def Execute(data):
    global game, GifDir
    message = ""
    max = 0
    number = 0
    basewidth = 0

    game = getGame()
    game = game.replace(" ", "").lower()

    if data.IsChatMessage() and data.GetParam(0) == "!getgame" and Parent.HasPermission(data.User, "Moderator", ""):
        message = "Current Game is: " + game
        
    if data.IsChatMessage() and data.GetParam(0) == settings["command"]:
        location = GifDir
        path = os.path.join(GifDir,game)

        max = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path,name))])
        if data.GetParam(1) != "":
            try:
                number = int(data.GetParam(1))
                if number > max:
                    number = random.randint(1,max)
            except:
                number = random.randint(1,max)
        else:  
            number = random.randint(1,max)

        gif = str(number) + ".gif"

        log("Max: " + str(max) + " - Rand: " + str(number))

        delay = settings["delay"]
        blank = "blank.gif"
        blank_be = "blank-backup.gif"

        # Display GIF, wait delay time
        sourcefile = os.path.join(path,gif)
        targetfile = os.path.join(GifDir,blank)

        try: 
            copyfile(sourcefile, targetfile)
            log("Gif Copied")
        except IOError as e:
            log("Unable to Copy File. %s" % e)
            return
        
        time.sleep(delay)

        sourcefile = os.path.join(GifDir,blank_be)
        targetfile = os.path.join(GifDir,blank)

        try: 
            copyfile(sourcefile, targetfile)
            log("Gif Reset")
        except IOError as e:
            log("Unable to Copy File. %s" % e)
            return
        
    send_message(message)
    return


def getGame():
    global game, jsonData    
    jsonData = json.loads(Parent.GetRequest("https://decapi.me/twitch/game/" + Parent.GetChannelName(), {}))
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
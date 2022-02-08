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
users = []

def Init():
    global settings, users

    work_dir = os.path.dirname(__file__)

    try:
        with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    
    except:
        settings = {
            "command": "!gif",
            "permission": "Everyone",
            "cooldown": 30,
            "bot_response": "Hier GIF einfügen",
            "onCooldown": "$user, $command is still on cooldown for $cd seconds!",
	        "onUserCooldown": "$user, $command is still on user cooldown for $cd seconds! "
        }

    temp = str(settings["users"])
    users = temp.split(",")
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
    global settings, users
    outputMessage = ""
    # !team branch
    if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, "Everyone", ""):
        
        if settings["users"] == "":
            return
        
        userId = data.User
        username = data.UserName
        if (Parent.IsOnCooldown(ScriptName, settings["command"]) or Parent.IsOnUserCooldown(ScriptName, settings["command"], userId)):
            if Parent.GetCooldownDuration(ScriptName, settings["command"]) > Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId):
                cdi = Parent.GetCooldownDuration(ScriptName, settings["command"])
                cd = str(cdi)
                outputMessage = settings["onCooldown"]
            else:
                cdi = Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId)
                cd = str(cdi)
                outputMessage = settings["onUserCooldown"]
            outputMessage = outputMessage.replace("$cd", cd)

        else:
            team = ""
            if len(users) == 1:
                team = users[0]
            else:
                for i in users[:-1]:
                    if i == "": 
                        continue

                    team = team + i + ", "
                else:
                    team = left(team,(len(team) -2)) + " und " + users[-1]
                
            outputMessage = settings["bot_response"]
            outputMessage = outputMessage.replace("$team", team)
            #outputMessage = "!team was triggered"

    # !setteam branch
    elif data.IsChatMessage() and data.GetParam(0).lower() == (left(settings["command"],1) + "set" + right(settings["command"],(len(settings["command"])-1))) and Parent.HasPermission(data.User, settings["permission"], ""):        
        paramCount = int(data.GetParamCount())
        users = []

        log("paramCount: "+ str(paramCount))

        for i in range(paramCount):
            if i == 0:
                continue
            else:
                try:
                    users.insert(i,data.GetParam(i))
                    log(str(i) + ": " + data.GetParam(i))
                except:
                    users.append(data.GetParam(i))
                    log(str(i) + ": " + data.GetParam(i))

        outputMessage = "Added users "
        userlist = ""
        if len(users) == 1:
            userlist = users[0]
            outputMessage = outputMessage + users[0]
        else:
            for x in users[:-1]:
                if x == "":
                    continue

                userlist = userlist + x + ","
                outputMessage = outputMessage + x + ", "
            else:
                userlist = userlist + users[-1]
                outputMessage = left(outputMessage,(len(outputMessage) -2)) + " und " + users[-1]

        settings["users"] = userlist
        

    # final send of message
    send_message(outputMessage)
    return

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
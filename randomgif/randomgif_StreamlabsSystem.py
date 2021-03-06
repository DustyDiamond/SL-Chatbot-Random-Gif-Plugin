#!/usr/bin/python
# -*- coding: utf-8 -*-
#---------------------------------------------------------
# Import Libraries
#---------------------------------------------------------
import os
import json
import codecs
import random
import time
from shutil import copyfile
from datetime import datetime

# SLOBS RC
#import clr
#clr.AddReference("IronPython.Modules.dll")
import re
import threading

#---------------------------------------------------------
# Script Information
#---------------------------------------------------------
ScriptName = "Random Gif Command"
Website = "http://www.dustydiamond.de/"
Description = "Chooses a suitable gif for the game you're streaming on twitch."
Creator = "DustyDiamond / Ocgineer"
Version = "1.1.0"
Command = "!gif"

#---------------------------------------------------------
# Global Vars
#---------------------------------------------------------
# SLOBS RC
BridgeApp = os.path.join(os.path.dirname(__file__), "bridge\\SLOBSRC.exe")
RegSLObsScene = None
RegSLObsGetItems = None
RegSLObsSource = None
RegSLObsSourceT = None
RegSLObsFolder = None
RegSLObsFolderT = None
RegSLObsSwap = None
RegSLObsReplaySwap = None

#OBS RC
RegObsScene = None
RegObsSource = None
RegObsTmdSrc = None
RegObsTmdScn = None

# misc
global settings, game, work_dir, streamingService
settings = {}
game = ""
work_dir = ""
last = []
streamingService = ""

#---------------------------------------------------------
# Functions
#---------------------------------------------------------
# Init gets called at Chatbot Startup and Script Load
#---------------------------------------------------------

def Init():
    # Init for SLOBS RC
    # Globals
    global RegSLObsScene
    global RegSLObsGetItems
    global RegSLObsSource
    global RegSLObsSourceT
    global RegSLObsFolder
    global RegSLObsFolderT
    global RegSLObsSwap
    global RegSLObsReplaySwap
    # Compile regexes in init
    RegSLObsScene = re.compile(r"(?:\$SLOBSscene\([\ ]*[\"\'](?P<scene>[^\"\']+)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<delay>\d*)[\"\'][\ ]*)?\))", re.U)
    RegSLObsGetItems = re.compile(r"(?:\$SLOBSgetItems\([\ ]*[\"\'](?P<scene>[^\"\']+)[\"\'][\ ]*)?\)", re.U)
    RegSLObsSource = re.compile(r"(?:\$SLOBSsource\([\ ]*[\"\'](?P<source>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<visibility>[^\"\']*)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<scene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)
    RegSLObsSourceT = re.compile(r"(?:\$SLOBSsourceT\([\ ]*[\"\'](?P<source>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<mode>[^\"\']*)[\"\'][\ ]*\,[\ ]*[\"\'](?P<delay>\d+)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<scene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)
    RegSLObsFolder = re.compile(r"(?:\$SLOBSfolder\([\ ]*[\"\'](?P<folder>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<visibility>[^\"\']*)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<scene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)
    RegSLObsFolderT = re.compile(r"(?:\$SLOBSfolderT\([\ ]*[\"\'](?P<folder>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<mode>[^\"\']*)[\"\'][\ ]*\,[\ ]*[\"\'](?P<delay>\d+)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<scene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)
    RegSLObsSwap = re.compile(r"(?:\$SLOBSswap\([\ ]*[\"\'](?P<scene>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<delay>\d*)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<returnscene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)
    RegSLObsReplaySwap = re.compile(r"(?:\$SLOBSsaveReplaySwap\([\ ]*[\"\'](?P<scene>[^\"\']+)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<offset>\d+)[\"\'][\ ]*)?\))", re.U)

    # Init for OBS Studio RC
    # Globals
    global RegObsScene
    global RegObsSource
    global RegObsTmdSrc
    global RegObsTmdScn

    # Compile regexes in init
    RegObsScene = re.compile(r"(?:\$OBSscene\([\ ]*[\"\'](?P<scene>[^\"\']+)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<delay>\d*)[\"\'][\ ]*)?\))", re.U)
    RegObsSource = re.compile(r"(?P<full>\$OBSsource\([\ ]*[\"\'](?P<source>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<enabled>[^\"\']*)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<scene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)
    RegObsTmdScn = re.compile(r"(?P<full>\$OBStimedScene\([\ ]*[\"\'](?P<s1>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<s2>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<delay>\d+)[\"\'][\ ]*\))", re.U)
    RegObsTmdSrc = re.compile(r"(?P<full>\$OBStimedSource\([\ ]*[\"\'](?P<source>[^\"\']+)[\"\'][\ ]*\,[\ ]*[\"\'](?P<mode>onoff|offon)[\"\'][\ ]*\,[\ ]*[\"\'](?P<delay>\d+)[\"\'][\ ]*(?:\,[\ ]*[\"\'](?P<scene>[^\"\']*)[\"\'][\ ]*)?\))", re.U)

    # Init for rest of script
    # Globals misc
    global settings, work_dir, streamingService


    work_dir = os.path.dirname(__file__)
    settings["work_dir"] = work_dir

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
	        "onUserCooldown": "$user, $command is still on user cooldown for $cd seconds! ",
            "delay": 2,
            "scene": "gifs",
            "programm": "SLOBS"
        }

    

    return

#---------------------------------------------------------
# logger for chatbot internal log
#---------------------------------------------------------
def log(message):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    Parent.Log("INFO: ","[" + ScriptName + "] " + dt_string + ": " + message)
    return

#---------------------------------------------------------
# send message to twitch chat as bot user
#---------------------------------------------------------
def send_message(message):
    Parent.SendStreamMessage(message)
    #log("Message Sent: " + message)
    return

#---------------------------------------------------------
# execute event, called when a message is posted in to 
# twitch chat. data contains info about message and user etc
#---------------------------------------------------------
def Execute(data):
    global game, settings
    message = ""
    max = 0
    number = 0

    game = getGame()
    game = game.replace(" ", "").lower()
    scene = settings["scene"]
    scene_list = []
    streamingService = settings["programm"] 

    # !getgame command to put game as interpreted in script in the chat for naming purposes
    if data.IsChatMessage() and data.GetParam(0) == "!getgame" and Parent.HasPermission(data.User, "Moderator", ""):
        message = "Current Game is: " + game

    # main branch (gif) 
    if data.IsChatMessage() and data.GetParam(0) == settings["command"]:
        # get Max from Nr of Sources in Scene
        bridge_answer = GetItems(scene)
        #log("Bridge Answer: " + bridge_answer)
        
        temp = bridge_answer
        scene_list = temp.split(",")

        for i in scene_list:
            #log(i)
            i = left(i, i.find("-"))
            if i == game:
                max = max + 1

        #log("Max: " + str(max))

        if max <= 0:
            max = 1

        #i=0
        #while i<=100:
        #    log(str(i) + ": " + str(exclusive_rand(max)))
        #    i=i+1

        # get random number to determine
        if data.GetParam(1) != "":
            try:
                number = int(data.GetParam(1))
                if number > max:
                    number = exclusive_rand(max)
            except:
                number = exclusive_rand(max)
        else:  
            number = exclusive_rand(max)
        

        gif = game + "-" + str(number)
        #log("Max: " + str(max) + " - Rand: " + str(number))
        
        delay = str(settings["delay"])
        
        if streamingService == "SLOBS":
            SetSourceVisibilityTimed(gif,"onoff",delay,scene)
            #message = '$SLOBSsourceT("' + gif + '", "onoff", "' + delay + '", "' + scene + '")'
            #log('$SLOBSsourceT("' + gif + '", "onoff", "' + delay + '", "' + scene + '")')
        elif streamingService == "OBS Studio":
            VisibilitySourceTimed(gif,"onoff",float(delay),scene)
            #message = '$OBStimedSource("' + gif + '", "onoff", "' + delay + '", "' + scene + '")'
            #log('$OBStimedSource("' + gif + '", "onoff", "' + delay + '", "' + scene + '")')

        
    #send_message(message)
    return

def exclusive_rand(x):
    global settings, last
    y = 2
    if x <= y:
        y = 1
        settings["notlast"] = False 

    if (settings["notlast"]):
        s = set(range(1,x+y))
        if x>y:
            reduced_list = list(s-(set(last)))
        else:
            reduced_list = list(s)

        i = random.randint(1,len(reduced_list))
        #log("i: " + str(i))
        last.append(reduced_list[i-1])
        if len(last)>y:
            last.pop(0)
        ret = reduced_list[i-1]
    else:
        ret = random.randint(1,x)
        settings["notlast"] = True 

    return ret

#---------------------------------------------------------
# calls decapi to get current game on twitch for channel owner
#---------------------------------------------------------
def getGame():
    global game, jsonData    
    jsonData = json.loads(Parent.GetRequest("https://decapi.me/twitch/game/" + Parent.GetChannelName(), {}))
    game = jsonData["response"]
    return game

#---------------------------------------------------------
# Reload all settings, call init()
#---------------------------------------------------------
def ReloadSettings(jsonData):
    Init()
    return

def Tick():
    return

def Unload():
    return

#---------------------------------------------------------
# Define Helper Functions
#---------------------------------------------------------
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

#---------------------------------------------------------
# SLOBS RC Functions
#---------------------------------------------------------
def GetItems(scene):
    #global settings
    """ Get Items contained in given Scene """
    os.popen("{0} get_items \"{1}\"".format(BridgeApp,scene)).read()
    #work_dir = settings["work_dir"]
    work_dir = os.path.dirname(__file__)
    scene_loc = os.path.join(work_dir, "bridge\\sources.txt")
    sources = ""
    with open(scene_loc, "r") as file:
        lines = file.readlines()

    for line in lines:
        sources = sources + line + "\n"

    return sources

def ChangeScene(scene, delay=None):
	""" Change to scene. """
	if delay:
		os.popen("{0} change_scene \"{1}\" {2}".format(BridgeApp, scene, delay)).read()
	else:
		os.popen("{0} change_scene \"{1}\"".format(BridgeApp, scene)).read()
	return

def ChangeSceneTimed(scene, delay, returnscene=None):
	""" Swap to scene and then back or to optional given scene. """
	if returnscene:
		os.popen("{0} swap_scenes \"{1}\" {2} \"{3}\"".format(BridgeApp, scene, delay, returnscene)).read()
	else:
		os.popen("{0} swap_scenes \"{1}\" {2}".format(BridgeApp, scene, delay)).read()
	return

def SetSourceVisibility(source, visibility, scene=None):
	""" Set the visibility of a source optionally in a targeted scene. """
	if scene:
		os.popen("{0} visibility_source_scene \"{1}\" \"{2}\" {3}".format(BridgeApp, source, scene, visibility)).read()
	else:
		os.popen("{0} visibility_source_active \"{1}\" {2}".format(BridgeApp, source, visibility)).read()
	return

def SetSourceVisibilityTimed(source, mode, delay, scene=None):
    """ Set the visibility of a source timed optionally in a targeted scene. """
    if scene:
        os.popen("{0} tvisibility_source_scene \"{1}\" \"{2}\" {3} {4}".format(BridgeApp, source, scene, delay, mode)).read()
    else:
        os.popen("{0} tvisibility_source_active \"{1}\" {2} {3}".format(BridgeApp, source, delay, mode)).read()
    return

def SetFolderVisibility(folder, visibility, scene=None):
	""" Set the visibility of a folder optinally in a targeted scene. """
	#Parent.Log("functest", "{0} and {1} on {2}".format(folder, visibility, scene))
	if scene:
		os.popen("{0} visibility_folder_scene \"{1}\" \"{2}\" {3}".format(BridgeApp, folder, scene, visibility)).read()
	else:
		os.popen("{0} visibility_folder_active \"{1}\" {2}".format(BridgeApp, folder, visibility)).read()
	return

def SetFolderVisibilityTimed(folder, mode, delay, scene=None):
	""" Set the visibility of a folder timed optionally in a targeted scene. """
	if scene:
		os.popen("{0} tvisibility_folder_scene \"{1}\" \"{2}\" {3} {4}".format(BridgeApp, folder, scene, delay, mode)).read()
	else:
		os.popen("{0} tvisibility_folder_active \"{1}\" {2} {3}".format(BridgeApp, folder, delay, mode)).read()
	return

def SaveReplaySwap(scene, offset=None):
	""" Save the replay and swap to a given "replay" scene. """
	if offset:
		os.popen("{0} save_replaybuffer_swap \"{1}\" {2}".format(BridgeApp, scene, offset)).read()
	else:
		os.popen("{0} save_replaybuffer_swap \"{1}\"".format(BridgeApp, scene)).read()
	return

def ThreadedFunction(command):
	os.popen("{0} {1}".format(BridgeApp, command)).read()
	return

#---------------------------------------
# OBS Studio Functions
#---------------------------------------
def CallbackLogger(response):
	""" Logs callback error response in scripts logger. """
	parsedresponse = json.loads(response)
	if parsedresponse["status"] == "error":
		Parent.Log("OBS Remote", parsedresponse["error"])
	return

def ChangeToScene(scene, delay=None):
	""" Swaps to a given scene, optionally after given amount of seconds. """
	if delay:
		time.sleep(delay)
	Parent.SetOBSCurrentScene(scene, CallbackLogger)
	return

def SetSourceVisibility(source, enabled, scene=None):
	""" Set the targeted source visibility optionally in a scene. """
	Parent.SetOBSSourceRender(source, enabled, scene, CallbackLogger)
	return

def ChangeScenesTimed(scene_one, scene_two, delay):
	""" Swap to one scene then to another scene after a set delay. """
	Parent.SetOBSCurrentScene(scene_one, CallbackLogger)
	if delay:
		time.sleep(delay)
	Parent.SetOBSCurrentScene(scene_two, CallbackLogger)
	return

def VisibilitySourceTimed(source, mode, delay, scene):
	""" Disables a given source in optional scene after given amount of seconds. """
	# off - delay - off
	if mode == "offon":
		Parent.SetOBSSourceRender(source, False, scene, CallbackLogger)
		if delay:
			time.sleep(delay)
		Parent.SetOBSSourceRender(source, True, scene, CallbackLogger)
	# on - delay - off
	else:
		Parent.SetOBSSourceRender(source, True, scene, CallbackLogger)
		if delay:
			time.sleep(delay)
		Parent.SetOBSSourceRender(source, False, scene, CallbackLogger)
	# done
	return

#---------------------------------------
# Parse parameters
#---------------------------------------
# SLOBS
#---------------------------------------
def Parse(parseString, user, target, message):
    """ Custom Parameter Parser. """

    # $SLOBSgetItems("scene")
    if "$SLOBSgetItems" in parseString:
        result = RegSLObsGetItems.search(parseString)
        if result:
            fullParameterMatch = result.group(0)
            scene = result.group("scene")

            threading.Thread(target=GetItems, args=(scene)).start()

            return parseString

	# $SLOBSscene("scene")
	# $SLOBSscene("scene", "delay")
    if "$SLOBSscene" in parseString:
		
        # Apply regex to verify correct parameter use
        result = RegObsScene.search(parseString)
        if result:		
			
			# Get results from regex match
            fullParameterMatch = result.group(0)
            scene = result.group("scene")
            delay = result.group("delay")

			# Start ChangeScene in separate thread
            threading.Thread(target=ChangeScene, args=(scene, delay)).start()

			# Replace the whole parameter with an empty string
            return parseString.replace(fullParameterMatch, "")

	# $SLOBSswap("scene", "delay")
	# $SLOBSswap("scene", "delay", "returnscene")
    if "$SLOBSswap" in parseString:
	
		# Apply regex to verify correct parameter use
        result = RegSLObsSwap.search(parseString)
        if result:

			# Get results from regex match
            fullParameterMatch = result.group(0)
            scene = result.group("scene")
            delay = result.group("delay")
            returnscene = result.group("returnscene")

			# Start ChangeSceneTimed in separate thread
            threading.Thread(target=ChangeSceneTimed, args=(scene, delay, returnscene)).start()

			# Replace the whole parameter with an empty string
        return parseString.replace(fullParameterMatch, "")

	# $SLOBSsourceT("source", "mode", "delay")
	# $SLOBSsourceT("source", "mode", "delay", "scene")
    if "$SLOBSsourceT" in parseString:

		# Apply regex to verify correct parameter use
        result = RegSLObsSourceT.search(parseString)
        if result:

			# Get match groups from regex
            fullParameterMatch = result.group(0)
            source = result.group("source")
            mode = result.group("mode")
            delay = result.group("delay")
            scene = result.group("scene")

			# Start SetSourceVisibilityTimed in separate thread
            threading.Thread(target=SetSourceVisibilityTimed, args=(source, mode, delay, scene)).start()

			# Replace the whole parameter with an empty string
            return parseString.replace(fullParameterMatch, "")

	# $SLOBSsource("source", "visibility")
	# $SLOBSsource("source", "visibility", "scene")
    if "$SLOBSsource" in parseString:

		# Apply regex to verify correct parameter use
        result = RegObsSource.search(parseString)
        if result:

            # Get match groups from regex
            fullParameterMatch = result.group(0)
            source = result.group("source")
            visibility = result.group("visibility")
            scene = result.group("scene")

            # Start SetSourceVisibility in separate thread
            threading.Thread(target=SetSourceVisibility, args=(source, visibility, scene)).start()

            # Replace the whole parameter with an empty string
            return parseString.replace(fullParameterMatch, "")

	# $SLOBSfolderT("folder", "mode", "delay")
	# $SLOBSfolderT("folder", "mode", "delay", "scene")
    if "$SLOBSfolderT" in parseString:

		# Apply regex to verify correct parameter use
        result = RegSLObsFolderT.search(parseString)
        if result:

            # Get match groups from regex
            fullParameterMatch = result.group(0)
            folder = result.group("folder")
            mode = result.group("mode")
            delay = result.group("delay")
            scene = result.group("scene")

            # Start SetFolderVisibilityTimed in separate thread
            threading.Thread(target=SetFolderVisibilityTimed, args=(folder, mode, delay, scene)).start()

            # Replace the whole parameter with an empty string
            return parseString.replace(fullParameterMatch, "")

	# $SLOBSfolder("folder", "visibility")
	# $SLOBSfolder("folder", "visibility", "scene")
    if "$SLOBSfolder" in parseString:

		# Apply regex to verify correct parameter use
        result = RegSLObsFolder.search(parseString)
        if result:
            
            # Get match groups from regex
            fullParameterMatch = result.group(0)
            folder = result.group("folder")
            visibility = result.group("visibility")
            scene = result.group("scene")

            # Start SetFolderVisibility in separate thread
            threading.Thread(target=SetFolderVisibility, args=(folder, visibility, scene)).start()

            # Replace the whole parameter with an empty string
            return parseString.replace(fullParameterMatch, "")

	# $SLOBSstartRecording
    if "$SLOBSstartRecording" in parseString:

        # Start Start Recording in separate thread
        threading.Thread(target=ThreadedFunction, args=("start_recording",)).start()

        # Replace $SLOBSstop with empty string
        return parseString.replace("$SLOBSstartRecording", "")
	
    # $SLOBSstopRecording
    if "$SLOBSstopRecording" in parseString:

        # Start Stop Recording in separate thread
        threading.Thread(target=ThreadedFunction, args=("stop_recording",)).start()

        # Replace $SLOBSstop with empty string
        return parseString.replace("$SLOBSstopRecording", "")
	
	# $SLOBSstartReplay
    if "$SLOBSstartReplay" in parseString:

        # Start Start Replay Buffer in separate thread
        threading.Thread(target=ThreadedFunction, args=("start_replaybuffer",)).start()

        # Replace $SLOBSstop with empty string
        return parseString.replace("$SLOBSstartReplay", "")

    # $SLOBSstopReplay
    if "$SLOBSstopReplay" in parseString:

        # Start Sttop Replay Buffer in separate thread
        threading.Thread(target=ThreadedFunction, args=("stop_replaybuffer",)).start()

        # Replace $SLOBSstop with empty string
        return parseString.replace("$SLOBSstopReplay", "")

	# $SLOBSsaveReplaySwap("scene")
	# $SLOBSsaveReplaySwap("scene","offset")
    if "$SLOBSsaveReplaySwap" in parseString:

        # Apply regex to verify correct parameter use
        result = RegSLObsReplaySwap.search(parseString)
        if result:		
			
            # Get results from regex match
            fullParameterMatch = result.group(0)
            scene = result.group("scene")
            offset = result.group("offset")

            # Start Save Replay and Swap in separate thread
            threading.Thread(target=SaveReplaySwap, args=(scene, offset)).start()

            # Replace the whole parameter with an empty string
            return parseString.replace(fullParameterMatch, "")

	# $SLOBSsaveReplay
    if "$SLOBSsaveReplay" in parseString:

        # Start Save Replay in separate thread
        threading.Thread(target=ThreadedFunction, args=("save_replaybuffer",)).start()

        # Replace $SLOBSstop with empty string
        return parseString.replace("$SLOBSsaveReplay", "")

	# $SLOBSstopStreaming
    if "$SLOBSstopStreaming" in parseString:
    
        # Start stop streaming in separate thread
        threading.Thread(target=ThreadedFunction, args=("stop_streaming",)).start()

        # Replace $SLOBSstop with empty string
        return parseString.replace("$SLOBSstop", "")

	# $SLOBSstartStreaming
#	if "$SLOBSstartStreaming" in parseString:
#
#		# Start stop streaming in separate thread
#		threading.Thread(target=ThreadedFunction, args=("start_streaming",)).start()
#
#		# Replace $SLOBSstop with empty string
#		return parseString.replace("$SLOBSstart", "")
		    
#---------------------------------------
# OBS Studio
#---------------------------------------

    # $OBSscene("scene") parameter
    # $OBSscene("scene", "delay") parameter
    if "$OBSscene" in parseString:

		# Apply regex to verify correct parameter use
        result = RegObsScene.search(parseString)
        if result:		

			# Get results from regex match
            fullParameterMatch = result.group(0)
            scene = result.group("scene")
            delay = int(result.group("delay")) if result.group("delay") else None

			# Change to another scene, using threading
            threading.Thread(target=ChangeToScene, args=(scene, delay)).start()

			# Replace the whole parameter with an empty string
            return parseString.replace(fullParameterMatch, "")

	# $OBSsource("source", "enabled")
	# $OBSsource("source", "enabled", "scene")
    if "$OBSsource" in parseString:

		# Apply regex to verify correct parameter use
        result = RegObsSource.search(parseString)
        if result:

			# Get match groups from regex
            fullParameterMatch = result.group(0)
            source = result.group("source")
            enabled = False if result.group("enabled").lower() == "false" else True
            scene = result.group("scene") if result.group("scene") else None

			# Set source visibility, using threading
            threading.Thread(target=SetSourceVisibility, args=(source, enabled, scene)).start()		

			# Replace the whole parameter with an empty string
            return parseString.replace(fullParameterMatch, "")

	# #OBStimedScene("scene_one", "scene_two", "delay")
    if "$OBStimedScene" in parseString:

		# Apply regext to verify correct parameter use
        result = RegObsTmdScn.search(parseString)
        if result:

			# Get match groups from regex
            fullParameterMatch = result.group(0)
            scene1 = result.group("s1")
            scene2 = result.group("s2")
            delay = int(result.group("delay")) if result.group("delay") else None

			# Change to scene one, then to two after set delay, using threading
            threading.Thread(target=ChangeScenesTimed, args=(scene1, scene2, delay)).start()

			# Replace the whole parameter with an empty string
            return parseString.replace(fullParameterMatch, "")

	# $OBStimedSource("source", "mode", "delay")
	# $OBStimedSource("source", "mode", "delay", "scene")
    if "$OBStimedSource" in parseString:

		# Apply regex to verify correct parameter use
        result = RegObsTmdSrc.search(parseString)
        if result:

			# Get match groups from regex
            fullParameterMatch = result.group(0)
            source = result.group("source")
            mode = result.group("mode")
            delay = int(result.group("delay")) if result.group("delay") else None
            scene = result.group("scene") if result.group("scene") else None

			# Start a new thread to disable the source again after amount of given seconds
            threading.Thread(target=VisibilitySourceTimed, args=(source, mode, delay, scene)).start()

			# Replace the whole parameter with an empty string
            return parseString.replace(fullParameterMatch, "")

	# $OBSstop parameter
    if "$OBSstop" in parseString:

		# Call Stop streaming
        Parent.StopOBSStreaming(CallbackLogger)

        # Replace the whole parameter with an empty string
        return parseString.replace("$OBSstop", "")
		    
	# Return unaltered parseString
    return parseString

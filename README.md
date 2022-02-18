# RandomGIF

![GitHub release (release name instead of tag name)](https://img.shields.io/github/v/release/dustydiamond/SL-Chatbot-Random-Gif-Plugin?include_prereleases&sort=date) ![GitHub](https://img.shields.io/github/license/DustyDiamond/SL-Chatbot-Random-Gif-Plugin)

Chooses a random gif suitable for the current game you play on twitch.  
Simply import every gif you want to display in a special scene in SLOBS.  
Name your Gif-Sources as `<game-name>-<nr> (heroesofthestorm-1)` make sure there aren't any duplicate numbers and that there isn't a number missing.  
With command `!getgame` you can read out your current game, the way the script interpretes the game. Take that exact game name to name your gifs.  
You can place your gifs in the scene as you wish. Then import that "gif-scene" into your live scenes or whereever you want to display your gifs. Make sure to set the name of the scene where your gifs are stored in chatbot settings.  

## Dependencies  

The script uses the SLOBS RC CONSOLE Application from [ocgineer](https://github.com/ocgineer). You can find it [here](https://github.com/ocgineer/SLOBS-RC-CONSOLE)  
A custom and extended version of the Console App is built and shipped with the script so the script won't work with the original bridge application.  
You can find docs to SLOBS RC [here](https://ocgineer.com/sl/chatbot/slobsremote.html)  
It's used to control SLOBS from Chatbot so you have to use Streamlabs OBS to get it working.  

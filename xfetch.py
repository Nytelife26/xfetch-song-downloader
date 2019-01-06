#########################################################
# Nytelife26's XFET(ch) Python music downloading system #
#########################################################

# Imports #
import os
import sys
import subprocess
import re
import platform

subprocess.call("pip install --upgrade -r requirements.txt >nul 2>&1")

if os.name != "nt":
    print("WARNING: This script assumes you have FFmpeg installed (on Windows, it will automatically install it for you).")
    input("Please make sure FFmpeg is installed before continuing. Hit enter when ready.")

# Prereqs #
print("INITIALIZING MODULES...")
try:
    from colorama import init
    init()
    from colorama import Fore, Back, Style
    import pyfiglet
    import youtube_dl
    import requests
    import progressbar
    from zipfile import ZipFile
    import numpy as np
except ImportError:
    print("[ERR] Some modules failed to import. Install all the program's requirements with the following command:\npip install --upgrade -r requirements.txt")
subprocess.call("cls" if os.name == "nt" else "clear", shell=True)
    
    
print(Style.NORMAL + Fore.RESET)
if os.name == "nt":
    print(Fore.BLUE + "Checking for / downloading FFMPEG binaries...")
    ff = ["ffmpeg.exe", "ffplay.exe", "ffprobe.exe"]
    if any([not os.path.exists(x) for x in ff]):
        print(Fore.GREEN)
        widgets = ["Downloading FFmpeg: ", 
                   progressbar.Bar(), " ", 
                   progressbar.Percentage(), 
                   progressbar.Timer(" (%(elapsed)s elapsed, "), 
                   progressbar.AdaptiveETA(), " remaining)"]
        if platform.uname()[4].lower() == "amd64": # 64-bit architecture
            arc = "64"
            mxc = 8000 # Chunks estimate
        else: # 32-bit architecture
            arc = "32"
            mxc = np.ceil(55159009 / 8096) # Chunks estimate
        
        url = "https://ffmpeg.zeranoe.com/builds/win{0}/static/ffmpeg-4.1-win{0}-static.zip".format(arc)
        fn = url.split("/")[-1]
        res = requests.get(url, stream=True)
        pb = progressbar.ProgressBar(widgets=widgets, max_value=mxc)
        pb.start()
        with open(fn, "wb") as fout:
            counter = 0
            for x in res.iter_content(chunk_size=8096):
                fout.write(x)
                counter += 1
                pb.update(counter)
        print("\n" + Fore.BLUE + "Extracting FFmpeg..")
        with ZipFile(fn) as zfile:
            base = "{}/bin/".format(".".join(fn.split(".")[0:2]))
            mem = ["{}{}".format(base, x) for x in ff]
            zfile.extractall(members=mem)
            for x in mem:
                os.rename(x, "{}/{}".format(os.getcwd(), x.split("/")[-1]))
    
        os.remove(fn)
    print(Fore.BLUE + "Finished FFMPEG checks and downloads. Running..." + Fore.RESET)
                
# Custom menu screen, because I like things to look nice #
subprocess.call("cls", shell=True)
text = pyfiglet.Figlet(font="epic").renderText("XFET(ch)").split("\n")
bar = os.get_terminal_size().columns
print(Style.NORMAL + Fore.RED + "~" * bar + "\n")
for x in text:
    print(Style.BRIGHT + Fore.RESET + x.center(bar))
print(Style.NORMAL + Fore.GREEN + "- The audio downloading utility by Nytelife26 -".center(bar))
print(Style.NORMAL + Fore.RED + "~" * bar + "\n")

# Main program #
def matcher(link):
    ytmtc = re.compile(r'^(https?\:\/\/)?(www\.|m\.)?(youtube\.com|youtu\.?be)\/.+$')
    scmtc = re.compile(r'^(https?\:\/\/)?(www\.)?(soundcloud\.com\/)')
    if ytmtc.match(url) or scmtc.match(url):
        return True
    return False
    
ytdl_cfg = {'source_address': '0.0.0.0', 'format': '43/best/bestaudio', 'extractaudio': True, 'audioformat': 'mp3', 'outtmpl': 'music/%(title)s.%(ext)s', 'noplaylist': True, 'nocheckcertificate': True, 'ignoreerrors': True, 'quiet': True, 'no_warnings': True}
ytdl = youtube_dl.YoutubeDL(ytdl_cfg)

print(Fore.RESET + "Enter the link(s) to download. Leave blank to end list. Can be inputted as Python list format for experimental purposes.")
songs = []
while True:
    toadd = input(Style.BRIGHT + "> ")
    if toadd.startswith("[") and toadd.endswith("]"):
        exec("songs = {}".format(toadd))
        break
        
    if toadd:
        songs.append(toadd)
    else:
        break

print(Style.NORMAL + "[INFO] Beginning download on {} songs.".format(len(songs)))
for url in songs:
    if matcher(url) and not url.endswith("/tracks"):
        vidinf = ytdl.extract_info(url, download=False, process=False)
        print(Style.NORMAL + Fore.GREEN + "[INFO] Currently downloading {} ({})...".format(vidinf["title"], vidinf["id"]) + Style.NORMAL + Fore.RESET)
        # TODO: Get youtube-dl to work in Python rather than relying on system calls.
        subprocess.call('youtube-dl -q --no-warnings --no-progress -f 43/bestaudio/best -x --audio-format mp3 --audio-quality 0 -o "music/%(title)s.%(ext)s" {}'.format(url))
        print(Style.NORMAL + Fore.GREEN + "[SUCCESS] Downloaded {} ({}). Moving on..".format(vidinf["title"], vidinf["id"]))
    else:
        print('{0}[ERR] {1}"{2}"{0} is an invalid YouTube or SoundCloud link and therefore could not be downloaded.'.format(Fore.RED, Fore.RESET, url))
print(Style.NORMAL + Fore.RESET + "[INFO] Finished downloading the song queue. " + Style.BRIGHT + "Thanks for using XFET(ch). " + Style.NORMAL + Fore.RED + "Exiting..")

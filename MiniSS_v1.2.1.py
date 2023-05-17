import subprocess
import datetime
import os
import zipfile
import io
import psutil
from termcolor import colored
import time
import glob
import requests
import json

magenta = '\033[35m'
blue = '\033[34m'
red = '\033[31m'
yellow = '\033[33m'

print(magenta + """
 ____    ____   _             _     ______    ______   
|_   \  /   _| (_)           (_)  .' ____ \ .' ____ \  
  |   \/   |   __   _ .--.   __   | (___ \_|| (___ \_| 
  | |\  /| |  [  | [ `.-. | [  |   _.____`.  _.____`.  
 _| |_\/_| |_  | |  | | | |  | |  | \____) || \____) | 
|_____||_____|[___][___||__][___]  \______.' \______.'
                                                       
""")
print(blue + "By lrxh#0001")

#Alt checker
ACCOUNTS_FILE_PATH = os.path.join(os.getenv("USERPROFILE"), ".lunarclient", "settings", "game", "accounts.json")
USERCACHE_FILE_PATH = os.path.join(os.getenv("APPDATA"), ".minecraft", "usercache.json")
USERNAMECACHE_FILE_PATH = os.path.join(os.getenv("APPDATA"), ".minecraft", "usernamecache.json")

# Strings
command = 'fsutil usn readjournal C: csv | findstr /i /c:.dll | findstr /i /c:0x80000200 | findstr /i /c:JNat'

# Strings for jar Clickers
jar_strings = ["Clicker", "AutoClicker", "Auto Refill", "Left Clicker", "Right Clicker", "7Clicker", "com.github.kwhat.jnativehook", "org.jnativehook"]

# Strings for forge mods
mods_strings = ["SelfDestruct", "Senura", "Raven", "Clicker", "AutoClicker", "Auto Refill", "Left Clicker", "Right Clicker"]

# Checks Values
cheating_found = False
mod_found = False
service_disabled = False
jarClicker_ininstance = False

# Recording Softwares Strings
recording_softwares = {'bdcam.exe': 'Bandicam',
                       'action.exe': 'Action',
                       'obs64.exe': 'OBS',
                       'dxtory.exe': 'Dxtory',
                       'nvsphelper64.exe': 'Geforce Experience',
                       'camtasia.exe': 'Camtasia',
                       'fraps.exe': 'Fraps',
                       'screencast.exe': 'Screencast',
                       'xsplit.exe': 'XSplit',
                       'playclaw.exe': 'PlayClaw',
                       'mirillis.exe': 'Mirillis Action',
                       'wmcap.exe': 'Bandicam',
                       'lightstream.exe': 'Lightstream',
                       'streamlabs.exe': 'Streamlabs OBS',
                       'webrtcvad.exe': 'Audacity (recording)',
                       'openbroadcastsoftware.exe': 'Open Broadcaster Software',
                       'movavi.screen.recorder.exe': 'Movavi Screen Recorder',
                       'icecreamscreenrecorder.exe': 'Icecream Screen Recorder',
                       'smartpixel.exe': 'Smartpixel',
                       'd3dgear.exe': 'D3DGear',
                       'gadwinprintscreen.exe': 'Gadwin PrintScreen',
                       'apowersoftfreescreenrecorder.exe': 'Apowersoft Free Screen Recorder',
                       'bandicamlauncher.exe': 'Bandicam (launcher)',
                       'hypercam.exe': 'HyperCam',
                       'loiloilgamerecorder.exe': 'LoiLo Game Recorder',
                       'nchexpressions.exe': 'Express Animate (recording)',
                       'captura.exe': 'Captura',
                       'vokoscreenNG': 'VokoscreenNG',
                       'simple.screen.recorder': 'SimpleScreenRecorder',
                       'recordmydesktop': 'RecordMyDesktop',
                       'kazam': 'Kazam',
                       'gtk-recordmydesktop': 'Gtk-RecordMyDesktop',
                       'screenstudio': 'ScreenStudio',
                       'screenkey': 'Screenkey',
                       'pycharm64.exe': 'PyCharm (recording)',
                       'jupyter-notebook.exe': 'Jupyter Notebook (recording)'}


# Jar Clicker check
try:
    time.sleep(2)
    print("")
    print(yellow + "Running jar check...")
    output = os.popen(command).read()
except subprocess.CalledProcessError as e:
    output = ""

deleted_dll_files = []
for line in output.splitlines():
    fields = line.split(",")
    file_name = fields[1].strip('"')
    deletion_date_str = fields[5].strip('"')
    deletion_date = datetime.datetime.strptime(deletion_date_str, "%d/%m/%Y %H:%M:%S")

    uptime_seconds = psutil.boot_time()
    system_uptime = datetime.datetime.fromtimestamp(uptime_seconds)
    deletion_age = datetime.datetime.now() - deletion_date - (datetime.datetime.now() - system_uptime)

    if deletion_age < datetime.timedelta(hours=7):
        deleted_dll_files.append({"file_name": file_name, "deletion_date": deletion_date})

if deleted_dll_files:
    cheating_found = True
    for file in deleted_dll_files:
        jarClicker_ininstance = True

directory = "C:\\"
dll_files = glob.glob(os.path.join(directory, '**', '*.dll'), recursive=True)
for file_path in dll_files:
    if "JNat" in file_path:
        created_time = os.path.getctime(file_path)
        created_time_str = datetime.datetime.fromtimestamp(created_time).strftime("%Y-%m-%d %H:%M:%S")
        for jar_filename in os.listdir(os.path.dirname(file_path)):
            if jar_filename.endswith(".jar") and jar_filename != os.path.basename(file_path.replace(".dll", ".jar")):
                with zipfile.ZipFile(os.path.join(os.path.dirname(file_path), jar_filename), 'r') as jar_file:
                    for jar_member in jar_file.infolist():
                        if not jar_member.is_dir() and jar_member.filename.endswith(".class"):
                            class_content = jar_file.read(jar_member.filename).decode(errors='ignore')
                            if any(jar_string in class_content for jar_string in jar_strings):
                                cheating_found = True

# Forge Mods Check
user_name = os.getlogin()
folder_path = os.path.join("C:/Users", user_name, "AppData/Roaming/.minecraft/mods")
print("")
print(yellow + "Running mods check...")
for file_name in os.listdir(folder_path):
    if file_name.endswith(".jar"):
        file_path = os.path.join(folder_path, file_name)
        with zipfile.ZipFile(file_path, "r") as jar_file:
            for zip_info in jar_file.infolist():
                if zip_info.filename.endswith(".class"):
                    with io.TextIOWrapper(jar_file.open(zip_info, "r"), errors="ignore") as class_file:
                        class_contents = class_file.read()
                        if any(mod_string in class_contents for mod_string in mods_strings):
                            mod_found = True
                            
# Recording Check
print("")
print(yellow + "Running recording check...")
Recording_found = any(proc.info['name'] in recording_softwares for proc in psutil.process_iter(['pid', 'name']))

# Service Check
print("")
print(yellow + "Running service check...")
services = ["dps", "sysmain"]
for service in services:
        cmd = f"sc query {service}"
output = os.popen(cmd).read()
if "STATE" in output and "RUNNING" not in output:
    service_disabled = True

# Final Section / DashBoard
os.system("cls")

result_text = ""
if jarClicker_ininstance:
    result_text += "• Java clicker in instance\n"
elif cheating_found:
    result_text += "• Java clicker out of instance\n"
if mod_found:
    result_text += "• Forge Cheat Mod \n"
if service_disabled:
    result_text += "• Disabled services\n"
if Recording_found:
    result_text += "• Recording Software in instance \n"
    result_text += "Alts: \n"

# Write result to a text file
result_filename = "result.txt"
with open(result_filename, "w") as file:
    file.write(result_text)

# Open the result file
subprocess.run(["start", result_filename], shell=True)

input(yellow + "Press Enter to exit")

# made by lrxh#0001

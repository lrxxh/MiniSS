import subprocess
import datetime
import os
import zipfile
import io
import psutil
import subprocess
from termcolor import colored


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




# Strings
command = 'fsutil usn readjournal C: csv | findstr /i /c:.dll | findstr /i /c:0x80000200 | findstr /i /c:JNat'

# Strings for jar Clickers
jar_strings = ["Clicker", "AutoClicker", "Auto Refill", "Left Clicker", "Right Clicker", "7Clicker", "com.github.kwhat.jnativehook", "org.jnativehook"]

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
    output = subprocess.check_output(command, shell=True)
except subprocess.CalledProcessError as e:
    output = b""

deleted_dll_files = []
for line in output.decode().splitlines():
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
    print(red + "Deleted DLL files.")
    for file in deleted_dll_files:
        print(yellow + f"{file['file_name']} (deleted {file['deletion_date']} ago)")
        jarClicker_ininstance = True
else:
    print(red + "No deleted DLL.")
directory = "C:\\"
for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith(".dll") and "JNat" in filename:
            created_time = os.path.getctime(os.path.join(root, filename))
            created_time_str = datetime.datetime.fromtimestamp(created_time).strftime("%Y-%m-%d %H:%M:%S")
            print(yellow + os.path.join(root, filename) + "-" + created_time_str)
            for jar_filename in os.listdir(root):
                if jar_filename.endswith(".jar") and jar_filename != filename.replace(".dll", ".jar"):
                    with zipfile.ZipFile(os.path.join(root, jar_filename), 'r') as jar_file:
                            for jar_member in jar_file.infolist():
                                if not jar_member.is_dir() and jar_member.filename.endswith(".class"):
                                    class_content = jar_file.read(jar_member.filename).decode(errors='ignore')
                                    for jar_string in jar_strings:
                                        if jar_string in class_content:
                                            print(yellow + "  Found {} in {} in {}".format(jar_string, jar_member.filename, os.path.join(root, jar_filename)))
                                            cheating_found = True
                                            
# Forge Mods Check
mods_strings = ["SelfDestruct", "Senura"]
user_name = os.getlogin()
folder_path = os.path.join("C:/Users", user_name, "AppData/Roaming/.minecraft/mods")

for file_name in os.listdir(folder_path):
    if file_name.endswith(".jar"):
        file_path = os.path.join(folder_path, file_name)
        with zipfile.ZipFile(file_path, "r") as jar_file:
            for zip_info in jar_file.infolist():
                if zip_info.filename.endswith(".class"):
                    with io.TextIOWrapper(jar_file.open(zip_info, "r"), errors="ignore") as class_file:
                        class_contents = class_file.read()
                        for mod_string in mods_strings:
                            if mod_string in class_contents:
                                print(f"{file_name} contains {mod_string}")
                                mod_found = True    
                                
# Recording Check      
Recording_found = False
for proc in psutil.process_iter(['pid', 'name']):
    if proc.info['name'] in recording_softwares:
        print(colored(f"{recording_softwares[proc.info['name']]} is running (PID: {proc.info['pid']})", "yellow"))
        Recording_found = True


# Service Check
services = ["dps", "sysmain"]

for service in services:
    cmd = f"sc query {service}"
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)


    if "STATE" in output and "RUNNING" not in output:
        print(f"Service {service} is disabled")
        service_disabled = True   

# Final Print
os.system("cls")

if jarClicker_ininstance:
    print(red + "          -|           Java clicker in instance                    |-")
elif cheating_found:
    print(red + "          -|           Java clicker out of instance                |-")
if mod_found:
    print(red + "          -|           Forge Cheat Mod                                 |-")
if service_disabled:
    print(red + "          -|           Disabled services                               |-")
if Recording_found:
    print(red + "          -|           Recording Software in instance                  |-")  

input(yellow + "Press Enter to continue")
# made by lrxh#0001
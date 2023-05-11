import subprocess
import datetime
import os
import zipfile
import io
import psutil
import subprocess

# Print CF
magenta = '\033[35m'
blue = '\033[34m'
red = '\033[31m'
yellow = '\033[33m'

text = [
    '██████╗███████╗',
    '██╔═══╝██╔════╝',
    '██║    █████╗',
    '██║    ██╔══╝',
    '██████╗██║',
    '╚═════╝╚═╝',
    'Clicker Fucker.'
]

gradient_length = len(text)
for i, line in enumerate(text):
    r = i / (gradient_length - 1)
    red_value = int(255 * (1 - r))
    green_value = 0
    blue_value = int(255 * r)
    color = f'\033[38;2;{red_value};{green_value};{blue_value}m'
    print(color + line)

# JNative deletion check
command = 'fsutil usn readjournal C: csv | findstr /i /c:.dll | findstr /i /c:0x80000200 | findstr /i /c:JNat'

# Execute the command and retrieve the output
try:
    output = subprocess.check_output(command, shell=True)
except subprocess.CalledProcessError as e:
    output = b""

# Print if any deleted .dll were found
deleted_dll_files = []
for line in output.decode().splitlines():
    fields = line.split(",")
    file_name = fields[1].strip('"')
    deletion_date_str = fields[5].strip('"')
    deletion_date = datetime.datetime.strptime(deletion_date_str, "%d/%m/%Y %H:%M:%S")

    # get system uptime
    uptime_seconds = psutil.boot_time()
    system_uptime = datetime.datetime.fromtimestamp(uptime_seconds)
    deletion_age = datetime.datetime.now() - deletion_date - (datetime.datetime.now() - system_uptime)

    # Check if the DLL file was deleted less than 7 hours ago
    if deletion_age < datetime.timedelta(hours=7):
        deleted_dll_files.append({"file_name": file_name, "deletion_date": deletion_date})

# Print all of deleted DLL files
if deleted_dll_files:
    cheating_found = True
    print(red + "Deleted DLL files.")
    for file in deleted_dll_files:
        print(yellow + f"{file['file_name']} (deleted {file['deletion_date']} ago)")
else:
    print(red + "No deleted DLL.")

directory = "C:\\"

# Strings
jar_strings = ["Clicker", "AutoClicker", "Auto Refill", "Left Clicker", "Right Clicker", "7Clicker", "com.github.kwhat.jnativehook", "org.jnativehook"]

# Cheat boolean
cheating_found = False

# mod boolean
mod_found = False

# service boolean
service_disabled = False

# Check for .dll files with "JNat" in their name
for root, dirs, files in os.walk(directory):
    for filename in files:
        # Check if the file is a .dll and contains "JNat" in the filename
        if filename.endswith(".dll") and "JNat" in filename:
            # Get the file's creation time as a Unix timestamp
            created_time = os.path.getctime(os.path.join(root, filename))
            # Convert the Unix timestamp to a human-readable string
            created_time_str = datetime.datetime.fromtimestamp(created_time).strftime("%Y-%m-%d %H:%M:%S")
            # Print the filename and creation time, separated by a yellow hyphen
            print(yellow + os.path.join(root, filename) + "-" + created_time_str)
            # Check if there are any .jar files in the same directory
            for jar_filename in os.listdir(root):
                if jar_filename.endswith(".jar") and jar_filename != filename.replace(".dll", ".jar"):
                    # Open the jar file and search for the strings
                    with zipfile.ZipFile(os.path.join(root, jar_filename), 'r') as jar_file:
                            for jar_member in jar_file.infolist():
                                if not jar_member.is_dir() and jar_member.filename.endswith(".class"):
                                    class_content = jar_file.read(jar_member.filename).decode(errors='ignore')
                                    for jar_string in jar_strings:
                                        if jar_string in class_content:
                                            # Print the directory of the jar file
                                            print(yellow + "  Found {} in {} in {}".format(jar_string, jar_member.filename, os.path.join(root, jar_filename)))
                                            cheating_found = True
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

# Define the services to check
services = ["dps", "sysmain"]

# Service Check
for service in services:
    cmd = f"sc query {service}"
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)

    # Check if the service is running
    if "STATE" in output and "RUNNING" not in output:
        print(f"Service {service} is disabled")
        service_disabled = True   



if cheating_found:
    print(red + "          -|           Player might be using a java autoclicker.          |-")
    
if mod_found:
    print(red + "          -|           Player is using a cheat forge mod.           |-")

if service_disabled:
    print(red + "          -|           Player has disabled services.           |-")

os.system("pause")

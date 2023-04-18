#! python3
#! /usr/bin/env python3

import os
import sys
import time
import json
import shutil
import requests
import subprocess

import tkinter as tk

plat = sys.platform
if not plat.startswith("win") and not plat.startswith("linux"):
    print("Unsupported operating system.")
    sys.exit(1)

# Get the user's screen ratio.
screen_ratios = {
    1.25: "5x4",
    1.33: "4x3",
    1.6: "16x10",
    1.78: "16x9",
    2.33: "21x9",
    3.56: "32x9",
    5.33: "48x9",
}
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
screen_ratio_decimal = round(screen_width / screen_height, 2)
screen_ratio = screen_ratios[screen_ratio_decimal]
root.destroy()

# Download webpage result data.
url = (
    "https://wallhaven.cc/api/v1/search?categories=111&purity=100&ratios="
    + screen_ratio
    + "&sorting=random&order=desc"
)
result = requests.get(url)
result.raise_for_status()


def name_the_file(wallpaper):
    file_type = wallpaper["file_type"].split("/")[1]
    favs = str(wallpaper["favorites"])
    views = str(wallpaper["views"])
    id = wallpaper["id"]
    wall_name = favs + "-" + views + "-" + id + "." + file_type
    return wall_name


# Find the wallpaper links and download them.
print('Downloading images...')
home_directory = os.path.expanduser("~")
destination = os.path.join(home_directory, "Pictures", "Temp_Wallhaven")
try:
    os.makedirs(destination)
except OSError:
    pass
wallpapers_path = destination
wall_json = json.loads(result.text)
progress_bar = 0
# Hide cursor in output.
print('\033[?25l', end="")
for wallpaper in wall_json["data"]:
    progress_bar += 4
    print(f'\r{progress_bar}%', end='')
    wall_name = name_the_file(wallpaper)
    img = requests.get(wallpaper["path"])
    with open(os.path.join(destination, wall_name), "wb") as img_file:
        for chunk in img.iter_content(100000):
            img_file.write(chunk)
print('\r100%')
# Show cursor.
print('\033[?25l', end="")

def open_file_explorer():
    if plat.startswith("win"):
        os.startfile(destination)
    if plat.startswith("linux"):
        subprocess.run(["xdg-open", destination])

# Create and open the temp_wallhaven folder for user to select the desired image.
print("Please select your fav among them.")
time.sleep(2)
print("Then, click and drag the image file to this window.")
time.sleep(3)
print("Opening images folder...")
open_file_explorer()

while True:
    fav_image = input('Click and drag the image file here: ')
    if not os.path.exists(fav_image):
        print('Invalid file path. Try again')
    break

# Send the image to the Wallhaven folder.
target = os.path.join(home_directory, "Pictures", "Wallhaven")
try:
    os.makedirs(target)
except OSError:
    pass

move_output = shutil.mv(destination, target)

print('Moved \033[35m' + os.path.basename(fav_image) + '\033[39m to \033[33m' + move_output + '\033[39m.')
print('Done!')
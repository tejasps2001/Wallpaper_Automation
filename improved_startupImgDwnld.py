#! python3
#! /usr/bin/env python3

import os
import time
import json
import requests

import tkinter as tk

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
home_directory = os.path.expanduser("~")
destination = os.path.join(home_directory, "Pictures", "Wallhaven")
try:
    os.makedirs(destination)
except OSError:
    pass
wallpapers_path = destination
wall_json = json.loads(result.text)
for wallpaper in wall_json["data"]:
    wall_name = name_the_file(wallpaper)
    img = requests.get(wallpaper["path"])
    with open(wall_name, "wb") as img_file:
        for chunk in img.iter_content(100000):
            img_file.write(chunk)

# Open the wallhaven folder for user to select the desired image.
print('Please select your fav among them.')
time.sleep(2)
print('Then, click and drag the image file to this window.')
time.sleep(3)
print("Opening images folder")

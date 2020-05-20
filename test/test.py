# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 21:26:00 2020

@author: thomp
"""

import requests
import tweepy
from PIL import Image, ImageFont, ImageDraw

# Twitter API config

# These are where the keys would go.

# Create API object
#api = tweepy.API(auth)

# Create a tweet
# api.update_status("Automated test.")

# Fetching navigation warnings

links = ["https://msi.nga.mil/api/publications/download?type=view&key=16694640/SFH00000/DailyMemIV.txt",
         "https://msi.nga.mil/api/publications/download?type=view&key=16694640/SFH00000/DailyMemLAN.txt",
         "https://msi.nga.mil/api/publications/download?type=view&key=16694640/SFH00000/DailyMemARC.txt",
         "https://msi.nga.mil/api/publications/download?type=view&key=16694640/SFH00000/DailyMemXII.txt",
         "https://msi.nga.mil/api/publications/download?type=view&key=16694640/SFH00000/DailyMemPAC.txt"]

post_msg = []
for link in links:
    r = requests.get(link)
    
    full_text = r.text
    separated_text = full_text.split("//")
    
    # Note: This works for testing on Windows, but DOES NOT work on Linux
    # due to the line endings.
    separated_text[0] = "\n".join(separated_text[0].split('\n')[14:])
    
    for msg in separated_text:
        if "SPACE" in msg or "MISSILE" in msg or "ROCKET" in msg:
            post_msg.append(msg)


with open("Previous.txt", "r") as file:
    previous_reports = file.readlines()

formatted_msg = []
# Formatting for posting
for i, messages in enumerate(post_msg):
    formatted_msg.append(messages.strip())
    
    # Checking which warnings are new
    message_name = formatted_msg[i].split('.')[0].split('(')[0]
    if (message_name + "\n") not in previous_reports:
        num_lines = formatted_msg[i].count("\n")
        
        image = Image.new("RGBA", (500,num_lines*20), (255,255,255))
        d_usr = ImageDraw.Draw(image)
        d_usr = d_usr.text((10,10), formatted_msg[i],(0,0,0))
        image.save("Warning.PNG", "PNG")
        
        with open("Previous.txt", "a") as file:
            file.writelines((message_name + "\n"))
            
        # Posting
        #mid = api.media_upload("Warning.PNG")
        #api.update_status(message_name, media_ids=[mid.media_id_string])
        
        print(("Posted" + message_name + "\n"))
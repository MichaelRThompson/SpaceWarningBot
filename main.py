import os
import requests
import tweepy
from PIL import Image, ImageFont, ImageDraw
from google.cloud import storage

# Twitter API config

auth = tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret'])
auth.set_access_token(os.environ['access_key'], os.environ['access_secret'])

# Download .txt file of previously posted warnings
client = storage.Client()
bucket = client.get_bucket('previously_posted_warnings')
blob = bucket.get_blob('Previous.txt')
blob.download_to_filename('/tmp/Previous.txt')

def post_warnings(dummy):
    
    # Create API object
    api = tweepy.API(auth)

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
        
        for msg in separated_text:
            if "SPACE" in msg or "MISSILE" in msg or "ROCKET" in msg:
                post_msg.append(msg)
    
    
    with open("/tmp/Previous.txt", "r") as file:
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
            image.save("/tmp/Warning.PNG", "PNG")
            
            with open("/tmp/Previous.txt", "a") as file:
                file.writelines((message_name + "\n"))
                
            # Posting
            mid = api.media_upload("/tmp/Warning.PNG")
            api.update_status(message_name, media_ids=[mid.media_id_string])
            
            print(("Posted" + message_name + "\n"))
    
    # Reupload
    blob = bucket.blob("Previous.txt")
    blob.upload_from_filename("/tmp/Previous.txt")
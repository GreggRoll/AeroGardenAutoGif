import time
import datetime
import os
import imageio
import tweepy 

from picamera import PiCamera
from secret import consumer_key, consumer_secret, access_token, access_token_secret

#lights turn on at 0600
#take image at 0700
#wait until 2200
#take image
#Compile Gif
#tweet gif
#wait until 

#take image 2x a day 1 at begginning of cycle, 1 at end
#save image as cycle_num_A/B.PNG
#every 7 cycles compile ALL images into a gif
#tweet the gif to my twitter

camera = PiCamera()
camera.resolution = (256, 256)

#runs for a whole year
for day in range(365):
    #start at 0600
    #wait 1 hour
    time.sleep(3600)
    #current time 0700
    #add current days images to folder
    for cycle in ['A', 'B']:
        camera.start_preview()
        #set for consistant pictures
        camera.iso = 100
        time.sleep(2)
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        #sleep till camera focused
        time.sleep(8)
        camera.capture(f'/home/pi/Desktop/AeroGarden/images/{day}_{cycle}_{datetime.datetime.now().time()}.jpg')
        camera.stop_preview()
        #wait 15hrs
        time.sleep(53990)
        #current time 2200
    
    #average code run length 2.34 seconds over 10 tests 
    #compile all images into a gif
    file_names = []
    for r, d, f in os.walk('images'):
        for item in f:
            file_names.append(item)
    #sort to put them in order for gif            
    file_names.sort()
    #reading images into list
    images = []
    for file in file_names:
        images.append(imageio.imread('images/'+file))
    #render gif and save
    imageio.mimwrite('movie.gif', images, fps=6)

    #tweet gif to twitter
    # authentication of consumer key and secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # authentication of access token and secret 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth) 
    
    today = datetime.date.today().strftime("%B %d %Y")
    tweet = f"""TEST: My #AeroGarden progress from September 08 2020 until {today}"""
    
    tweet = api.update_with_media(filename = '/home/pi/Desktop/AeroGarden/movie.gif', status = tweet)
    #wait 6 hrs - the 2.34 seconds the code takes
    time.sleep(21597.66)
    
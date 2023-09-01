#!/usr/bin/env python3

import pygame
import requests
from os.path import exists

url = "http://benchung.dev:8001"
sound_path = "sounds/waa.mp3"

pods_endpoint = "/api/v1/namespaces/default/pods"

def get_api_response():
    r = requests.get(url + pods_endpoint).json()
    return r['items'][0]['status']['containerStatuses']

def check_failed():
    ret = False
    for image in get_api_response():
        if not image['state'].get('running'):
            ret = True
    return ret

def play_sound():
    pygame.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()

if __name__ == "__main__":
    print("""
      _____________________________
     | ___________________________ |
     | |                         | |
     | |                         | |
     | |                         | |
     | |_________________________| |
     |_____________________________|

    Kubernetes horn, a HPE Innovation
    """)

    try:
        print("Attempting to find a kubernetes proxy on given url... ", end="")
        api_exists = requests.get(url).json().get('paths')
        print("Done!")
    except:
        print("\nERROR : Could not find kubernetes api running on given domain! Try modifying config.yaml")
        exit(1)


    # Check sound file exists
    if not exists(sound_path):
        print(f"Could not find sound file at path {sound_path}! Try modifying config.yaml")


    while True:
        if check_failed():
            play_sound()

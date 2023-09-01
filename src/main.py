#!/usr/bin/env python3

import pygame
import requests
from os.path import exists
import yaml
from time import sleep

url = ""
sound_path = ""
wait_time = 0

pods_endpoint = "/api/v1/namespaces/default/pods"

def get_api_response():
    r = requests.get(url + pods_endpoint).json()
    return r['items'][0]['status']['containerStatuses']

def check_failed():
    ret = False
    for image in get_api_response():
        if not image['state'].get('running'):
            ret = True
    if ret:
        sleep(wait_time)
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
     | |_________________________| |
     |_____________________________|

    Kubernetes horn, a HPE Innovation
    """)

    with open("config.yaml", "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

    # Lift variables from the yaml file
    url = data.get("url")
    sound_path = data.get("sound_path")
    wait_time = int(data.get("check_again_time"))

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

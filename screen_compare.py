from datetime import datetime
from pathlib import Path
import cv2
import mss
import numpy as np
import pyautogui
import pygetwindow
import os

def find_images(base_image, other_images):
    # Load the base image
    base = cv2.imread(base_image)
    found_cards = []

    # Loop through each image in the array
    for image in other_images:
        # Load the image
        img = cv2.imread(image)

        # Convert the images to grayscale
        base_gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Get the dimensions of the image
        h, w = img_gray.shape

        for i in range (36, 44):
            scale = i * 0.02
            resized_img = cv2.resize(img_gray, (int(w*scale), int(h*scale)))

            # Perform template matching
            result = cv2.matchTemplate(base_gray, resized_img, cv2.TM_CCOEFF_NORMED)
            # Set a threshold for the match
            threshold = 0.8

            # Get the locations where the match exceeds the threshold
            locations = np.where(result >= threshold)

            # If any match is found, print the coordinates
            if len(locations[0]) > 0:
                print (f'Found {os.path.basename(os.path.splitext(image)[0])}')
                found_cards.append(os.path.basename(os.path.splitext(image)[0]))
                break

    return found_cards

def get_monitor_screenshot(monitor_number):
    with mss.mss() as sct:
        # Get information of monitor
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top": mon["top"] + 175,
            "left": mon["left"] + 250,
            "width": 1000,
            "height": 800,
            "mon": monitor_number,
        }
        output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)
        img = np.array(sct.grab(monitor)) # BGR Image
        
        Path("data\\current_draft").mkdir(exist_ok=True)
        path = 'data\\current_draft\\current_screen.png'
        cv2.imwrite(path, img)


def find_cards(set_name, card_list=None):
    print(datetime.now())

    base_image = 'data/current_draft/current_screen.png'
    get_monitor_screenshot(2)

    path_list = []
    if card_list == None:
        search_list = os.listdir(f'data/{set_name}/cards')
    else:
        search_list = list(map(lambda c: f'{c}.png', card_list))

    for card in search_list:
        path_list.append(f"data/{set_name}/cards/{card}")
    cards_in_pack = find_images(base_image, path_list)
    print(len(cards_in_pack))
    print(cards_in_pack)

    print(datetime.now())

    return cards_in_pack

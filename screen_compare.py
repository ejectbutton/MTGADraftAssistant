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

        scale = 0.38
        resized_img = cv2.resize(img_gray, (int(w*scale), int(h*scale)))

        # Perform template matching
        result = cv2.matchTemplate(base_gray, resized_img, cv2.TM_CCOEFF_NORMED)
        # Set a threshold for the match
        threshold = 0.8

        # Get the locations where the match exceeds the threshold
        locations = np.where(result >= threshold)

        # If any match is found, print the coordinates
        if len(locations[0]) > 0:
            found_cards.append(os.path.basename(os.path.splitext(image)[0]))

    return found_cards

def get_monitor_screenshot(monitor_number):
    with mss.mss() as sct:
        # Get information of monitor
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }
        output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)
        img = np.array(sct.grab(monitor)) # BGR Image
        
        Path("data\\current_draft").mkdir(exist_ok=True)
        path = 'data\\current_draft\\current_screen.png'
        cv2.imwrite(path, img)

print(datetime.now())

window_title = "MTGA"
base_image = 'data/current_draft/current_screen.png'
get_monitor_screenshot(2)

other_images = []
for card in os.listdir('data/OTJ/cards'):
    other_images.append(f"data/OTJ/cards/{card}")
cards_in_pack = find_images(base_image, other_images)
print(len(cards_in_pack))
print(cards_in_pack)

print(datetime.now())

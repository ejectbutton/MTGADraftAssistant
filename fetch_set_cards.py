import requests
import urllib.request
import time
from pathlib import Path
from PIL import Image
from unidecode import unidecode

scryfall_endpoint = 'https://api.scryfall.com/cards/search'

def crop_image(image_path, x, y, width, height):
    # Open the image
    image = Image.open(image_path)

    # Crop the image
    cropped_image = image.crop((x, y, x + width, y + height))

    # Overwrite the original image with the cropped image
    cropped_image.save(image_path)

def get_cards(sets, x=None, y=None, width=None, height=None):
    set_name = sets.split(',')[0]
    for i in range(1,6): # each page can have up to 175 cards. No draft set is expected to exceed 1k cards
        response = requests.get(f"{scryfall_endpoint}?q=e:{sets}&page={i}")
        if response.status_code != 200:
            return
        response_data = response.json()
        Path(f"data\\{set_name}\\cards").mkdir(exist_ok=True)
        for card in response_data['data']:
            name = unidecode(card['name'].split('/')[0].strip())
            if 'card_faces' in card and 'image_uris' not in card:
                card = card['card_faces'][0]
            uri = card['image_uris']['normal']
            urllib.request.urlretrieve(uri, f"data\\{set_name}\\cards\\{name}.png")
            if width != None and height != None:
                crop_image(f"data\\{set_name}\\cards\\{name}.png", x, y, width, height)
    time.sleep(2)



#set = 'OTJ'
#query = 'OTJ,OTP,BIG'

# Whole Card
#get_cards('OTJ,BIG')
#get_cards('OTP')

# Just Art
#get_cards('OTJ,BIG', 40, 79, 407, 296)
#get_cards('OTP', 27, 117, 434, 272)

get_cards('MH3', 95, 100, 250, 250)

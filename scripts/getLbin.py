import requests
import json
import os
import csv
from datetime import datetime
from main.models import Skin, Item
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SkinTracker.settings')
django.setup()

def getLbin(item_name):
    url = f"https://sky.coflnet.com/api/auctions/tag/{item_name}/active/bin"
    response = requests.get(url)
    prices = []
    if response.status_code == 200:
        data = response.json()
        starting_bids = [item['startingBid'] for item in data if item['startingBid'] >= 1000000]
        if starting_bids:
            return min(starting_bids)
        else:
            print(f"No sales for {item_name}")
            return 0
    else:
        print(f"Failed to fetch data:{response.status_code} for {item_name}")
        return 0

def getMapping():
    file_path = 'C:\\dev\\SkinTracker\\main\\utils\\cofl_mapping'
    mappings = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                # Ignore empty lines and strip the newline characters
                if line.strip():
                    old_name, new_name = line.strip().split(':')
                    mappings[old_name] = new_name
    return mappings
def getTranslateName(old_name, mappings):
    return mappings.get(old_name, old_name)

def updateLbin(skin, mappings):
    try:
        translated_name = getTranslateName(skin.name,mappings)
        new_lbin = getLbin(translated_name)
        if new_lbin != 0:
            skin.lbin = new_lbin
            skin.save()
            print(f"Updated {skin.name} with lbin: {skin.lbin}")
    except Exception as e:
        print(f"{e} for skin {skin.name}")

def add_mapping_to_file():
    file_path = 'C:\\dev\\SkinTracker\\main\\utils\\cofl_mapping'
    old_names = badskin()
    # Check if the mapping already exists
    mappings = getMapping()
    for old_name in old_names:
        if old_name in mappings:
            print(f"Mapping for {old_name} already exists.")
        else:
            new_name = input(f"{old_name} -> :").strip()
            mappings[old_name] = new_name
            with open(file_path, 'a') as f:
                f.write(f"{old_name}:{new_name}\n")
            print(f"Added new mapping: {old_name} -> {new_name}")

def badskin():
    file_path = f"C:\\Users\\Alix Hiscock\\Documents\\Useful\\badskins.txt"
    names = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # Ignore empty lines and strip the newline characters
            if line.strip():
                names.append(line.strip())
    return names

def updateLbinAll():
    skins = Skin.objects.all()
    mappings = getMapping()
    for skin in skins:
        try:
            updateLbin(skin, mappings)
        except Exception as e:
            print(f"Failed to fetch skin {skin.name}: {e}")
#updateLbin(Skin.objects.get(name="cosmic_blue_whale"))
updateLbinAll()

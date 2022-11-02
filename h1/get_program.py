#!/usr/bin/env /ptv/healer/bbplats/h1/.venv/bin/python3

import os, sys, time, json, requests, argparse, yaml, asyncio, time, jdatetime, datetime, pytz

# Get current time and save it to a variable called start_time in unix format
start_time = time.time()

# Read the file /ptv/healer/creds.yaml and parse as yaml
with open("/ptv/healer/creds.yaml", 'r') as stream:
    try:
        creds = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:
        print(exc)

creds = creds['healer']['bbplats']['h1']
# Select the element h1username and h1token from the yaml file
h1username = creds['h1username']
h1token = creds['h1token']

def get_program(h1username, h1token, handle):
    # Create a requests object 
    r = requests.get(f"https://api.hackerone.com/v1/hackers/programs/{handle}", auth=(h1username, h1token), headers = {'Accept': 'application/vnd.api+json'})
    return r

# read file h1_tgts_new.json and parse as json
with open('/ptv/healer/bbplats/h1/h1_tgts_new.json', 'r') as f:
    h1_tgts = json.load(f)


# Iterate through the json file and get the handle for each program and add it to the list h1_tgts_new_handles
h1_tgts_new_handles = []
tgt_counter = 0
for i in h1_tgts:
    try:
        this_handle = i['attributes']['handle']
        # print(f"Getting program {this_handle}")
        h1_tgts_new_handles.append(this_handle)
        tgt_counter += 1
    except:
        pass
print(f"Total targets: {tgt_counter}")

# Iterate through the list h1_tgts_new_handles and get the program details for each handle
h1_tgts_new_full = []
for i in h1_tgts_new_handles:
    # Print the progress (e.g. Fetching Programs Full data : 14/615), edit the line not printing a new line if i's index mod 10 is 0
    if h1_tgts_new_handles.index(i) % 10 == 0 or h1_tgts_new_handles.index(i) == len(h1_tgts_new_handles):
        print(f"Fetching Programs Full data : {h1_tgts_new_handles.index(i)}/{len(h1_tgts_new_handles)}", end="\r")
    getting_pro = get_program(h1username, h1token, i)
    # Append the json response to the list h1_tgts_new_full
    h1_tgts_new_full.append(getting_pro.json())


# Write the list h1_tgts_new_full to the file h1_tgts_new_full.json
with open('/ptv/healer/bbplats/h1/h1_tgts_new_full.json', 'w') as f:
    json.dump(h1_tgts_new_full, f)

# Get current time and save it to a variable called end_time in unix format
end_time = time.time()
print(f"Done fetching programs in {end_time - start_time} seconds")
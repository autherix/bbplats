#!/usr/bin/env python3

import os, sys, requests, json, yaml

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

# Run a notifio_sender script to send a notification to the discord.debug channel, saying that the script has started
# os.popen("notifio_sender --title 'Job started' --discord.debug \"Started the get_programs.py script\" > /dev/null 2>&1")
# os.popen("notifio_sender --discord.debug 'HackerOne: Started getting programs' > /dev/null 2>&1")

def get_h1_tgts(h1username,h1token,page_num, page_size=100):
    # Send a request to the API server: https://api.hackerone.com/v1/ with GET method and Header -H Accept: application/json
    # With parameters: page[number]=page_num&page[size]=page_size
    # The request is a GET request to the /hackers/programs endpoint
    # The request is authenticated with the username and token
    # The response is stored in the variable r
    r = requests.get('https://api.hackerone.com/v1/hackers/programs', auth=(h1username, h1token), headers={'Accept': 'application/json'}, params={'page[number]': page_num, 'page[size]': page_size})
    # Return the response
    return r

# Define an empty list called tgts_info
tgts_info = []
page_num = 1
# Parse the response as json, and select the element data, which is a list of dictionaries, and save it in the variable data
r = get_h1_tgts(h1username,h1token,page_num)
data = r.json()['data']

while data:
    # append the data to the tgts_info list
    tgts_info.extend(data)
    print(f"Page {page_num} has {len(data)} targets")
    # increment the page_num by 1
    page_num += 1
    # get the next page of data
    r = get_h1_tgts(h1username,h1token,page_num)
    data = r.json()['data']

# Export the list of dictionaries as a json file
with open('h1_tgts_new.json', 'w') as f:
    json.dump(tgts_info, f, indent=4)

print("All the data has been retrieved")
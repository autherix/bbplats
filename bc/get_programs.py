#!/usr/bin/env python3

import os, requests, sys, time, json, yaml, argparse, jdatetime, datetime, html
from bs4 import BeautifulSoup

pagenum = 1
base_url = f"https://bugcrowd.com/programs.json?page[]={pagenum}"

# Make a request to the page and parse the response as json
r = requests.get(base_url, headers={
    'authority': 'bugcrowd.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'cache-control': 'max-age=0',
    'if-none-match': 'W/"32bf0159f4f70b1597121a10d503e25f"',
    'referer': 'https://bugcrowd.com/programs?sort[]=promoted-desc',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
})

# Define an empty list to store the programs urls
programs = r.json()['programs']
programs_urls = []
# Select the element programs and iterate over it
for program in programs:
    if program['program_url']:
        programs_urls.append(program['program_url'])

# Parse the response as json
data = r.json()

# Get the total number of pages
total_pages = data['meta']['totalPages']

# Get the total number of programs
total_programs = data['meta']['totalHits']

while pagenum <= total_pages:
    # Print with \r to overwrite the previous line, saying that we are on page X
    print(f"Getting page {pagenum} of {total_pages}...", end="\r")
    # Increment the page number
    pagenum += 1
    # Get the total number of pages
    total_pages = data['meta']['totalPages']
    # Update the url with the current page number
    base_url = f"https://bugcrowd.com/programs.json?page[]={pagenum}"
    # Make a request to the page and parse the response as json
    r = requests.get(base_url, headers={
        'authority': 'bugcrowd.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"32bf0159f4f70b1597121a10d503e25f"',
        'referer': 'https://bugcrowd.com/programs?sort[]=promoted-desc',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    })

    # Parse the response as json
    data = r.json()
    # Define an empty list to store the programs urls
    programs = r.json()['programs']
    # Select the element programs and iterate over it
    for program in programs:
        if program['program_url']:
            programs_urls.append(program['program_url'])

# Check if the number of programs is equal to total_programs
if len(programs_urls) == total_programs:
    print(f"[+] Successfully got {len(programs_urls)} programs urls.")
else:
    print(f"[!] Not all programs urls were fetched. {len(programs_urls)} out of {total_programs} were fetched.")

# if length of targets' urls is more than 0, write the programs urls to a file named programs_urls.json
if len(programs_urls) > 0:
    with open('/ptv/healer/bbplats/bc/programs_urls.json', 'w') as f:
        json.dump(programs_urls, f)

print(f"[+] Successfully wrote {len(programs_urls)} of the programs urls to programs_urls.json")
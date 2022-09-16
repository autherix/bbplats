#!/usrr/bin/env python3

import os, requests, sys, time, json, yaml, argparse, jdatetime, datetime, html
from bs4 import BeautifulSoup


# If there is a cookies.txt file, read it and parse as json
if os.path.isfile("/ptv/healer/bbplats/bc/cookies.txt"):
    with open("/ptv/healer/bbplats/bc/cookies.txt", 'r') as stream:
        try:
            cookies = json.load(stream)
            print("Cookies File Loaded")
        except json.JSONDecodeError as exc:
            cookies = None
            # Remove cookies file
            os.remove("/ptv/healer/bbplats/bc/cookies.txt")
else:
    cookies = None
# If cookies is defined:
if cookies:
    # Use the cookies and make a request to the page after updating the cookies
    session = requests.Session()
    session.cookies.update(cookies)
    # Now make a request to the page "https://bugcrowd.com/dashboard"
    r = session.get("https://bugcrowd.com/dashboard",allow_redirects=False ,headers={
        'authority': 'bugcrowd.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"32bf0159f4f70b1597121a10d503e25f"',
        'referer': 'https://bugcrowd.com/programs?sort[]=promoted-desc',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    })
    # Check if we're logged in, If we remained in the dashboard, we're logged in
    if r.status_code == 200:
        print("Logged in with cookies")
        logged_in = True
    else:
        logged_in = False
        cookies = None
        # Remove cookies file
        os.remove("/ptv/healer/bbplats/bc/cookies.txt")
        print("Cookies are invalid, trying to load credentials")
else: 
    logged_in = False
    print("No cookies, trying to load credentials")
if not logged_in:
    # Read the file /ptv/healer/creds.yaml and parse as yaml
    with open("/ptv/healer/creds.yaml", 'r') as stream:
        try:
            creds = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
    creds = creds['healer']['bbplats']['bugcrowd']
    # Select elements email and password 
    email = creds['email']
    password = creds['password']

    request_curl = """curl 'https://bugcrowd.com/user/sign_in' \
    -H 'authority: bugcrowd.com' \
    -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
    -H 'accept-language: en-US,en;q=0.9,fa;q=0.8' \
    -H 'cache-control: max-age=0' \
    -H 'cookie: _gcl_au=1.1.641430010.1663169277; _ga=GA1.1.1499110423.1663169279; _fbp=fb.1.1663169279550.1620145825; _ga_4J3ZM9L5RL=GS1.1.1663208603.2.1.1663209034.0.0.0; __cf_bm=VAXN3m3Wzca5m5mCKRpv8D0o.m7zhXh0hDxseNqd1DY-1663209598-0-AWirtbVJtyYVe3yU131oqL0rRGpKYtlB5uXF/124mWnR/3pVofdueFCFVu8dUZVTaDPzENo7XGqYbT+k4J7sxhQ=; _crowdcontrol_session=ZnFJSGZaMEJCZjV4RkZZajBPdHorRWR0TDBLZXVoQnY0STBaajVNYXJNUHMvQ0dNd1ZOZ0V1b0Q4aUVSdlhxWEl3VzA3ZzJ3NTNIckQxNkg5U1EyLzlseGxic0tDVEU5N09FRVhMVjF6VFUxTHRyUDFOUmZyQnBSVHZpejNnUXJpd2lCazZqUDRsTHVadjhicG5KcytnPT0tLWZ5Tk1aV2tONDMyV3hvWnFTK2hUcmc9PQ%3D%3D--16db5921d8536b806092a00a0b5ab1f95345ac3b' \
    -H 'if-none-match: W/"32bf0159f4f70b1597121a10d503e25f"' \
    -H 'referer: https://bugcrowd.com/programs?sort[]=promoted-desc' \
    -H 'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'sec-ch-ua-platform: "Windows"' \
    -H 'sec-fetch-dest: document' \
    -H 'sec-fetch-mode: navigate' \
    -H 'sec-fetch-site: same-origin' \
    -H 'sec-fetch-user: ?1' \
    -H 'upgrade-insecure-requests: 1' \
    -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' \
    --compressed"""

    # Create a session
    session = requests.Session()
    # rewrite the above request as a python request
    r = session.get('https://bugcrowd.com/user/sign_in', headers={
        'authority': 'bugcrowd.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"32bf0159f4f70b1597121a10d503e25f"',
        'referer': 'https://bugcrowd.com/programs?sort[]=promoted-desc',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    })

    # Get all the cookies from the response and save to variable called cookies
    cookies = r.cookies

    ## Get CSRF tokens from the response
    # Parse the response as html
    soup = BeautifulSoup(r.text, 'html.parser')
    # Find meta tag with name csrf-token
    csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})['content']
    # print(f"csrf_token: {csrf_token}")
    # Find meta tag with name csrf-param
    # csrf_param = soup.find('meta', attrs={'name': 'csrf-param'})['content']
    # print(f"csrf_param: {csrf_param}")

    # Find a div object with a property data-react-props, and get this property's value
    # data_react_props = soup.find('div', attrs={'data-react-props': True})['data-react-props']
    # html decode the value
    # data_react_props = html.unescape(data_react_props)
    # parse the value as json
    # data_react_props = json.loads(data_react_props)
    # Get the value of the key 'csrfToken'
    # csrf_token_react = data_react_props['csrfToken']
    # print the value
    # print(f"csrf_token_react: {csrf_token_react}")

    # Let's login
    login_curl = """curl 'https://bugcrowd.com/user/sign_in' \
    -H 'authority: bugcrowd.com' \
    -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
    -H 'accept-language: en-US,en;q=0.9,fa;q=0.8' \
    -H 'cache-control: max-age=0' \
    -H 'content-type: application/x-www-form-urlencoded' \
    -H 'cookie: __cf_bm=xxv_vAISFMZZkm36ritoPBrhN8ocq3XbdeC.6mDnhVM-1663216208-0-ATZHoLxVLrV8y6vkeS80cAjXZTYpfUYhaE3j1A4XToBQqKLs46HvDEPcwF10etjmHFRzc7nXrgEnbRBrgItVhw4=; _crowdcontrol_session=QmthTG4wREJ1dDJBNkdVQTZTUExIK0Z1KzFQZWZyZm5kWWg3WmdES0ZVY1gwNHJyekJQTDJ3SDlvOVdJemN6eU1uL2k0MldwM281dGZpQnhudlJvMHExYTI4OTdxZ1NSQ3JrSmNndTlHclpENHp1T3VZZm1SLzlKd0NOekk4UkdraW5UczJCV1prUTZFS2cvcXdkWGM2YzZyOFN3MThlUHlxVTYvc2Q0ZVIyU09SaE41OHg5T0p1d2FvOTFWZFRNTVd4aFlDRHE1STFtT2J1c1ZuZVNVbFRmNFZyRnVmS01GbkpSenNVQ081ST0tLXhCNnRUOUFQMW82ZCtNYld4RzlWRmc9PQ%3D%3D--a27b7a9bcbbf65bbf9de03417e115666575849e8' \
    -H 'origin: https://bugcrowd.com' \
    -H 'referer: https://bugcrowd.com/user/sign_in' \
    -H 'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'sec-ch-ua-platform: "Windows"' \
    -H 'sec-fetch-dest: document' \
    -H 'sec-fetch-mode: navigate' \
    -H 'sec-fetch-site: same-origin' \
    -H 'sec-fetch-user: ?1' \
    -H 'upgrade-insecure-requests: 1' \
    -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' \
    --data-raw 'utf8=%E2%9C%93&authenticity_token=IEDagdEbVyfktP95nizU38fXEhnJTU3Opn2tmYGlBqUXSbChuvO95zzUAwWeD0CyZPzkgjcqZ3U4SNjud08BoQ%3D%3D&user%5Bredirect_to%5D=&user%5Bemail%5D=test%40test.test&user%5Bpassword%5D=test&commit=Log+in' \
    --compressed"""

    # Rewrite the above curl command as a python request using the above session and cookies (update them if needed)
    r = session.post('https://bugcrowd.com/user/sign_in', data={
        'utf8': '✓',
        'authenticity_token': csrf_token,
        'user[redirect_to]': '',
        'user[email]': f"{email}",
        'user[password]': f"{password}",
        'commit': 'Log in'
    }, cookies=cookies)

    # Check if the login was successful, If the response text contains the string "Log in to Bugcrowd - Bugcrowd" then the login was failed, else if it contains the string "Dashboard - Bugcrowd" then the login was successful
    if "Log in to Bugcrowd - Bugcrowd" in r.text:
        print("Login failed")
        exit(1)
    else:
        logged_in = True
        print("Login with Credentials successful !\n")
        # Print current location
    # Save login cookies to a file, also session cookies
    with open('/ptv/healer/bbplats/bc/cookies.txt', 'w') as f:
        json.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
    print(f"Saved cookies to file: {f.name}")

# If still we're not logged in, exit with error code 1
if not logged_in:
    print("Login failed with both credentials and cookies")
    exit(1)


## Part 2: Get programs and their details
# Read the file /ptv/healer/bbplats/bc/targets_urls.json and parse it as json, if the file doesn't exist, print error message and exit 
try:
    with open('/ptv/healer/bbplats/bc/targets_urls.json', 'r') as f:
        targets_urls = json.load(f)
except FileNotFoundError:
    print("File targets_urls.json not found")
    exit(1)

# Define an empty list to store the programs details in
programs_details = []
base_url = "https://bugcrowd.com"
# Iterate over the targets_urls list 
for target_url in targets_urls:
    # Create a url for the program if the target_url is not empty or is not / 
    if target_url != "" and target_url != "/":
        url = f"{base_url}{target_url}"
    else:
        print(f"Skipping {target_url}")
        continue
    
    # Get the program details page using the url
    r = session.get(url, headers=[
        'authority': 'bugcrowd.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"32bf0159f4f70b1597121a10d503e25f"',
        'referer': 'https://bugcrowd.com/programs?sort[]=promoted-desc',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    ])

    # Parse the response text using BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')

    # Let's check whether its public or private program
    # Select <a class="bc-btn bc-btn--small" href="/namejet/submissions/new">Submit report</a>
    # If there is a <a> tag with class "bc-btn bc-btn--small" and text "Submit report" then it's a public program
    if soup.select_one('a.bc-btn.bc-btn--small:contains("Submit report")'):
        state = "public"
        print(f"Target: {url} is a Public Program")
    # <span class='bc-label bc-mb-0'>Public code</span>
    # IF there is a <span> tag with class 'bc-label bc-mb-0' and text "Public code" then it's a Private program
    elif soup.select_one('span.bc-label.bc-mb-0:contains("Public code")'):
        state = "private"
        print(f"Target: {url} is a Private Program")
        # <span class='bc-badge bc-badge--text bc-badge--success'>Joinable</span>
        # If there is a <span> tag with class 'bc-badge bc-badge--text bc-badge--success' and text "Joinable" then it's a Joinable program
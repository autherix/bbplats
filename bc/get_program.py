#!/usrr/bin/env python3

import os, requests, sys, time, json, yaml, argparse, jdatetime, datetime, html
from bs4 import BeautifulSoup

# Save start time of the program to var called start_time
start_time = time.time()

# If there is a cookies.txt file, read it and parse as json
if os.path.isfile("/ptv/healer/bbplats/bc/cookies.txt"):
    with open("/ptv/healer/bbplats/bc/cookies.txt", 'r') as stream:
        try:
            cookies = json.load(stream)
            print("[+] Cookies File Loaded")
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
        print("[+] Logged in with cookies")
        logged_in = True
    else:
        logged_in = False
        cookies = None
        # Remove cookies file
        os.remove("/ptv/healer/bbplats/bc/cookies.txt")
        print("[+] Cookies are invalid, trying to load credentials")
else: 
    logged_in = False
    print("[+] No cookies, trying to load credentials")
if not logged_in:
    # Read the file /ptv/healer/creds.yaml and parse as yaml
    with open("/ptv/healer/creds.yaml", 'r') as stream:
        try:
            creds = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
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
        print("[-] Login failed")
        exit(1)
    else:
        logged_in = True
        print("[+] Login with Credentials successful !\n")
        # Print current location
    # Save login cookies to a file, also session cookies
    with open('/ptv/healer/bbplats/bc/cookies.txt', 'w') as f:
        json.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
    print(f"[+] Saved cookies to file: {f.name}")

# If still we're not logged in, exit with error code 1
if not logged_in:
    print("[-] Login failed with both credentials and cookies")
    exit(1)

# Convert cookies to string for curl
cookies_str = ""
for cookie in session.cookies:
    cookies_str += f"{cookie.name}={cookie.value}; "





## Part 2: Get programs and their details


# Read the file /ptv/healer/bbplats/bc/programs_info.json and parse it as json, if the file doesn't exist, print error message and exit 
try:
    with open('/ptv/healer/bbplats/bc/programs_info.json', 'r') as f:
        programs_info = json.load(f)
except FileNotFoundError:
    print("[-] File programs_info.json not found")
    exit(1)

# Define an empty list to store the programs details in
programs_details = []
can_subscribes = 0
# Iterate over the targets_urls list 
print(f"[+] Fetched {len(programs_details)}/{len(programs_info)} programs details", end='\r')
for program_info in programs_info:
    # If the program's can_subscribe is true
    if program_info['can_subscribe']:
        can_subscribes += 1
        program_url = program_info['program_url']
        # Create a url for the program if the program_url is not empty or is not / 
        base_url = f"https://bugcrowd.com{program_url}"
        fetch_headers = {
            'authority': 'bugcrowd.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'content-type': 'application/json',
            'cookie': cookies_str,
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        # Send a request to the program base_url to get the csrf token, use the session
        response_base = session.get(base_url, headers=fetch_headers)
        # Parse the response to get the csrf token
        soup = BeautifulSoup(response_base.text, 'html.parser')
        x_csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})['content']

        fetch_url_curl = """curl 'https://bugcrowd.com/redox' \
        -H 'authority: bugcrowd.com' \
        -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
        -H 'accept-language: en-US,en;q=0.9,fa;q=0.8' \
        -H 'cache-control: max-age=0' \
        -H 'cookie: _gcl_au=1.1.665411146.1663222062; _ga=GA1.1.1387914877.1663222063; _fbp=fb.1.1663222063626.15440810; _ga_4J3ZM9L5RL=GS1.1.1663222062.1.1.1663222213.0.0.0; __cf_bm=EAiTAnTO65QsVA7aA5CVFt2t8BqbtTx9OZe7cni91bk-1663306870-0-AYFwuCidJU9c7GKvGizPqb9bfMYiMbJIK5NXgI/W9KWVj+MhJ/9eA/LRG+xssq0iFWXWn/rM8guDZDQuOH/BVbM=; _crowdcontrol_session=bHc5VmMzR2Q1cWFlRmpRa2d4dWw5SEpWZ1ZTUFhwUTV5THY0RVVuK1pFcUhxRGt0V0p4bi8wMk5DQUtVYmhHa2RsOTIxa3lzWmoreWx1dGlUa2tqRENVamE1RWlaNmkraHBKQi9vMWVsLzFXODBjQWtkdTJyelJ6RlRPVWcvckkvY0VsQU9iQjdvOWpsM3ZXd1d3TlpMZTM4Q0lhRDZaT3JnVHpQbjVZTXYwV21adXpOWHBGNE9qanMwYVpuencyM2ljZmJ1VTBQWitpdVJ0Z04rMjIvWXhNcWVQQ2plaXlackpQdzVWcG51OW9wOUxCYTgwVlFKUGx3L3g2UkNwU0h2d3hmY3hRYWdGcnlEeFVtN1FEWlkxVysxZ0NjMzN3clFSdkJVdm1LdjByMXVUU2JKaUtId3Nrb3VqSEc5QTF5RzcrdXp2UVZNWEVhaW12UXBydWdtOHBsUUJ0VUlQM0dtRXduNlVFZi9DMVNtT2dldWhwdEdwZ091Q2xrQmVGU3czTTB5NGJMWklTSXdRM2pwT2pBSVVpTVhJOTV6WjVrUVQvZEhLSGRlZ2FaYm1ma1FyelI3a3AwbnZuMWNNNTIyYkhFc3VXY3RjM1ZiOXY0bk91N1FmSDlWNmc1SVZZVjQwY1lUUHIwam8zSE5KVitrTEx2Q0U3UDJxTWJoWWdWdi8reFZtWU82bUc4bytkYW9aM3dOUmJWVTFSalltdElaYzJ3alpYSVRZPS0tU1lNVTNNUldLOWVNVUF0ZnNwK0lnQT09--5589a55b7420233e71cd87f67690f5192857a752' \
        -H 'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"' \
        -H 'sec-ch-ua-mobile: ?0' \
        -H 'sec-ch-ua-platform: "Windows"' \
        -H 'sec-fetch-dest: document' \
        -H 'sec-fetch-mode: navigate' \
        -H 'sec-fetch-site: none' \
        -H 'sec-fetch-user: ?1' \
        -H 'upgrade-insecure-requests: 1' \
        -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' \
        --compressed"""
        fetch_headers = {
            'authority': 'bugcrowd.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'content-type': 'application/json',
            'cookie': cookies_str,
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'x-csrf-token': x_csrf_token,
        }
        # print(f"csrf token: {x_csrf_token}")
        # Send a request to get target_groups_info 
        fetch_url = f"https://bugcrowd.com/{program_url}/target_groups"
        target_groups_info = session.get(fetch_url, headers=fetch_headers).json()
        groups = target_groups_info['groups']
        target_groups_info['groups_all_data'] = []

        # Iterate over the groups 
        for group in target_groups_info['groups']:
            # group_id = group['id']
            # group_name = group['name']
            # group_in_scope = group['in_scope']
            # group_reward_range = group['reward_range']
            group_url = group['targets_url']
            # print(f"Group Name: {group_name}\nIn Scope: {group_in_scope}\nReward Range: {group_reward_range}\nURL: {group_url}\n")

            fetch_group_curl = """curl 'https://bugcrowd.com/redox/target_groups/305c03fe-59cd-4338-be19-dbf65a1c8def/targets' \
            -H 'authority: bugcrowd.com' \
            -H 'accept: */*' \
            -H 'accept-language: en-US,en;q=0.9,fa;q=0.8' \
            -H 'content-type: application/json' \
            -H 'cookie: _gcl_au=1.1.665411146.1663222062; _ga=GA1.1.1387914877.1663222063; _fbp=fb.1.1663222063626.15440810; _ga_4J3ZM9L5RL=GS1.1.1663222062.1.1.1663222213.0.0.0; __cf_bm=EAiTAnTO65QsVA7aA5CVFt2t8BqbtTx9OZe7cni91bk-1663306870-0-AYFwuCidJU9c7GKvGizPqb9bfMYiMbJIK5NXgI/W9KWVj+MhJ/9eA/LRG+xssq0iFWXWn/rM8guDZDQuOH/BVbM=; _crowdcontrol_session=NjBUVzNrcm4xV2ZuWGtlOE5lakRYdndZNDFxYVR5dlM0U2t4eVJHN0hiVytTcW9MaWFVNC9UVjY3ckJFZXRTMllOMHNYZ3k2Q1RMdWFtOTl4dGtYYVBlb1dVV1dGR3UyNHNScDJqQUYvdUJiOWdvTEF1MndLNTBQT3EwMVFBR3Vkbm5mZG9OOEVERmtKb3dCSmM0STl4Ni9ybWh6NFcrTm8xajRRSWI4QnJwK3hBWm4velk5ZlZyQkJQWWtHaGFPQmVwL0tkNWYweDk4M0dXNDlNUkFKSzZPVndpOUl0SmtLbjlNZ0RQRS9VenZINlg4eUxlNUR4Z0pHWFhZMjhoTC9qdFhuenFDc2M4RWpUTVY0aWZ1eHJJRG5adUI2bnlUdEdPUGZ0cnVNWkxzRmsyZ04yR29wSThFcE5UZW9ZNU04YzNFdWR5ZE5rNVV3dG9NUlZ3V1ZJWVJPTGo4a2FDTFRQNmtwS3ExMFNsT05Gbm5tWncrL0xsU25saWtWaTBXMFZPUUxuU29jazFPTkV2VDVCVjJaOEcyckszdlBnbkt4d2wrS2t1c052M3M2ZHZPRFR2eXNob1BSWTlqb1JFOElKYzF1NG5QQTNoMndOWWFsMmJiRDUzMnZGSDBHNEZtbk82M2ZXZmphUWFzYXlSWndRVXhVWFdxS1RnbDkxMGN6OWx3R1hLYTRZOVhURmVmQkNiNnh5RjZOR2NoYjB1TTZ4UDJVeHNXSTJzPS0tS2g1SW5HVE45S1c0REs3Yzd4OUdldz09--31b11dd31ff8d46887ca69908bc24040684062ef' \
            -H 'referer: https://bugcrowd.com/redox' \
            -H 'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"' \
            -H 'sec-ch-ua-mobile: ?0' \
            -H 'sec-ch-ua-platform: "Windows"' \
            -H 'sec-fetch-dest: empty' \
            -H 'sec-fetch-mode: cors' \
            -H 'sec-fetch-site: same-origin' \
            -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' \
            -H 'x-csrf-token: quczwaPCcNHTiGNLPTD0MoL5gi1iypYSWez4inmZdc/qxbarq3FpBsdVspjnDo7f9n6FKTKzyro4LyYQ4q1x1Q==' \
            --compressed"""

            # rewrite the above curl to python requests using the session and cookies
            fetch_group_url = f"https://bugcrowd.com{group_url}"
            fetch_group_headers = {
                'authority': 'bugcrowd.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
                'content-type': 'application/json',
                'cookie': cookies_str,
                'referer': f"https://bugcrowd.com/{program_url}",
                'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                'x-csrf-token': f"{x_csrf_token}"
            }

            # print(f"csrf token: {x_csrf_token}")

            # print(f"Fetching group: {group_url}")
            group_json_raw = session.get(fetch_group_url, headers=fetch_group_headers)
            
            # print(f"Group JSON: {group_json_raw}")
            
            # print(group_json_raw.text)
            
            # If the response is not 200, then we have an error, so print the error and continue
            if group_json_raw.status_code != 200:
                print(f"[-] Error fetching group: {group_url}")
                continue
            
            group_json = group_json_raw.json()
            targets = group_json['targets']
            # for target in targets:
            #     target_id = target['id']
            #     target_name = target['name']
            #     target_type = target['category']
            #     target_uri = target['uri']
            #     target_tags_json = target['target']['tags']
            #     target_tags = []
            #     for tag in target_tags_json:
            #         target_tags.append(tag['name'])
            #     target_tags = ', '.join(target_tags)
            #     target_sort_order = target['sort_order']
            # # Print the target details in order of their sort order
            # for target in sorted(targets, key=lambda k: k['sort_order']):
            #     target_id = target['id']
            #     target_name = target['name']
            #     target_type = target['category']
            #     target_uri = target['uri']
            #     target_tags_json = target['target']['tags']
            #     target_tags = []
            #     for tag in target_tags_json:
            #         target_tags.append(tag['name'])
            #     target_tags = ', '.join(target_tags)
            #     target_sort_order = target['sort_order']
        
            # Append group_json to group and then append the group to target_groups_info
            group['targets_info'] = group_json
            target_groups_info['groups_all_data'].append(group)
        
        # Append target_groups_info to program_info
        program_info['target_groups_info'] = target_groups_info

        # Append program_info to programs_details
        programs_details.append(program_info)

        # if len(programs_details) mode 10 equals 0, then 
        if len(programs_details) % 10 == 0:
            # Print on single line
            print(f"[+] Fetched {len(programs_details)}/{len(programs_info)} programs details" , end='\r')

# Save program_details to a file json called programs_details.json
with open(f'/ptv/healer/bbplats/bc/programs_details_new.json', 'w') as f:
    json.dump(programs_details, f)
print(f"[+] Done! {len(programs_details)}/{can_subscribes} programs details saved to programs_details.json")

print(f"[+] Fetching programs details took {time.time() - start_time} seconds")
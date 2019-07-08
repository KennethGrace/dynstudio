import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'Content-Type': 'application/json'}
jar = requests.cookies.RequestsCookieJar()

def post(url, payload, json=False):
    if json:
        r = requests.post(url, headers=headers, json=payload, verify=False, cookies=jar)
    else:
        r = requests.post(url, headers=headers, data=payload, verify=False, cookies=jar)
    return r

def get(url, payload=None, json=False):
    r = requests.get(url, headers=headers, verify=False, cookies=jar)
    return r
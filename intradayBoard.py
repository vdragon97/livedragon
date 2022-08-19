import requests
import string
import random
from requests.structures import CaseInsensitiveDict

urlMainPage = "https://livedragon.vdsc.com.vn/general/intradayBoard.rv"
setCookie = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
setCookie = 'abcd'
def accessMainPage():
    headers = CaseInsensitiveDict()
    headers["Cookie"] = setCookie
    try:
        response = requests.get(urlMainPage, headers=headers)
    except:
        print("intradayBoard.py: Try request GET false")
        return "exitMainPage"
    #print(response.status_code)
    #print(response.headers)
    #print(response.text)
    CookiePartOne = response.headers["Set-Cookie"][0:160]
    return CookiePartOne
    
if __name__=="__main__":
    accessMainPage()
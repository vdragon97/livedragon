import requests
from requests.structures import CaseInsensitiveDict

urlCheckSession = "https://livedragon.vdsc.com.vn/general/checkSession.rv?status=0"

def checkSessionFunction(inputCookiePartOne):
    #print("inputCookiePartOne = " + inputCookiePartOne)        
    headers = CaseInsensitiveDict()
    headers["Content-Length"] = "0"
    headers["User-agent"] = ""
    headers["Cookie"] = inputCookiePartOne
    try:
        response = requests.get(urlCheckSession, headers=headers)
    except:
        print("checkSession.py: Try check session false")
        return "exitCheckSession"
    #print(response.status_code)
    #print(response.headers)
    #print(response.text)
    inputCookiePartThree_1 = response.headers["Set-Cookie"][0:44]
    inputCookiePartThree_2 = response.headers["Set-Cookie"][68:159]
    #print(inputCookiePartThree_1 + " " + inputCookiePartThree_2)
    return (inputCookiePartThree_1 + " " + inputCookiePartThree_2)
if __name__=="__main__":
    test = checkSessionFunction("abcd")
    print(test)
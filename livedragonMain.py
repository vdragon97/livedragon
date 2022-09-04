import intradayBoard
import checkSession
import intradaySearch
import string
import random
import time
import sys
from datetime import datetime, timedelta, date
from colorama import init, Fore, Back, Style

init(convert=True)

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def callLiveDragon(checkDate, checkContract, checkSensitive, checkFromTime, checkToTime):
    CookiePartOne = intradayBoard.accessMainPage()
    #print("CookiePartOne = " + CookiePartOne)
    if CookiePartOne =="exitMainPage":
        return
    CookiePartTwo ="; hideMarketChartCKName=0; allCustomGroupsCkName=ALL_DEFAULT_GROUP_ID%23%23%23%23%23%23%23%23CTD%3BDHG%3BDRC%3BFPT%3BHPG%3BHSG%3BKDC%3BMWG%3BNT2%3BPAC%3BPC1%3BPNJ%3BTAC%3BVCB%3BVDS%3BVGC%3BVJC%3BVNM%3B%23%23%23%23%23%23%23%23T%C3%B9y%20ch%E1%BB%8Dn; "
    
    CookiePartThree = checkSession.checkSessionFunction(CookiePartOne)
    if CookiePartThree =="exitCheckSession":
        return
    CookiePartFour = 'RV9cd20160034=' + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(192))
    
    CookiePartFive = "; rv_avraaaaaaaaaaaaaaaa_session_=JKFNGBKNNJONIPPCPPAHKMDMJFHCFKIKMNGGNBKABEMPGKJMECDCHBJODECEEFNFDJCDOMNLNBEPOLCEAPIABICLKGDFHBAMFGMDHGDILAHBKANJKBMCCGAFKDKPIIEA"
    
    Cookie = CookiePartOne + CookiePartTwo + CookiePartThree + CookiePartFour + CookiePartFive
    #print (Cookie)
    workingTime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")    
    print (Fore.YELLOW + "---------------------workingTime = " + workingTime + "--------------------" + Style.RESET_ALL)
    print (Fore.YELLOW + "  checkDate = " + checkDate + "    checkContract = " + checkContract + "    Sensitive = " + checkSensitive + " " + Style.RESET_ALL)
    print ("---------------------------------------------------------------------------")
    print (Fore.YELLOW + "TradeTime|  Bid1  | MPrice | Offer1 | Shark | g L Vol | g S Vol | MTotalVol" + Style.RESET_ALL)
    print ("---------------------------------------------------------------------------")
    intradaySearch.intradaySearchFunction(checkDate, checkContract, checkSensitive, Cookie, checkFromTime, checkToTime)
    
if __name__=="__main__":    
    while(True):
        if (len(sys.argv) == 6):
            #single date
            callLiveDragon(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        elif (len(sys.argv) == 7):
            #from date to date
            fromDate = datetime.strptime(sys.argv[1], "%d/%m/%Y")
            toDate = datetime.strptime(sys.argv[2], "%d/%m/%Y")
            for dt in daterange(fromDate, toDate):
                callLiveDragon(dt.strftime("%d/%m/%Y"), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        else: 
            #print(datetime.now().strftime("%d/%m/%Y"))
            #print("VN30F" + datetime.now().strftime("%Y")[2:4] + datetime.now().strftime("%m"))
            callLiveDragon(datetime.now().strftime("%d/%m/%Y"), "VN30F" + datetime.now().strftime("%Y")[2:4] + datetime.now().strftime("%m"), "0.8", "09:00:00", "14:30:00")
            print("--------------------------------------------------")
        time.sleep(10)
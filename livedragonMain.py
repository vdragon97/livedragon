import intradayBoard
import checkSession
import intradaySearch
import string
import random
import time
import sys
from datetime import datetime

def callLiveDragon(checkDate, checkContract, checkSensitive):
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
    print ("---------------workingTime = " + workingTime + "---------------")
    print ("checkDate = " + checkDate + " checkContract = " + checkContract + " Sensitive = " + checkSensitive)
    print ("----------------------------------------------------------------")
    print ("TradeTime|  Bid1  | MPrice | Offer1 | Shark | gapVol | MTotalVol")
    print ("----------------------------------------------------------------")
    intradaySearch.intradaySearchFunction(checkDate, checkContract, checkSensitive, Cookie)
    
if __name__=="__main__":    
    while(True):
        if (len(sys.argv) > 1):
            callLiveDragon(sys.argv[1], sys.argv[2], sys.argv[3])
        else: 
            #print(datetime.now().strftime("%d/%m/%Y"))
            #print("VN30F" + datetime.now().strftime("%Y")[2:4] + datetime.now().strftime("%m"))
            callLiveDragon(datetime.now().strftime("%d/%m/%Y"), "VN30F" + datetime.now().strftime("%Y")[2:4] + datetime.now().strftime("%m"))
            print("--------------------------------------------------")
        time.sleep(10)
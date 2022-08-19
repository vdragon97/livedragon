import requests
import string
import random
from requests.structures import CaseInsensitiveDict
from datetime import datetime
import os
'''
python livedragon.py inputDate inputMode

inputDate: dd/mm/yyyy
inputMode: all/ctn
'''

def intradaySearchFunction(inputDate, inputContract, inputCookie):   
    url = "https://livedragon.vdsc.com.vn/general/intradaySearch.rv?stockCode=" + inputContract +"&boardDate=" + inputDate
    headers = CaseInsensitiveDict()
    headers["Content-Length"] = "0"
    headers["Cookie"] = inputCookie
    headers["User-agent"] = ""
    headers["Connection"] = "keep-alive"
    headers["Accept"] = "*/*"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    #print(headers)
    try:
        resp = requests.post(url, headers=headers, timeout=10)
    except:
        print("intradaySearch.py: Try search false")
        return
    #print(resp.headers) #headers looks like that {'Content-Type': 'application/json;charset=UTF-8', 'Content-Language': 'vi-VN', 'Transfer-Encoding': 'chunked', 'Date': 'Fri, 05 Aug 2022 16:28:58 GMT'}
    data = resp.json() #all data is a dictionary
    '''
    {
        "success": true,
        "message": "",
        "list": [{}, {}, ...{}]
    }
    '''
    diff = 0.8
    long_cnt = 0
    short_cnt = 0
    total_match_vol = 0
    list = data['list']  #get the list which named "list"
    size = len(list) #row count of the grid
    #print("row count = "+ str(size))
    now = datetime.now() # current date and time
    folderName = now.strftime("%Y%m%d")
    isExist = os.path.exists("./" + folderName)
    if not isExist:
        os.makedirs(folderName)
    fileName = now.strftime("%H%M%S") + ".txt"
    #f=open("./" + folderName + "/" + fileName,'w')
    for x in reversed(range(size)):
        if list[x]['TradeTime'] > "08:59:00" and list[x]['TradeTime'] < "14:30:00" and list[x]['BidPrice1'] > 0 and list[x]['MatchedPrice'] > 0 and list[x]['OfferPrice1'] > 0:
            #f.seek(0) #get to the first position
            output = str(list[x]['TradeTime']) + " | " + str(list[x]['BidPrice1']) + " | " + str(list[x]['MatchedPrice']) + " | " + str(list[x]['OfferPrice1'])
            #f.write(output)
            #f.write("\n")
            if round(list[x]['BidPrice1'] - list[x - 1]['BidPrice1'], 1) >= diff and round(list[x]['BidPrice1'] - list[x]['MatchedPrice'], 1) >= diff and round(list[x]['OfferPrice1'] - list[x]['MatchedPrice'], 1) >= diff and round(list[x]['OfferPrice1'] - list[x - 1]['OfferPrice1'], 1) >= diff:
                print(output + " | LONG")
                long_cnt = long_cnt + 1
            if round(list[x]['BidPrice1'] - list[x - 1]['BidPrice1'], 1) <= -diff and round(list[x]['BidPrice1'] - list[x]['MatchedPrice'], 1) <= -diff and round(list[x]['OfferPrice1'] - list[x]['MatchedPrice'], 1) <= -diff and round(list[x]['OfferPrice1'] - list[x - 1]['OfferPrice1'], 1) <= -diff:
                print(output + " | SHORT")
                short_cnt = short_cnt + 1
        total_match_vol = total_match_vol + list[x]['MatchedVol'] 
    print("Total LONG = " + str(long_cnt) + " | Total SHORT = " + str(short_cnt) + " | Total Matched Vol = " + str(total_match_vol * 10))
    #f.close()    
    

if __name__=="__main__":
    intradaySearchFunction("05/08/2022", "VN30F2208", "")

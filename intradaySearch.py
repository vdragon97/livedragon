import requests
import string
import random
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from colorama import init, Fore, Back, Style
import os
'''
python livedragon.py inputDate inputMode

inputDate: dd/mm/yyyy
inputMode: all/ctn
'''
init(convert=True)

def intradaySearchFunction(inputDate, inputContract, inputSensitive, inputCookie):   
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
    sensitive = round(float(inputSensitive), 1)
    long_cnt = 0
    short_cnt = 0
    total_match_vol = 0
    total_gap_long_vol = 0
    total_gap_short_vol = 0
    list = data['list']  #get the list which named "list"
    size = len(list) #row count of the grid
    #print("row count = "+ str(size))
    now = datetime.now() # current date and time
    folderName = now.strftime("%Y%m%d") + "-" + inputSensitive
    isExist = os.path.exists("./" + folderName)
    if not isExist:
        os.makedirs(folderName)
    fileName = now.strftime("%H%M%S") + ".csv"
    f=open("./" + folderName + "/" + fileName,'w')
    #add column name
    f.write("TradeTime|Bid1|MatchedPrice|Offer1|Shark|gapLongVol|gapShortVol|MTotalVol" + "\n")
    for x in reversed(range(size)):
        if list[x]['TradeTime'] > "09:00:00" and list[x]['TradeTime'] < "14:30:00" and list[x]['BidPrice1'] > 0 and list[x]['MatchedPrice'] > 0 and list[x]['OfferPrice1'] > 0:
            #f.seek(0) #get to the first position
            output_price = str(list[x]['TradeTime']) + " | " + str(list[x]['BidPrice1']) + " | " + str(list[x]['MatchedPrice']) + " | " + str(list[x]['OfferPrice1'])
            #f.write(output_price)
            #f.write("\n")
            n = 0
            listMatchedTotalVol = []
            if round(list[x]['BidPrice1'] - list[x - 1]['BidPrice1'], 1) >= sensitive and round(list[x]['BidPrice1'] - list[x]['MatchedPrice'], 1) >= sensitive and round(list[x]['OfferPrice1'] - list[x]['MatchedPrice'], 1) >= sensitive and round(list[x]['OfferPrice1'] - list[x - 1]['OfferPrice1'], 1) >= sensitive:
                try:
                    while list[x]['BidPrice1'] == list[x + n]['BidPrice1'] and list[x]['OfferPrice1'] == list[x + n]['OfferPrice1']:
                        #print(f"{list[x + n]['MatchedTotalVol']:,d}")
                        listMatchedTotalVol.append(list[x + n]['MatchedTotalVol'])
                        n = n + 1
                    gapLongVol = max(listMatchedTotalVol) - min(listMatchedTotalVol)
                    output_long = output_price + " |  LONG | " + str(f"{gapLongVol:,d}").rjust(7," ") + " | " + "        |  " + str(f"{list[x]['MatchedTotalVol']:,d}").rjust(8," ")
                    print(Fore.GREEN + output_long + Style.RESET_ALL)
                    f.write(output_long)
                    f.write("\n")
                    total_gap_long_vol = total_gap_long_vol + gapLongVol
                    long_cnt = long_cnt + 1
                except:
                    continue
                signal_long = Fore.CYAN + "!" + Style.RESET_ALL
                signal_short = ""
            if round(list[x]['BidPrice1'] - list[x - 1]['BidPrice1'], 1) <= -sensitive and round(list[x]['BidPrice1'] - list[x]['MatchedPrice'], 1) <= -sensitive and round(list[x]['OfferPrice1'] - list[x]['MatchedPrice'], 1) <= -sensitive and round(list[x]['OfferPrice1'] - list[x - 1]['OfferPrice1'], 1) <= -sensitive:
                try:
                    while list[x]['BidPrice1'] == list[x + n]['BidPrice1'] and list[x]['OfferPrice1'] == list[x + n]['OfferPrice1']:
                        #print(f"{list[x + n]['MatchedTotalVol']:,d}")
                        listMatchedTotalVol.append(list[x + n]['MatchedTotalVol'])
                        n = n + 1
                    gapShortVol = max(listMatchedTotalVol) - min(listMatchedTotalVol)
                    output_short = output_price + " | SHORT | " + "        | " + str(f"{gapShortVol:,d}").rjust(7," ") + " |  "  + str(f"{list[x]['MatchedTotalVol']:,d}").rjust(8," ")
                    print(Fore.RED + output_short + Style.RESET_ALL)
                    f.write(output_short)
                    f.write("\n")
                    total_gap_short_vol = total_gap_short_vol + gapShortVol
                    short_cnt = short_cnt + 1
                except:
                    continue
                signal_long = ""
                signal_short = Fore.WHITE + "!" + Style.RESET_ALL
        total_match_vol = max(total_match_vol, list[x]['MatchedTotalVol'] )
    print ("---------------------------------------------------------------------------")
    try:
        print(Fore.GREEN + "Total shark LONG  = " + str(long_cnt).rjust(3," ") +  " | Total gapVol LONG  = " + str(f"{total_gap_long_vol:,d}").rjust(6," ") + " |         | %V = " + str(f'{total_gap_long_vol/total_match_vol:.0%}').rjust(3," ") + Style.RESET_ALL + signal_long )
        print(Fore.RED + "Total shark SHORT = " + str(short_cnt).rjust(3," ") + " | Total gapVol SHORT =        | " + str(f"{total_gap_short_vol:,d}").rjust(7," ") + " | %V = " + str(f'{total_gap_short_vol/total_match_vol:.0%}').rjust(3," ")  + Style.RESET_ALL + signal_short)
    except:
        pass
    print ("---------------------------------------------------------------------------")
    f.close()    
    

if __name__=="__main__":
    intradaySearchFunction("05/08/2022", "VN30F2208", "")
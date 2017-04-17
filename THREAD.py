import re
import requests
from bs4 import BeautifulSoup
from threading import Thread
import time

Tlist=['幣別','即期買匯','即期賣匯','現金買匯','現金賣匯']
SB={}
SS={}
CB={}
CS={}

CURRENCY={'USD':'美金','HKD':'港幣','GBP':'英鎊','JPY':'日圓','AUD':'澳幣',
          'CAD':'加拿大幣','SGD':'新加坡幣','ZAR':'南非幣','SEK':'瑞典幣','CHF':'瑞士法郎',
          'THB':'泰銖','NZD':'紐西蘭幣','EUR':'歐元','KRW':'韓元','MYR':'馬來幣',
          'IDR':'印尼幣','PHP':'菲國比索','MOP':'澳門幣','VND':'越南盾','CNY':'人民幣',
          'TRY':'土耳其里拉','DKK':'丹麥克朗','INR':'印度盧比','CNH':'離岸人民幣'}

for i in range(0,len(set(CURRENCY.keys()))):
    SB[list(CURRENCY.keys())[i]]={}
    SS[list(CURRENCY.keys())[i]]={}
    CB[list(CURRENCY.keys())[i]]={}
    CS[list(CURRENCY.keys())[i]]={}


BANKcurrency={'兆豐銀行':['USD','HKD','GBP','JPY','AUD',
              'CAD','SGD','ZAR','SEK','CHF',
              'THB','NZD','EUR','KRW','MYR',
              'IDR','PHP','MOP','VND','CNY'],
              '土地銀行':['USD', 'JPY', 'GBP', 'HKD', 'AUD',
              'CAD', 'SGD', 'CHF', 'SEK', 'ZAR',
              'THB', 'NZD', 'EUR', 'CNY'],
              '第一銀行':['USD', 'GBP', 'HKD', 'AUD', 'SGD',
              'CHF', 'CAD', 'JPY', 'ZAR', 'SEK',
              'THB', 'NZD', 'EUR', 'CNY', 'TRY'],
              '國泰世華銀行':['USD', 'CNY', 'HKD', 'GBP', 'CHF',
              'AUD', 'SGD', 'CAD', 'SEK', 'ZAR',
              'JPY', 'DKK', 'THB', 'NZD', 'EUR',
              'TRY'],
              '台新銀行':['AUD', 'CAD', 'CHF', 'CNY', 'EUR',
              'GBP', 'HKD', 'JPY', 'NZD', 'SEK',
              'SGD', 'THB', 'USD', 'ZAR'],
              '中國信託商業銀行':['USD', 'JPY', 'HKD', 'GBP', 'CHF',
              'SGD', 'ZAR', 'SEK', 'AUD', 'CAD',
              'MYR', 'NZD', 'THB', 'PHP', 'EUR',
              'IDR', 'KRW', 'INR', 'VND', 'CNY'],
              '永豐銀行':['USD', 'JPY', 'HKD', 'EUR', 'GBP',
              'CHF', 'AUD', 'SGD', 'SEK', 'CAD',
              'THB', 'ZAR', 'NZD', 'MOP', 'CNY',
              'CNH'],
              '凱基銀行':['USD', 'HKD', 'JPY', 'EUR', 'GBP',
              'AUD', 'CAD', 'CHF', 'NZD', 'SEK',
              'SGD', 'CNH', 'THB', 'ZAR']}
BANKcurrencyX={'兆豐銀行':['USD','HKD','GBP','JPY','AUD',
              'CAD','SGD','ZAR','SEK','CHF',
              'THB','NZD','EUR','KRW','MYR',
              'IDR','PHP','MOP','VND','CNY'],
              '土地銀行':['USD', 'JPY', 'GBP', 'HKD', 'AUD',
              'CAD', 'SGD', 'CHF', 'SEK', 'ZAR',
              'THB', 'NZD', 'EUR', 'CNY'],
              '第一銀行':['USD', 'GBP', 'HKD', 'AUD', 'SGD',
              'CHF', 'CAD', 'JPY', 'ZAR', 'SEK',
              'THB', 'NZD', 'EUR', 'CNY', 'TRY'],
              '國泰世華銀行':['USD', 'CNY', 'HKD', 'GBP', 'CHF',
              'AUD', 'SGD', 'CAD', 'SEK', 'ZAR',
              'JPY', 'DKK', 'THB', 'NZD', 'EUR',
              'TRY'],
              '台新銀行':['AUD', 'CAD', 'CHF', 'CNY', 'EUR',
              'GBP', 'HKD', 'JPY', 'NZD', 'SEK',
              'SGD', 'THB', 'USD', 'ZAR'],
              '永豐銀行':['USD', 'JPY', 'HKD', 'EUR', 'GBP',
              'CHF', 'AUD', 'SGD', 'SEK', 'CAD',
              'THB', 'ZAR', 'NZD', 'MOP', 'CNY',
              'CNH'],
              '凱基銀行':['USD', 'HKD', 'JPY', 'EUR', 'GBP',
              'AUD', 'CAD', 'CHF', 'NZD', 'SEK',
              'SGD', 'CNH', 'THB', 'ZAR']}

BANKcurrencyC={
              '中國信託商業銀行':['USD', 'JPY', 'HKD', 'GBP', 'CHF',
              'SGD', 'ZAR', 'SEK', 'AUD', 'CAD',
              'MYR', 'NZD', 'THB', 'PHP', 'EUR',
              'IDR', 'KRW', 'INR', 'VND', 'CNY']
              }
BANKset=set(BANKcurrency.keys())

"""
BANKkeywords2={'兆':{'兆豐銀行'},
              '豐':{'兆豐銀行','永豐銀行'},
              '土':{'土地銀行'},
              '地':{'土地銀行'},
              '第':{'第一銀行'},
              '一':{'第一銀行'},
              '國':{'國泰世華銀行','中國信託商業銀行'},
              '泰':{'國泰世華銀行'},
              '世':{'國泰世華銀行'},
              '華':{'國泰世華銀行'},
              '台':{'台新銀行'},
              '新':{'台新銀行'},
              '中':{'中國信託商業銀行'},
              '信':{'中國信託商業銀行'},
              '託':{'中國信託商業銀行'},
              '永':{'永豐銀行'},
              '凱':{'凱基銀行'},
              '基':{'凱基銀行'}}
"""

BANKkeywords={}
for bk in BANKset:
    for word in bk.strip("銀行").strip("商業"):
        if word in BANKkeywords.keys():
            BANKkeywords[word].add(bk)
        else:
            BANKkeywords[word]={bk}

"""
for old in BANKkeywords2.keys():
    if BANKkeywords[old] == BANKkeywords2[old]:
        print(BANKkeywords[old])
    else:
        print("Here is a difference")
print(BANKkeywords2 == BANKkeywords)
"""


def SCSB(BANKname, fxrate):
    for i in range(0,len(BANKcurrency[BANKname])*4,4):
        try:
            SB[BANKcurrency[BANKname][int(i/4)]][BANKname]=float(fxrate[i])
        except ValueError:
            SB[BANKcurrency[BANKname][int(i/4)]][BANKname]=fxrate[i]
        try:
            SS[BANKcurrency[BANKname][int(i/4)]][BANKname]=float(fxrate[i+1])
        except ValueError:
            SS[BANKcurrency[BANKname][int(i/4)]][BANKname]=fxrate[i+1]
        try:
            CB[BANKcurrency[BANKname][int(i/4)]][BANKname]=float(fxrate[i+2])
        except ValueError:
            CB[BANKcurrency[BANKname][int(i/4)]][BANKname]=fxrate[i+2]
        try:
            CS[BANKcurrency[BANKname][int(i/4)]][BANKname]=float(fxrate[i+3])
        except ValueError:
            CS[BANKcurrency[BANKname][int(i/4)]][BANKname]=fxrate[i+3]

    
class parsing:

    def __init__(self):
        
        self.BKpar={'兆豐銀行' : self.MEGApar,
                    '土地銀行' : self.LANDpar,
                    '第一銀行' : self.FIRSTpar,
                    '國泰世華銀行' : self.CATHAYpar,
                    '台新銀行' : self.TAISHINpar,
                    '中國信託商業銀行' : self.CTBCpar,
                    '永豐銀行' : self.SINOPACpar,
                    '凱基銀行' : self.KGIpar}
        
    def MEGApar(self):
        
        try:
            MEGAs=time.time()
        
            urlviewF = 'https://wwwfile.megabank.com.tw/rates/M001/viewF.asp'
            resF=requests.get(urlviewF)
            cookievalue=dict(resF.cookies)['mega%5Fstatus']

            urlV = 'https://wwwfile.megabank.com.tw/rates/D001/_@V_.asp'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
            cookie = {'mega%5Fstatus':cookievalue}

            resV=requests.get(urlV, cookies=cookie)
            resV.encoding='UTF-8'
            resVtext=resV.text

            strtext=str()
            strlist=list()
    
            strtext = resVtext.replace('__header_=0;','')
            strtext = strtext.replace('#','')
        

            strtext = strtext.strip('\n')
            strlist = strtext.split(';')
            del strlist[-1]
            splitime = strlist[0].split('|')
        
            #MEGAtime = splitime[0]+' '+splitime[1]
        
            strlist[0]=splitime[2]
    
            for i in range(0,len(strlist),5):
                strlist[i],strlist[i+1],strlist[i+2],strlist[i+3],strlist[i+4]=\
                strlist[i+2],strlist[i+3],strlist[i],strlist[i+1],strlist[i+4]
            #print(strlist)
    
            fxrate=[]

            for i in range(0,100):
                if i%5 !=0:
                    fxrate.append(strlist[i].split('=')[1])
            for i in range(0,80,4):
                fxrate[i+1] , fxrate[i+2] = fxrate[i+2] , fxrate[i+1]
            print(len(fxrate))
            
            SCSB('兆豐銀行', fxrate)

            print('MEGA {}'.format(time.time()-MEGAs))
        
        except:
            disconnectlist.append('兆豐銀行')




    def LANDpar(self):
        
        try:
            LANDs=time.time()

            url = 'https://ebank.landbank.com.tw/infor/infor.aspx?__eventtarget=querycurrency'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            res=requests.get(url)       
            res.encoding='UTF-8'
            restext=res.text
        
            bs=BeautifulSoup(restext, "html.parser")
        
            tableRATE=bs.find("table", {'class':'disptab'})
            findcol=tableRATE.findAll("td",{'align':'Right'})

            fxrate=[]
        
            for i in range(0,len(BANKcurrency['土地銀行'])*4):
                recordrate=findcol[i].get_text()
                fxrate.append(recordrate)
            print(len(fxrate))

            SCSB('土地銀行', fxrate)
            
            print('LAND {}'.format(time.time()-LANDs))
        

        except :
            disconnectlist.append('土地銀行')

    def FIRSTpar(self):
    
        try:
            FIRSTs=time.time()

            url = 'https://ibank.firstbank.com.tw/NetBank/7/0201.html?sh=none'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            res=requests.get(url)
        
            res.encoding='UTF-8'

            restext=res.text

            bs=BeautifulSoup(restext, "html.parser")
        
            tableRATE=bs.findAll("td",{'align':'right'})
        
            fxrate=[]
        
            for i in range(0,44):
                recordrate=tableRATE[i].get_text()
                recordrate=recordrate.strip('\r\n                \r\n                \r\n                    ')
            
                fxrate.append(recordrate)
                if i in (13,15,17,27,29,31,33,43):
                    fxrate.append('--')
                    fxrate.append('--')
            print(len(fxrate))

            SCSB('第一銀行', fxrate)

            print('FIRST {}'.format(time.time()-FIRSTs))
        
        except :
            disconnectlist.append('第一銀行')

    def CATHAYpar(self):
    
        try:
            CATHAYs=time.time()

            url = 'https://www.cathaybk.com.tw/cathaybk/exchange/currency-billboard.asp?page=current'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            res=requests.get(url)       
            res.encoding='UTF-8'
            restext=res.text

            bs=BeautifulSoup(restext, "html.parser")
        
            tableRATE=bs.find("table",{'class':'table_rate'}).get_text()
            recordrate=[]
            for i in tableRATE.split():
                try:
                    recordrate.append(float(i))
                except:
                    pass
    
            fxrate=[]
            for i in range(0,len(recordrate)):
                fxrate.append(recordrate[i])
                if i in (13,15,17,19,21,23,25,31,33,35,41):
                    fxrate.append('--')
                    fxrate.append('--')
            print(len(fxrate))
            SCSB('國泰世華銀行', fxrate)
            
            print('CATHAY {}'.format(time.time()-CATHAYs))
            
        except :
            disconnectlist.append('國泰世華銀行')

    def TAISHINpar(self):
    
        try:
            TAISHINs=time.time()

            url = 'https://www.taishinbank.com.tw/TS/TS06/TS0605/TS060502/index.htm?urlPath1=TS02&urlPath2=TS0202'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            res=requests.get(url, headers=header)       
            res.encoding='UTF-8'
            restext=res.text

            bs=BeautifulSoup(restext, "html.parser")
            findcol=bs.findAll("td",{'align':'center'})
        
            fxrate=[]
            for i in range(0,len(BANKcurrency['台新銀行'])*4):
                fxrate.append(findcol[i].get_text())
            print(len(fxrate))
        
            SCSB('台新銀行', fxrate)

            print('TAISHIN {}'.format(time.time()-TAISHINs))
        
        except :
            disconnectlist.append('台新銀行')

    def CTBCpar(self):
    
        try:
            CTBCs=time.time()

            url = 'https://www.ctbcbank.com/CTCBPortalWeb/toPage?id=TW_RB_CM_ebank_018001'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            res=requests.get(url)
        
            res.encoding='UTF-8'
            
            restext=res.text

            bs=BeautifulSoup(restext, "html.parser")
            findcol=bs.findAll("td",{'class':'defaultDash column_text'})

            CTBCloopstart=time.time()
            print('start for loop from {}'.format(CTBCloopstart-CTBCs))

            fxrate=[]
            for i in range(0,len(BANKcurrency['中國信託商業銀行'])*4):
                if len(findcol[i].get_text())>0:
                    fxrate.append(findcol[i].get_text())
                else:
                    fxrate.append('--')
            print(len(fxrate))
            print('complete CTBC for loop in {}'.format(time.time()-CTBCloopstart))

            SCSB('中國信託商業銀行', fxrate)

            print('CTBC {}'.format(time.time()-CTBCs))
        
        except :
            disconnectlist.append('中國信託商業銀行')

    def SINOPACpar(self):
    
        try:
            SINOPACs=time.time()

            urlSPOT = 'https://mma.sinopac.com/ws/share/rate/ws_exchange.ashx?exchangeType=REMIT'
            urlCASH = 'https://mma.sinopac.com/ws/share/rate/ws_exchange.ashx?exchangeType=CASH'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            resSPOT=requests.get(urlSPOT)
        
            resSPOT.encoding='UTF-8'

            restextSPOT=resSPOT.text
            restextSPOT=restextSPOT.replace('","','')
            restextSPOT=restextSPOT.replace('2":"','')
            restextSPOT=restextSPOT.replace('3":"','')
            restextSPOT=restextSPOT.split('DataValue')[7:]
            SPOT=[]
            for i in range(0,len(restextSPOT),5):
                SPOT.append(restextSPOT[i+1])
                SPOT.append(restextSPOT[i+2])

            resCASH=requests.get(urlCASH)
        
            resCASH.encoding='UTF-8'

            restextCASH=resCASH.text
            restextCASH=restextCASH.replace('","','')
            restextCASH=restextCASH.replace('2":"','')
            restextCASH=restextCASH.replace('3":"','')
            restextCASH=restextCASH.split('DataValue')[7:]
            CASH=[]
            for i in range(0,len(restextCASH),5):
                CASH.append(restextCASH[i+1])
                CASH.append(restextCASH[i+2])
        
            fxrate=[]
            for i in range(0,len(SPOT),2):
                fxrate.append(SPOT[i])
                fxrate.append(SPOT[i+1])
                fxrate.append(CASH[i])
                fxrate.append(CASH[i+1])
            print(len(fxrate))
        
            SCSB('永豐銀行', fxrate)

            print('SINOPAC {}'.format(time.time()-SINOPACs))
        
        except :
            disconnectlist.append('永豐銀行')

    def KGIpar(self):
    
        try:
            KGIs=time.time()

            url = 'https://www.kgibank.com/T01/T0111/rate03.jsp'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            res=requests.get(url)
        
            res.encoding='UTF-8'

            restext=res.text

            bs=BeautifulSoup(restext, "html.parser")
            findcol=bs.findAll("td")
            fxrate=[]
            for i in range(10,len(findcol)):
                if len(findcol[i].get_text())>0 and i%10 in (2,3,4,5):
                    fxrate.append(findcol[i].get_text())
                elif len(findcol[i].get_text())==0:
                    fxrate.append('--')
                else:
                    pass           
            print(len(fxrate))
            
            SCSB('凱基銀行', fxrate)

            print('KGI {}'.format(time.time()-KGIs))
        
        except :
            disconnectlist.append('凱基銀行')

class ThreadPar(Thread):
    def __init__(self,parsing,bank):
        super().__init__()
        self.parsing = parsing
        self.bank = bank

    def run(self):
        self.parsing.BKpar[self.bank]()

disconnectlist={}
parTHREAD=parsing()
threads = [ThreadPar(parTHREAD,bk) for bk in BANKset]
startTHREAD=time.time()
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print('parsing with Thread complete in {time} seconds.'.format(time = time.time()-startTHREAD))
print('cannot connect ',disconnectlist)

disconnectlist={}
par=parsing()
start=time.time()
for bk in BANKset:
    par.BKpar[bk]()
print('parsing complete in {time} seconds.'.format(time = time.time()-start))
print('cannot connect ',disconnectlist)

''''''''''''''''''''''''''''
                
def MAXMIN(compareCurrency, SBSSCBCS, EXTREME):
    #根據 SBSSCBCS的參數來決定是 即期/現金 買/賣匯
    if SBSSCBCS == SB:
        SCSBCHT=Tlist[1]
    elif SBSSCBCS == SS:
        SCSBCHT=Tlist[2]
    elif SBSSCBCS == CB:
        SCSBCHT=Tlist[3]
    elif SBSSCBCS == CS:
        SCSBCHT=Tlist[4]
    #確認compareCURRENCY裡面的幣別有沒有在各家銀行的幣別清單裡,再確認有無現金賣出價格,把現金賣出價格加入comparelist當中        
    for i in compareCurrency:
            
        comparelist=[]
        for j in BANKset:
            if j not in disconnectlist and i in BANKcurrency[j] and isinstance(SBSSCBCS[i][j], float):
                comparelist.append(SBSSCBCS[i][j])
                
            else:
                pass
        #從comparelist中選一個最小的數字,回傳幣別與銀行等訊息
        if len(comparelist) > 0 and EXTREME == 'MIN':
            minrate=min(comparelist)
            
            BESTretailer=[]
            for j in BANKset:
                if j not in disconnectlist and i in BANKcurrency[j]: 
                    if minrate == SBSSCBCS[i][j]:
                        BESTretailer.append(j)
                else:
                    pass
            replytxtlist.append(' 與 '.join(BESTretailer)+'的 '+i+' '+SCSBCHT+'最低價, 匯率為'+str(SBSSCBCS[i][BESTretailer[0]]))
        elif len(comparelist) > 0 and EXTREME == 'MAX':
            maxrate=max(comparelist)
            
            BESTretailer=[]
            for j in BANKset:
                if j not in disconnectlist and i in BANKcurrency[j]: 
                    if maxrate == SBSSCBCS[i][j]:
                        BESTretailer.append(j)
                else:
                    pass
            replytxtlist.append(' 與 '.join(BESTretailer)+'的 '+i+' '+SCSBCHT+'最高價, 匯率為'+str(SBSSCBCS[i][BESTretailer[0]]))
             

def compare(inputmsg):
    global replytxtlist, replytxt, disconnectlist
    disconnectlist=[]
    
    for key in BKpar.keys():
        BKpar[key]()
    
    replytxtlist=[]
    compareCurrency=[]
    #用CURRENCY的key跟value去比對inputmsg裡面有沒有中英文幣別訊息,把幣別訊息加入compareCURRENCY裡面
    for i in list(CURRENCY.keys()):
        if re.search(i, inputmsg, re.IGNORECASE) or CURRENCY[i] in inputmsg or (inputmsg in CURRENCY[i] and inputmsg != ('幣','元','圓')):
            compareCurrency.append(i)
    print(compareCurrency)
    
    MAXMIN(compareCurrency, SB, 'MAX')
    MAXMIN(compareCurrency, SS, 'MIN')
    MAXMIN(compareCurrency, CB, 'MAX')
    MAXMIN(compareCurrency, CS, 'MIN')
        
    if len(disconnectlist) > 0:
        replytxtlist.append(str(' 與 '.join(disconnectlist)+'無法連線'))
    replytxt='\n'.join(replytxtlist)
            
    if len(compareCurrency) == 0 :
        replytxt='阿ㄆㄧㄚˇ哥聽不懂 '+text+' 也許凱子知道那是什麼...'
'''''''''''''''''''''''''''''


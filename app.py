import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from threading import Thread
import time

app = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


line_bot_api = LineBotApi(channel_access_token) #Your Channel Access Token
handler = WebhookHandler(channel_secret) #Your Channel Secret

class parsing:

    def __init__(self):

        self.CURRENCY={'USD':'美金','HKD':'港幣','GBP':'英鎊','JPY':'日圓','AUD':'澳幣',
                       'CAD':'加拿大幣','SGD':'新加坡幣','ZAR':'南非幣','SEK':'瑞典幣','CHF':'瑞士法郎',
                       'THB':'泰銖','NZD':'紐西蘭幣','EUR':'歐元','KRW':'韓元','MYR':'馬來幣',
                       'IDR':'印尼幣','PHP':'菲國比索','MOP':'澳門幣','VND':'越南盾','CNY':'人民幣',
                       'TRY':'土耳其里拉','DKK':'丹麥克朗','INR':'印度盧比','CNH':'離岸人民幣'}

        self.BANKcurrency={'兆豐銀行':['USD','HKD','GBP','JPY','AUD',
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

        self.BANKkeywords={}
        for bk in set(self.BANKcurrency.keys()):
            for word in bk.strip("銀行").strip("商業"):
                if word in self.BANKkeywords.keys():
                    self.BANKkeywords[word].add(bk)
                else:
                    self.BANKkeywords[word]={bk}        
        
        self.BKpar={'兆豐銀行' : self.MEGApar,
                    '土地銀行' : self.LANDpar,
                    '第一銀行' : self.FIRSTpar,
                    '國泰世華銀行' : self.CATHAYpar,
                    '台新銀行' : self.TAISHINpar,
                    '中國信託商業銀行' : self.CTBCpar,
                    '永豐銀行' : self.SINOPACpar,
                    '凱基銀行' : self.KGIpar}
        self.SB={}
        self.SS={}
        self.CB={}
        self.CS={}
        
        for i in range(0,len(set(self.CURRENCY.keys()))):
            self.SB[list(self.CURRENCY.keys())[i]]={}
            self.SS[list(self.CURRENCY.keys())[i]]={}
            self.CB[list(self.CURRENCY.keys())[i]]={}
            self.CS[list(self.CURRENCY.keys())[i]]={}

        self.titleDICT={'CURRENCY':'幣別',
                              'SB':['即期買匯',self.SB],
                              'SS':['即期賣匯',self.SS],
                              'CB':['現金買匯',self.CB],
                              'CS':['現金賣匯',self.CS]}
            
        self.disconnectlist=[]
            
    def SCSB(self,BANKname,fxrate):
        for i in range(0,len(self.BANKcurrency[BANKname])*4,4):
            try:
                self.SB[self.BANKcurrency[BANKname][int(i/4)]][BANKname]=float(fxrate[i])
            except ValueError:
                self.SB[self.BANKcurrency[BANKname][int(i/4)]][BANKname]=fxrate[i]
            try:
                self.SS[self.BANKcurrency[BANKname][int(i/4)]][BANKname]=float(fxrate[i+1])
            except ValueError:
                self.SS[self.BANKcurrency[BANKname][int(i/4)]][BANKname]=fxrate[i+1]
            try:
                self.CB[self.BANKcurrency[BANKname][int(i/4)]][BANKname]=float(fxrate[i+2])
            except ValueError:
                self.CB[self.BANKcurrency[BANKname][int(i/4)]][BANKname]=fxrate[i+2]
            try:
                self.CS[self.BANKcurrency[BANKname][int(i/4)]][BANKname]=float(fxrate[i+3])
            except ValueError:
                self.CS[self.BANKcurrency[BANKname][int(i/4)]][BANKname]=fxrate[i+3]
        
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
            
            self.SCSB('兆豐銀行', fxrate)

            print('MEGA {}'.format(time.time()-MEGAs))
        
        except :
            self.disconnectlist.append('兆豐銀行')




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
        
            for i in range(0,len(self.BANKcurrency['土地銀行'])*4):
                recordrate=findcol[i].get_text()
                fxrate.append(recordrate)
            print(len(fxrate))

            self.SCSB('土地銀行', fxrate)
            
            print('LAND {}'.format(time.time()-LANDs))
        

        except :
            self.disconnectlist.append('土地銀行')

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

            self.SCSB('第一銀行', fxrate)

            print('FIRST {}'.format(time.time()-FIRSTs))
        
        except :
            self.disconnectlist.append('第一銀行')

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
            self.SCSB('國泰世華銀行', fxrate)
            
            print('CATHAY {}'.format(time.time()-CATHAYs))
            
        except :
            self.disconnectlist.append('國泰世華銀行')

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
            for i in range(0,len(self.BANKcurrency['台新銀行'])*4):
                fxrate.append(findcol[i].get_text())
            print(len(fxrate))
        
            self.SCSB('台新銀行', fxrate)

            print('TAISHIN {}'.format(time.time()-TAISHINs))
        
        except :
            self.disconnectlist.append('台新銀行')

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

            fxrate=[]
            for i in range(0,len(self.BANKcurrency['中國信託商業銀行'])*4):
                if len(findcol[i].get_text())>0:
                    fxrate.append(findcol[i].get_text())
                else:
                    fxrate.append('--')
            print(len(fxrate))

            self.SCSB('中國信託商業銀行', fxrate)

            print('CTBC {}'.format(time.time()-CTBCs))
        
        except :
            self.disconnectlist.append('中國信託商業銀行')

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
        
            self.SCSB('永豐銀行', fxrate)

            print('SINOPAC {}'.format(time.time()-SINOPACs))
        
        except :
            self.disconnectlist.append('永豐銀行')

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
            
            self.SCSB('凱基銀行', fxrate)

            print('KGI {}'.format(time.time()-KGIs))
        
        except :
            self.disconnectlist.append('凱基銀行')


class ThreadPar(Thread):
    def __init__(self,parsing,bank):
        super().__init__()
        self.parsing = parsing
        self.bank = bank

    def run(self):
        self.parsing.BKpar[self.bank]()

class ReplyFX:
    def __init__(self,parsing):
        self.parsing = parsing
        self.replytxtlist = []
        self.compareresultlist=[]

    def comparebyTDtype(self,currency,BKselectedSET,tdtypeEN,EXTREME):
        tdtypeCHT=self.parsing.titleDICT[tdtypeEN][0]
        tdtype=self.parsing.titleDICT[tdtypeEN][1]
        
        #確認compareCURRENCY裡面的幣別有沒有在各家銀行的幣別清單裡,再確認有無現金賣出價格,把現金賣出價格加入comparelist當中        
        comparelist=[tdtype[currency][bk] for bk in BKselectedSET if bk not in self.parsing.disconnectlist and (currency in self.parsing.BANKcurrency[bk]) and isinstance(tdtype[currency][bk], float)]

        #從comparelist中選一個最小的數字,回傳幣別與銀行等訊息
        if len(comparelist) > 0 and EXTREME == 'MIN':
            minrate=min(comparelist)
             
            BESTretailer=[]
            for bk in BKselectedSET:
                if bk not in self.parsing.disconnectlist and currency in self.parsing.BANKcurrency[bk]: 
                    if minrate == tdtype[currency][bk]:
                        BESTretailer.append(bk)
                else:
                    pass
            self.compareresultlist.append('{BANK}的 {CURRENCY} {tdtypeCHT}最低價, 匯率為{FXrate}'.format(BANK=' 與 '.join(BESTretailer),CURRENCY=currency,tdtypeCHT=tdtypeCHT,FXrate=tdtype[currency][BESTretailer[0]]))
        elif len(comparelist) > 0 and EXTREME == 'MAX':
            maxrate=max(comparelist)
            
            BESTretailer=[]
            for bk in BKselectedSET:
                if bk not in self.parsing.disconnectlist and currency in self.parsing.BANKcurrency[bk]: 
                    if maxrate == tdtype[currency][bk]:
                        BESTretailer.append(bk)
                else:
                     pass
            self.compareresultlist.append('{BANK}的 {CURRENCY} {tdtypeCHT}最高價, 匯率為{FXrate}'.format(BANK=' 與 '.join(BESTretailer),CURRENCY=currency,tdtypeCHT=tdtypeCHT,FXrate=tdtype[currency][BESTretailer[0]]))    


    def showrate(self,inputmsg):
        print('disconnectlist is ',self.parsing.disconnectlist)
        compareCurrency=set()
        BKselectedSET=set()
        try:
            textFX=inputmsg.split(' ')[0]
            textBK=inputmsg.split(' ')[1]
            for c in set(self.parsing.CURRENCY.keys()):
                if re.search(c, textFX, re.IGNORECASE) or (self.parsing.CURRENCY[c] in textFX) or (textFX in self.parsing.CURRENCY[c] and textFX != ('幣','元','圓')):
                    compareCurrency.add(c)
            print(compareCurrency)
            for keyindex in range(0,len(textBK)):
                try:
                    for bk in self.parsing.BANKkeywords[textBK[keyindex]]:
                        BKselectedSET.add(bk)
                except:
                    pass
            print(BKselectedSET)
        
            threads = [ThreadPar(self.parsing,bk) for bk in BKselectedSET]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            
            for bk in BKselectedSET:
                for c in compareCurrency:
                    print(c)
                    if c in self.parsing.BANKcurrency[bk] and bk not in self.parsing.disconnectlist:
                        self.replytxtlist.append(bk+' '+c+':\n'+
                                            self.parsing.titleDICT['SB'][0]+' '+str(self.parsing.SB[c][bk])+'\n'+
                                            self.parsing.titleDICT['SS'][0]+' '+str(self.parsing.SS[c][bk])+'\n'+
                                            self.parsing.titleDICT['CB'][0]+' '+str(self.parsing.CB[c][bk])+'\n'+
                                            self.parsing.titleDICT['CS'][0]+' '+str(self.parsing.CS[c][bk])+'\n')
                    elif bk not in self.parsing.disconnectlist:
                        self.replytxtlist.append(bk+' 沒有提供 '+c)
                    else:
                        pass

            if len(BKselectedSET) >1:   
                for currency in compareCurrency:
                    self.comparebyTDtype(currency,BKselectedSET,'SB','MAX')
                    self.comparebyTDtype(currency,BKselectedSET,'SS','MIN')
                    self.comparebyTDtype(currency,BKselectedSET,'CB','MAX')
                    self.comparebyTDtype(currency,BKselectedSET,'CS','MIN')
            
                self.replytxtlist.extend(self.compareresultlist)
                
                    
            if len(self.parsing.disconnectlist) > 0:
                self.replytxtlist.append('{} 無法連線'.format(' 與 '.join(self.parsing.disconnectlist)))
    
            self.replytxt='\n'.join(self.replytxtlist)

            if len(self.replytxt) == 0:
                self.replytxt='阿ㄆㄧㄚˇ哥聽不懂 '+inputmsg+' 也許凱子知道那是什麼...'
        except :            
            self.replytxt='阿ㄆㄧㄚˇ哥聽不懂 '+inputmsg+' 也許凱子知道那是什麼...' 



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    
    text = event.message.text #message from user
    
    if re.search('HELP', text, re.IGNORECASE)==None:
        par=parsing()
        reply=ReplyFX(par)
        reply.showrate(text)
                  
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply.replytxt))
    else:
        pass

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])

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

for i in range(0,len(list(CURRENCY.keys()))):
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
BANKset=set(BANKcurrency.keys())

BANKkeywords={}
for bk in BANKset:
    for word in bk.strip("銀行").strip("商業"):
        if word in BANKkeywords.keys():
            BANKkeywords[word].add(bk)
        else:
            BANKkeywords[word]={bk}


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
        
        global BKpar
        BKpar={'兆豐銀行' : self.MEGApar,
               '土地銀行' : self.LANDpar,
               '第一銀行' : self.FIRSTpar,
               '國泰世華銀行' : self.CATHAYpar,
               '台新銀行' : self.TAISHINpar,
               '中國信託商業銀行' : self.CTBCpar,
               '永豐銀行' : self.SINOPACpar,
               '凱基銀行' : self.KGIpar}
        
    def MEGApar(self):
        
        try:
        
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
        
        except:
            disconnectlist.append('兆豐銀行')




    def LANDpar(self):
        
        try:

            url = 'https://ebank.landbank.com.tw/infor/infor.aspx?__eventtarget=querycurrency'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            res=requests.get(url)       
            res.encoding='UTF-8'
            restext=res.text
        
            bs=BeautifulSoup(restext, "html.parser")
        
            tableRATE=bs.find("table", {'class':'disptab'})

            fxrate=[]
        
            for i in range(0,len(BANKcurrency['土地銀行'])*4):
                recordrate=tableRATE.findAll("td",{'align':'Right'})[i].get_text()
                fxrate.append(recordrate)
            print(len(fxrate))

            SCSB('土地銀行', fxrate)
        

        except :
            disconnectlist.append('土地銀行')

    def FIRSTpar(self):
    
        try:

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
        
        except :
            disconnectlist.append('第一銀行')

    def CATHAYpar(self):
    
        try:

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
        except :
            disconnectlist.append('國泰世華銀行')

    def TAISHINpar(self):
    
        try:

            url = 'https://www.taishinbank.com.tw/TS/TS06/TS0605/TS060502/index.htm?urlPath1=TS02&urlPath2=TS0202'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            res=requests.get(url, headers=header)       
            res.encoding='UTF-8'
            restext=res.text

            bs=BeautifulSoup(restext, "html.parser")
        
            fxrate=[]
            for i in range(0,len(BANKcurrency['台新銀行'])*4):
                fxrate.append(bs.findAll("td",{'align':'center'})[i].get_text())
            print(len(fxrate))
        
            SCSB('台新銀行', fxrate)
        
        except :
            disconnectlist.append('台新銀行')

    def CTBCpar(self):
    
        try:

            url = 'https://www.ctbcbank.com/CTCBPortalWeb/toPage?id=TW_RB_CM_ebank_018001'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            res=requests.get(url)
        
            res.encoding='UTF-8'

            restext=res.text

            bs=BeautifulSoup(restext, "html.parser")
        

            fxrate=[]
            for i in range(0,len(BANKcurrency['中國信託商業銀行'])*4):
                if len(bs.findAll("td",{'class':'defaultDash column_text'})[i].get_text())>0:
                    fxrate.append(bs.findAll("td",{'class':'defaultDash column_text'})[i].get_text())
                else:
                    fxrate.append('--')
            print(len(fxrate))

            SCSB('中國信託商業銀行', fxrate)
        
        except :
            disconnectlist.append('中國信託商業銀行')

    def SINOPACpar(self):
    
        try:

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
        
        except :
            disconnectlist.append('永豐銀行')

    def KGIpar(self):
    
        try:

            url = 'https://www.kgibank.com/T01/T0111/rate03.jsp'
            header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

            res=requests.get(url)
        
            res.encoding='UTF-8'

            restext=res.text

            bs=BeautifulSoup(restext, "html.parser")
            fxrate=[]
            for i in range(10,len(bs.findAll("td"))):
                if len(bs.findAll("td")[i].get_text())>0 and i%10 in (2,3,4,5):
                    fxrate.append(bs.findAll("td")[i].get_text())
                elif len(bs.findAll("td")[i].get_text())==0:
                    fxrate.append('--')
                else:
                    pass           
            print(len(fxrate))
            
            SCSB('凱基銀行', fxrate)
        
        except :
            disconnectlist.append('凱基銀行')

def showrate(inputmsg):
    global replytxtlist, replytxt, disconnectlist
    replytxtlist=[]
    compareCurrency=set()
    disconnectlist=[]
    chooseBKset=set()
    try:
        textFX=inputmsg.split(' ')[0]
        textBK=inputmsg.split(' ')[1]
        for i in set(CURRENCY.keys()):
            if re.search(i, textFX, re.IGNORECASE) or CURRENCY[i] in textFX or (textFX in CURRENCY[i] and textFX != ('幣','元','圓')):
                compareCurrency.add(i)
        print(compareCurrency)
        for i in range(0,len(textBK)):
            try:
                for j in BANKkeywords[textBK[i]]:
                    chooseBKset.add(j)
            except:
                pass
        print(chooseBKset)
        for i in chooseBKset:
            try:
                BKpar[i]()
                for j in compareCurrency:
                    if j in BANKcurrency[i]:
                        replytxtlist.append(i+' '+j+':\n'+
                                            Tlist[1]+' '+str(SB[j][i])+'\n'+
                                            Tlist[2]+' '+str(SS[j][i])+'\n'+
                                            Tlist[3]+' '+str(CB[j][i])+'\n'+
                                            Tlist[4]+' '+str(CS[j][i])+'\n')
                    else:
                        replytxtlist.append(i+' 沒有提供 '+j)
            except:
                pass
        
        if len(disconnectlist) > 0:
            replytxtlist.append(str(' 與 '.join(disconnectlist)+'無法連線'))
        replytxt='\n'.join(replytxtlist)       
        
        if len(replytxt) == 0:
            replytxt='阿ㄆㄧㄚˇ哥聽不懂 '+inputmsg+' 也許凱子知道那是什麼...'
    except:
       replytxt='阿ㄆㄧㄚˇ哥聽不懂 '+inputmsg+' 也許凱子知道那是什麼...'



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
        showrate(text)
                  
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=replytxt))
    else:
        pass

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])

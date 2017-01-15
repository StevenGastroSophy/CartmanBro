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

line_bot_api = LineBotApi('Cg/E1nZbM6LzTn9DRYVJmbTEG/UTlB0+ps0xAp9Io6ABiE8/EZaFl1ZeBfDy335uxNDUSaM+qgqsSzUV2N1qCUfZU02FvrVrfH2JO9k9ljfbbC3Y+zm77d851EPkVt5GlxL8i+mmJLdlTUi5q9SpcgdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('e7ffb93630e35d82110e58132aa344d2') #Your Channel Secret

Tlist=['幣別','即期買匯','現金買匯','即期賣匯','現金賣匯']
SB={}
CB={}
SS={}
CS={}

CURRENCY={'USD':'美金','HKD':'港幣','GBP':'英鎊','JPY':'日圓','AUD':'澳幣',
          'CAD':'加拿大幣','SGD':'新加坡幣','ZAR':'南非幣','SEK':'瑞典幣','CHF':'瑞士法郎',
          'THB':'泰幣','NZD':'紐西蘭幣','EUR':'歐元','KRW':'韓元','MYR':'馬來幣',
          'IDR':'印尼幣','PHP':'菲國比索','MOP':'澳門幣','VND':'越南盾','CNY':'人民幣'}

for i in range(0,len(list(CURRENCY.keys()))):
    SB[list(CURRENCY.keys())[i]]={}
    CB[list(CURRENCY.keys())[i]]={}
    SS[list(CURRENCY.keys())[i]]={}
    CS[list(CURRENCY.keys())[i]]={}

print(SB) ; print(CB) ; print(SS) ; print(CS)
print(len(SB)) ; print(len(CB)) ; print(len(SS)) ; print(len(CS))

LANDcurrency=['USD', 'JPY', 'GBP', 'HKD', 'AUD',
              'CAD', 'SGD', 'CHF', 'SEK', 'ZAR',
              'THB', 'NZD', 'EUR', 'CNY']


def par():
    
    try:

        url = 'https://ebank.landbank.com.tw/infor/infor.aspx?__eventtarget=querycurrency'
        header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

        res=requests.get(url)
        
        res.encoding='UTF-8'

        restext=res.text
        
        bs=BeautifulSoup(restext, "html.parser")

        tableTIME=bs.find("table", {'id':'tblDisplay'})
        timeCHT=tableTIME.find("span",{'class':'TimeText'}).get_text()
        timeCHT=timeCHT.strip('資料時間 : ')
        timeCHT=timeCHT.replace('年','/') ; timeCHT=timeCHT.replace('月','/') ; timeCHT=timeCHT.replace('日','')
        LANDtime=timeCHT[:-3]
        print(LANDtime)
        
        tableRATE=bs.find("table", {'class':'disptab'})

        fxrate=[]
        
        for i in range(0,56):
            recordrate=tableRATE.findAll("td",{'align':'Right'})[i].get_text()
            fxrate.append(recordrate)
        print(fxrate)
        print(len(fxrate))

        for i in range(0,int(len(LANDcurrency)*4),4):
            try:
                SB[LANDcurrency[int(i/4)]]['土地銀行']=float(fxrate[i])
            except ValueError:
                pass
            try:
                SS[LANDcurrency[int(i/4)]]['土地銀行']=float(fxrate[i+1])
            except ValueError:
                pass
            try:
                CB[LANDcurrency[int(i/4)]]['土地銀行']=float(fxrate[i+2])
            except ValueError:
                pass
            try:
                CS[LANDcurrency[int(i/4)]]['土地銀行']=float(fxrate[i+3])
            except ValueError:
                pass

        print(SB) ; print(len(SB))
        print(SS) ; print(len(SS))
        print(CB) ; print(len(CB))
        print(CS) ; print(len(CS))
        print(type(SB['SGD']['土地銀行']))
        

    except requests.exceptions.ConnectionError:
        pass

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

    par()
    replytxt=SB['SGD']['土地銀行']

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=replytxt)) 
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])

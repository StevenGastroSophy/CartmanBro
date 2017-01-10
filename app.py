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

global Flist,Tlist

Flist = ['USD','HKD','GBP','JPY','AUD','CAD','SGD','ZAR','SEK','CHF','THB','NZD','EUR','KRW','MYR','IDR','PHP','MOP','VND','CNY']
Tlist = ['幣別','即期買匯','現金買匯','即期賣匯','現金賣匯']

def par():
    
    try:
        
        urlviewF = 'https://wwwfile.megabank.com.tw/rates/M001/viewF.asp'
        resF = requests.get(urlviewF)
        cookievalue = dict(resF.cookies)['mega%5Fstatus']


        urlV = 'https://wwwfile.megabank.com.tw/rates/D001/_@V_.asp'
        header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
        cookie = {'mega%5Fstatus':cookievalue}


        resV = requests.get(urlV, cookies=cookie)


        resV.encoding = 'UTF-8'

        resVtext = resV.text


        strtext = str()
        strlist = list()

        strtext = resVtext.replace('__header_=0;','')
        strtext = strtext.replace('#','')
        strtext = strtext.replace('col2','現金買匯')
        strtext = strtext.replace('col3','即期賣匯')
        strtext = strtext.replace('col0','幣別')
        strtext = strtext.replace('col1','即期買匯')
        strtext = strtext.replace('col4','現金賣匯')

        global USD,HKD,GBP,JPY,AUD,CAD,SGD,ZAR,SEK,CHF,THB,NZD,EUR,KRW,MYR,IDR,PHP,MOP,VND,CNY,FTime

        strtext = strtext.strip('\n')
        strlist = strtext.split(';')
        del strlist[-1]
        splitime = strlist[0].split('|')
        Ftime = splitime[0]+' '+splitime[1]
        strlist[0] = splitime[2]


        for i in range(0,len(strlist),5):
            strlist[i],strlist[i+1],strlist[i+2],strlist[i+3],strlist[i+4] = strlist[i+2],strlist[i+3],strlist[i],strlist[i+1],strlist[i+4]

        print(strlist)


        USD={};HKD={};GBP={};JPY={};AUD={}
        CAD={};SGD={};ZAR={};SEK={};CHF={}
        THB={};NZD={};EUR={};KRW={};MYR={}
        IDR={};PHP={};MOP={};VND={};CNY={}

        for x in range(0,5):
            USD[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(5,10):
            HKD[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(10,15):
            GBP[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(15,20):
            JPY[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(20,25):
            AUD[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(25,30):
            CAD[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(30,35):
            SGD[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(35,40):
            ZAR[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(40,45):
            SEK[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(45,50):
            CHF[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(50,55):
            THB[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(55,60):
            NZD[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(60,65):
            EUR[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(65,70):
            KRW[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(70,75):
            MYR[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(75,80):
            IDR[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(80,85):
            PHP[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(85,90):
            MOP[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(90,95):
            VND[strlist[x].split('=')[0]] = strlist[x].split('=')[1]
        for x in range(95,100):
            CNY[strlist[x].split('=')[0]] = strlist[x].split('=')[1]



        

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

    try:
        
        if re.search(Flist[0], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            USDreply = replySTD.format(FX=USD[Tlist[0]], tSB=Tlist[1], SB=USD[Tlist[1]], tCB=Tlist[2], CB=USD[Tlist[2]],
                                       tSS=Tlist[3], SS=USD[Tlist[3]], tCS=Tlist[4], CS=USD[Tlist[4]], TIME=FTime)
            replytxt=USDreply
            
        elif re.search(Flist[1], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            HKDreply = replySTD.format(FX=HKD[Tlist[0]], tSB=Tlist[1], SB=HKD[Tlist[1]], tCB=Tlist[2], CB=HKD[Tlist[2]],
                                       tSS=Tlist[3], SS=HKD[Tlist[3]], tCS=Tlist[4], CS=HKD[Tlist[4]], TIME=FTime)
            replytxt=HKDreply
        
        elif re.search(Flist[2], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            GBPreply = replySTD.format(FX=GBP[Tlist[0]], tSB=Tlist[1], SB=GBP[Tlist[1]], tCB=Tlist[2], CB=GBP[Tlist[2]],
                                       tSS=Tlist[3], SS=GBP[Tlist[3]], tCS=Tlist[4], CS=GBP[Tlist[4]], TIME=FTime)
            replytxt=GBPreply
    
        elif re.search(Flist[3], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            JPYreply = replySTD.format(FX=JPY[Tlist[0]], tSB=Tlist[1], SB=JPY[Tlist[1]], tCB=Tlist[2], CB=JPY[Tlist[2]],
                                       tSS=Tlist[3], SS=JPY[Tlist[3]], tCS=Tlist[4], CS=JPY[Tlist[4]], TIME=FTime)
            replytxt=JPYreply
    
        elif re.search(Flist[4], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            AUDreply = replySTD.format(FX=AUD[Tlist[0]], tSB=Tlist[1], SB=AUD[Tlist[1]], tCB=Tlist[2], CB=AUD[Tlist[2]],
                                       tSS=Tlist[3], SS=AUD[Tlist[3]], tCS=Tlist[4], CS=AUD[Tlist[4]], TIME=FTime)
            replytxt=AUDreply
            
        elif re.search(Flist[5], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            CADreply = replySTD.format(FX=CAD[Tlist[0]], tSB=Tlist[1], SB=CAD[Tlist[1]], tCB=Tlist[2], CB=CAD[Tlist[2]],
                                       tSS=Tlist[3], SS=CAD[Tlist[3]], tCS=Tlist[4], CS=CAD[Tlist[4]], TIME=FTime)
            replytxt=CADreply
            
        elif re.search(Flist[6], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            SGDreply = replySTD.format(FX=SGD[Tlist[0]], tSB=Tlist[1], SB=SGD[Tlist[1]], tCB=Tlist[2], CB=SGD[Tlist[2]],
                                       tSS=Tlist[3], SS=SGD[Tlist[3]], tCS=Tlist[4], CS=SGD[Tlist[4]], TIME=FTime)
            replytxt=SGDreply
            
        elif re.search(Flist[7], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            ZARreply = replySTD.format(FX=ZAR[Tlist[0]], tSB=Tlist[1], SB=ZAR[Tlist[1]], tCB=Tlist[2], CB=ZAR[Tlist[2]],
                                       tSS=Tlist[3], SS=ZAR[Tlist[3]], tCS=Tlist[4], CS=ZAR[Tlist[4]], TIME=FTime)
            replytxt=ZARreply
            
        elif re.search(Flist[8], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            SEKreply = replySTD.format(FX=SEK[Tlist[0]], tSB=Tlist[1], SB=SEK[Tlist[1]], tCB=Tlist[2], CB=SEK[Tlist[2]],
                                       tSS=Tlist[3], SS=SEK[Tlist[3]], tCS=Tlist[4], CS=SEK[Tlist[4]], TIME=FTime)
            replytxt=SEKreply
        
        elif re.search(Flist[9], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            CHFreply = replySTD.format(FX=CHF[Tlist[0]], tSB=Tlist[1], SB=CHF[Tlist[1]], tCB=Tlist[2], CB=CHF[Tlist[2]],
                                       tSS=Tlist[3], SS=CHF[Tlist[3]], tCS=Tlist[4], CS=CHF[Tlist[4]], TIME=FTime)
            replytxt=CHFreply
            
        elif re.search(Flist[10], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            THBreply = replySTD.format(FX=THB[Tlist[0]], tSB=Tlist[1], SB=THB[Tlist[1]], tCB=Tlist[2], CB=THB[Tlist[2]],
                                       tSS=Tlist[3], SS=THB[Tlist[3]], tCS=Tlist[4], CS=THB[Tlist[4]], TIME=FTime)
            replytxt=THBreply
            
        elif re.search(Flist[11], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            NZDreply = replySTD.format(FX=NZD[Tlist[0]], tSB=Tlist[1], SB=NZD[Tlist[1]], tCB=Tlist[2], CB=NZD[Tlist[2]],
                                       tSS=Tlist[3], SS=NZD[Tlist[3]], tCS=Tlist[4], CS=NZD[Tlist[4]], TIME=FTime)
            replytxt=NZDreply
            
        elif re.search(Flist[12], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            EURreply = replySTD.format(FX=EUR[Tlist[0]], tSB=Tlist[1], SB=EUR[Tlist[1]], tCB=Tlist[2], CB=EUR[Tlist[2]],
                                       tSS=Tlist[3], SS=EUR[Tlist[3]], tCS=Tlist[4], CS=EUR[Tlist[4]], TIME=FTime)
            replytxt=EURreply
            
        elif re.search(Flist[13], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            KRWreply = replySTD.format(FX=KRW[Tlist[0]], tSB=Tlist[1], SB=KRW[Tlist[1]], tCB=Tlist[2], CB=KRW[Tlist[2]],
                                       tSS=Tlist[3], SS=KRW[Tlist[3]], tCS=Tlist[4], CS=KRW[Tlist[4]], TIME=FTime)
            replytxt=KRWreply
            
        elif re.search(Flist[14], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            MYRreply = replySTD.format(FX=MYR[Tlist[0]], tSB=Tlist[1], SB=MYR[Tlist[1]], tCB=Tlist[2], CB=MYR[Tlist[2]],
                                       tSS=Tlist[3], SS=MYR[Tlist[3]], tCS=Tlist[4], CS=MYR[Tlist[4]], TIME=FTime)
            replytxt=MYRreply
            
        elif re.search(Flist[15], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            IDRreply = replySTD.format(FX=IDR[Tlist[0]], tSB=Tlist[1], SB=IDR[Tlist[1]], tCB=Tlist[2], CB=IDR[Tlist[2]],
                                       tSS=Tlist[3], SS=IDR[Tlist[3]], tCS=Tlist[4], CS=IDR[Tlist[4]], TIME=FTime)
            replytxt=IDRreply
            
        elif re.search(Flist[16], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            PHPreply = replySTD.format(FX=PHP[Tlist[0]], tSB=Tlist[1], SB=PHP[Tlist[1]], tCB=Tlist[2], CB=PHP[Tlist[2]],
                                       tSS=Tlist[3], SS=PHP[Tlist[3]], tCS=Tlist[4], CS=PHP[Tlist[4]], TIME=FTime)
            replytxt=PHPreply
        
        elif re.search(Flist[17], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            MOPreply = replySTD.format(FX=MOP[Tlist[0]], tSB=Tlist[1], SB=MOP[Tlist[1]], tCB=Tlist[2], CB=MOP[Tlist[2]],
                                       tSS=Tlist[3], SS=MOP[Tlist[3]], tCS=Tlist[4], CS=MOP[Tlist[4]], TIME=FTime)
            replytxt=MOPreply
        
        elif re.search(Flist[18], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            VNDreply = replySTD.format(FX=VND[Tlist[0]], tSB=Tlist[1], SB=VND[Tlist[1]], tCB=Tlist[2], CB=VND[Tlist[2]],
                                       tSS=Tlist[3], SS=VND[Tlist[3]], tCS=Tlist[4], CS=VND[Tlist[4]], TIME=FTime)
            replytxt=VNDreply
            
        elif re.search(Flist[19], text, re.IGNORECASE):
            par()
            replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}\n since {TIME}'
            CNYreply = replySTD.format(FX=CNY[Tlist[0]], tSB=Tlist[1], SB=CNY[Tlist[1]], tCB=Tlist[2], CB=CNY[Tlist[2]],
                                       tSS=Tlist[3], SS=CNY[Tlist[3]], tCS=Tlist[4], CS=CNY[Tlist[4]], TIME=FTime)
            replytxt=CNYreply
            
                                                            
        else:
            replytxt='Yo said that? '+text+'? Cartman braaaaaah!'
    except:
        replytxt='mmmm...there must be some problem with the server...'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=replytxt)) 
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])

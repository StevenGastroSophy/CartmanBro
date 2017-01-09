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

        strtext = strtext.strip('\n')
        strlist = strtext.split(';')
        del strlist[-1]
        splitime = strlist[0].split('|')
        Ftime = splitime[0]+' '+splitime[1]
        strlist[0] = splitime[2]


        for i in range(0,len(strlist),5):
            strlist[i],strlist[i+1],strlist[i+2],strlist[i+3],strlist[i+4] = strlist[i+2],strlist[i+3],strlist[i],strlist[i+1],strlist[i+4]

        print(strlist)

        global Flist,Tlist

        Flist = ['USD','HKD','GBP','JPY','AUD','CAD','SGD','ZAR','SEK','CHF','THB','NZD','EUR','KRW','MYR','IDR','PHP','MOP','VND','CNY']
        Tlist = ['幣別','即期買匯','現金買匯','即期賣匯','現金賣匯']
        global USD,HKD,GBP,JPY,AUD,CAD,SGD,ZAR,SEK,CHF,THB,NZD,EUR,KRW,MYR,IDR,PHP,MOP,VND,CNY

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

        FTimeshname = Ftime.replace('/','')
        FTimeshname = FTimeshname.replace(':','')

        

    except requests.exceptions.ConnectionError:
        global cannotcon
        cannotcon = "Cannot connect megabank's server. "

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
    
    if text == Flist[0]:
        par()
        replySTD = '{FX} :\n{tSB} : {SB}\n{tCB} : {CB}\n{tSS} : {SS}\n{tCS} : {CS}'
        USDreply = replySTD.fotmat(FX=USD[Tlist[0]], tSB=Tlist[1], SB=USD[Tlist[1]], tCB=Tlist[2], CB=USD[Tlist[2]],
                                   tSS=Tlist[3], SS=USD[Tlist[3]], tCS=Tlist[4], CS=USD[Tlist[4]])
        replytxt=USDreply
    else:
        replytxt='Yo said that? '+text+'? Cartman braaaaaah!'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=replytxt)) 
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])

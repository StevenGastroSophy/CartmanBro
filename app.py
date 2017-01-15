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

BANKcurrency={'兆豐銀行':['USD','HKD','GBP','JPY','AUD',
              'CAD','SGD','ZAR','SEK','CHF',
              'THB','NZD','EUR','KRW','MYR',
              'IDR','PHP','MOP','VND','CNY'],
              '土地銀行':['USD', 'JPY', 'GBP', 'HKD', 'AUD',
              'CAD', 'SGD', 'CHF', 'SEK', 'ZAR',
              'THB', 'NZD', 'EUR', 'CNY']}
BANKlist=BANKcurrency.keys(

def MEGApar():
    
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
        strtext = strtext.replace('col2','現金買匯')
        strtext = strtext.replace('col3','即期賣匯')
        strtext = strtext.replace('col0','幣別')
        strtext = strtext.replace('col1','即期買匯')
        strtext = strtext.replace('col4','現金賣匯')

        strtext = strtext.strip('\n')
        strlist = strtext.split(';')
        del strlist[-1]
        splitime = strlist[0].split('|')
        
        global MEGAtime
        MEGAtime = splitime[0]+' '+splitime[1]
        
        strlist[0]=splitime[2]

        for i in range(0,len(strlist),5):
            strlist[i],strlist[i+1],strlist[i+2],strlist[i+3],strlist[i+4]=strlist[i+2],strlist[i+3],strlist[i],strlist[i+1],strlist[i+4]
        print(strlist)

        fxrate=[]

        for i in range(0,100):
            if i%5 !=0:
                fxrate.append(strlist[i].split('=')[1])
        print(len(fxrate))
            
        for i in range(0,int(len(BANKcurrency['兆豐銀行'])*4),4):
            try:
                SB[BANKcurrency['兆豐銀行'][int(i/4)]]['兆豐銀行']=float(fxrate[i])
            except ValueError:
                SB[BANKcurrency['兆豐銀行'][int(i/4)]]['兆豐銀行']=fxrate[i]
            try:
                CB[BANKcurrency['兆豐銀行'][int(i/4)]]['兆豐銀行']=float(fxrate[i+1])
            except ValueError:
                CB[BANKcurrency['兆豐銀行'][int(i/4)]]['兆豐銀行']=fxrate[i+1]
            try:
                SS[BANKcurrency['兆豐銀行'][int(i/4)]]['兆豐銀行']=float(fxrate[i+2])
            except ValueError:
                SS[BANKcurrency['兆豐銀行'][int(i/4)]]['兆豐銀行']=fxrate[i+2]
            try:
                CS[BANKcurrency['兆豐銀行'][int(i/4)]]['兆豐銀行']=float(fxrate[i+3])
            except ValueError:
                CS[BANKcurrency['兆豐銀行'][int(i/4)]]['兆豐銀行']=fxrate[i+3]

        print(SB) ; print(CB)
        print(SS) ; print(CS)
        print(len(SB)) ; print(len(CB))
        print(len(SS)) ; print(len(CS))
        print(type(SB['SGD']['兆豐銀行']))
        
    except requests.exceptions.ConnectionError:
        pass




def LANDpar():
    
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

        global LANDtime
        LANDtime=timeCHT[:-3]
        print(LANDtime)
        
        tableRATE=bs.find("table", {'class':'disptab'})

        fxrate=[]
        
        for i in range(0,56):
            recordrate=tableRATE.findAll("td",{'align':'Right'})[i].get_text()
            fxrate.append(recordrate)
        print(fxrate)
        print(len(fxrate))

        for i in range(0,int(len(BANKcurrency['土地銀行'])*4),4):
            try:
                SB[BANKcurrency['土地銀行'][int(i/4)]]['土地銀行']=float(fxrate[i])
            except ValueError:
                SB[BANKcurrency['土地銀行'][int(i/4)]]['土地銀行']=fxrate[i]
            try:
                SS[BANKcurrency['土地銀行'][int(i/4)]]['土地銀行']=float(fxrate[i+1])
            except ValueError:
                SS[BANKcurrency['土地銀行'][int(i/4)]]['土地銀行']=fxrate[i+1]
            try:
                CB[BANKcurrency['土地銀行'][int(i/4)]]['土地銀行']=float(fxrate[i+2])
            except ValueError:
                CB[BANKcurrency['土地銀行'][int(i/4)]]['土地銀行']=fxrate[i+2]
            try:
                CS[BANKcurrency['土地銀行'][int(i/4)]]['土地銀行']=float(fxrate[i+3])
            except ValueError:
                CS[BANKcurrency['土地銀行'][int(i/4)]]['土地銀行']=fxrate[i+3]

        print(SB) ; print(len(SB))
        print(SS) ; print(len(SS))
        print(CB) ; print(len(CB))
        print(CS) ; print(len(CS))
        print(type(SB['SGD']['土地銀行']))
        

    except requests.exceptions.ConnectionError:
        pass

def compare(inputmsg):
    replytxtlist=[]
    global replytxt
    MEGApar()
    LANDpar()
    try:
        compareCurrency=[]
        #用CURRENCY的key跟value去比對inputmsg裡面有沒有中英文幣別訊息,把幣別訊息加入compareCURRENCY裡面
        for i in list(CURRENCY.keys()):
            if i in inputmsg or CURRENCY[i] in inputmsg:
                compareCurrency.append(i)
        print(compareCurrency)
        #先確認compareCURRENCY裡面的幣別有沒有在各家銀行的幣別清單裡,再確認有無現金賣出價格,把現金賣出價格加入comparelist當中
        for i in compareCurrency:
            comparelist=[]
            for j in BANKlist:
                if i in BANKcurrency[j] and isinstance(CS[i][j], float):
                    comparelist.append(CS[i][j])
            #從comparelist中選一個最小的數字,回傳幣別與銀行等訊息
            minrate=min(comparelist)
            
            BESTretailer=[]
            for j in BANKlist:
                if minrate == CS[i][j]:
                    BESTretailer.append(j)     
            replytxtlist.append(str(BESTretailer)+'買 '+i+' 最便宜, 匯率為'+str(CS[i][BESTretailer[0]]))
        replytxt=replytxtlist[0]
            
    except:
        replytxt='mmmm...there must be some problem with the server...'

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

    replytxt='沒有變化'
    
    compare(text)
         
         
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(replytxt)))

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])

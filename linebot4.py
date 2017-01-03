#encoding=UTF-8
"""
Datetime:2016/12/17
Author:Ethan.Y
Purpose:
1.練習使用Line Messaging API
2.練習閱讀官方的Document
Functions:
1.收到訊息之後回復
2.若收到的訊息當中還有(掰掰)字串，則回應特定內容
3.如果訊息開頭加上小寫(dic)，則回傳到yahoo dictionary查詢的結果。EX:dic apple，則回傳查詢apple的結果。
"""
from flask import Flask,request
import requests
import json #回呼api的時候，需要將data透過json.dumps(data)做處理。
import re
from bs4 import BeautifulSoup as bs
#可以直接利用Line提供的SDK來處理，但在這個練習的程式碼當中，先暫時沒有使用。
#from linebot import LineBotApi
#from linebot.models import TextSendMessage

app = Flask(__name__)

@app.route("/",methods=["GET"])
def index():
    return "hello world",200

#在Line的Document當中有寫到，webhook URL會透過post request呼叫 https://{urladdress}/callback
@app.route("/callback",methods=["POST"])
def index2():
    temp = request.get_json()
    for i in temp['events']:
            ttt=i['replyToken']
            print(i['source']['userId'])
            if i['message']['type']=='text':
                msg = i['message']['text']
                replyapi(ttt,msg)
    return "hello world",200
    
def replyapi(accesstoken,msg):
    channeltoken={'Cg/E1nZbM6LzTn9DRYVJmbTEG/UTlB0+ps0xAp9Io6ABiE8/EZaFl1ZeBfDy335uxNDUSaM+qgqsSzUV2N1qCUfZU02FvrVrfH2JO9k9ljfbbC3Y+zm77d851EPkVt5GlxL8i+mmJLdlTUi5q9SpcgdB04t89/1O/w1cDnyilFU='}   
    
    #下面註解起來的程式碼，是利用Line SDK的方式，做reply的作業。   

    t = msg.encode('utf-8')
    count=0
    if 'dic' in t:
        a = t.split(" ")
        print(a[1])
        res = requests.get('http://tw.dictionary.search.yahoo.com/search?p='+a[1])
        print(res.status_code)
        soup = bs(res.content,'html.parser')
        ttt = soup.find_all('ul',attrs={'class':'compArticleList mb-15 ml-10'})
        outputstring = ""
        for i in ttt:
            outputstring += (i.text.encode('utf-8') + '\n')
            count=1
        print(outputstring)
        mat=[]
    else:
        pat = re.compile(r".*(掰掰).*")
        print(type(msg))
        mat = pat.findall(t)
    
    if len(mat)==0:
        if count==1:
            data={
            'replyToken':accesstoken,
            'messages':[{'type':'text','text':outputstring}]
            }
        else:
            data={
            'replyToken':accesstoken,
            'messages':[{'type':'text','text':'朕知道了'},{'type':'text','text':'可以退下了'}]
            }
    else:
        data={
        'replyToken':accesstoken,
        'messages':[{'type':'text','text':'慢走不送'}]
        }
    
    headers={'Content-Type':'application/json','Authorization':'Bearer '+channeltoken}
    urladdress = 'https://api.line.me/v2/bot/message/reply'
    datajson = json.dumps(data)
    res=requests.post(urladdress,headers=headers,data=datajson)
    print(res.status_code)
    

if __name__=='__main__':
    app.run()

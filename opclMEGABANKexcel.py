import requests
from bs4 import BeautifulSoup
import xlwt
import os
import time
import datetime
import sched    
import tkinter as tk

wbook=xlwt.Workbook() #開啟一個虛擬的 excel試算表 wbook
FTimeshRecord=list()

class tradhrs:
    def __init__(self,op,cl):
        self.op=op #以小時形式表示的開盤與收盤時間
        self.cl=cl

    def opentime(self,time):
        if self.cl>self.op:
            self.open=datetime.datetime(time.year, time.month, time.day,self.op,0,0)
        elif self.cl<self.op:
            timeplusoned=time+datetime.timedelta(days=1)
            self.open=datetime.datetime(time.year, time.month, time.day,self.op,0,0)
        return self.open #完整的開盤時間

    def closetime(self,time):
        if self.cl>self.op:
            self.close=datetime.datetime(time.year, time.month, time.day,self.cl,0,0)
        elif self.cl<self.op:
            timeplusoned=time+datetime.timedelta(days=1)
            self.close=datetime.datetime(timeplusoned.year, timeplusoned.month, timeplusoned.day,self.cl,0,0)
        return self.close #完整的收盤時間

TWFX=tradhrs(9,16)

FXmarket=TWFX #開盤/收盤時間依照台灣匯市




def par():
    
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
        Ftime = splitime[0]+' '+splitime[1]
        strlist[0]=splitime[2]


        for i in range(0,len(strlist),5):
            strlist[i],strlist[i+1],strlist[i+2],strlist[i+3],strlist[i+4]=strlist[i+2],strlist[i+3],strlist[i],strlist[i+1],strlist[i+4]

        print(strlist)    

        Flist=['USD','HKD','GBP','JPY','AUD','CAD','SGD','ZAR','SEK','CHF','THB','NZD','EUR','KRW','MYR','IDR','PHP','MOP','VND','CNY']
        Tlist=['幣別','即期買匯','現金買匯','即期賣匯','現金賣匯']

        USD={};HKD={};GBP={};JPY={};AUD={}
        CAD={};SGD={};ZAR={};SEK={};CHF={}
        THB={};NZD={};EUR={};KRW={};MYR={}
        IDR={};PHP={};MOP={};VND={};CNY={}

        for x in range(0,5):
            USD[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(5,10):
            HKD[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(10,15):
            GBP[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(15,20):
            JPY[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(20,25):
            AUD[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(25,30):
            CAD[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(30,35):
            SGD[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(35,40):
            ZAR[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(40,45):
            SEK[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(45,50):
            CHF[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(50,55):
            THB[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(55,60):
            NZD[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(60,65):
            EUR[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(65,70):
            KRW[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(70,75):
            MYR[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(75,80):
            IDR[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(80,85):
            PHP[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(85,90):
            MOP[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(90,95):
            VND[strlist[x].split('=')[0]]=strlist[x].split('=')[1]
        for x in range(95,100):
            CNY[strlist[x].split('=')[0]]=strlist[x].split('=')[1]

        FTimeshname=Ftime.replace('/','')
        FTimeshname=FTimeshname.replace(':','')
    

        if FTimeshname not in FTimeshRecord:
            wsheet=wbook.add_sheet(FTimeshname) #在 wbook裡面加入工作表 wsheet
            FTimeshRecord.append(FTimeshname)
            for x in range(0,5):
                wsheet.write(0,x,Tlist[x]) ; wsheet.write(1,x,USD[Tlist[x]])   
                wsheet.write(2,x,HKD[Tlist[x]]) ; wsheet.write(3,x,GBP[Tlist[x]])
                wsheet.write(4,x,JPY[Tlist[x]]) ; wsheet.write(5,x,AUD[Tlist[x]]) 
                wsheet.write(6,x,CAD[Tlist[x]]) ; wsheet.write(7,x,SGD[Tlist[x]])
                wsheet.write(8,x,ZAR[Tlist[x]]) ; wsheet.write(9,x,SEK[Tlist[x]])
                wsheet.write(10,x,CHF[Tlist[x]]) ; wsheet.write(11,x,THB[Tlist[x]])
                wsheet.write(12,x,NZD[Tlist[x]]) ; wsheet.write(13,x,EUR[Tlist[x]])
                wsheet.write(14,x,KRW[Tlist[x]]) ; wsheet.write(15,x,MYR[Tlist[x]])
                wsheet.write(16,x,IDR[Tlist[x]]) ; wsheet.write(17,x,PHP[Tlist[x]])
                wsheet.write(18,x,MOP[Tlist[x]]) ; wsheet.write(19,x,VND[Tlist[x]])
                wsheet.write(20,x,CNY[Tlist[x]])
                x+=1
            print('add sheet')
        labelCount.configure(text="目前共有"+str(len(FTimeshRecord))+"筆資料",font=30,height=5)
        print('FTimeshRecord is '+str(FTimeshRecord))
    except requests.exceptions.ConnectionError:
        timediscon=datetime.datetime.today()
        labelStat.configure(text="無法連線到網站,於 "+timediscon.strftime("%Y/%m/%d %H:%M:%S")+"停止抓取",font=30,height=5)
        buttonStart['state'] = 'normal'
def export():
    try:
        timexp=time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(time.time()))
        timexpname=time.strftime("%Y%m%d %H%M%S",time.localtime(time.time()))
        wbook.save('FXrate'+timexpname+'.xls') #把虛擬的 wbook另存新檔
        labelStat.configure(text="輸出成功於 "+timexp,font=30,height=5)
    except PermissionError:
        labelStat.configure(text="請關閉 FXrate.xls再輸出檔案",font=30,height=5)
    except IndexError:
        labelStat.configure(text="請關閉 FXrate.xls再輸出檔案",font=30,height=5)
            
        
    
        
def start():
    try:
        buttonStart['state'] = 'disabled'
        timestart=datetime.datetime.today()
        print('timestart is: '+str(timestart))

        hrs=ehr.get() ; mis=emi.get()
        if ehr.get()=='':
            hrs=0  
        if emi.get()=='':
            mis=0
        hr=datetime.timedelta(hours=int(hrs)) ; mi=datetime.timedelta(minutes=int(mis))
        global timestop
        timestop=timestart+hr+mi
        print('timestop is: '+str(timestop))

        
        FXOP=FXmarket.opentime(timestart)
        FXCL=FXmarket.closetime(timestop)
        print("FXmarket.opentime(timestart) is "+str(FXmarket.opentime(timestart)))
        print("FXmarket.closetime(timestop) is "+str(FXmarket.closetime(timestop)))

        plusoned=timestart+datetime.timedelta(days=1)
        nextopen=datetime.datetime(plusoned.year, plusoned.month, plusoned.day,FXmarket.op,0,0)
        
        if FXCL>timestart>=FXOP:
            startmod=timestart
        elif FXOP>timestart and timestop>datetime.datetime(timestart.year, timestart.month, timestart.day,FXmarket.op,0,0):
            startmod=datetime.datetime(timestart.year, timestart.month, timestart.day,FXmarket.op,0,0)
        elif FXOP>timestart and datetime.datetime(timestart.year, timestart.month, timestart.day,FXmarket.op,0,0)>timestop:
            startmod=timestart
        elif timestart>=FXCL and timestop>=nextopen:
            startmod=nextopen
        elif timestart>=FXCL and nextopen>timestop:
            startmod=timestart
        print('startmod is: '+str(startmod))
        
        if FXCL>timestop>=FXOP:
            stopmod=timestop
        elif FXOP>timestop:
            subtroned=timestop-datetime.timedelta(days=1)
            stopmod=datetime.datetime(subtroned.year, subtroned.month, subtroned.day,FXmarket.cl,1,0)
        elif timestop>=FXCL:
            stopmod=datetime.datetime(timestop.year, timestop.month, timestop.day,FXmarket.cl,1,0)

        print('stopmod is: '+str(stopmod))
        timestopstr=timestop.strftime("%Y/%m/%d %H:%M:%S")
        labelStat.configure(text="將於"+timestopstr+"停止",font=30,height=5)
    
        while True:
            timenow=datetime.datetime.today()
            print(timenow)
            
            if startmod.strftime("%Y/%m/%d %H:%M:%S")>timenow.strftime("%Y/%m/%d %H:%M:%S") :
                par()
                print('等待 '+str((startmod-timenow).seconds)+' 秒後啟動')
                labelStat.configure(text='等待 '+str((startmod-timenow).seconds)+' 秒後啟動',font=30,height=5)
                s = sched.scheduler(time.time, time.sleep)
                s.enter((startmod-timenow).seconds,0,startagain,())
                s.run()
            
            else:
                if timenow.strftime("%Y/%m/%d %H:%M:%S")>=stopmod.strftime("%Y/%m/%d %H:%M:%S") :
                    
                    labelStat.configure(text="抓取已停止",font=30,height=5)
                    par()
                    buttonExport['state'] = 'normal'
                    buttonStart['state'] = 'normal'
                    break
                elif timenow.second ==0:
                    par()
    except ValueError:
        labelStat.configure(text="X,Y 欄位只能輸入數字",font=30,height=5)
        buttonStart['state'] = 'normal'

        
def startagain():
    try:
        timestart=datetime.datetime.today()
        print('timestart is: '+str(timestart))

        FXOP=FXmarket.opentime(timestart)
        FXCL=FXmarket.closetime(timestop)
        print("FXmarket.opentime(timestart) is "+str(FXmarket.opentime(timestart)))
        print("FXmarket.closetime(timestop) is "+str(FXmarket.closetime(timestop)))

        plusoned=timestart+datetime.timedelta(days=1)
        nextopen=datetime.datetime(plusoned.year, plusoned.month, plusoned.day,FXmarket.op,0,0)
        
        if FXCL>timestart>=FXOP:
            startmod=timestart
        elif FXOP>timestart and timestop>datetime.datetime(timestart.year, timestart.month, timestart.day,FXmarket.op,0,0):
            startmod=datetime.datetime(timestart.year, timestart.month, timestart.day,FXmarket.op,0,0)
        elif FXOP>timestart and datetime.datetime(timestart.year, timestart.month, timestart.day,FXmarket.op,0,0)>timestop:
            startmod=timestart
        elif timestart>=FXCL and timestop>=nextopen:
            startmod=nextopen
        elif timestart>=FXCL and nextopen>timestop:
            startmod=timestart
        print('startmod is: '+str(startmod))
        
        if FXCL>timestop>=FXOP:
            stopmod=timestop
        elif FXOP>timestop:
            subtroned=timestop-datetime.timedelta(days=1)
            stopmod=datetime.datetime(subtroned.year, subtroned.month, subtroned.day,FXmarket.cl,1,0)
        elif timestop>=FXCL:
            stopmod=datetime.datetime(timestop.year, timestop.month, timestop.day,FXmarket.cl,1,0)

        print('stopmod is: '+str(stopmod))
        timestopstr=timestop.strftime("%Y/%m/%d %H:%M:%S")
        labelStat.configure(text="將於"+timestopstr+"停止",font=30,height=5)
    
        while True:
            timenow=datetime.datetime.today()
            print(timenow)
            
            if startmod.strftime("%Y/%m/%d %H:%M:%S")>timenow.strftime("%Y/%m/%d %H:%M:%S") :
                par()
                print('等待 '+str((startmod-timenow).seconds)+' 秒後啟動')
                labelStat.configure(text='等待 '+str((startmod-timenow).seconds)+' 秒後啟動',font=30,height=5)
                s = sched.scheduler(time.time, time.sleep)
                s.enter((startmod-timenow).seconds,0,startagain,())
                s.run()
            
            else:
                if timenow.strftime("%Y/%m/%d %H:%M:%S")>=stopmod.strftime("%Y/%m/%d %H:%M:%S") :
                    
                    labelStat.configure(text="抓取已停止",font=30,height=5)
                    par()
                    buttonExport['state'] = 'normal'
                    buttonStart['state'] = 'normal'
                    break
                elif timenow.second ==0:
                    par()
    except ValueError:
        labelStat.configure(text="X,Y 欄位只能輸入數字",font=30,height=5)
        buttonStart['state'] = 'normal'
  
MBS=chr(77)+chr(69)+chr(71)+chr(65)+chr(66)+chr(65)+chr(78)+chr(75)+chr(32)+chr(83)+chr(99)+chr(114)+chr(97)+chr(112)+chr(121)+chr(45)+chr(49)+chr(32)+chr(116)+chr(105)+chr(109)+chr(101)+chr(47)+chr(109)+chr(105)+chr(110)+chr(32)   
MBK=chr(77)+chr(97)+chr(100)+chr(101)+chr(32)+chr(98)+chr(121)+chr(32)+chr(75)+chr(97)+chr(115)+chr(112)+chr(101)+chr(114)

window=tk.Tk()
window.title(MBS+MBK)
window.geometry('300x400')

labelGuide=tk.Label(window, text="請按Start 開始,再按Export 輸出成XLS 檔案",font=30,height=5) 
labelGuide.grid(row=0,columnspan=2)

buttonStart=tk.Button(window,text='Start Crawling',width=15,height=2,font=30,command=start,state='normal')
buttonStart.grid(row=1, column=1, sticky="WE")

buttonExport=tk.Button(window,text='Export to XLS',width=15,height=2,font=30,command=export,state='disabled')
buttonExport.grid(row=1, column=0, sticky="WE")

labelCount=tk.Label(window, text="運作停止時會顯示資料筆數於此",font=30,height=5)
labelCount.grid(row=2,columnspan=2)

labelStat=tk.Label(window, text="將於X 小時Y 分後停止,收盤時間以16:01計",font=30,height=5)
labelStat.grid(row=3,columnspan=2)

labelX=tk.Label(window, text="X (取整數): ",font=30)
labelX.grid(row=4, column=0)

labelY=tk.Label(window, text="Y (取整數): ",font=30)
labelY.grid(row=4, column=1)

ehr=tk.Entry(window,width=10,show=None)
ehr.grid(row=5, column=0)

emi=tk.Entry(window,width=10,show=None)
emi.grid(row=5, column=1)

window.mainloop()













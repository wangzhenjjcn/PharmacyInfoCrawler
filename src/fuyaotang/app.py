#!/usr/bin/env python
#-*- coding:utf-8 -*-
try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

import os, sys,re,pygame,time,urllib,lxml,threading,time,requests,base64,json
import config
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from aip import AipSpeech

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('fuyaotang.com数据读取系统')
        self.master.geometry('792x485')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('ChromeControlFrame.TLabelframe',font=('宋体',9))
        self.ChromeControlFrame = LabelFrame(self.top, text='模拟器设置', style='ChromeControlFrame.TLabelframe')
        self.ChromeControlFrame.place(relx=0.758, rely=0.082, relwidth=0.234, relheight=0.827)

        self.style.configure('MainFrame.TLabelframe',font=('宋体',9))
        self.MainFrame = LabelFrame(self.top, text='操作中心', style='MainFrame.TLabelframe')
        self.MainFrame.place(relx=0.01, rely=0.082, relwidth=0.739, relheight=0.827)

        self.style.configure('InitialChromeBtn.TButton',font=('宋体',9))
        self.InitialChromeBtn = Button(self.ChromeControlFrame, text='初始化浏览器', command=self.InitialChromeBtn_Cmd, style='InitialChromeBtn.TButton')
        self.InitialChromeBtn.place(relx=0.173, rely=0.08, relwidth=0.611, relheight=0.082)

        self.ProgressBar1Var = StringVar(value='')
        self.ProgressBar1 = Progressbar(self.MainFrame, orient='horizontal', maximum=100, variable=self.ProgressBar1Var)
        self.ProgressBar1.place(relx=0.451, rely=0.898, relwidth=0.494, relheight=0.062)

        self.style.configure('DoReadBtn.TButton',font=('宋体',9))
        self.DoReadBtn = Button(self.MainFrame, text='下载选择的省市药店数据/下载所有', command=self.DoReadBtn_Cmd, style='DoReadBtn.TButton')
        self.DoReadBtn.place(relx=0.492, rely=0.239, relwidth=0.426, relheight=0.102)

        self.style.configure('ReadListBtn.TButton',font=('宋体',9))
        self.ReadListBtn = Button(self.MainFrame, text='读取省市列表', command=self.ReadListBtn_Cmd, style='ReadListBtn.TButton')
        self.ReadListBtn.place(relx=0.492, rely=0.08, relwidth=0.426, relheight=0.102)

        self.ProvinceCityListBoxVar = StringVar(value='点击读取省市列表以显示')
        self.ProvinceCityListBoxFont = Font(font=('宋体',9))
        self.ProvinceCityListBox = Listbox(self.MainFrame, listvariable=self.ProvinceCityListBoxVar, font=self.ProvinceCityListBoxFont,selectmode=EXTENDED)
        self.ProvinceCityListBox.place(relx=0.027, rely=0.06, relwidth=0.371, relheight=0.908)






class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        self.configs={}
        self.browser=None
        self.ProvinceURLList={}



    def InitialChromeBtn_Cmd(self, event=None):
        #TODO, Please finish the function here!
        d = threading.Thread(target=self.InitialChrome)
        d.start()
        pass

    def InitialChrome(self,event=None):
        if self.browser!=None:
            try:
                self.browser.quit()
                print('Close current page')
                pass
            except Exception as e:
                print("in Close current page")
                print(e)
        try:
            display=True
            login=False
            driverPath=os.path.dirname(os.path.realpath(sys.argv[0]))+"\\chromedriver.exe"
            chrome_options = webdriver.ChromeOptions()
            user_data_dir=self.getConf("最后用户目录地址","","一次性设置")
            if user_data_dir==None or user_data_dir=="" or not os.path.exists(user_data_dir):
                user_data_dir=os.getenv('TEMP')+"\\"+str(time.time()).replace(".","")+"\\"
                self.writeConfig("最后用户目录地址",user_data_dir,"一次性设置")
            chrome_options.add_argument('--user-data-dir='+user_data_dir)
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--profile-directory=Default')
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-plugins-discovery")
            chrome_options.add_argument("--start-maximized")
            if display:
                print("现在显示打开模式")
            else:
                print("显示处于后台模式")
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--enable-javascript')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--disable-popup-blocking')
            chrome_options.add_argument('-–single-process')
            chrome_options.add_argument('--ignore-ssl-errors')
            browser_ = webdriver.Chrome(chrome_options=chrome_options,executable_path=driverPath)
            if login:
                print("cookie keep")
            else :
                browser_.delete_all_cookies()
                print("cookie delete")
            browser_.set_page_load_timeout(5000) 
            browser_.get("chrome://version/")
            self.InitialChromeBtn.config(state="NORMAL")
        except Exception as e:
            if 'already in use' in str(e):
                print(str(e))
            print(e)
            self.InitialChromeBtn.config(state="NORMAL")
        self.browser=browser_
       



    def getConf(self,name,initValue,path):
        tmp_=str(initValue)
        try:
            value= config.read_config('config.ini', path, name)
            if value==None or value=="":
                self.writeConfig(name,tmp_,path)
                return initValue
            else:
                return value
        except Exception as e:
            print(e)
            self.writeConfig(name,tmp_,path)
            return initValue

    def writeConfig(self,confName,confValue,path):
        path_=path
        if path==None:
            path_="通用设置"
        config.write_config('config.ini', path_, confName,confValue)
        return confValue



    def ReadListBtn_Cmd(self, event=None):
        try:
            self.browser.get("http://www.fuyaotang.com/yd")
            provinceListDiv=BeautifulSoup(self.browser.page_source, "lxml").find("div",id="wrap") 
            provinceListUL=provinceListDiv.find("ul")
            provinceListAs=provinceListUL.findAll("a")
            ProvinceURLList_={}
            for provinceListA in provinceListAs:
                ProvinceURLList_[provinceListA.text]="http://www.fuyaotang.com"+ provinceListA.attrs["href"]
            self.ProvinceCityListBox.delete(0,END)
            self.ProvinceURLList=ProvinceURLList_
            for ProvinceName in ProvinceURLList_.keys():
                self.ProvinceCityListBox.insert(END,ProvinceName)    


        except:
            pass
 

    def DoReadBtn_Cmd(self, event=None):
        #TODO, Please finish the function here!
        selects=self.ProvinceCityListBox.curselection()
       
        if len(selects)==0:
            print('download all data')
            for ProvinceURLkey in self.ProvinceURLList.keys():
                print("download:"+ProvinceURLkey+"  &URL:"+self.ProvinceURLList[str(ProvinceURLkey)])
                self.DoDownLoadAll(self.ProvinceURLList[str(ProvinceURLkey)])
            pass
        else:
            for i,id in enumerate(selects):
                currentSelect=self.ProvinceCityListBox.get(id)
                print(currentSelect+"   "+self.ProvinceURLList[str(currentSelect)])
                self.DoDownLoadAll(self.ProvinceURLList[str(currentSelect)])
            pass
        
    def DoDownLoadAll(self,data, event=None):
        print("Now Download:"+str(data))
        try:
            self.browser.get(data)
            pageLinkA=BeautifulSoup(self.browser.page_source, "lxml").find_all("a", text="末页")[0]
            pages=1
            csclass=BeautifulSoup(self.browser.page_source, "lxml").find("div",class_="cs")
            title=csclass.find("h1").text
            if "_"in pageLinkA.attrs['href']:
                pages_=str(pageLinkA.attrs['href']).split('_')[1]
                pages=int(pages_)
                pass
            pass
            
            datas=""
            

            relatedClass=BeautifulSoup(self.browser.page_source, "lxml").find("div",class_="related")
            As=relatedClass.findAll("a",href=True)
            for a in As:
                name= a.find("h3").text
                address=a.findAll("p")[0].text
                tel=a.findAll("p")[1].text
                datanew=name+','+address+','+tel+','+'\n'
                datas+=datanew
                pass


            if pages>1:
                for page in range(2,pages+1):
                    print(str(data)+'_'+str(page))
                    self.browser.get(str(data)+'_'+str(page))
                    relatedClass=BeautifulSoup(self.browser.page_source, "lxml").find("div",class_="related")
                    As=relatedClass.findAll("a",href=True)
                    for a in As:
                        name= a.find("h3").text
                        address=a.findAll("p")[0].text
                        tel=a.findAll("p")[1].text
                        datanew=name+','+address+','+tel+','+'\n'
                        datas+=datanew
                        pass
            
            filename=os.path.dirname(os.path.realpath(sys.argv[0]))+'\\'+title+'.csv' 
            print(filename)
            
            # if(isinstance(datas, str)):
            #     datas=datas.encode('gb2312')
            # else:
            #     datas=datas.decode('utf8').encode('gb2312')


            with open(filename ,'a+',encoding="utf-8-sig",) as f:
                f.write(datas)

                
            
        except Exception as e:
            print(e)
        
        pass


    def saveData(self,data,event=None):
        

        pass



def removeBom(file):
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s==BOM else False

    f = open(file, 'rb')
    if existBom( f.read(3) ):
        fbody = f.read()
        #f.close()
        with open(file, 'wb') as f:
            f.write(fbody)


def is_nan(x):
    for s in x:
        if s==1 or s=="1": continue
        if s==2 or s=="2": continue
        if s==3 or s=="3": continue
        if s==4 or s=="4": continue
        if s==5 or s=="5": continue
        if s==6 or s=="6": continue
        if s==7 or s=="7": continue
        if s==8 or s=="8": continue
        if s==9 or s=="9": continue
        if s==0 or s=="0": continue
        if s=="." : continue
        return True
    return False






if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
    try: top.destroy()
    except: pass







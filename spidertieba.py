#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/5 9:49
# @Author  : Aries
# @Site    : 
# @File    : spidertieba.py
# @Software: PyCharm Community Edition
import random
import  os
from bs4 import BeautifulSoup
import urllib
from urllib.error import URLError,HTTPError
from urllib.request import Request,urlopen
import re
import  requests
#定义工具类，对帖子内容格式化
class Tool:
    #去除image标签
    removeImg=re.compile('<img.*?>| {7}|')
    #删除超链接
    removeAddr=re.compile('<a href.*?>|</a>')
    #换行标签替换为/n
    replaceline=re.compile('<tr>|<div>|</div>|</p>')
    #制表符替换为/t
    replacetd=re.compile('<td>')
    replacehead=re.compile('<p.*?>')
    replacebr=re.compile('<br>|</br><br>')
    removeother=re.compile('<.*?>')
    def replace(self,x):
        x=re.sub(self.removeImg,"",x)
        x=re.sub(self.removeAddr,"",x)
        x=re.sub(self.replaceline,"\n",x)
        x=re.sub(self.replacetd,"\t",x)
        x=re.sub(self.replacehead,"\n",x)
        x=re.sub(self.replacebr,"\n",x)
        x=re.sub(self.removeother,"",x)
        return x.strip()



class BDTB:
    #初始化相关参数，URL以及请求参数
    def __init__(self,baseurl,seelz,floortag):
        self.baseurl=baseurl
        self.seelz='?see_lz='+str(seelz)
        self.tool=Tool()#在此处初始化类使用
        self.file=None
        self.floor=1
        self.defaultTitle=u"百度贴吧"
        self.floortag=floortag

    #传入页码，获取帖子内容
    def getpage(self,pagenum):
        try:
            url=self.baseurl+self.seelz+'&pn='+str(pagenum)
            request=urllib.request.Request(url)
            response=urlopen(request)
            content=response.read().decode("utf-8")
            return content
        except urllib.error.HTTPError as e:
            print(e.code)
    #获取帖子标题
    def gettitle(self,page):
         page=self.getpage(1)
         pattern=re.compile('<title.*?>(.*?)</title>')
         title=re.search(pattern,page)
         if title:
             return title.group(1).strip()
         else:
             return '百度贴吧'

    # 获取帖子页数
    def getpagenum(self,page):
        page=self.getpage(1)
        pattern=re.compile('<li class="l_reply_num".*?</span>.*?<span.*?>(.*?)</span>',re.S)
        pagenum=re.search(pattern,page)
        if pagenum:
            return pagenum.group(1).strip()
        else:
            return None
    #获取帖子内容
    def getcontent(self,page):
        pattern=re.compile('div id="post_content_.*?>(.*?)</div>', re.S)
        items=re.findall(pattern,page)
        contents=[]
        floor=1
        for item in items:
            # print(floor,u"楼------------------------------------------------------------------------")
            # print(self.tool.replace(item))
            # floor+=1
            content="\n"+self.tool.replace(item)+"\n"
            contents.append(content.encode('utf-8'))
        return contents
    def setfiletitle(self,title):
        if title is not None:
            self.file=open(title+'.txt','wb')
        else:
            self.file=open(self.defaultTitle+'.txt'+'wb')
    def writedata(self,contents):
        for item in contents:
            if self.floortag==1:
                floorline="\n"+str(self.floor)+u"楼层-----------------"+"\n"
                self.file.write(floorline)
            self.file.write(item)
            self.floor+=1
    def start(self):
        indexpage=self.getpage(1)
        pagenum=self.getpagenum(indexpage)
        # pagenum=5
        # title='百度贴吧'
        title=self.gettitle(indexpage)
        self.setfiletitle(title)
        if pagenum==None:
            print('文件已失效')
            return
        try:
            print('该帖子共有'+str(pagenum)+'页')
            for i in range (1,int(pagenum)+1):
                print('正在写入第'+str(i)+'页')
                page=self.getpage(i)
                contents=self.getcontent(page)
                self.writedata(contents)
                self.getimg(page)
                print('图片保存成功')
        except IOError as e:
            print(e.code)
        finally:
            print('任务完成')
    def getimg(self,page):
        pattern = re.compile('<img class="BDE_Image" src="(.*?)"*?pic_ext="jpeg".*?>',re.S)
        img=re.findall(pattern, page)
        for img_url in img:
            img_url=re.sub("\"",'',img_url)
            filename = 'test' + str(random.randint(0, 1000)) + '.jpg'
            fpath = 'E:/awesome-python3-webapp/download/' + filename
            response=urllib.request.urlopen(img_url)
            page=response.read()
            # print(page)
            with open(fpath, 'wb') as f:
                f.write(page)




    def save_image(self,image_url):
        filename = 'test' + str(random.randint(0, 1000)) + '.jpg'
        fpath = 'e:/' + filename
        print(fpath)
        response = requests.get(image_url)
        page = response.content
        with open(fpath, 'wb') as f:
            f.write(page)


baseurl='https://tieba.baidu.com/p/3138733512'
dbtb=BDTB(baseurl,1,0)
# dbtb.getpage(1)
# dbtb.gettitle()
# dbtb.getpagenum()
# dbtb.getcontent(dbtb.getpage(1))
dbtb.start()
# dbtb.getimg(dbtb.getpage(1))
# image_urls=dbtb.getimg(dbtb.getpage(1))
# print(image_urls)
# dbtb.save_image(image_urls)




# import requests
# response=requests.get('https://imgsa.baidu.com/forum/w%3D580/sign=d66bf2aeaf345982c58ae59a3cf6310b/15c79f3df8dcd100fb179efb708b4710b8122f64.jpg')
# page=response.content
# print(page)
# with open('E:/test.jpg','wb') as f:
#     f.write(page)

# import requests
# import random
# img_url='https://imgsa.baidu.com/forum/pic/item/33950a7b02087bf4a0652833f0d3572c10dfcf5b.jpg'
# print(img_url)
# filename='test'+str(random.randint(0,1000))+'.jpg'
# fpath = 'e:/'+filename
# print(fpath)
# response=requests.get(img_url)
# page=response.content
# print(page)
# with open(fpath, 'wb') as f:
#     f.write(page)\
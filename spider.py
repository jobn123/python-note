# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
#test
# res = urllib2.urlopen('http://www.baidu.com')
# print res.read()

#post
# value = {"username":"1016903103@qq.com","password":"XXXX"}
# data = urllib.urlencode(values) 
# url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
# request = urllib2.Request(url,data)
# response = urllib2.urlopen(request)
# print response.read()

#get
# values={}
# values['username'] = "1016903103@qq.com"
# values['password']="XXXX"
# data = urllib.urlencode(values) 
# url = "http://passport.csdn.net/account/login"
# geturl = url + "?"+data
# request = urllib2.Request(geturl)
# response = urllib2.urlopen(request)
# print response.read()

class QSBK:
  def __init__(self):
    self.pageIndex = 1
    self.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    # 初始化herder
    self.headers = {'User-Agent': self.userAgent}
    # 存放段子
    self.stories = []
    #存放程序是否继续运行的变量
    self.enable = False
    
  # 获取某一页数据
  def getPage(self, pageIndex):
    try:
      url = 'https://www.qiushibaike.com/hot/page/' + str(pageIndex)
      # 构建请求的repuest
      request = urllib2.Request(url, headers = self.headers)
      # 利用urlopen 获取页面代码
      response = urllib2.urlopen(request)
      # 页面 utf-8 转码
      pageCode = response.read().decode('utf-8')
      return pageCode
    except urllib2.URLError, e:
      if hasattr(e, "reason"):
        print u"连接糗事百科失败", e.reason
        return None
  
  #传入某一页代码，返回本页不带图片的段子列表
  def getPageItems(self, pageIndex):
    pageCode = self.getPage(pageIndex)
    if not pageCode:
      print "页面加载失败"
      return None
    
    pattern = re.compile('<div.*?author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>(.*?)<div class="stats">.*?class="number">(.*?)</i>.*?<i class="number">(.*?)</i>', re.S)
    
    items = re.findall(pattern, pageCode)
    #用来存储每页的段子们
    pageStories = []
    for item in items:
      #是否含有图片
      haveImg = re.search("img",item[3])
      #如果不含有图片，把它加入list中
      if not haveImg:
        replaceBR = re.compile('<br/>')
        text = re.sub(replaceBR,"\n",item[1])
        #item[0]是一个段子的发布者，item[1]是内容，item[2]是发布时间,item[4]是点赞数
        pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[4].strip()])
    return pageStories

  #加载并提取页面的内容，加入到列表中
  def loadPage(self):
    #如果当前未看的页数少于2页，则加载新一页
    if self.enable == True:
      if len(self.stories) < 2:
        #获取新一页
        pageStories = self.getPageItems(self.pageIndex)
        #将该页的段子存放到全局list中
        if pageStories:
          self.stories.append(pageStories)
          #获取完之后页码索引加一，表示下次读取下一页
          self.pageIndex += 1

  #调用该方法，每次敲回车打印输出一个段子       
  def getOneStory(self, pageStories, page):
    #遍历一页的段子
    for story in pageStories:
      #等待用户输入
      input = raw_input()
      # 输入回车，判断是否加载新页面
      self.loadPage()
      # 如果输入Q则程序退出
      if input == "Q":
        self.enable = False
        return
      print u"第%d页\t发布人:%s\t赞:%s\n%s" %(page,story[0],story[3],story[1])
      # print u"第%d页\t发布人:%s\t评论:%s\t赞:%s\n%s" %(page,story[0],story[2],story[3],story[1])
  
  #爬虫入口方法
  def start(self):
    print u"正在读取糗事百科，按回车查看新段子，Q退出"
    #enable True 程序可运行
    self.enable = True
    #先加载一页内容
    self.loadPage()
    #局部变量，控制当前读到了第几页
    nowPage = 0
    while self.enable:
      if len(self.stories)>0:
        #从全局list中获取一页的段子
        pageStories = self.stories[0]
        #当前读到的页数加一
        nowPage += 1
        #将全局list中第一个元素删除，因为已经取出
        del self.stories[0]
        #输出该页的段子
        self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()

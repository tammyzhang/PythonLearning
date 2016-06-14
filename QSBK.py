# coding=utf-8
import urllib
import urllib2
import re
import thread
import time

class QSBK:

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent' :self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print "error",e.reason
                return None

    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "page load error"
            return None
        pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</',re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,"\n",item[1])
            pageStories.append([item[0].strip(),text.strip(),item[2].strip()])
        return pageStories

    def loadPage(self):
        if self.enable==True:
            if len(self.stories)<1:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex +=1

    def getOneStory(self,pageStories,pageIndex):
        for story in pageStories:          
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"发布人：%s\t 赞：%s\n%s" %(story[0],story[2],story[1])

    def start(self):        
        self.enable = True
        print u"正在读取糗事百科,需要加载小段时间，请稍等..."
        self.loadPage()
        print u'读取完成，开始解析'
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage +=1
                del self.stories[0]
                print u'\n\n第%d页...' %(nowPage)
                print u'按回车查看段子，Q退出'
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()

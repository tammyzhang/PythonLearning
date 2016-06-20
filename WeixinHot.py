# coding:utf8

import urllib
import urllib2
import re
# import xlwt


class WeixinHot:
    def __init__(self, baseURL):
        self.baseURL = baseURL
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent' :self.user_agent}
        self.file = None
        #self.filename=None
        #self.sheet=None
        self.index=0
        
    def getPage(self,url):
        try:
            request = urllib2.Request(url, headers=self.headers)
            reponse = urllib2.urlopen(request)

            content = reponse.read() #.decode('utf-8')
            # print content
            return content
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print 'Connection failure, reason: ', e.reason
                return None

    def pagePaser(self, pageContent):
        # 0 weixin name
        # 1 artical subject
        # 2 artical digest
        # 3 viewtimes
        # print pageContent
        print 'Start Parsing...'
        pattern = re.compile('<p title=".*?>(.*?)</p>.*?<a uigs="pc_.*?_tit_.*?>(.*?)</a>.*?<a uigs="pc_.*?_summary_.*?>(.*?)</a>.*?mycollect_.*?</span>.*?;(.*?)&',re.S) 
        items = re.findall(pattern, pageContent)
        print 'Total %d articals' %(len(items))

        articals =[]
       
        for item in items:
##            print item[0]
##            print item[1]
##            print item[2]           
##            print item[3]+'\n'

            articals.append([item[0],item[1],item[2],item[3]])
             
        return articals

    def checkURLValid(self, url):
        code = urllib.urlopen(url).getcode()
        # print code
        if code == 200:
            return True
        else:
            return False
        
    def getURL(self, typeIndex,pageIndex):
        url = self.baseURL + 'pcindex/pc/pc_'+str(typeIndex)+'/'
        if pageIndex == 0:
            url += 'pc_'+str(typeIndex)+'.html'
        else:
            url += str(pageIndex)+'.html'

        print 'LoadUrl=', url
        return url
        
    def writeArticals(self, articals):
        
        for item in articals:
            print str(self.index)+'\t'+item[0].decode('utf-8')
            self.file.write(item[0]+'\t'+item[3]+'\t'+item[1]+'\t'+item[2]+'\n')
            self.index+=1
           
    
    def start(self):
        
        try:
            self.file = open("WeixinHotArticals.txt","w+")

            for typeIndex in range(0,20):
                pageIndex=0
                while True:                
                    url = self.getURL(typeIndex,pageIndex)
                    
                    print 'Get one URL =',url
                    if self.checkURLValid(url):
                        print 'Valid URL'
                        content = self.getPage(url)

                        if content == None:
                            print 'Cannot get the content'
                            pass
                        else:
                            print 'Get the Content'
                            articals = self.pagePaser(content)
                            print 'Write this page to file'
                            self.writeArticals(articals)
                           
                            print 'Finish this page written.'
                            pageIndex +=1
                    else:
                        print 'URL is invalid'
                        break
          
        except IOError,e:
            print 'IO error' + e.message
        finally:
            self.file.close()           
            
            print 'Finished'

                
baseURL = 'http://weixin.sogou.com/'
weixinSpider = WeixinHot(baseURL)

weixinSpider.start()

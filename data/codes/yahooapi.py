import urllib2
import urllib
#import json
#import xml.etree.ElementTree

class yahoo_api(object):

    def __init__(self):
        self.params={}
        self.url=''

    def code_para(self):
        return urllib.urlencode(self.params)

    def get_response(self):
        codedpara=self.code_para()
        req = urllib2.Request(self.url,data=codedpara)
        try:
            response = urllib2.urlopen(req)
            return response
        except urllib2.HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            return None
        except urllib2.URLError, e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            return None


class api_history(yahoo_api):
    def __init__(self,aucID,num_page=1):
        self.url='http://auctions.yahooapis.jp/AuctionWebService/V1/BidHistoryDetail'
        self.params={
            'auctionID':aucID,
            'appid':'dj0zaiZpPXlvZHVobmUxRmJoViZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-',
            #'output':'json',
            'page':num_page
            }

class api_goods(yahoo_api):
    def __init__(self,aucID):
        self.url='http://auctions.yahooapis.jp/AuctionWebService/V2/auctionItem'
        self.params={
            'auctionID':aucID,
            'appid':'dj0zaiZpPXlvZHVobmUxRmJoViZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-',
            #'output':'json'
            }

class api_search(yahoo_api):
    def __init__(self,categoryID,page=1):
        self.url='http://auctions.yahooapis.jp/AuctionWebService/V2/categoryLeaf'
        self.params={
            'category':categoryID,
            'appid':'dj0zaiZpPXlvZHVobmUxRmJoViZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-',
            'output':'xml',
            'page':page,
            'ranking':'popular',
            'sort' : 'end',
            'order' : 'd'
            }



#auction1=api_goods('h187497791')
#auction2=api_history('w101107767',1)
#res=auction1.get_response()
#jobject=json.load(res)
#page=res.read()
#print page
#f1=open('auction1.xml','w')
#f1.write(page)
##
##page=res.readlines()
##for e in page:
##   f1.write(e)
#f1.close

#f1=open('auction1.json','w')
#f1.write(page)
#f1.close
#tree = xml.etree.ElementTree.XML(page)
#f1=open("test.xml",'w')
#tree.write("test.xml")#, encoding="utf-8")
#f1.close


#jobject=json.loads(page[7:-1],encoding="cp932")
#jobject[u'ResultSet'][u'Result'][u'Description']=u""


#import codecs

#f1 = codecs.open('auction1.json', "w", "utf-8")
#f1=open('auction1.json','w')
#json.dumps(jobject,f1, indent=4,ensure_ascii=False)
#f1.close()



#f = codecs.open('auction2history.json', "w", "utf-8")
#json.dump(jobject, f, indent=2, sort_keys=True, ensure_ascii=False)
#f.close()


#page=json.dumps(jobject, indent=4)
#f1.write(json.dumps(jobject, indent=4))

#print (json.dumps(jobject, indent=4)).encode('utf-8')
#print ("\u5bcc\u58eb\u901a").encode('utf-8')


#print json.dumps(jobject, sort_keys=True, indent=4)

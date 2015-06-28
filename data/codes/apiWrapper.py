# coding:utf-8
# 
import urllib2
import urllib
import re
import pickle
import xml.dom.minidom
import json

def auction_title(auctionIDlist,outstr,option='a',discription=False):
    '''オークションのタイトルを取る関数
    入力はauctionIDlist：オークションIDのリスト　outstr：書き出すファイルの名前　option：書き出すのオプション、デフォルトは追加、新しいのを作りたい場合はwに
    タイトルだけではなく他のものを取り出したい場合はtitle = jobject[u'ResultSet'][u'Result'][u'Title']に適当に変形すればよい
    使用例としては下のsearch_auctionをまず利用してIDのリストを取り、そのリストをauction_titleに渡してタイトルをとる'''
    f2=open(outstr,option)
    for index in xrange(len(auctionIDlist)):
        print index
        aucres=api_goods(auctionIDlist[index],output='json').get_response()
        if aucres == None:
            break
        page = aucres.read()
        #print page
        jobject=json.loads(page[7:-1],encoding="cp932")
        #jobject=json.load(aucres)
        try:
            title = jobject[u'ResultSet'][u'Result'][u'Title']
            title = re.sub(r' \t|\v|\r|,', ' ' , title)
            if discription == True:
                Auc_disc = jobject[u'ResultSet'][u'Result'][u'Description']
                temp = re.sub(r'<[^(?:<|>)]+>',' ', Auc_disc)
                dst = re.sub(r' \t|\v|\r|,', ' ' , temp)
                Initprice = jobject[u'ResultSet'][u'Result'][u'Initprice']
                Price = jobject[u'ResultSet'][u'Result'][u'Price']
                Bids = jobject[u'ResultSet'][u'Result'][u'Bids']
                line=auctionIDlist[index] + " , " +title + " , "+ dst+ " , "+ Initprice+ " , "+ Price+ " , "+ Bids +"\n"
            else:
                line=auctionIDlist[index] + " , " +title + "\n"
            f2.write(line)
        except KeyError as e:
            print e
    f2.close()



def Auction_data_xml(auctionIDlist,outstr,option='a'):
    '''オークションの詳細リストをファイルに書き出す関数：
	入力はauctionIDlist：オークションIDのリスト　outstr：書き出すファイルの名前　option：書き出すのオプション、デフォルトは追加、新しいのを作りたい場合はwに
	htmlタグなどがエラーになるため"Description"タグを削除した、ほかに"ResultSet"と'?xml'も削除
	今はxmlにしたがデータベースなどを考えるとあとにjsonに変更する可能性ある'''
    if type(auctionIDlist) != list:
        auctionIDlist=[auctionIDlist]

    f2=open(auctionIDlist,option)
    for index in xrange(len(auctionIDlist)):
        print index
        aucres=api_goods(auctionIDlist[index],output='xml').get_response()
        if aucres == None:
            continue
        line=aucres.readline()
        while line != "":
            if "ResultSet" in line or '?xml' in line: 
                pass
            elif "Description" in line:
                temp = re.sub(r'<[^(?:<|>)]+>',' ', Auc_disc)
                dst = re.sub(r' \t|\v|\r|,', ' ' , temp)
            else:
                f2.write(line)
            line=aucres.readline()
    f2.close()
    
    
def Auction_data_json(auctionIDlist,outstr,option='a'):
    '''オークションの詳細リストをファイルに書き出す関数：
    入力はauctionIDlist：オークションIDのリスト　outstr：書き出すファイルの名前　option：書き出すのオプション、デフォルトは追加、新しいのを作りたい場合はwに
    htmlタグなどがエラーになるため"Description"タグを削除した、ほかに"ResultSet"と'?xml'も削除
    今はxmlにしたがデータベースなどを考えるとあとにjsonに変更する可能性ある'''
    if type(auctionIDlist) != list:
        auctionIDlist=[auctionIDlist]

<<<<<<< HEAD
<<<<<<< HEAD
def Auction_data_json(auctionIDlist,outstr,option='a'):
    '''オークションの詳細リストをファイルに書き出す関数：
    入力はauctionIDlist：オークションIDのリスト　outstr：書き出すファイルの名前　option：書き出すのオプション、デフォルトは追加、新しいのを作りたい場合はwに
    htmlタグなどがエラーになるため"Description"タグを削除した、ほかに"ResultSet"と'?xml'も削除
    今はxmlにしたがデータベースなどを考えるとあとにjsonに変更する可能性ある'''
    if type(auctionIDlist) != list:
        auctionIDlist=[auctionIDlist]

    f2=open(auctionIDlist,option)
    for index in xrange(len(auctionIDlist)):
        print index
        aucres=api_goods(auctionIDlist[index],output='json').get_response()
        if aucres == None:
            continue
        page = aucres.read()
        jobject=json.loads(page[7:-1],encoding="cp932")
    f2.close()
    return json.dumps(jobject,indent=4,ensure_ascii=False)
=======
    f2=open(auctionIDlist,option)
=======
    ret = {'result': []}
>>>>>>> 61231a94d2ccaa7b4a773ef5886e1a2282550ce5
    for index in xrange(len(auctionIDlist)):
        aucres=api_goods(auctionIDlist[index],output='json').get_response()
        if aucres == None:
            continue
        page = aucres.read()
        jobject=json.loads(page[7:-1],encoding="cp932")
        ret['result'].append(jobject['ResultSet']['Result'])

    return ret

def search_auction_plus(catagoryID,startPage=1,pages=5,tagName='AuctionID'):
    '''中丸追記'''
    result=[]
    for i in xrange(startPage,startPage+pages,1):
        category1=api_search(catagoryID,page=i)
        if category1==None:
            break

        res=category1.get_response()
        doms = xml.dom.minidom.parse(res)
        for dom in doms.getElementsByTagName(tagName):
            result += [dom.childNodes[0].data]
    return result
>>>>>>> 28bd09630cc9d9bea305f122c66524abfb5aedbb

def search_auction(catagoryID,pages=5,tagName='AuctionID'):
    '''特定のcatagoryIDの商品を検索し、そのcatagoryの商品の特定のフィルドを返す（デフォルト）はAuctionIDのリストを返す
	入力はcatagoryID：catagoryのID　pages：何ページまで検索、デフォルトは５　tagName：catagoryの商品の特定のフィルドを指定、デフォルトはAuctionID'''
    result=[]
    for i in xrange(1,pages+1,1):
        category1=api_search(catagoryID,page=i)
        if category1==None:
            break

        res=category1.get_response()
        doms = xml.dom.minidom.parse(res)
        for dom in doms.getElementsByTagName(tagName):
            result += [dom.childNodes[0].data]
    return result


def createdisc(l):
    dist={}
    for id in l:
        dist[id] = search_auction(id,pages=5,tagName='AuctionID')
        print id 
        print "success"
    print 'success'
    return dist



def save_object(savething,text_name,option='w'):
    '''ある特定のオブジェクトをテキストファイルに保存'''
    f = open(text_name, option)
    pickle.dump(savething, f)
    f.close()
    print 'save successfully!'

def load_object(text_name):
    '''テキストファイルに保存したオブジェクトをロード'''
    f1=open(text_name)
    l = pickle.load(f1)
    f1.close()
    return l



'''API問い合わせクラスの定義'''
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
    def __init__(self,aucID,num_page=1,output='xml'):
        self.url='http://auctions.yahooapis.jp/AuctionWebService/V1/BidHistoryDetail'
        self.params={
            'auctionID':aucID,
            'appid':'dj0zaiZpPXlvZHVobmUxRmJoViZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-',
            'output':output,
            'page':num_page
            }

class api_goods(yahoo_api):
    def __init__(self,aucID,output='json'):
        self.url='http://auctions.yahooapis.jp/AuctionWebService/V2/auctionItem'
        self.params={
            'auctionID':aucID,
            'appid':'dj0zaiZpPXlvZHVobmUxRmJoViZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-',
            'output':output
            }

class api_search(yahoo_api):
    def __init__(self,categoryID,page=1,output='xml'):
        self.url='http://auctions.yahooapis.jp/AuctionWebService/V2/categoryLeaf'
        self.params={
            'category':categoryID,
            'appid':'dj0zaiZpPXlvZHVobmUxRmJoViZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-',
            'output':output,
            'page':page,
            'ranking':'popular',
            'sort' : 'bids',
            'order' : 'd'
            }

class api_search(yahoo_api):
    def __init__(self,categoryID,page=1,output='xml'):
        self.url='http://auctions.yahooapis.jp/AuctionWebService/V2/categoryLeaf'
        self.params={
            'category':categoryID,
            'appid':'dj0zaiZpPXlvZHVobmUxRmJoViZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-',
            'output':output,
            'page':page,
            'ranking':'popular',
            'sort' : 'bids',
            'order' : 'd'
            }



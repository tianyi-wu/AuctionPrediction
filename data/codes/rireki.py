# -*- coding: utf-8 -*-

import yahooapi
import xml.dom.minidom

def rireki(aucID):
#　入札履歴をの時間と価格のリストを返す
#　[price(n),price(n-1),…,price(1),time(n),time(n-1),…,time(1)]で返す（nは入札）  
    page=1
    n=1
    listprice=[]
    listdate=[]
    listlength=0

    while n==1:
        n=n+1
        history=yahooapi.api_history(aucID,page)
        res=history.get_response()
#        print "%s %d"%(aucID,page)
        if res == None:
            listlength=0
            continue
        doms = xml.dom.minidom.parse(res)
        for dom in doms.getElementsByTagName("Price"):
            listprice.append(dom.firstChild.data.replace(".00",""))
        for dom in doms.getElementsByTagName("Date"):
            his=dom.firstChild.data.replace("\n2","2")
            listdate.append(his.replace("+09:00\t\t",""))
            n=n+1
            listlength=listlength+1
        for dom in doms.getElementsByTagName("IsCanceled"):
            if dom.firstChild.data == "true":
                listlength=listlength-1
        if n==52:
            n=1
        page=page+1
        if listlength == 0:
            break

    listresult=listprice+listdate
    return listresult

if __name__ == "__main__":
    print rireki("r113027514")

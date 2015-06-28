
def createList(openstr):
	f=open(openstr)
	IDlist=[]
	line=f.readline()
	while line != "":
		print line
		try:
			IDlist.append(int(line))
		except:
			break
		line=f.readline()
	print 'success'
	f.close()
	return IDlist


def createdisc(l):
	dist={}
	for id in l:
		dist[id] = search_auction(catagoryID,pages=5,tagName='AuctionID')
	print 'success'
	return dist

# -*- coding: utf-8 -*-

# run "pip install mysql-python" before use
import MySQLdb
import pandas as pd

makers=[]


def get_all_data(makers):
	maker_list=[]
	for maker in makers:
		try:
			maker_list += categoryIDdic[maker]
		except KeyError as e:
			print maker, " not find"
			print e
			return None
	category = "("+reduce(lambda a,b: str(a)+","+str(b), maker_list) +")"
	field ='*'
	sql = "SELECT %s FROM item WHERE category_id IN %s" % (field ,category)
	#limit=10, offset=0
	#sql += " ORDER BY auction_id ASC LIMIT %d OFFSET %d" % (limit, offset)
	result = query(sql)
	return pd.DataFrame(result)


def get_maker_data(maker):
	try:
		IDlist = categoryIDdic[maker]
	except KeyError as e:
		print maker, " not find"
		print e
		return None

	category = "("+reduce(lambda a,b: str(a)+","+str(b), IDlist) +")"
	field ='*'
	sql = "SELECT %s FROM item WHERE category_id IN %s" % (field ,category)
	#limit=10, offset=0
	#sql += " ORDER BY auction_id ASC LIMIT %d OFFSET %d" % (limit, offset)
	result = query(sql)
	return pd.DataFrame(result)




# read
def get_categories():
    sql = "SELECT DISTINCT(category_id) FROM item"
    ret = []
    ctgs = query(sql)
    for r in ctgs:
        ret.append(r['category_id'])
    return ret


def get_ids(category, limit=10, offset=0, id_only=False):
    field = 'auction_id' if id_only else '*'
    sql = "SELECT %s FROM item WHERE category_id = '%s'" % (field ,category)
    sql += " ORDER BY auction_id ASC LIMIT %d OFFSET %d" % (limit, offset)
    return query(sql)


# write
def insert_id(no, ctg):
    sql = "INSERT INTO item (auction_id, category_id)"
    sql += " VALUES ('%s', '%s')" % (str(no), str(ctg))
    query(sql)


def insert_ids(ls):
    for no, ctg in ls:
        insert_id(no, ctg)


# run query
def query(sql):
    connector = MySQLdb.connect(
        host="suri-auction.cp8hyreygaih.ap-northeast-1.rds.amazonaws.com",
        db="auction",
        user="suri",
        passwd="surirokken",
        charset="utf8"
    )
    cursor = connector.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(sql)

    result = cursor.fetchall()
    res = []
    for r in result:
        res.append(dict(r))

    connector.commit()
    cursor.close()
    connector.close()

    return res



def categoryIDtoMaker():
	result = {}
	for key in categoryIDdic:
		for ids in categoryIDdic[key]:
			result[ids] = key
	return result




categoryIDdic = {
	'ASUS':[2084307163,2084307164,2084307165,2084307166,2084307167],
	
	'Gateway':[2084307168,2084307169,2084307170,2084307171,2084307172],
	
	'HP':[2084307173,2084307174,2084307175,2084307176,2084307177],
	
	'IBM':[2084193598,2084193597,2084193596,2084193595],
	
	'NEC':[2084193571,2084193570,2084193569,2084193568,2084193567],
	
	'OTHERS':[2084042163,2084239900,2084239898,2084042164,2084042165,2084239901,2084239899,2084048237,2084042174],
	
	'ACER':[2084307178,2084307179,2084307180,2084307181,2084307182],
	
	'SHARP':[2084193576,2084193575,2084193574,2084193573,2084193572],
	
	'SOTEC':[2084307183,2084307184,2084307185,2084307186,2084307187],
	
	'SONY':[2084193581,2084193580,2084193579,2084193578,2084193577],
	
	'DELL':[2084193586,2084193585,2084193584,2084193583,2084193582],

	'PASONIC':[2084193589,2084193588,2084193587],
	
	'LENOVO':[2084307188,2084307189,2084307190,2084307191,2084307192],
	
	'TOSHIBA':[2084193594,2084193593,2084193592,2084193591,2084193590],
	
	'HITACHI':[2084307193,2084307194,2084307195,2084307196,2084307197],

	'FUJITSU':[2084193603,2084193602,2084193601,2084193600,2084193599]
	
}
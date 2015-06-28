# coding:utf-8


from apiWrapper import search_auction_plus
import xml.dom.minidom
import json

# run "pip install mysql-python" before use
import MySQLdb


# read
def get_categories():
    sql = "SELECT DISTINCT(category_id) FROM item"
    ret = []
    ctgs = query(sql)
    for r in ctgs:
        ret.append(r['category_id'])
    return ret


def get_data(category, limit=10, offset=0, id_only=False):
    field = 'auction_id' if id_only else '*'
    sql = "SELECT %s FROM item WHERE category_id = '%s'" % (field ,category)
    sql += " ORDER BY auction_id ASC LIMIT %d OFFSET %d" % (limit, offset)
    return query(sql)


# write
def insert_data(no, ctg, title, desc):
    sql = "REPLACE INTO item (auction_id, category_id, title, description)"
    sql += " VALUES ('%s', '%s', '%s', '%s')" % (str(no), str(ctg), title, desc)
    try:
        query(sql)
    except:
        pass


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


if __name__ == '__main__':
    from apiWrapper import Auction_data_json

    ctgs = get_categories()
    for c in ctgs:
        print 'start category', c
        ids = get_data(c, 100, 0, True)
        ids = [e['auction_id'] for e in ids]
        res = Auction_data_json(ids, '/Users/TomokiNakamaru/Desktop/test.txt')
        res = res['result']

        for r in res:
            aid = r['AuctionID']
            title = r['Title']
            desc = r['Description']
            ctg = r['CategoryID']
            print 'inserting', c, aid
            insert_data(aid, ctg, title, desc)

    # ctgs = [
    #     2084307163,
    #     2084307164,
    #     2084307165,
    #     2084307166,
    #     2084307167,
    #     2084307168,
    #     2084307169,
    #     2084307170,
    #     2084307171,
    #     2084307172,
    #     2084307173,
    #     2084307174,
    #     2084307175,
    #     2084307176,
    #     2084307177,
    #     2084193598,
    #     2084193597,
    #     2084193596,
    #     2084193595,
    #     2084193571,
    #     2084193570,
    #     2084193569,
    #     2084193568,
    #     2084193567,
    #     2084042163,
    #     2084239900,
    #     2084307178,
    #     2084307179,
    #     2084307180,
    #     2084307181,
    #     2084307182,
    #     2084193576,
    #     2084193575,
    #     2084193574,
    #     2084193573,
    #     2084193572,
    #     2084307183,
    #     2084307184,
    #     2084307185,
    #     2084307186,
    #     2084307187,
    #     2084193581,
    #     2084193580,
    #     2084193579,
    #     2084193578,
    #     2084193577,
    #     2084193586,
    #     2084193585,
    #     2084193584,
    #     2084193583,
    #     2084193582,
    #     2084193589,
    #     2084193588,
    #     2084193587,
    #     2084307188,
    #     2084307189,
    #     2084307190,
    #     2084307191,
    #     2084307192,
    #     2084048237,
    #     2084193594,
    #     2084193593,
    #     2084193592,
    #     2084193591,
    #     2084193590,
    #     2084307193,
    #     2084307194,
    #     2084307195,
    #     2084307196,
    #     2084307197,
    #     2084193603,
    #     2084193602,
    #     2084193601,
    #     2084193600,
    #     2084193599,
    # ]

    # for c in ctgs:
    #     page = 1
    #     for i in range(1):
    #         print c, page, '...',
    #         ret = search_auction_plus(c, page+1, 5)
    #         for aid in ret:
    #             insert_id(aid, c)
    #         print 'done'
    #         page += 5

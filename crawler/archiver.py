# coding:utf-8
import MySQLdb


def add_item(e):
    keys = []
    vals = []

    for k, v in e.items():
        keys.append(k)
        if v is None:
            vals.append('NULL')
        else:
            vals.append(v)

    q = "REPLACE INTO item(`%s`) VALUES ('%s')" % (
        '`,`'.join(keys), "','".join(vals)
    )
    try:
        query(q)
    except:
        print 'insert error @ %s' % e['auction_id']


def update_item(info):
    pass


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

    return result


def get_ids(page=1):
    ret = query('select auction_id from _item limit 10 offset %d' % (page*10))
    vals = []
    for d in ret:
        vals.append(d['auction_id'])
    return vals

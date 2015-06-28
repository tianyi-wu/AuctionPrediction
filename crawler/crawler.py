# coding:utf-8
import urllib
import json
import re

# appid
appid = 'dj0zaiZpPXlvZHVobmUxRmJoViZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-'


def yahoo_api(path, params):
    url = 'http://auctions.yahooapis.jp%s?appid=%s' % (path, appid)
    for k, v in params.items():
        url += '&%s=%s' % (k, str(v))
    response = urllib.urlopen(url).read()
    try:
        return json.loads(response[7:-1])
    except:
        return {}


def fetch_item(aid):
    obj = yahoo_api(
        '/AuctionWebService/V2/json/auctionItem',
        {'auctionID': aid}
    )

    item = {}
    if 'ResultSet' in obj:
        if 'Result' in obj['ResultSet']:
            item = obj['ResultSet']['Result']

    result = {}
    result['auction_id'] = item['AuctionID'] if 'AuctionID' in item else None
    result['category_id']\
        = item['CategoryID'] if 'CategoryID' in item else None
    result['title'] = item['Title'] if 'Title' in item else None

    desc = item['Description'] if 'Description' in item else None
    desc = re.sub('<[^<]+?>', '', desc)
    desc = re.sub('\s', '', desc)
    desc = re.sub(',|\'', '', desc)
    result['description'] = desc

    result['current_price'] = item['Price'] if 'Price' in item else None
    result['init_price'] = item['Initprice'] if 'Initprice' in item else None
    result['start_time'] = item['StartTime'] if 'StartTime' in item else None
    result['end_time'] = item['EndTime'] if 'EndTime' in item else None
    result['bids'] = item['Bids'] if 'Bids' in item else None
    result['bid_or_buy'] = item['Bidorbuy'] if 'Bidorbuy' in item else None

    result['condition'] = None
    if 'ItemStatus' in item:
        if 'Condition' in item['ItemStatus']:
            result['condition'] = item['ItemStatus']['Condition']

    result['seller_point'] = None
    if 'Seller' in item:
        if 'Rating' in item['Seller']:
            if 'Point' in item['Seller']['Rating']:
                result['seller_point'] = item['Seller']['Rating']['Point']

    return result


def fetch_item_list(ctg, page=1):
    # http://auctions.yahooapis.jp/AuctionWebService/V2/json/search
    obj = yahoo_api(
        #'/AuctionWebService/V2/json/search',
        '/AuctionWebService/V2/json/categoryLeaf',
        {
            'category': ctg,
            'page': page,
            'sort': 'bids',
            'order': 'a'
        }
    )
    items = []
    if 'ResultSet' in obj:
        if 'Result' in obj['ResultSet']:
            if 'Item' in obj['ResultSet']['Result']:
                items = obj['ResultSet']['Result']['Item']
    ids = []
    for item in items:
        if isinstance(item, dict) and 'AuctionID' in item:
            ids.append(item['AuctionID'])

    return ids

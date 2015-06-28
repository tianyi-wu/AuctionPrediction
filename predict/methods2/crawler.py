# coding:utf-8
import urllib
import json

# appid
appid = 'dj0zaiZpPXlvZHVobmUxRmJoViZzPWNvbnN1bWVyc2VjcmV0Jng9ZDk-'


def yahoo_api(path, params):
    url = 'http://auctions.yahooapis.jp%s?appid=%s' % (path, appid)
    for k, v in params.items():
        url += '&%s=%s' % (k, str(v))
    response = urllib.urlopen(url).read()
    return json.loads(response[7:-1])


def fetch_item(aid):
    obj = yahoo_api(
        '/AuctionWebService/V2/json/auctionItem',
        {'auctionID': aid}
    )
    item = obj['ResultSet']['Result']

    result = {}
    result['auction_id'] = item['AuctionID']
    result['category_id'] = item['CategoryID']
    result['title'] = item['Title']
    result['description'] = item['Description']
    result['current_price'] = item['Price']
    result['init_price'] = item['Initprice']
    result['start_time'] = item['StartTime']
    result['end_time'] = item['EndTime']
    result['seller_point'] = item['Seller']['Rating']['Point']
    result['bids'] = item['Bids']
    result['condition'] = item['ItemStatus']['Condition']
    result['bid_or_buy'] = item['Bidorbuy'] if 'Bidorbuy' in item else None

    return result


def fetch_item_list(ctg, page=1):
    obj = yahoo_api(
        '/AuctionWebService/V2/json/categoryLeaf',
        {
            'category': ctg,
            'page': page
        }
    )
    items = obj['ResultSet']['Result']['Item']
    ids = []
    for item in items:
        ids.append(item['AuctionID'])

    return ids

# coding:utf-8

from bulk_insert import query
import time

while(True):
    print query('SELECT COUNT(auction_id) FROM item WHERE title IS NOT NULL')[0]['COUNT(auction_id)']
    time.sleep(1)

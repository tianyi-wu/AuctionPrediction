# -*- coding: utf-8 -*-
import predict_by_multi

from get_data_DB import get_all_data



def test(data_from="2014-6-04 23:59:59",data_to="2014-6-07 23:59:59"):
	maker_list=['NEC','SONY','FUJITSU','DELL','TOSHIBA']
	data = get_all_data(maker_list)
	test_data = data[(data_from < data.end_time) & (data.end_time < data_to)]
	true_price = test_data.current_price.values
	#predict_price = [predict_by_all(a_id) for a_id in test_data.auction_id.values]
	predict_price =[]
	for i in range(len(test_data.auction_id.values)):
		try:
			price = predict_by_multi.predict_by_all(test_data.auction_id.values[i])
			predict_price.append((i,price))
		except KeyError ,e:
			print e
			pass

	price_list=[(true_price[e[0]],e[1]) for e in predict_price]
	predict_range = map(lambda x : 1 if (x[0] > x[1][1] and x[0] < x[1][2]) else 0, price_list)
	prange = sum(predict_range)*1.0 / len(predict_range)

	predict_rate = map(lambda x : abs(x[0] - x[1][0]) * 1.0 / x[0] , price_list)
	predict_rate2 = map(lambda x : 1 if x < 0.25 else 0, predict_rate)
	prate = sum(predict_rate2)*1.0/ len(predict_rate2)

	return prange,prate




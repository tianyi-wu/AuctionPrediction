# -*- coding: utf-8 -*-
import LDA_one
import LDA_all
import predict

maker_list=['NEC','SONY','FUJITSU','DELL','TOSHIBA']
#LDA_one.LDA_initial_all(maker_list,date="2014-6-04 23:59:59")
#LDA_all.LDA_initial(maker_list,date="2014-6-04 23:59:59")

PredictOne = LDA_one.LDA_one(maker_list)
PredictAll = LDA_all.LDA_all(maker_list)

predict.update_LR()
predict.update_LR2()
predict.update_KN()





def predict_by_all(auction_id):
	LR1 = predict.predict_LR(auction_id)
	LR2 = predict.predict_LR2(auction_id)
	KN = predict.predict_KN(auction_id)
	
	LDAone = PredictOne.predict(auction_id)
	LDAall = PredictAll.predict(auction_id)
	
	PredictList = [LR1[0],LR2[0],KN[0],LDAone[0],LDAall[0]]
	return predict_list(PredictList)
	


def predict_list(predict_list):
	prices = sorted(predict_list)
	return (prices[len(prices)/2],prices[1],prices[-1])
	#return sorted([p1[0],p1[0],p2[0]])[1],sorted([p1[1],p1[1],p2[1]])[1],sorted([p1[2],p1[2],p2[2]])[1]]




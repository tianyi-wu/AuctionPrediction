# -*- coding: utf-8 -*-
from get_data_DB import get_maker_data,categoryIDtoMaker
from LDAmodel import lda_parts,Auction,FilterDate
from crawler import fetch_item


def LDA_initial(maker,date="2014-6-7 23:59:59",filters = True,show=False,no_below=5, no_above=0.75,num_topics=150):
	print "begin "+maker

	data = get_maker_data(maker)
	data = FilterDate(data,date)
	data_title = data["title"].values
	data_description = data["description"].values
	print "read data of" + maker

	title_lda = lda_parts(data_title)
	title_lda.dictionary_corpus(filter=filters,show=show,no_below=no_below, no_above=no_above)

	#need to change
	title_lda.LDA_model(num_topics=num_topics,save=("./model/"+maker+"_title.model"),show=show,set_matrix=False)
	print "titile's model of "+maker +" made"


	description_lda = lda_parts(data_description)
	description_lda.dictionary_corpus(filter=filters,show=show,no_below=no_below, no_above=no_above)

	#need to change
	description_lda.LDA_model(num_topics=num_topics,save=("./model/"+maker+"_description.model"),show=show,set_matrix=False)
	      
	print "description's model of "+maker +" made"


def LDA_initial_all(maker_list):
	for maker in maker_list:
		LDA_initial(maker)
	print "all updated"



class LDA_one(object):
	def __init__(self,makers,date="2014-6-7 23:59:59",filters = True,show=False,no_below=5, no_above=0.75,num_topics=150):
		self.categoryID = categoryIDtoMaker()
		self.Auction_model ={}

		for maker in makers:
			data = get_maker_data(maker)
			data = FilterDate(data,date)
			self.Auction_model[maker] = Auction(data,maker,filters = filters,show=show,no_below=no_below, no_above=no_above)
			print "load model of ", maker

	def predict(self,ID,threhold = 0.0,rate=2):
		testee = fetch_item(ID)
		try:
			maker = self.categoryID[int(testee['category_id'])]
			return self.Auction_model[maker].predict(testee['title'],testee['description'],threhold = threhold,rate=rate)
		except KeyError as e:
			print e
			raise NameError('No category_id found')
			#self.Auction.predict(testee['title'],testee['description'],threhold = threhold,rate=rate)






if __name__ == '__main__':
	maker_list=['NEC','SONY','FUJITSU','DELL','TOSHIBA']
	LDA_initial_all(maker_list)
	#PredictOne = LDA_one(maker_list)


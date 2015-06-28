# -*- coding: utf-8 -*-
from get_data_DB import get_all_data,categoryIDtoMaker
from LDAmodel import lda_parts,Auction,FilterDate
from crawler import fetch_item


def LDA_initial(makers,date="2014-6-04 23:59:59",filters = True,show=False,no_below=5, no_above=0.75,num_topics=300):
	print "begin ", makers

	data = get_all_data(makers)
	data = FilterDate(data,date)
	data_title = data["title"].values
	data_description = data["description"].values
	print "read data of", makers

	title_lda = lda_parts(data_title)
	title_lda.dictionary_corpus(filter=filters,show=show,no_below=no_below, no_above=no_above)

	#need to change
	title_lda.LDA_model(num_topics=num_topics,save=("./model/all_title.model"),show=show,set_matrix=False)

	print "titile's model of ", makers ," made"

	description_lda = lda_parts(data_description)
	description_lda.dictionary_corpus(filter=filters,show=show,no_below=no_below, no_above=no_above)

	#need to change
	description_lda.LDA_model(num_topics=num_topics,save=("./model/all_description.model"),show=show,set_matrix=False)
	      
	print "description's model of ", makers ," made"


class LDA_all(object):
	def __init__(self,makers,date="2014-6-04 23:59:59",filters = True,show=False,no_below=5, no_above=0.75,num_topics=300):
		self.categoryID = categoryIDtoMaker()
		self.makers = makers
		data = get_all_data(makers)
		data = FilterDate(data,date)
		print "data read"
		self.Auction = Auction(data,"all",filters = filters,show=show,no_below=no_below, no_above=no_above)
		print "model read"

	def predict(self,ID,threhold = 0.0,rate=2):
		testee = fetch_item(ID)
		if self.categoryID[int(testee['category_id'])] not in self.makers:
			raise NameError('No category_id found')
		else:
			return self.Auction.predict(testee['title'],testee['description'],threhold = threhold,rate=rate)




if __name__ == '__main__':
	maker_list=['NEC','SONY','FUJITSU','DELL','TOSHIBA']
	LDA_initial(maker_list)
	#PredictAll = LDA_all(maker_list)

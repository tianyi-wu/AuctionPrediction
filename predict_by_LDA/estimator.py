#coding:utf-8
import pandas as pd
import numpy as np
import MeCab
import math
import get_data_DB as db
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn import neighbors
from sklearn import svm
from sklearn import linear_model
from sklearn import cross_validation
from sklearn.preprocessing import Normalizer
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import crawler

'''
scikitのライブラリを使うためのテンプレート
estimatorを継承して、使いたいモデルを定義

.fit() をしてから
.predict('...')　でタイトルから価格を予測

.cross_validation() でデータを訓練用とテスト用に分け,それに基づいてscoreをだす
'''

def get_data(ID):
    data = crawler.fetch_item(ID)
    if data['condition']== u'new':
        condition = 1.0
    else: condition = 0.0
    data = [data['title'], float(data['init_price'])**(0.5), float(data['seller_point']), condition]
    return data

def analyzer(text):
    ret = []
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text.encode('utf-8'))
    while node:
        if node.feature.split(',')[0] == u'名詞'.encode('utf-8'):
            if len(node.surface) > 1:
                ret.append(node.surface)
        node = node.next
    return ret

def condition(text):
    if text == 'new': return 1
    else: return 0


def choice(price, x):
    aic = 10000000000
    dellist = []
    ind = None
    while 1:

        lis = [i for i in range(x.shape[1])]
        if aic != 10000000000: lis.pop(ind)
        x_cur = x[:, lis]
        model = sm.OLS(price, x_cur)
        results = model.fit()
        aic_tmp = results.aic
        #print aic_tmp, aic

        if aic < aic_tmp:
            dellist.pop()
            break

        #print 'delete variable'
        ind = results.pvalues.argmax()
        dellist.append(ind)
        x = x_cur
        aic = aic_tmp
    return x, dellist

def del_vector(vector, dellist):
    for i in range(len(dellist)):
        lis = [j for j in range(vector.shape[1])]
        lis.pop(dellist[i])
        vector = vector[:, lis]
    return vector


class data_store:
    
    def __init__(self, maker, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=10, exclude_0=True):
        
        self.MAX_DF = MAX_DF
        self.MAX_FEATURES = MAX_FEATURES
        self.LSA_DIM = LSA_DIM
        
        self.data = db.get_maker_data(maker)
        if exclude_0:
            self.data = self.data[self.data['bids']>0]
            
        self.data = self.data[self.data['end_time'] < datetime.datetime(2014, 6, 4, 23, 59)]
        self.price = map((lambda x: x**(0.5)),  self.data['current_price'].values)
        data = self.data[['init_price', 'seller_point', 'condition']]
        data['init_price'] = data['init_price'].apply(lambda x: x**(0.5))
        data['condition'] = data['condition'].apply(condition)
        data = data.astype(float)
        
        self.title_list = []
        for i in self.data.index:
            self.title_list.append(self.data.ix[i, 'title']) 
        self.tf, self.vectorizer, self.lsa = self.to_vector(self.title_list)
        
        self.sum = np.sum(data.values**2.0, axis=0)
        self.other = Normalizer(copy=False).fit_transform(data.T).T
        self.x = np.hstack([self.tf, self.other])
        
        
    def to_vector(self, title_list):
        
        vectorizer = TfidfVectorizer(analyzer=analyzer, max_df=self.MAX_DF)
        vectorizer.max_features = self.MAX_FEATURES       
        vectorizer.fit(title_list)
        tf = vectorizer.transform(title_list)
        
        lsa = TruncatedSVD(self.LSA_DIM)
        lsa.fit(tf)
        tf = lsa.transform(tf)
        return tf, vectorizer, lsa
    
    
    def output(self):
        return self.tf, self.data
    
    
class estimator(data_store):
    
    def __init__(self, maker, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=10, exclude_0=True):
        
        data_store.__init__(self, maker, MAX_DF, MAX_FEATURES, LSA_DIM, exclude_0)
    
    def fit(self):
        
        self.model.fit(self.x, self.price)
        
    def predict(self, ID): 
        
        list1 = get_data(ID)
        vector = self.vectorizer.transform([list1[0]])
        vector = self.lsa.transform(vector)
        array = np.array([list1[1:4]])**2 / self.sum
        array = array**0.5 
        vector= np.hstack([vector, array])
        
        estimated = self.model.predict(vector)
        return estimated
        
    
    def cross_validation(self):
        
        train_x, test_x, train_price, test_price = cross_validation.train_test_split(self.x, self.price, test_size=0.1, random_state=0)
        self.model.fit(train_x, train_price)
        
        return self.model.score(test_x, test_price)
    
    
    
'''
以下のように、使いたいモデルをself.modelに代入すればいい
パラメータや、predictの返り値で追加するものがあれば、改めて定義する
'''     

class KNeighbors(estimator):
    
    def __init__(self, maker, n_neighbors = 3, MAX_DF=0.3, MAX_FEATURES=300, LSA_DIM=30): #追加のパラメータがある場合はここに
        
        estimator.__init__(self, maker, MAX_DF, MAX_FEATURES, LSA_DIM)
        self.model = neighbors.KNeighborsRegressor(n_neighbors, weights='distance')
        
    def predict(self, ID): #近くの商品も調べたいので、改めて定義
        
        list1 = get_data(ID)
        vector = self.vectorizer.transform([list1[0]])
        vector = self.lsa.transform(vector)
        array = np.array([list1[1:4]])**2 / self.sum
        array = array**0.5 
        vector= np.hstack([vector, array])
        
        estimated = self.model.predict(vector)
        dist, ind = self.model.kneighbors(vector) 
        simmilar = self.data.ix[self.data.index[ind.tolist()[0]]]
        return estimated[0]**2.0 , simmilar
    
    
class SVR(estimator):
    
    def __init__(self, maker, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=10):
        
        estimator.__init__(self, maker, MAX_DF, MAX_FEATURES, LSA_DIM)
        self.model = svm.SVR(fit_intercept=False)
        
        
class LinearRegression(estimator):
    
    def __init__(self, maker, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=10):
        
        estimator.__init__(self, maker, MAX_DF, MAX_FEATURES, LSA_DIM)
        self.model = linear_model.LinearRegression(fit_intercept=False)
        
        
class BayesianRidge(estimator):
    
    def __init__(self, maker, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=10):
        
        data_store.__init__(self, maker, MAX_DF, MAX_FEATURES, LSA_DIM)
        self.model = linear_model.BayesianRidge( fit_intercept=False, normalize=True)


class Ridge(estimator):
    
    def __init__(self, maker, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=10):
        
        data_store.__init__(self, maker, MAX_DF, MAX_FEATURES, LSA_DIM)
        self.model = linear_model.RidgeCV(alphas=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5], fit_intercept=False, normalize=True, store_cv_values=True)
    
class Lasso(estimator):
    
    def __init__(self, maker, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=10, alpha=0.5):
        
        data_store.__init__(self, maker, MAX_DF, MAX_FEATURES, LSA_DIM)
        self.model = linear_model.Lasso(alpha=alpha, fit_intercept=False, normalize=True)
        
        
class LinearRegression2(estimator):
    
    def __init__(self, maker, MAX_DF=0.3, MAX_FEATURES=300, LSA_DIM=30, exclude_0=True):
        
        data_store.__init__(self, maker, MAX_DF, MAX_FEATURES, LSA_DIM, exclude_0)
        
        
    def fit(self):
        self.model = sm.OLS(self.price, self.x)
        results = self.model.fit()
        '''
        indlist = []
        for i in range(len(results.pvalues)):
            if results.pvalues[i] < 0.05:
                indlist.append(i)
        self.x = self.x[:, indlist]
        '''
        
        self.x, self.dellist = choice(self.price, self.x)
        self.model = sm.OLS(self.price, self.x)
        results = self.model.fit()
        self.results = results
               
    def predict(self, ID, ALPHA=0.5):
        list1 = get_data(ID)
        vector = self.vectorizer.transform([list1[0]])
        vector = self.lsa.transform(vector)
        array = np.array([list1[1:4]])**2.0 / self.sum
        array = array**0.5
        vector= np.hstack([vector, array])
        vector = del_vector(vector, self.dellist)
        
        estimated = self.results.predict(vector)
        prstdn, infa, supa = wls_prediction_std(self.results, vector, alpha = ALPHA)
        if infa[0] < 0:
            infa[0] = 0
        return estimated[0]**2.0, infa[0]**2.0, supa[0]**2.0
    
class LinearRegression3(estimator):
    
    def __init__(self, maker, MAX_DF=0.3, MAX_FEATURES=300, LSA_DIM=10, exclude_0=True):
        
        data_store.__init__(self, maker, MAX_DF, MAX_FEATURES, LSA_DIM, exclude_0)
        length = self.x.shape[1]
        
        for i in range(length):
            for j in range(i, length):
                tmp = self.x[:, i] * self.x[:, j]
                tmp = tmp[:, np.newaxis]
                self.x = np.hstack([self.x, tmp])
        '''
        for i in range(length):
            tmp = self.x[:, i] * self.x[:, i]
            tmp = tmp[:, np.newaxis]
            self.x = np.hstack([self.x, tmp])
        '''
        
    def fit(self):
        self.model = sm.OLS(self.price, self.x)
        results = self.model.fit()
        '''
        indlist = []
        for i in range(len(results.pvalues)):
            if results.pvalues[i] < 0.05:
                indlist.append(i)
        self.x = self.x[:, indlist]
        
        '''
        self.x, self.dellist = choice(self.price, self.x)
        self.model = sm.OLS(self.price, self.x)
        results = self.model.fit()
        self.results = results

        
    def predict(self, ID, ALPHA=0.5):
        list1 = get_data(ID)
        vector = self.vectorizer.transform([list1[0]])
        vector = self.lsa.transform(vector)
        array = np.array([list1[1:4]])**2.0 / self.sum
        array = array**0.5
        vector= np.hstack([vector, array])
        length = vector.shape[1]
        '''
        for i in range(length):
            tmp = vector[0][i] * vector[0][i]
            tmp = np.array([[tmp]])
            vector = np.hstack([vector, tmp])
        '''
        
        for i in range(length):
            for j in range(i, length):
                tmp = vector[0][i] * vector[0][j]
                tmp = np.array([[tmp]])
                vector = np.hstack([vector, tmp])        
        vector = del_vector(vector, self.dellist)
        
        estimated = self.results.predict(vector)
        prstdn, infa, supa = wls_prediction_std(self.results, vector, alpha = ALPHA)
        
        
        if infa[0] < 0:
            infa[0] = 0
        return estimated[0]**2.0, infa[0]**2.0, supa[0]**2.0         
            
            
            
            
            
            
            
            
            
        
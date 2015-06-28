#coding:utf-8
import pandas as pd
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn import neighbors
from sklearn import svm
from sklearn import linear_model
from sklearn import cross_validation

'''
scikitのライブラリを使うためのテンプレート
estimatorを継承して、使いたいモデルを定義

.fit() をしてから
.predict('...')　でタイトルから価格を予測

.cross_validation() でデータを訓練用とテスト用に分け,それに基づいてscoreをだす
'''


def analyzer(text):
    ret = []
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text.encode('utf-8'))
    while node:
        if node.feature.split(',')[0] == u'名詞'.encode('utf-8'):
            ret.append(node.surface)
        node = node.next
    return ret

class data_store:
    
    def __init__(self, filename, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=100):
        
        self.MAX_DF = MAX_DF
        self.MAX_FEATURES = MAX_FEATURES
        self.LSA_DIM = LSA_DIM
        
        self.data = pd.read_csv(filename)
        self.price = self.data['Price'].values
        self.title_list = []
        for i in self.data.index:
            self.title_list.append(self.data.ix[i, 'Title'].decode('utf-8')) 
        self.tf, self.vectorizer, self.lsa = self.to_vector(self.title_list)
        
    def to_vector(self, title_list):
        
        vectorizer = TfidfVectorizer(analyzer=analyzer, max_df=self.MAX_DF)
        vectorizer.max_features = self.MAX_FEATURES       
        vectorizer.fit(title_list)
        tf = vectorizer.transform(title_list)
        
        lsa = TruncatedSVD(self.LSA_DIM)
        lsa.fit(tf)
        tf = lsa.transform(tf)
        
        return tf, vectorizer, lsa
        
    def add_data(self, filename):
        
        newdata = pd.read_csv(filename)
        for i in newdata.index:
            self.title_list.append(newdata.ix[i, 'Title'].decode('utf-8'))
        self.data.append(newdata)
        self.price = self.data['Price'].values
        
        self.tf, self.vectorizer, self.lsa = self.to_vector(self.title_list)
    
    def output(self):
        return self.tf, self.data
    
    
class estimator(data_store):
    
    def __init__(self, filename, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=100):
        
        data_store.__init__(self, filename, MAX_DF, MAX_FEATURES, LSA_DIM)
    
    def fit(self):
        
        self.model.fit(self.tf, self.price)
        
    def predict(self, testee):
        
        vector = self.vectorizer.transform([testee.decode('utf-8')])
        vector = self.lsa.transform(vector)
        estimated = self.model.predict(vector)
        
        return estimated
    
    def cross_validation(self):
        
        train_tf, test_tf, train_price, test_price = cross_validation.train_test_split(self.tf, self.price, test_size=0.1, random_state=0)
        self.model.fit(train_tf, train_price)
        
        return self.model.score(test_tf, test_price)
    
    
    
    
'''
以下のように、使いたいモデルをself.modelに代入すればいい
パラメータや、predictの返り値で追加するものがあれば、改めて定義する
'''     

class KNeighbors(estimator):
    
    def __init__(self, filename, n_neighbors = 5, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=100): #追加のパラメータがある場合はここに
        
        estimator.__init__(self, filename, MAX_DF, MAX_FEATURES, LSA_DIM)
        self.model = neighbors.KNeighborsRegressor(n_neighbors,'uniform')
        
    def predict(self, testee): #近くの商品も調べたいので、改めて定義
        
        vector = self.vectorizer.transform([testee.decode('utf-8')])
        vector = self.lsa.transform(vector)
        estimated = self.model.predict(vector)
        dist, ind = self.model.kneighbors(vector) 
        simmilar = self.data.ix[ind.tolist()[0]]
        return estimated, simmilar, dist
    
    
class SVR(estimator):
    
    def __init__(self, filename, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=100):
        
        estimator.__init__(self, filename, MAX_DF, MAX_FEATURES, LSA_DIM)
        self.model = svm.SVR()
        
        
class LinearRegression(estimator):
    
    def __init__(self, filename, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=100):
        
        estimator.__init__(self, filename, MAX_DF, MAX_FEATURES, LSA_DIM)
        self.model = linear_model.LinearRegression()
        
        
class BayesianRidge(estimator):
    
    def __init__(self, filename, MAX_DF=0.1, MAX_FEATURES=300, LSA_DIM=100):
        
        data_store.__init__(self, filename, MAX_DF, MAX_FEATURES, LSA_DIM)
        self.model = linear_model.BayesianRidge()
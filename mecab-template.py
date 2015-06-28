#coding:utf-8
import pandas as pd
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

stopwords = [u'\u3000', u'\u2606', u'\u2605', u'\u25c7', u'\u25c6', u'\u25cb', u'\u25cf', u'\u25a0', u'\u25a1']

def analyzer(text):
    ret = []
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text.encode('utf-8'))
    while node:
        if node.feature.split(',')[0] == u'名詞':
            ret.append(node.surface)
        node = node.next
    return ret


def transform_data(filename,MAX_DF = 0.9, MAX_FEATURES = 500, LSA_DIM = 100):
    '''mecabのテンプレート、ファイルを読み込み、タイトルを形態素解析して次元圧縮して正規化かする。戻り値はデータセットとタイトルの行列'''
    data = pd.read_csv(filename)
    title = []
    for i in data.index:
        title.append(data.ix[i, 'Title'].decode('utf-8'))
    
    vectorizer = TfidfVectorizer(analyzer=analyzer ,max_df=MAX_DF, stop_words = stopwords)
    vectorizer.max_features = MAX_FEATURES
    X = vectorizer.fit_transform(title)
    lsa= TruncatedSVD(LSA_DIM)
    X = lsa.fit_transform(X)
    X = Normalizer(copy=False).fit_transform(X)

    return data,X

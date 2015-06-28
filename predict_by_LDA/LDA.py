# -*- coding: utf-8 -*-
import MeCab
import pandas as pd
import gensim

'''
def tokenize(text):
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text.encode('utf-8'))
    node = node.next
    while node:
        yield node.feature.split(',')[-3].decode('utf-8')
        node = node.next
'''

def get_words(contents):
    ret = []
    for content in contents:
        ret.append(get_words_main(content))
    return ret

def get_words_main(content):
    return tokenlize(content)

def read_data(filename):
    data = pd.read_csv(filename,header=0,sep=",")
    title_list = []
    for i in data.index:
        title_list.append(data.ix[i, 'Title'])#.decode('utf-8'))
    return data,title_list


def tokenlize(text):
    #mecab = MeCab.Tagger("-Owakati")
    #node = mecab.parse(text.encode('utf-8'))
    #return node
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text)#.encode('utf-8'))
    keywords = []
    while node:
        if node.feature.split(",")[0] == u"名詞":
            #yield node.surface
            keywords.append(node.surface)
        node = node.next
    return keywords

def vector_and_dictionary(titles,filter = False, save=None,show=False,no_below=3, no_above=0.6):
    ret=get_words(titles)
    dictionary = gensim.corpora.Dictionary(ret)

    if filter != True:
        unfiltered = dictionary.token2id.keys()
        dictionary.filter_extremes(no_below,no_above)
        filtered = dictionary.token2id.keys()
        filtered_out = set(unfiltered) - set(filtered)
        print filtered_out

    corpus = [dictionary.doc2bow(titleret) for titleret in ret]

    if show == True:
        print(dictionary.token2id)

    if save != None:
        dictionary.save_as_text(save)

    return ret,dictionary,corpus

def LDA_model(corpus,dictionary,num_topics=30,save=None,load=None,show=False):

    #dictionary = gensim.corpora.Dictionary.load_from_text('title_dic_filted.txt')
    if load == None:
        lda = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)    
        lda.save('ldawithoutnumber.model')
    else:
        lda = gensim.models.LdaModel.load(load)
    if show == True:
        for topic in lda.show_topics(-1):
            print topic
    #for topics_per_document in lda[corpus]:
    #print topics_per_document
    return lda






if __name__ == "__main__":
    data,titles=read_data("data.csv")
    ret,dictionary,corpus=vector_and_dictionary(titles,filter = True)   
    lda = LDA_model(corpus,dictionary,load='ldawithoutnumber.model')

    lda_index = gensim.similarities.MatrixSimilarity(lda[corpus])



    for m in xrange(len(titles)):
        lda_sims = lda_index[lda[corpus[m]]]
        print data['Price'][m],",  title : "  + titles[m]

        for (num,point) in sorted(enumerate(lda_sims), key=lambda item: -item[1])[:20]:
            print "title is similar with " + titles[num]
            print point, data['Price'][num]





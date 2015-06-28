import estimator
import crawler 
'''
categoryIDdic = {
    'ASUS':[2084307163,2084307164,2084307165,2084307166,2084307167],
    
    'Gateway':[2084307168,2084307169,2084307170,2084307171,2084307172],
    
    'HP':[2084307173,2084307174,2084307175,2084307176,2084307177],
    
    'IBM':[2084193598,2084193597,2084193596,2084193595],
    
    'NEC':[2084193571,2084193570,2084193569,2084193568,2084193567],
    
    'OTHERS':[2084042163,2084239900,2084239898,2084042164,2084042165,2084239901,2084239899,2084048237,2084042174],
    
    'ACER':[2084307178,2084307179,2084307180,2084307181,2084307182],
    
    'SHARP':[2084193576,2084193575,2084193574,2084193573,2084193572],
    
    'SOTEC':[2084307183,2084307184,2084307185,2084307186,2084307187],
    
    'SONY':[2084193581,2084193580,2084193579,2084193578,2084193577],
    
    'DELL':[2084193586,2084193585,2084193584,2084193583,2084193582],

    'PASONIC':[2084193589,2084193588,2084193587],
    
    'LENOVO':[2084307188,2084307189,2084307190,2084307191,2084307192],
    
    'TOSHIBA':[2084193594,2084193593,2084193592,2084193591,2084193590],
    
    'HITACHI':[2084307193,2084307194,2084307195,2084307196,2084307197],

    'FUJITSU':[2084193603,2084193602,2084193601,2084193600,2084193599]
    
}
'''
categoryIDdic = {
                 'NEC':[2084193571,2084193570,2084193569,2084193568,2084193567],
                 'SONY':[2084193581,2084193580,2084193579,2084193578,2084193577],
                 'FUJITSU':[2084193603,2084193602,2084193601,2084193600,2084193599],
                 'DELL':[2084193586,2084193585,2084193584,2084193583,2084193582],
                 'TOSHIBA':[2084193594,2084193593,2084193592,2084193591,2084193590]
                 }

dic_LR = {}
dic_LR2 = {}
dic_KN = {}


def search_maker(categoryID):
    
    for maker in categoryIDdic:
        if categoryID in categoryIDdic[maker]:
            return maker
    return 1

def update_LR():
    
    for maker in categoryIDdic:
        dic_LR[maker] = estimator.LinearRegression2(maker, LSA_DIM=30)
        dic_LR[maker].fit()
        
def update_LR2():
    
    for maker in categoryIDdic:
        dic_LR2[maker] = estimator.LinearRegression3(maker, LSA_DIM=10)
        dic_LR2[maker].fit()
        
def update_KN():
    
    for maker in categoryIDdic:
        dic_KN[maker] = estimator.KNeighbors(maker, LSA_DIM=10, n_neighbors=10)
        dic_KN[maker].fit()
        

def predict_LR(ID):
    
    testee = crawler.fetch_item(ID)
    maker = search_maker(int(testee['category_id']))
    if maker == 1: return 'Error'
    return dic_LR[maker].predict(ID)

def predict_LR2(ID):
    
    testee = crawler.fetch_item(ID)
    maker = search_maker(int(testee['category_id']))
    if maker == 1: return 'Error'
    return dic_LR2[maker].predict(ID)
    
def predict_KN(ID):
    
    testee = crawler.fetch_item(ID)
    maker = search_maker(int(testee['category_id']))
    if maker == 1: return 'Error'
    result = dic_KN[maker].predict(ID)
    cu = result[1].sort('current_price')
    return (result[0], cu.ix[cu.index[2], 'current_price'], cu.ix[cu.index[7], 'current_price'])
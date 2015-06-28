#coding:utf-8
import estimator

if __name__ == '__main__':
    
    KN = estimator.KNeighbors('data.csv', MAX_DF=0.2)
    SVR = estimator.SVR('data.csv', MAX_DF=0.2)
    LR = estimator.LinearRegression('data.csv', MAX_DF=0.2)
    BR = estimator.BayesianRidge('data.csv', MAX_DF=0.2)
    
    score = {'KN' : KN.cross_validation(), 'SVR' : SVR.cross_validation(), 'LR' : LR.cross_validation(), 'BR' : BR.cross_validation()}
    print score
    
    LR.fit()
    print LR.predict('VAIO VPCEA2AFJ Win7Home Corei5 160G 4G リカバリー済み')
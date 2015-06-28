#coding:utf-8
import clustering as cl

if __name__ == '__main__':
    '''
    クラス01234をcsvで出力
    文字コードはutf-8。　エクセルで見る場合は、サクラエディタとかでshift_JISに変換してから    
    '''
    
    current = cl.clustering('sony.csv')
    current.output_csv()
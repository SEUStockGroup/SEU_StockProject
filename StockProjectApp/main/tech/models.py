#先引入后面可能用到的包（package）
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from app.main import db
import datetime
import yfinance as yf
import pickle
import os
from sqlalchemy.sql import func
sns.set()

#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False


def get_data(stocks, start_date, end_date):
    '''stocks为股票代码和简称字典'''
    pk_path = "data.pk"
    if not os.path.exists(pk_path):
        data = pd.DataFrame()
        for code, name in stocks.items():
            dd = yf.Ticker(code)
            data[name] = dd.history(start=start_date, end=end_date)['Close']
        with open(pk_path, r"wb")as f:
            pickle.dump(data, f)
    else:
        with open(pk_path, r"rb")as f:
            data = pickle.load(f)
    data = data.iloc[2:, :].fillna(method='ffill')
    return data

# Machine Learning
class MachineLearning():
    # __tablename__ = 'stock_basic'
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # symbol = db.Column(db.String(30), index=True, comment=u"TS代码")



    def __init__(self):
        StockIndexs = {
            '000001.SS': '上证综指',
            '^DJI': '道琼斯',
            '^IXIC': '纳斯达克',
            '^N225': '日经225',
            '^HSI': '香港恒生',
            '^FCHI': '法国CAC40',
            '^GDAXI': '德国DAX'}
        # 获取数据
        start_date = '2019-01-01'
        end_date = '2019-10-31'
        self.data = get_data(StockIndexs, start_date, end_date)

        self.data.head()
        # 收益率相关性
        ret = self.data.apply(lambda x: (x / x.shift(1) - 1) * 100).dropna()
        sns.clustermap(ret.corr())
        plt.title('全球主要指数相关性', size=15)
        plt.show()

    def get(self):
        return self.data
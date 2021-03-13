# coding:utf-8
from flask import request, render_template, Response, globals

from app.main.tech import tech
from flask_login import login_required
import json
from app.main.tech.models import *
from app.main.common.alchemyEncoder import AlchemyEncoder
import datetime
from app.main.utils import utils


def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 股票列表
@tech.route('/涨跌预测', methods=["GET", "POST"])
@login_required
def stockList():
    if request.method == 'POST':
        ml = MachineLearning()
        count = 1
        items = ml.get()
        result = {
            "code": 0,
            "msg": "获取成功",
            "count": count,
            "data": items
        }
        return json.dumps(result, cls=AlchemyEncoder, ensure_ascii=False)
    return render_template('tech/涨跌预测.html')

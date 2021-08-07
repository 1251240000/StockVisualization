import re
import requests


def get_stock_basic(stock):
    url = f'https://hq.sinajs.cn/?list={stock.sinacode},{stock.sinacode}_i'
    
    try:
        req = requests.get(url)
        price, info = re.findall(r'"(.*)"', req.text)
        price, info = price.split(','), info.split(',')
        res = {
            'name': price[0],                   # 名称
            'code': stock.symbol,               # 代码
            'price': float(price[3]),           # 当前价格
            'date': price[30],                  # 更新日期
            'time': price[31],                  # 更新时间
            'open': float(price[1]),            # 今开
            'preclose': float(price[2]),       # 昨收
            'high': float(price[4]),            # 最高
            'low': float(price[5]),             # 最低
            'volume': float(price[8]),          # 成交量（股）
            'amount': float(price[9]),          # 成交额
            'pb': float(price[3]) / float(info[5]),     # 市净率
            'pe': float(price[3]) / float(info[3]),     # 市盈率
            'eps': float(info[25].split('|')[1]) / (float(info[7]) * 10000),    # 每股收益
            'bvps': float(info[5]),                     # 每股净资
            'totals': float(info[7]) * 10000,           # 总股本
            'outstanding': float(info[8]) * 10000,      # 流通股本
            'totalassets': float(price[3]) * float(info[7]) * 10000,    # 总资产
            'liquidassets': float(price[3]) * float(info[8]) * 10000,   # 流通资产
        }
        return res
    except Exception as e:
        print(e)
    
    return {}
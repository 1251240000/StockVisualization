'''
Description: 
Version: 1.0.1
Autor: hrlu.cn
Date: 2021-09-30 16:38:48
LastEditors: hrlu.cn
LastEditTime: 2021-09-30 17:41:05
'''
import re
import math
import requests

from utils.logger import Logger


''' 相邻排名 主营收
https://stock.finance.sina.com.cn/stock/api/jsonp.php//StockService.getRankBySymbol?symbol=sh600600&sort=cwblzyywsr&type=xl
'''
''' 相邻排名 净资产
https://stock.finance.sina.com.cn/stock/api/jsonp.php//StockService.getRankBySymbol?symbol=sh600600&sort=cwbljzcsyl&type=xl
'''
''' 资讯
https://quotes.sina.com.cn/cn/api/openapi.php/CB_AllService.getMemordlistbysymbol?callback=var%20noticeData=&num=8&PaperCode=600600
'''


def get_stock_basic_in_bulk(stocks):
    if not isinstance(stocks, (list, tuple)):
        stocks = stocks.values_list('sinacode', flat=True)
    
    sinacodes = stocks
    page_size = 128
    res = []
    
    for i in range(math.ceil(len(sinacodes) / page_size)):
        page = sinacodes[i * page_size: (i + 1) * page_size]
        query_param = '?list=' +  ','.join(f'{c},{c}_i' for c in page)
        url = "https://hq.sinajs.cn/" + query_param

        try:
            req = requests.get(url)
            rows = re.findall(r'"(.*)"', req.text)
            codes = re.findall(r'hq_str_(\D{2}\d{6})_i', req.text)

            for price, info, code in zip(rows[0::2], rows[1::2], codes):
                price, info = price.split(','), info.split(',')
                symbol = re.search(r'\d{6}', code).group()

                try:
                    res.append(
                        {
                            'name': price[0],                   # 名称
                            'sinacode': code,                   # 新浪编码
                            'code': symbol,                     # 代码
                            'price': float(price[3]),           # 当前价格
                            'date': price[30],                  # 更新日期
                            'time': price[31],                  # 更新时间
                            'open': float(price[1]),            # 今开
                            'preclose': float(price[2]),        # 昨收
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
                            'total_assets': float(price[3]) * float(info[7]) * 10000,    # 总资产
                            'liquid_assets': float(price[3]) * float(info[8]) * 10000,   # 流通资产
                        }
                    )
                except Exception as e:
                    Logger.warning("<utils.api.get_stock_basic_in_bulk>"
                                  f"Stock {symbol} parsing failed", e)

        except Exception as e:
            Logger.error("<utils.api.get_stock_basic_in_bulk>",
                         "Stock Basic fetching failed", e)
            return []
    
    return res


def get_stock_basic(stock):
    res = get_stock_basic_in_bulk([stock.sinacode])
    if res:
        return res[0]
    return {}
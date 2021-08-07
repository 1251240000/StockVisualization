import datetime

import tushare as ts

from config import TUSHARE_TOKEN, DEFAULT_PERIOD

ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api()


def get_stock_list(stock=None):
    '''
    input: None
    outputs: [
        {
            'ts_code': '000001.SZ', 'symbol': '000001', 'name': '平安银行', 
            'area': '深圳', 'industry': '银行', 'market': '主板', 'list_date': '19910403'
        },
        ………………
    ]
    input: < StockBasic 000001.SZ >
    outputs: {
        'ts_code': '000001.SZ', 'symbol': '000001', 'name': '平安银行', 
        'area': '深圳', 'industry': '银行', 'market': '主板', 'list_date': '19910403'
    }
    '''
    if stock is not None:
        df = pro.stock_basic(ts_code=stock.tscode)
        return df.loc[0].to_dict()
    
    df = pro.stock_basic()
    return df.to_dict('records')


def get_daily_quotation(stock):
    today = datetime.date.today()
    df = ts.pro_bar(
        ts_code=stock.tscode,
        start_date=str(
            today - datetime.timedelta(days=DEFAULT_PERIOD)
        ),
        ma=[5, 10, 20],
    )
    df['trade_date'] = df['trade_date'].apply(
        lambda x: x[:4]+'-'+x[4:6]+'-'+x[6:])
    return df.fillna(0)[::-1].to_dict('list')

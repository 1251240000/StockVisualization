from .models import *
import tushare as ts
import json

def get_stock(stockcode):
    try:
        stock_hist_data = ts.get_hist_data(stockcode)
        realtime_data = ts.get_realtime_quotes(stockcode).to_dict('record')[0]
        stock_basic = StockBasic.objects.get(code=stockcode)
    except:
        stock_hist_data = ts.get_hist_data('sh')
        realtime_data = ts.get_realtime_quotes('sh').to_dict('record')[0]
        stock_basic = StockBasic.objects.get(code='sh')
    
    stock_chart = {}
    stock_info = {}
    
    if stock_hist_data.index.tolist()[0] != realtime_data['date']:
        stock_chart['name'] = json.dumps(realtime_data['name'])
        stock_chart['date'] = json.dumps([realtime_data['date']] + stock_hist_data.index.tolist())
        stock_chart['open'] = json.dumps([float(realtime_data['open'])] + stock_hist_data['open'].tolist())
        stock_chart['close'] = json.dumps([float(realtime_data['price'])] + stock_hist_data['close'].tolist())
        stock_chart['high'] = json.dumps([float(realtime_data['high'])] + stock_hist_data['high'].tolist())
        stock_chart['low'] = json.dumps([float(realtime_data['low'])] + stock_hist_data['low'].tolist())
        stock_chart['volume'] = json.dumps([float(realtime_data['volume'])/100] + stock_hist_data['volume'].tolist())
        stock_chart['ma5'] = json.dumps([sum(json.loads(stock_chart['close'])[0:5])/5] + stock_hist_data['ma5'].tolist())
        stock_chart['ma10'] = json.dumps([sum(json.loads(stock_chart['close'])[0:10])/10] + stock_hist_data['ma10'].tolist())
        stock_chart['ma20'] = json.dumps([sum(json.loads(stock_chart['close'])[0:20])/20] + stock_hist_data['ma20'].tolist())
    else:
        stock_chart['name'] = json.dumps(realtime_data['name'])
        stock_chart['date'] = json.dumps(stock_hist_data.index.tolist())
        for i in ['open', 'close', 'high', 'low', 'volume', 'ma5', 'ma10', 'ma20']:
            stock_chart[i] = json.dumps(stock_hist_data[i].tolist())
    
    
    for i in ['name', 'code', 'date', 'time', 'price', 'open', 'pre_close', 'high', 'low', 'volume', 'amount']:
        if i in ['name', 'code', 'date', 'time']:
            stock_info[i] = realtime_data[i]
        elif i in ['price', 'open', 'pre_close', 'high', 'low']:
            stock_info[i] = '%.2f'%float(realtime_data[i])
        elif i in ['volume', 'amount']:
            stock_info[i] = '%.2f'%(float(realtime_data[i])/1e8)+'亿' if float(realtime_data[i])>1e8 else '%.2f'%(float(realtime_data[i])/1e4)+'万'
    #stock_info['max'] = '%.2f'%(1.1*float(realtime_data['pre_close']))
    #stock_info['min'] = '%.2f'%(0.9*float(realtime_data['pre_close']))
    stock_info['change'] = '%.2f'%(float(stock_info['price']) - float(stock_info['pre_close']))
    stock_info['pchange'] = '%.2f'%(float(stock_info['change'])*100 / float(stock_info['pre_close'])) + '%'
    
    
    stock_info['pb'] = '%.2f'%float(stock_basic.pb) if stock_basic.pb != '-' else '-'
    stock_info['pe'] = '%.2f'%float(stock_basic.pe) if stock_basic.pe != '-' else '-'
    stock_info['esp'] = '%.2f'%float(stock_basic.esp) if stock_basic.esp != '-' else '-'
    stock_info['bvps'] = '%.2f'%float(stock_basic.bvps) if stock_basic.bvps != '-' else '-'
    stock_info['totals'] = '%.2f'%float(stock_basic.totals)+'亿' if stock_basic.totals != '-' else '-'
    stock_info['outstanding'] = '%.2f'%float(stock_basic.outstanding)+'亿' if stock_basic.outstanding != '-' else '-'
    stock_info['totalAssets'] = '%.2f'%float(stock_basic.totalAssets)+'亿' if stock_basic.totalAssets != '-' else '-'
    stock_info['liquidAssets'] = '%.2f'%float(stock_basic.liquidAssets)+'亿' if stock_basic.liquidAssets != '-' else '-'
    
    return {'stock_chart': stock_chart, 'stock_info': stock_info }


def get_stock_quote(stockcode):
    try:
        realtime_data = ts.get_realtime_quotes(stockcode).to_dict('record')[0]
    except:
        realtime_data = ts.get_realtime_quotes('000001').to_dict('record')[0]
    
    stock_quote ={}
    
    for i in realtime_data.keys():
        if i not in ['price', 'open', 'pre_close', 'high', 'low', 'a1_p', 'a2_p', 'a3_p', 'a4_p', 'a5_p', 'b1_p', 'b2_p', 'b3_p', 'b4_p', 'b5_p']:
            stock_quote[i] = realtime_data[i]
        else:
            stock_quote[i] = '%.2f'%float(realtime_data[i])
            
    stock_quote['change'] = '%.2f'%(float(stock_quote['price']) - float(stock_quote['pre_close']))
    stock_quote['pchange'] = '%.2f'%(float(stock_quote['change'])*100 / float(stock_quote['pre_close'])) + '%'
    
    return {'stock_quote': stock_quote }
    
def get_stocks(stockcodes):
    realtime_data = ts.get_realtime_quotes(stockcodes)
    stock_sim_info = []
    for i in realtime_data.index:
        stock_sim_info.append({'sindex': stockcodes[i], 'code': realtime_data.loc[i]['code'], 'name': realtime_data.loc[i]['name'], 'price': '%.2f'%float(realtime_data.loc[i]['price']), 'pchange': '%.2f'%((float(realtime_data.loc[i]['price']) - float(realtime_data.loc[i]['pre_close']))*100 / float(realtime_data.loc[i]['pre_close'])) + '%' })
    return {'stock_sim_info': stock_sim_info }
    
def get_rf_list():
    rise_list = [{'code':i.code,'name':i.name,'changepercent':'%.2f'%float(i.changepercent)+"%",'trade':i.trade,'open':i.open,'high':i.high,'low':i.low,'settlement':i.settlement,'volume':'%.2f'%(float(i.volume)/1e8)+'亿' if float(i.volume)>1e8 else '%.2f'%(float(i.volume)/1e4)+'万','turnoverratio':'%.2f'%float(i.turnoverratio)+"%",'amount':'%.2f'%(float(i.amount)/1e8)+'亿' if float(i.amount)>1e8 else '%.2f'%(float(i.amount)/1e4)+'万','per':'%.2f'%float(i.per),'pb':'%.2f'%float(i.pb),'mktcap':i.mktcap,'nmc':i.nmc} for i in StockRank.objects.all() if '-' not in i.changepercent]
    fall_list = [{'code':i.code,'name':i.name,'changepercent':'%.2f'%float(i.changepercent)+"%",'trade':i.trade,'open':i.open,'high':i.high,'low':i.low,'settlement':i.settlement,'volume':'%.2f'%(float(i.volume)/1e8)+'亿' if float(i.volume)>1e8 else '%.2f'%(float(i.volume)/1e4)+'万','turnoverratio':'%.2f'%float(i.turnoverratio)+"%",'amount':'%.2f'%(float(i.amount)/1e8)+'亿' if float(i.amount)>1e8 else '%.2f'%(float(i.amount)/1e4)+'万','per':'%.2f'%float(i.per),'pb':'%.2f'%float(i.pb),'mktcap':i.mktcap,'nmc':i.nmc} for i in StockRank.objects.all() if '-' in i.changepercent]
    return {'rise_list': rise_list, 'fall_list': fall_list }

def get_news():
    news_list = [{'title':i.title, 'content':i.content, 'pubtime':i.pubtime, 'src':i.src} for i in MajorNews.objects.all()]
    return {'news_list': news_list }

def get_user_photo(uid):
    user_photo = {}
    if uid:
        user_photo['src'] = '/static/img/h1.png'
    else:
        user_photo['src'] = '/static/img/guest.png'
    return {'user_photo': user_photo }

def get_user_profile(uid):
    try:
        u = UserInfo.objects.get(id=uid)
    except:
        return None
    user_profile = {}
    user_profile['name'] = u.name
    user_profile['email'] = u.email if u.email != None else "未填写"
    user_profile['phone'] = u.phone
    user_profile['country'] = u.country
    user_profile['createtime'] = u.createtime
    return {'user_profile': user_profile }
    
def get_records(uid):
    records = UserInfo.objects.get(id=uid).selfrecords
    if records == None:
        return {'b_records': [], 'a_records': [] }
    rindex = records.split(';')
    stockcodes = [Records.objects.get(id=i).code for i in rindex]
    realtime_data = ts.get_realtime_quotes(stockcodes)
    stockprices ={realtime_data.loc[i]['code']:'%.2f'%float(realtime_data.loc[i]['price']) for i in realtime_data.index}
    
    b_records = []
    a_records = []
    for i in rindex:
        record = {}
        record['id'] = i
        record['code'] = Records.objects.get(id=i).code
        record['name'] = Records.objects.get(id=i).name
        record['price'] = stockprices[record['code']]
        record['bprice'] = Records.objects.get(id=i).bprice
        record['bvolume'] = Records.objects.get(id=i).bvolume
        record['btime'] = Records.objects.get(id=i).btime
        if not Records.objects.get(id=i).issold:
            b_records.append(record)
        else:
            record['aprice'] = Records.objects.get(id=i).aprice
            a_records.append(record)
    return {'b_records': b_records, 'a_records': a_records }



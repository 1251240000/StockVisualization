import tushare as ts
from ui.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'refresh data'

    def handle(self, *args, **option):
        stock_basics = ts.get_stock_basics()
        sb = []
                
        for i in stock_basics.index:
            sb.append(StockBasic(code = i, name = stock_basics.loc[i]['name'], industry = stock_basics.loc[i]['industry'], area = stock_basics.loc[i]['area'], pb = str(stock_basics.loc[i]['pb'])[:10], pe = str(stock_basics.loc[i]['pe'])[:10], esp = str(stock_basics.loc[i]['esp'])[:10], bvps = str(stock_basics.loc[i]['bvps'])[:10], totals = str(stock_basics.loc[i]['totals'])[:10], outstanding = str(stock_basics.loc[i]['outstanding'])[:10], totalAssets = str(stock_basics.loc[i]['totalAssets'])[:10], liquidAssets = str(stock_basics.loc[i]['liquidAssets'])[:10]))
        for i in ['sh', 'sz', 'sh000001', 'sz000001', 'hs300', 'sz50', 'zxb', 'cyb']:
            sb.append(StockBasic(code = i, name = '-', industry = '-', area = '-', pb = '-', pe = '-', esp = '-', bvps = '-', totals = '-', outstanding = '-', totalAssets = '-', liquidAssets = '-'))
                
        StockBasic.objects.all().delete()
        try:
            StockBasic.objects.bulk_create(sb)
        except:
            for i in sb:
                i.save()
                

        today_all = ts.get_today_all()
        ta = []
                
        for i in range(60):
            s = today_all.loc[today_all['changepercent']==today_all.loc[:,'changepercent'].max()] if i < 30 else today_all.loc[today_all['changepercent']==today_all.loc[:,'changepercent'].min()]
            ta.append(StockRank(code = s.code[s.index[0]], name = s.name[s.index[0]], changepercent = str(s.changepercent[s.index[0]])[:10], trade = str(s.trade[s.index[0]])[:10], open = str(s.open[s.index[0]])[:10], high = str(s.high[s.index[0]])[:10], low = str(s.low[s.index[0]])[:10], settlement = str(s.settlement[s.index[0]])[:10], volume = str(s.volume[s.index[0]])[:10], turnoverratio = str(s.turnoverratio[s.index[0]])[:10], amount = str(s.amount[s.index[0]])[:10], per = str(s.per[s.index[0]])[:10], pb = str(s.pb[s.index[0]])[:10], mktcap = str(s.mktcap[s.index[0]])[:10], nmc = str(s.nmc[s.index[0]])[:10]))
            today_all = today_all.drop(s.index[0])
                    
        StockRank.objects.all().delete()
        try:
            StockRank.objects.bulk_create(ta)
        except:
            for i in ta:
                i.save()


        ts.set_token('28f87746bb4a4ba473955c650ce102cea7e5d07affc5a18266a12a1a')
        tp = ts.pro_api()
        major_news = tp.major_news(fields='title,content,pub_time,src')

        mn = []

        for i in major_news.index:
            content_fixed = major_news.loc[i]['content'].replace('\n','<br>')
            content_fixed = content_fixed.replace('(image_address=','<img style="float:left;" src=')
            content_fixed = content_fixed.replace('")','">')
            content_fixed = content_fixed[:content_fixed.find('关注同花顺')] if content_fixed.find('关注同花顺') else content_fixed
            content_fixed = content_fixed.replace('😊','')
            mn.append(MajorNews(title = major_news.loc[i]['title'], content = content_fixed, pubtime = major_news.loc[i]['pub_time'], src = major_news.loc[i]['src']))

        MajorNews.objects.all().delete()
        try:
            MajorNews.objects.bulk_create(mn)
        except:
            for i in mn:
                i.save()

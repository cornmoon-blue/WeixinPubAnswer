#-*- coding:utf-8 -*-
import urllib2
import sys
import string
from stockcode import DICT_STOCKCODE

#reload(sys)
#sys.setdefaultencoding('gbk')

def is_stockcode(aKey):  #检查用户输入是否股票代码
    if aKey.isdigit():
        if DICT_STOCKCODE.has_key(aKey):
            return True
        else:
            return False
    else:
        return False

################################################################
def get_stock_info(symbol):  #获得股票相关信息
    ex_symbol = ("sh" if (int(symbol) // 100000 > 3) else "sz") + symbol
    url = 'http://hq.sinajs.cn/list=%s' % ex_symbol
    except_times = 0
    try:
        req = urllib2.Request(url)
        res =  urllib2.urlopen(req)
        data = res.read()
        res.close()
    except:
        except_times += 1
        if except_times>4:
            return None
        else:
            data = get_stock_info(symbol)
    return data

class StockInfo:
    """docstring for ClassName"""
    def __init__(self,symbol):
        if is_stockcode(symbol):
            self.is_stockcode = True
            self.stock_code = symbol
            self.stock_abbr = DICT_STOCKCODE[symbol].decode('utf8')
            data = get_stock_info(symbol)
            data_list = data.split(',')
            if len(data_list)==1:
                self.is_nodata = True
                self.price_open = '0.0'
                self.price_current = '0.0'
                self.price_high = '0.0'
                self.price_low = '0.0'
                self.volume = '0.0'
                self.trade_date = '0'
                self.trade_time = '0'
            else:
                self.is_nodata = False
                self.price_open = data_list[1]
                self.price_current = data_list[3]
                self.price_high = data_list[4]
                self.price_low = data_list[5]
                self.volume = data_list[8]
                self.trade_date = data_list[30]
                self.trade_time = data_list[31]
        else:
            self.is_stockcode = False
            self.stock_code = ''
            self.stock_abbr = ''
    
    def get_price_open(self):
        if self.is_stockcode and (not self.is_nodata):
            return self.price_open
        else:
            return 0.0
    def get_price_current(self):
        if self.is_stockcode and (not self.is_nodata):
            return self.price_current
        else:
            return 0.0
    def get_price_high(self):
        if self.is_stockcode and (not self.is_nodata):
            return self.price_high
        else:
            return 0.0
    def get_price_low(self):
        if self.is_stockcode and (not self.is_nodata):
            return self.price_low
        else:
            return 0.0
    def get_volume(self):
        if self.is_stockcode and (not self.is_nodata):
            return round(float(self.volume)/1000000,4)  #单位：万手
        else:
            return 0.0
    def get_trade_date(self):
        if self.is_stockcode and (not self.is_nodata):
            return self.trade_date
        else:
            return 0.0
    def get_trade_time(self):
        if self.is_stockcode and (not self.is_nodata):
            return self.trade_time
        else:
            return 0.0
    def get_pricechange_percentage(self):
        if float(self.price_open)>0 and self.is_stockcode and (not self.is_nodata):
            return round(((float(self.price_current) - float(self.price_open))/float(self.price_open)) * 100, 2)  #百分值
        else:
            return 0.0
    
    def output_plain_info(self):
        if self.is_stockcode:
            if self.is_nodata:
                content = u'@_@...未查询到股票 '+self.stock_code+u' 的信息...'
                return content
            else:
                content = u"您查询的信息如下：\n" \
                u'股票代码：'+self.stock_code+'('+self.stock_abbr+')\n' \
            	u'交易日期：'+self.trade_date + u'\n'\
            	u'更新时间：'+self.trade_time + u'\n'\
            	u'开  盘  价：'+self.price_open + u'  元\n'\
            	u'当  前  价：'+self.price_current + u'  元\n'\
            	u'当日高价：'+self.price_high + u'  元\n'\
            	u'当日低价：'+self.price_low + u'  元\n'\
            	u'涨  跌  幅：'+str(self.get_pricechange_percentage()) + u'%\n'\
            	u'成  交  量：'+str(self.get_volume()) + u'万手'
            	return content
        else:
            content = u'提醒：您输入的股票代码有误...《-请输入六位数字股票代码-》'
            return content
        
    def output_Kgraph_url(self):
        symbol = self.stock_code
        ex_symbol = ("sh" if (int(symbol) // 100000 > 3) else "sz") + symbol
        url = 'http://image.sinajs.cn/newchart/daily/n/%s.gif' % ex_symbol  #新浪K线图
        return url
    def output_ifeng_stockpage(self):
        symbol = self.stock_code
        ex_symbol = ("sh" if (int(symbol) // 100000 > 3) else "sz") + symbol
        url = 'http://i.ifeng.com/finance/hq/finance/hq/hs_stock?code=' + ex_symbol  #凤凰财经
        #url = 'http://m.10jqka.com.cn/doctor/%s/' % symbol  #同花顺诊股
        return url
    def output_description(self):
        desc_txt = u'交易日期：'+self.trade_date +'@'+self.trade_time + '\n'+\
        u'开盘价：'+self.price_open + u'元；' + u'当日高价：'+self.price_high + u'元\n' +\
        u'当前价：'+self.price_current + u'元；' + u'当日低价：'+self.price_low + u'元\n' +\
        u'涨跌幅：'+str(self.get_pricechange_percentage()) + u'%；' + u'成交量：'+str(self.get_volume()) + u'万手'
        return desc_txt
    
    def output_news_data(self):
        symbol = self.stock_code
        ex_symbol = ("sh" if (int(symbol) // 100000 > 3) else "sz") + symbol
        
        title_head = self.stock_code+'('+self.stock_abbr+')'+u'【行情速递】'
        desc_txt_head = u'交易日期：'+self.trade_date +'@'+self.trade_time + '\n'+\
        	u'开盘价：'+self.price_open + u'元；' + u'当日高价：'+self.price_high + u'元\n' +\
        	u'当前价：'+self.price_current + u'元；' + u'当日低价：'+self.price_low + u'元\n' +\
        	u'涨跌幅：'+str(self.get_pricechange_percentage()) + u'%；' + u'成交量：'+str(self.get_volume()) + u'万手'
        url_img_head = 'http://image.sinajs.cn/newchart/daily/n/%s.gif' % ex_symbol  #新浪K线图
        #url_page_A = url = 'http://i.ifeng.com/finance/hq/finance/hq/hs_stock?code=' + ex_symbol  #凤凰财经
        url_page_A = 'http://stocks.sina.cn/sh/?code='+ ex_symbol + '&vt=4'  #新浪财经
        
        title_page_B = self.stock_code+'('+self.stock_abbr+')'+u'【同花顺诊股】'
        desc_txt_B = u'同花顺诊股：'+title_head
        url_img_B = 'http://images.liqucn.com/h43/h73/images201504180323290128_info72X72.png'
        url_page_B = 'http://m.10jqka.com.cn/doctor/%s/' % symbol  #同花顺诊股
        
        title_page_C = self.stock_code+'('+self.stock_abbr+')'+u'【雪球论股】'
        desc_txt_C = u'雪球论股：'+title_head
        url_img_C = 'http://a1575.phobos.apple.com/us/r1000/092/Purple2/v4/fb/2d/b1/fb2db1f1-c0af-ef55-ad1e-a6975867b97b/mzl.duqxcdwg.png'
        url_page_C = 'http://xueqiu.com/S/%s' % ex_symbol  #雪球论股
        
        data = [[title_head,desc_txt_head,url_img_head,url_page_A],\
                [title_page_C,desc_txt_C,url_img_C,url_page_C],\
                [title_page_B,desc_txt_B,url_img_B,url_page_B]]
        return data
##################################################################################
        
        

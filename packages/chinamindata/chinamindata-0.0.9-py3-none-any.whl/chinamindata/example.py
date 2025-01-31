# 示例调用

#重要：：：token必须设置：：：
import chinamindata.min as ts

ts.set_token('b3020476da6c9bc7d919e45f16417bc25')
ts.pro_api('3020476da6c9bc7d919e45f16417bc25')

import chinamindata.min as ts

#1可以获取大A股票分钟，freq取值1min'、'5min'、'15min'、'30min'、'60min'

df = ts.pro_bar(ts_code = '000001.SZ', start_date = '2024-07-07 09:00:00',
                       end_date = '2024-07-22 15:00:00',freq='60min',)
print(df)

#2可以获取大A股票分钟开盘竞价

pro = ts.pro_api()
df=pro.stk_auction_o(trade_date='20241122')
print(df)

# #3可以获取大A股票分钟闭盘竞价

pro = ts.pro_api()
df=pro.stk_auction_c(trade_date='20241122')
print(df)
#
#
# #4可以获取大A股票、指数、基金的列表.type取值'stock',"MSCI","CSI","SSE","SZSE","CICC","SW","OTH","E","O"
from chinamindata.china_list import get_list
ts.set_token('3020476da6c9bc7d919e45f16417bc25')
df = get_list(type="stock")
print(df)
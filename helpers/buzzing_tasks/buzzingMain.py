import requests,pandas as pd,datetime
from bs4 import BeautifulSoup

pe_threshold = 25
pb_threshold = 2.75
mkt_cr_threshold = 1
skip_row_count = 2
date_obj = datetime.datetime.now()
selected_stock_golden,selected_stock = [],[]

buzz_request_list = [
    ['https://chartink.com/screener/golden-crossover-50-200-sma','scan_clause=(+%7Bcash%7D+(+50+days+ago+sma(+close%2C20+)+%3E+200+days+ago+sma(+close%2C20+)+)+)+','Golden Cross Over based on fundamentals'],
    ['https://chartink.com/screener/short-term-breakouts','scan_clause=(+%7Bcash%7D+(+latest+max(+5+%2C+latest+close+)+%3E+6+days+ago+max(+120+%2C+latest+close+)+*+1.05+and+latest+volume+%3E+latest+sma(+volume%2C5+)+and+latest+close+%3E+1+day+ago+close+)+)+','Short term breakout'],
    ['https://chartink.com/screener/15-minute-stock-breakouts','scan_clause=(+%7B57960%7D+(+%5B0%5D+15+minute+close+%3E+%5B-1%5D+15+minute+max(+20+%2C+%5B0%5D+15+minute+close+)+and+%5B0%5D+15+minute+volume+%3E+%5B0%5D+15+minute+sma(+volume%2C20+)+)+)+','15 minutes breakout'],
    ['https://chartink.com/screener/bullish-marubozu-for-15-min','scan_clause=(+%7B57960%7D+(+%5B0%5D+15+minute+close+%3E+%5B0%5D+15+minute+open+and+%5B0%5D+15+minute+high+%3C%3D+%5B0%5D+15+minute+close+*+1.0005+and+%5B0%5D+15+minute+low+%3E%3D+%5B0%5D+15+minute+open+*+0.9995+and+%5B0%5D+15+minute+close+%3E+latest+open+*+1.05+and(+%5B0%5D+15+minute+high+-+%5B0%5D+15+minute+open+)+*+.65+%3C%3D+(+%5B0%5D+15+minute+close+-+%5B0%5D+15+minute+open+)+and+%5B0%5D+15+minute+close+%3E+%5B0%5D+15+minute+open+and+%5B0%5D+15+minute+volume+%3E%3D+1000+)+)+','Bullish marubozu - 15 min']
]

def goldenChecker(symbol):
    try:
        url = f'https://site.financialmodelingprep.com/financial-summary/{symbol}.NS'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        df = pd.read_html(str(soup))
        pe_flag,pb_flag,mc_flag = False,False,False
        for x in df:
            tb = x.values.tolist()
            for t in tb:
                key = t[0]
                value = t[1]      
                if(key =='P/E' and value != '-'):            
                    pe_num = float(value)
                    pe_flag = 1 < pe_num < pe_threshold
                if(key =='P/B' and value != '-'):
                    pb_num = float(value)
                    pb_flag = pb_num > 0 and pb_num < pb_threshold
                if(key=='Market Cap' and value != '-'):
                # 1 million = 0.1 Crores  ||   1 billion = 100 Crores  ||  1 trillion = 100000 Crores
                    if('T' in value or 'B' in value or  'M' in value):
                        v = value.replace('T','').replace('M','').replace('B','')
                        mc_num = float(v)
                    else:
                        mc_num = float(value)
                    if('T' in value):
                        mc_num = mc_num * 100000
                    elif('B' in value):
                        mc_num = mc_num * 100
                    elif('M' in value):
                        mc_num = mc_num * 0.1
                    if mc_num > mkt_cr_threshold :
                        mc_flag = True
        if (pe_flag == True and pb_flag == True and mc_flag == True):
            selected_stock_golden.append(symbol)
                    
    except Exception as e:
        print(str(e))

def getLogoUrl(ticker):
        return requests.get(f'https://gateway.alphaq.uat.fegno.com/api/v1/utilities/search?q={ticker}')

def request_report(token,qry,file_bio):
    cookies = {
        'XSRF-TOKEN': token[0],
        'ci_session': token[1],
    }

    headers = {
        'Host': 'chartink.com',
        # 'Content-Length': '96',
        'Sec-Ch-Ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'X-Csrf-Token': token[2],
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Origin': 'https://chartink.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://chartink.com/screener/golden-crossover-50-200-sma',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        # 'Cookie': 'XSRF-TOKEN=eyJpdiI6Im1yTTZOcVNlT1ZHUU1yQU1NeThQbGc9PSIsInZhbHVlIjoiTmh0NzJaeVk2amFYd2VBRG5KdUtFem4vcGRwOVp6TWUxYlNSUEFnWUY5dzcvZGhDK2FFZzRkNnRZei94ZjN3NDl0UmNYNEVzWkdINFRpT0RLdk5iRXA0WTc0b1Ftc0ZJV1dicG92Q2I2NzBwRGdqMW5ObVUycEV0bG5MaDJSYWkiLCJtYWMiOiI2OThhMDgyY2FkMDEyMDE1MzQ0MzQ5ZmE0ODQ1NzhjMTVkZmMzZGRiMGIxNTM0OTQyZDBlZjJlMTA4NmVjNzAzIiwidGFnIjoiIn0%3D; ci_session=eyJpdiI6Ik94VXVKR2cwbmxkUno4QzBHZit1ZUE9PSIsInZhbHVlIjoiR3poRWRZNkQ3U05mRmVVbVozTnd0aVU5TlRWeFZLbUpQK3FVMVhndkFpaGhUV043YjVQMkNNM0J1d0lZKyt3RVdFY3ZaTWxPNEtGRC90czA5R1dwdElPU3dJdW1MOWw1ZnZlVk5PYnR6OGdzVXNlQlhJZXlXd0Njc01VR3htUlkiLCJtYWMiOiI4YTMzOGQ4MTExYzU1OGFjODc1Y2Y1YzJmOTQyNTdkOTQ1Y2JkMmZjNjM4NjZmZjc2NTE2MTE4ZTJmOWRkYzNjIiwidGFnIjoiIn0%3D',
    }

    data = qry

    response = requests.post('https://chartink.com/screener/process', cookies=cookies, headers=headers, data=data, verify=False)
    df = pd.DataFrame(response.json())
    data_df =df['data']
    df_price_based = [d['nsecode'] for d in data_df if 50 < d['close'] < 250]
    
    if(file_bio == 'Golden Cross Over based on fundamentals'):
        for s in df_price_based:
            logoUrl = goldenChecker(s)
            if len(selected_stock_golden) == 4:
                break
        for sc in selected_stock_golden:
            logoUrl = ((getLogoUrl(sc)).json())['results'][0]['logo']
            selected_cell = [sc, 'Long Term', logoUrl, file_bio]
            selected_stock.append(selected_cell)     

    else:
        for si in df_price_based[0:3]: 
            if(si !='M&MFIN'): #TODO: remove this line
                logoUrl = ((getLogoUrl(si)).json())['results'][0]['logo']
                selected_cell = [si, 'Short Term', logoUrl, file_bio]
                selected_stock.append(selected_cell)

def getBuzzStocks(count):    
    for bx in buzz_request_list:
        main_response = requests.get(bx[0])
        token = main_response.cookies.values()
        soup = BeautifulSoup(main_response.text,'html.parser')
        csrf_token = soup.find('meta',{'name':'csrf-token'})
        if csrf_token:
            token.append(csrf_token['content'])
        request_report(token,qry = bx[1],file_bio = bx[2])
    return selected_stock[:count]
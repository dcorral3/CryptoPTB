from datetime import datetime
from pprint import pprint

def parse_coin_cc(data=None, currency='USD'):
    update_time = datetime.fromtimestamp(data['LASTUPDATE']).strftime("%H:%M:%S")
    coin = {
            'symbol': data['FROMSYMBOL'],
            'value': data['PRICE'],
            'time': update_time
           }
    return coin

def parse_coin_cmc(data=None, currency='USD'):
    _coin = data['quotes'][currency]
    name = data['name']
    percent_change_1h = _coin['percent_change_1h']
    percent_change_24h = _coin['percent_change_24h']
    percent_change_7d = _coin['percent_change_7d']
    coin = {'name': name,
            'percent_change_1h': percent_change_1h,
            'percent_change_24h': percent_change_24h,
            'percent_change_7d': percent_change_7d}
    return coin

def clear_cmc_list(coins=None):
    coin_list = []
    for coin in coins:
        my_dict = {
                    '_id': coin['id'],
                    'name': coin['name'],
                    'symbol': coin['symbol']
                  }

        coin_list.append(my_dict)
    return coin_list

def clear_cc_list(coins=None):
    coin_list = []
    for coin in coins.items():
        my_dict = {
                    '_id': coin[1]['Id'],
                    'name': coin[1]['CoinName'],
                    'symbol': coin[1]['Symbol']
                  }
        coin_list.append(my_dict)
    return coin_list

def url_generator(url_type=None, symbol=None, coin_id=None, currency='USD'):
    url = {
        'cc_single_coin' : "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}".format(symbol, currency),
        'cmc_single_coin': "https://api.coinmarketcap.com/v2/ticker/{}/?convert={}".format(coin_id, currency),
        'top_10'         : "https://api.coinmarketcap.com/v2/ticker/?structure=array&limit=10",
        'all_coins'      : "https://api.coinmarketcap.com/v2/listings/",
        'hour_graph'     : "https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit=59".format(symbol, currency),
        'day_graph'      : "https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit=1440".format(symbol, currency),
        'week_graph'     : "https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&limit=168".format(symbol, currency),
        'month_graph'    : "https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&limit=720".format(symbol, currency)
    }
    return url[url_type]
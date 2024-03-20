from requests import get, Response

MARKETS = {
    'binance': {
        'name':    'Binance',
        'api_url': 'https://api.binance.com/api/v3/ticker/price?symbol={}'
    },
    'coinbase': {
        'name':    'Coinbase',
        'api_url': 'https://api.coinbase.com/v2/exchange-rates?currency={}'
    },
    'blockchain.com': {
        'name':    'Blockchain.com',
        'api_url': 'https://blockchain.info/tobtc?currency={}&value=1'
    }
}


def get_available_markets() -> list[str]:
    return sorted([MARKETS[market]['name'] for market in MARKETS])


def get_symbol_price(pair: str, market: str = 'Binance', prefer_currency: str = 'USDT') -> float:
    market = market.lower()
    pair = pair.upper()
    match market:
        case 'binance':
            return get(MARKETS[market]['api_url'].format(pair.replace('/', ''))).json()['price']
        case 'coinbase':
            return get(MARKETS[market]['api_url'].format(pair.split('/')[0])).json()['data']['rates'][pair.split('/')[1] if len(pair.split('/')) > 1 else prefer_currency.upper()]
        case 'blockchain.com':
            if (pair.split('/')[1] if len(pair.split('/')) > 1 else prefer_currency.upper()) != 'BTC':
                raise ValueError('"blockchain.com" supports conversion to BTC only')
            return get(MARKETS[market]['api_url'].format(pair.split('/')[0])).json()
    raise ValueError(f'No such market: "{market}"')

def get_symbols_prices(pairs: list[str], market: str = 'Binance') -> dict[str, float | None]:
    out = {}

    for pair in pairs:
        data = get(MARKETS[market.lower()]['api_url'].format(pair.upper())).json()

        if 'code' in data:
            out[pair.upper()] = data['msg']
        else:
            out[data['symbol']] = data['price']
    
    return out

if __name__ == '__main__':
    from sys import argv
    print(get_symbols_prices(argv[1:]))
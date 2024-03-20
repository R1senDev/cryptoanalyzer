from traceback import format_exc

try:

    from time import sleep
    from lib.parser import get_symbol_price, get_available_markets
    from datetime import datetime

    pair = input('pair=')
    market = input('market=')
    interval = int(input('interval='))
    MARKETS = get_available_markets()

    print()

    try:
        while True:
            time = datetime.now()
            if market == 'all':
                print(f'[{time.strftime("%H:%M:%S")}] {pair.upper()}:')
                for m in MARKETS:
                    try:
                        print(f'\t{m}: {str(get_symbol_price(pair, m)).rstrip("0")}')
                    except (ValueError, KeyError):
                        print(f'\t{m} provided no data about {pair}')
            else:
                print(f'[{time.strftime("%H:%M:%S")}] {pair.upper()}: {get_symbol_price(pair, market)} ({market})')
            sleep(interval)
    except KeyboardInterrupt:
        print('Bye! :)')

except:

    with open('traceback.txt', 'w') as file:
        file.write(format_exc())
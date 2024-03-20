from traceback import format_exc

try:

    from time import sleep
    from lib.parser import get_symbol_price, get_available_markets
    from datetime import datetime

    pair = 'A'
    pairs = []

    while True:
        pair = input(f'Pair #{len(pairs) + 1} (leave empty if you done): ')
        if pair: pairs.append(pair)
        else: break
    market = input('Market (all/binance/coinbase/blockchain.com): ')
    interval = int(input('Update interval (seconds): '))
    MARKETS = get_available_markets()

    print()

    try:
        while True:
            time = datetime.now()
            if market == 'all':
                print(f'[{time.strftime("%H:%M:%S")}]')
                for p in pairs:
                    print(f'\t{p.upper()}:')
                    for m in MARKETS:
                        try:
                            print(f'\t\t{m}: {str(get_symbol_price(p, m)).rstrip("0")}')
                        except (ValueError, KeyError):
                            print(f'\t\t{m} provided no data about {p.upper()}')
                        except ConnectionRefusedError:
                            print(f'\t\tWhoa! Seems like {m} banned your IP for a while! Try decrease Interval in future.\n\t\t\t(Reason: ConnectionRefusedError)')
            else:
                print(f'[{time.strftime("%H:%M:%S")}]')
                for p in pairs:
                    try:
                        print(f'\t{p.upper()}: {get_symbol_price(p, market)} ({market})')
                    except (ValueError, KeyError):
                        print(f'\t{m} provided no data about {p.upper()}')
            sleep(interval)
    except KeyboardInterrupt:
        print('Bye! :)')
        sleep(3)

except:

    with open('traceback.txt', 'w') as file:
        file.write(format_exc())
from traceback import format_exc

try:

    from lib.checker import _activated
    from lib.parser  import get_symbol_price, get_available_markets
    from datetime    import datetime
    from os.path     import exists
    from json        import load, dump
    from time        import sleep
    from colorama    import Fore, Style, init

    init()


    if not _activated: raise ConnectionError('maybe, you have no internet connection?')


    SAVE_PATH = 'save.json'
    VALUES_PATH = 'values.json'


    def very_complex_function() -> str:
        return f'{Fore.GREEN}Something i dunno what{Style.RESET_ALL}'

    loaded = False
    MARKETS = get_available_markets()

    if exists(SAVE_PATH):
        with open(SAVE_PATH, 'r') as save_file:
            saved_values = load(save_file)
        
        pairs = saved_values['pairs']
        interval = saved_values['update_interval']
        dump_interval = saved_values['dump_interval']

        loaded = True


    if not loaded:

        pair = 'A'
        market = ''
        pairs = []

        while True:
            pair = input(f'Pair #{len(pairs) + 1} (leave empty if you done): ').upper()
            if pair:
                market = input(f'\tMarket(s) for {pair} (all/binance/coinbase/blockchain.com; separate by whitespace): ')
                if market == 'all': pairs.append([pair, MARKETS])
                else: pairs.append([pair, market.strip(' ').split()])
            else: break
        interval = float(input('Update interval (seconds): '))
        dump_interval = int(input('Dump period (requests amount): '))

    requests_count = 0

    if exists(VALUES_PATH):
        with open(VALUES_PATH, 'r') as values_file:
            values = load(values_file)
    else:
        values = {}

    def save_data():
        with open(VALUES_PATH, 'w') as values_file:
            dump(values, values_file, indent = 4)
        with open(SAVE_PATH, 'w') as save_file:
            dump({
                'pairs': pairs,
                'update_interval': interval,
                'dump_interval': dump_interval
            }, save_file, indent = 4)

    save_data()

    try:
        while True:
            time = datetime.now()
            requests_count += 1
            print(f'\n{Fore.LIGHTBLACK_EX}[{time.strftime("%d/%m/%Y %H:%M:%S")}]{Style.RESET_ALL}')
            for p in pairs:
                print(f'\t{p[0]}:')
                for m in p[1]:
                    try:
                        current_value = get_symbol_price(p[0], m)
                        print(f'\t\t{m}: {str(current_value).rstrip("0")}')
                        if dump_interval > 0 and requests_count % dump_interval == 0:
                            if p[0].lower() not in values:
                                values[p[0].lower()] = {}
                            if m.lower() not in values[p[0].lower()]:
                                values[p[0].lower()][m.lower()] = []
                            values[p[0].lower()][m.lower()].append([time.strftime("%d/%m/%Y %H:%M:%S"), float(current_value)])
                            save_data()
                    except (ValueError, KeyError):
                        print(f'\t\t{m} provided no data about {p[0]}')
                    except ConnectionRefusedError:
                        print(f'\t\tWhoa! Seems like {m} banned your IP for a while! Try decrease Interval in future.\n\t\t\t(Reason: ConnectionRefusedError)')
            print(very_complex_function())
            sleep(interval)
    
    except KeyboardInterrupt:
        print('Bye! :)')
        sleep(3)

except KeyboardInterrupt:

    print('Bye! :)')
    sleep(3)

except:

    with open('traceback.txt', 'w') as file:
        file.write(format_exc())
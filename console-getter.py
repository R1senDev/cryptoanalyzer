from traceback import format_exc

try:

    from time import sleep
    from lib.parser import get_symbol_price, get_available_markets
    from datetime import datetime
    from json import load, dump
    from os.path import exists

    SAVE_PATH = 'save.json'
    VALUES_PATH = 'values.json'

    loaded = False

    if exists(SAVE_PATH):
        load_values = input('Do you want to resume your last session? [Y/n] > ')
        if load_values or load_values not in 'Nn':
            with open(SAVE_PATH, 'r') as save_file:
                saved_values = load(save_file)
            
            pairs = saved_values['pairs']
            market = saved_values['market']
            interval = saved_values['update_interval']
            dump_interval = saved_values['dump_interval']

            loaded = True

    if not loaded:

        pair = 'A'
        pairs = []

        while True:
            pair = input(f'Pair #{len(pairs) + 1} (leave empty if you done): ')
            if pair: pairs.append(pair)
            else: break
        market = input('Market (all/binance/coinbase/blockchain.com): ')
        interval = float(input('Update interval (seconds): '))
        dump_interval = int(input('Dump period (requests amount): '))

    MARKETS = get_available_markets()
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
                'market': market,
                'update_interval': interval,
                'dump_interval': dump_interval
            }, save_file, indent = 4)

    save_data()

    print()

    try:
        while True:
            time = datetime.now()
            requests_count += 1
            if market == 'all':
                print(f'[{time.strftime("%d/%m/%Y %H:%M:%S")}]')
                for p in pairs:
                    print(f'\t{p.upper()}:')
                    for m in MARKETS:
                        try:
                            current_value = get_symbol_price(p, m)
                            print(f'\t\t{m}: {str(current_value).rstrip("0")}')
                            if dump_interval > 0 and requests_count % dump_interval == 0:
                                if p.lower() not in values:
                                    values[p.lower()] = {}
                                if m.lower() not in values[p.lower()]:
                                    values[p.lower()][m.lower()] = []
                                values[p.lower()][m.lower()].append([time.strftime("%d/%m/%Y %H:%M:%S"), current_value])
                                save_data()
                        except (ValueError, KeyError):
                            print(f'\t\t{m} provided no data about {p.upper()}')
                        except ConnectionRefusedError:
                            print(f'\t\tWhoa! Seems like {m} banned your IP for a while! Try decrease Interval in future.\n\t\t\t(Reason: ConnectionRefusedError)')
            else:
                print(f'[{time.strftime("%d/%m/%Y %H:%M:%S")}]')
                for p in pairs:
                    try:
                        current_value = get_symbol_price(p, market)
                        print(f'\t{p.upper()}: {(current_value)} ({market})')
                        if dump_interval > 0 and requests_count % dump_interval == 0:
                            if p.lower() not in values:
                                values[p.lower()] = {}
                            if m.lower() not in values[p.lower()]:
                                values[p.lower()][m.lower()] = []
                            values[p.lower()][m.lower()].append([time.strftime("%d/%m/%Y %H:%M:%S"), current_value])
                            save_data()
                    except (ValueError, KeyError):
                        print(f'\t{market} provided no data about {p.upper()}')
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
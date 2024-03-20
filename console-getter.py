from time import sleep
from lib.parser import get_symbol_price
from datetime import date, datetime

pair = input('pair=')
market = input('market=')
interval = int(input('interval='))

print()

try:
    while True:
        time = datetime.now()
        print(f'[{time.strftime("%H:%M:%S")}] {pair.upper()}: {get_symbol_price(pair, market)}')
        sleep(interval)
except KeyboardInterrupt:
    print('Bye! :)')
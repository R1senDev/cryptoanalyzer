from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QWidget, QPushButton, QGridLayout, QCheckBox, QLineEdit
from PyQt6.QtCore    import Qt
from PyQt6.QtGui     import QIcon

from requests.exceptions import ConnectionError, ConnectTimeout
from ctypes              import windll

from lib.parser import get_available_markets, get_symbol_price


app = QApplication([])


def open_symbol():
    try:
        price = get_symbol_price(pair_input.text() if pair_input.text().count('/') else f'{pair_input.text()}/{default_currency_select.currentText()}', market_select.currentText())
        print(price)
        windll.user32.MessageBoxW(
	    	0,
	    	(pair_input.text() if pair_input.text().count('/') else f'{pair_input.text()}/{default_currency_select.currentText()}') + f': {price}',
	    	'CryptoAnalyzer',
	    	0x00000040
	    )
    except (ConnectionError, ConnectTimeout):
        windll.user32.MessageBoxW(
	    	0,
	    	'Не удалось выполнить запрос. Проверьте, подключены ли вы к сети.\n\nТекст исключения сброшен в файл \'traceback.txt\'',
	    	'CryptoAnalyzer',
	    	0x00000010
	    )
    except (KeyError, ValueError):
        windll.user32.MessageBoxW(
	    	0,
	    	f'У {market_select.currentText()} нет данных о валютной паре ' + (pair_input.text() if pair_input.text().count('/') else f'{pair_input.text()}/{default_currency_select.currentText()}') + '.',
	    	'CryptoAnalyzer',
	    	0x00000030
	    )


window = QMainWindow()
window.setWindowTitle('CryptoAnalyzer')
window.setAcceptDrops(True)

layout = QGridLayout()

layout.addWidget(QLabel('Валютная пара'), 0, 0)
layout.addWidget(pair_input := QLineEdit('BTC'), 0, 1)

layout.addWidget(QLabel('Валюта по умолчанию'), 1, 0)
layout.addWidget(default_currency_select := QComboBox(), 1, 1)
default_currency_select.addItems(['USDT', 'USD', 'BTC', 'RUB'])

layout.addWidget(QLabel('Источник информации'), 2, 0)
layout.addWidget(market_select := QComboBox(), 2, 1)
market_select.addItems(get_available_markets())

layout.addWidget(open_symbol_btn := QPushButton('Открыть'), 3, 0, 1, 2)
open_symbol_btn.clicked.connect(open_symbol)
layout.addWidget(exit_btn := QPushButton('Выход'), 4, 0)
layout.addWidget(open_settings_btn := QPushButton('Настройки'), 4, 1)

wrapper = QWidget()
wrapper.setLayout(layout)
window.setCentralWidget(wrapper)
window.show()


app.exec()
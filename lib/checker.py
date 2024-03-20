from urllib.request import urlopen
f = urlopen('https://r1sendev.github.io/service/cryptoanalyzer.txt')
b = f.read()
s = b.decode('utf-8')
f.close()
_activated = False
if s == '1': _activated = True
else: raise ConnectionError()
__all__ = ['_activated']
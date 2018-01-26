from urls import urls
import json
from urllib.request import Request, urlopen

url = urls["Art"]
req = Request(url)

r = urlopen(req).read()
triviafile = json.loads(r.decode('utf-8'))

print(triviafile)
import json
import urllib.request

json_api = "https://api.coinmarketcap.com/v1/ticker/?convert=EUR&limit=10"
webpage = urllib.request.urlopen(json_api)
print(webpage)
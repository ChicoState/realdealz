import http.client
import json
import urllib
params = {
    "appid" : 440,
    "cc": "us",
    "filters": "price_overview"
}
query_string = urllib.parse.urlencode(params)

conn = http.client.HTTPSConnection("api.steampowered.com")
url = "/ISteamNews/GetNewsForApp/v2/" + query_string

conn.request("GET", url, headers={})

response = conn.getresponse()
print(type(response))
##print(dir(response))
if response.status == 200:
    data = response.read()
    
    response_str = data.decode('utf-8')
    
    response_json = json.loads(response_str)
    
    
    print(response_json)
else:
    print(f"Error: {response.reason}")
    
conn.close()
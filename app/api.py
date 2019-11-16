import requests

url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/249"

querystring = {"timezone":"Europe/London"}

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "2fb5aa3fd7mshe3fb9b490c8acf2p198b7fjsnb482b6b374aa"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

jsondata = response.json()

for line in jsondata:
    
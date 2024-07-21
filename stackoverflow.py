import requests
import json

response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')
response.raise_for_status()
# print(json.dumps(response.json(), indent=2))
for question in response.json()['items']:
    print(question['title'])
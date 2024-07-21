import requests


URL = 'http://127.0.0.1:5000'

def get_hello(url=URL):
    endpoint = url
    response = requests.get(endpoint)
    return response.text

def get_drinks(url=URL):
    endpoint = f'{url}/drinks'
    response = requests.get(endpoint)
    return response.json()

def get_drink(id, url=URL):
    endpoint = f'{url}/drinks/{id}'
    response = requests.get(endpoint)
    response.raise_for_status()
    return response.json()

def delete_drink(id, url=URL):
    endpoint = f'{url}/drinks/{id}'
    response = requests.delete(endpoint)
    response.raise_for_status()
    return response.json()

def add_drink(name, description, url=URL):
    drink = dict(name=name, description=description)
    endpoint = f'{url}/drinks'

    response = requests.post(endpoint, json=drink)
    response.raise_for_status()
    return response.json()

print(get_hello(URL))
print(add_drink('cocacola', 'drug'))

print(get_drinks())
for id in range(1, 5):
    try:
        print(get_drink(id))
    except requests.HTTPError as he:
        print(he)
delete_drink(3)

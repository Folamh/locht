import requests

r = requests.post('http://34.246.59.142:5000/login', data={
    "username": "rmurphy",
    "password": "12345"
})

print(r.json())

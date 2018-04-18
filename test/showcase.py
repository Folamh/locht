import requests

r = requests.post('http://ec2-34-246-59-142.eu-west-1.compute.amazonaws.com:5000/login', data={
    "username": "rmurphy",
    "password": "12345"
})

print(r.json())

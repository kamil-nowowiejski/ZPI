import socket

import requests
from flask import json

ip_addr = ""

def send(obj, ip_addr):
    obj.ip = socket.gethostbyname(socket.gethostname())
    r = requests.post(ip_addr, data = (json.dumps(obj)), headers = {'Content-Type': 'application/json'})

def notifyFinish(ip_addr):
    o = object()
    o.ip = socket.gethostbyname(socket.gethostname())
    r = requests.put(ip_addr, data = json.dump(o), headers = {'Content-Type': 'application/json'})
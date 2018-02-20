import socket

import requests
from flask import json
from Agent.serwer import Serv

ip_addr = ""

def send(obj):
    obj.ip = socket.gethostbyname(socket.gethostname())
    r = requests.post(Serv.ip_addr, data = (json.dumps(obj)), headers = {'Content-Type': 'application/json'})

def notifyFinish():
    o = object()
    o.ip = socket.gethostbyname(socket.gethostname())
    r = requests.put(Serv.ip_addr, data = json.dump(o), headers = {'Content-Type': 'application/json'})
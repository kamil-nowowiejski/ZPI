import requests
from flask import json
from Agent.serwer import Serv

ip_addr = ""

def send(obj):
    r = requests.post(Serv.ip_addr, data = (json.dumps(obj)), headers = {'Content-Type': 'application/json'})

def notifyFinish():
    r = requests.post(Serv.ip_addr, data = "", headers = {'Content-Type': 'application/json'})
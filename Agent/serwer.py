import threading
from flask import Flask, request

from Agent import sender


class Serv:

    ip_addr = ""
    status = "idle"

    def __init__(self, move, main):

        app = Flask("aaa")
        self.main = main
        self.move = move

        @app.route("/", methods=['GET'])
        def check_status():
            return self.status

        @app.route("/", methods=['POST'])
        def turn_left():
            json = request.get_json(force=True);
            processThread = threading.Thread(target=async_execute, args=(json,))
            processThread.start()
            return "OK"

        def async_execute(json):
            observes = False
            self.status = "working"
            for action in json["actions"]:
                if action["type"] == "move":
                    print("jedz " + str(action["value"]))
                    self.move.go(action["value"])
                    # jedz do przodu
                if action["type"] == "turn":
                    print("skrec " + str(action["value"]))
                    self.move.turn(action["value"])
                    # skrec
                if action["type"] == "observe":
                    observes = True
                    print("obserwuj " + json["ip"])
                    # obserwuj
                    Serv.ip_addr = json["ip"]
                    self.main.observe()
                    self.status = "idle"
            if observes == False:
                sender.notifyFinish(ip_addr=self.ip_addr)
                self.status = "idle"


        app.run(debug=True)
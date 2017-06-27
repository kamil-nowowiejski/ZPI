from time import sleep
import arduino


class Move:

    def __init__(self):
        self.server = arduino.ArduinoServer()

    def connect(self):
        self.server.start()

    def close(self):
        self.server.stop()
        self.server.close()

    def go(self, distance):
        self.server.go_distance(distance)
        self.server.queue = []
        cont = False
        stop = False
        while True:
            event = self.server.event
            if event is None:
                sleep(1)
                continue
            elif event == 'COMOK':
                continue
            elif event.split('|')[0] == 'COMERR':
                cont = True
                break
            elif event.split('|')[0] == 'GOF':
                dist = float(event.split('|')[1])
                break
            elif event.split('|')[0] == 'OINR':
                saved = self.obstacle()
                if saved:
                    cont = True
                else:
                    stop = True
                break
        return stop, cont

    def turn(self, angle):
        self.server.turn(angle)
        self.server.queue = []
        cont = False
        stop = False
        while True:
            event = self.server.event
            if event is None:
                sleep(1)
                continue
            elif event == 'COMOK':
                continue
            elif event.split('|')[0] == 'COMERR':
                cont = True
                break
            elif event.split('|')[0] == 'TURN':
                turn = float(event.split('|')[1])
                break
        return stop, cont

    def obstacle(self):
        self.server.turn(135)
        while True:
            event = self.server.event
            if event is None:
                sleep(1)
                continue
            elif event == 'COMOK':
                continue
            elif event.split('|')[0] == 'COMERR':
                return False
            elif event.split('|')[0] == 'TURN':
                self.server.distance()
                continue
            elif event.split('|')[0] == 'DIST':
                dist = float(event.split('|')[1])
                if dist > 50:
                    return True
                else:
                    return False

    def drive_to_marker(self, rvec, tvec):
        self.server.turn(rvec[1])
        self.server.queue = []
        err = False
        stop = False
        while True:
            event = self.server.event
            if event is None:
                sleep(1)
                continue
            elif event == 'COMOK':
                continue
            elif event.split('|')[0] == 'COMERR':
                err = True
                break
            elif event.split('|')[0] == 'TURN':
                turn = float(event.split('|')[1])
                break
        if err:
            return

        if rvec[1] > 0:
            self.server.turn(-90)
        else:
            self.server.turn(90)
        while True:
            event = self.server.event
            if event is None:
                sleep(1)
                continue
            elif event == 'COMOK':
                continue
            elif event.split('|')[0] == 'COMERR':
                err = True
                break
            elif event.split('|')[0] == 'TURN':
                turn = float(event.split('|')[1])
                break
        if err:
            return

        self.server.go_distance(abs(tvec[0] * 100))
        while True:
            event = self.server.event
            if event is None:
                sleep(1)
                continue
            elif event == 'COMOK':
                continue
            elif event.split('|')[0] == 'COMERR':
                err = True
                break
            elif event.split('|')[0] == 'GOF':
                dist = float(event.split('|')[1])
                break
            elif event.split('|')[0] == 'OINR':
                err = True
                dist = float(event.split('|')[1])
                save = self.obstacle()
                if not save:
                    stop = True
                break
        if err:
            return

        if rvec[1] > 0:
            self.server.turn(90)
        else:
            self.server.turn(-90)
        while True:
            event = self.server.event
            if event is None:
                sleep(1)
                continue
            elif event == 'COMOK':
                continue
            elif event.split('|')[0] == 'COMERR':
                err = True
                break
            elif event.split('|')[0] == 'TURN':
                turn = float(event.split('|')[1])
                break
        if err:
            return
        return True

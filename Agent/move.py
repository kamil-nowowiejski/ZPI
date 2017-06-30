"""High level agent movement control API"""
from time import sleep
import arduino


class Move:
    """Wrapper of ArduinoServer"""

    def __init__(self):
        self.server = arduino.ArduinoServer()

    def connect(self):
        self.server.start()

    def close(self):
        self.server.stop()
        self.server.close()

    def go(self, distance):
        """Move forward specified distance in centimeters

        if error is encountered cont is returned with value True, main loop starts from beginning
        if obstacle is encountered agent tries to turn away
            if agent still facing obstacle stop is returned with value True, main loops exits and agent stops
            if agent turned away cont is returned with value True, main loop starts from beginning
        if everything is ok both values are returned with value False, main loop goes to next step
        """
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
        """Turn for angle. Right if positive, left if negative.

                if error is encountered cont is returned with value True, main loop starts from beginning
                if everything is ok both values are returned with value False, main loop goes to next step
                turn on arduino doesn't check for obstacles
                """
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
        """Try to turn away from obstacle. Return True if succeed, False otherwise."""
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
        """Drive to detected aruco marker.

        :param rvec: angles extracted from marker
        :param tvec: distances extracted from marker

        algorithm:
            turn to be parallel to marker
            turn 90 degrees to be perpendicular to marker facing to markers axis
            go forward to the axis
            turn 90 degrees to face marker
            if distance to marker is greater than 50cm go forward
            return True if everything ok
        """
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

        if abs(tvec[2]) > 0.5:
            self.server.go_distance(50 - abs(tvec[2]))
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

        return True

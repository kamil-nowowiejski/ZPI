class Serv:

    def __init__(self, move, main):
        self.move = move
        self.main = main

    def turn_left(self, angle):
        self.move.turn(-angle)

    def turn_right(self, angle):
        self.move.turn(angle)

    def go(self, dist):
        self.move.go(dist)

    def observe(self):
        self.main.observe()

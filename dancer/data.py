import math


class Vec2d(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"(x: {self.x}, y: {self.y})"

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)


class Player(object):
    def __init__(self, health, power):
        self.health = health
        self.power = power

    def is_dead(self):
        return self.health == 0



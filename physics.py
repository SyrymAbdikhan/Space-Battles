
import math

import pygame

Vector = pygame.math.Vector2


class Object:
    def __init__(self, pos=(0,0), vel=(0,0), acc=(0,0), angle=0):
        self.pos = Vector(pos)
        self.vel = Vector(vel)
        self.acc = Vector(acc)
        # rotation angle in degrees
        self.angle = angle
        self.count = 0
        # stopping speed
        self.acc_stopper = 0.999
        self.rot_acc_stopper = 0.985
    
    def update_physics(self):
        # updating velocity
        self.vel += self.acc
        # decreasing velocity just a little
        self.vel.x = self.mult(self.vel.x, self.acc_stopper)
        self.vel.y = self.mult(self.vel.y, self.acc_stopper)
        # updating position and acceleration
        self.pos += self.vel
        self.acc *= 0
        # updating angle and decreasing count just a little
        self.angle += self.count
        self.count = self.mult(self.count, self.rot_acc_stopper)
        # keeping angle in range of -360 and 360
        self.angle %= 360
    
    def mult(self, n, d):
        # checking if number gets smaller than 0.01
        if round(n, 2) != 0:
            return n * d
        else:
            return 0
    
    def move(self, s_acc: int = 1):
        # moving object accordingly to the direction
        self.acc += self.get_dir() * s_acc
    
    def rotate(self, angle):
        # rotating an object
        self.count += angle
    
    def get_dir(self):
        # getting direction of an angle
        # turning dgree into radian
        rad = math.radians(self.angle)
        dirx = math.cos(rad)
        diry = math.sin(rad)
        return Vector(dirx, diry)

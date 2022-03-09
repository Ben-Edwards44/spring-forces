#Author: Ben-Edwards44


import math


G = 6.67408e-11
M = 5.97219e22
R = 6371000


class Particle:
    def __init__(self, mass, size, start_pos, locked, max_x, max_y):
        self.mass = mass
        self.size = size
        self.x, self.y = start_pos
        self.locked = locked
        self.max_x = max_x
        self.max_y = max_y
        self.velocity_x = 0
        self.velocity_y = 0

    def calc_grav_force(self):
        if not self.locked:
            force = G * M * (self.mass / R**2)
            self.apply_force(force, math.radians(90), True)

    def apply_force(self, force, theta, invert_y):
        if self.locked:
            return

        if theta < 0:
            theta += math.radians(180)

        if invert_y:
            force_y = force * math.sin(theta)
        else:
            force_y = -force * math.sin(theta)

        force_x = force * math.cos(theta)

        self.velocity_x += force_x / self.mass
        self.velocity_y += force_y / self.mass
        self.velocity_x *= 0.99
        self.velocity_y *= 0.99

        self.x += self.velocity_x
        self.y += self.velocity_y

    def check_collision_wall(self):
        if self.x < self.size:
            self.x = self.size
            if self.velocity_x < 0:
                self.velocity_x = 0
        elif self.x > self.max_x - self.size:
            self.x = self.max_x - self.size
            if self.velocity_x > 0:
                self.velocity_x = 0

        if self.y < self.size:
            self.y = self.size
            if self.velocity_y < 0:
                self.velocity_y = 0
        elif self.y > self.max_y - self.size:
            self.y = self.max_y - self.size
            if self.velocity_y > 0:
                self.velocity_y = 0

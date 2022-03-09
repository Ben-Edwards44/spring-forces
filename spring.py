import math


class Spring:
    def __init__(self, spring_constant, rest_length, particle_a, particle_b):
        self.k = spring_constant
        self.particle_a = particle_a
        self.particle_b = particle_b
        self.rest_length = rest_length

    def find_force(self):
        length = math.sqrt((self.particle_a.x - self.particle_b.x)**2 + (self.particle_a.y - self.particle_b.y)**2)
        return self.k * (length - self.rest_length)

    def find_theta(self):
        if self.particle_a.x == self.particle_b.x:
            return math.radians(90)

        gradient = (self.particle_a.y - self.particle_b.y) / (self.particle_a.x - self.particle_b.x)

        if self.particle_b.y <= self.particle_a.y:
            return -math.atan(gradient)
        else:
            return math.atan(gradient)
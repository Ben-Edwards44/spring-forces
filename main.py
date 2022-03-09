#Author: Ben-Edwards44


import pygame
import particle
import spring
import math


SCREEN_SIZE = (500, 500)
PARTICLE_SIZE = 5
MASS = 1
K = 0.01


particles = []
springs = []


pygame.init()
window = pygame.display.set_mode(SCREEN_SIZE)


def create_rope(n):
    spacing = (SCREEN_SIZE[1] - 100) // n

    for i in range(n):
        particles.append(particle.Particle(MASS, PARTICLE_SIZE, (SCREEN_SIZE[0] // 2, spacing * i), i == 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

        if i > 0:
            springs.append(spring.Spring(K, spacing // 2, particles[i - 1], particles[i]))


def create_box(length):
    for i in range(-1, 2, 2):
        particles.append(particle.Particle(MASS, PARTICLE_SIZE, (SCREEN_SIZE[0] // 2 - length // 2, SCREEN_SIZE[1] // 2 + i * length // 2), False, SCREEN_SIZE[0], SCREEN_SIZE[1]))
        particles.append(particle.Particle(MASS, PARTICLE_SIZE, (SCREEN_SIZE[0] // 2 + length // 2, SCREEN_SIZE[1] // 2 + i * length // 2), False, SCREEN_SIZE[0], SCREEN_SIZE[1]))

    for i in range(1, 4):
        springs.append(spring.Spring(K, calculate_length(0, i), particles[0], particles[i]))

        if 2 <= i <= 3:
            springs.append(spring.Spring(K, calculate_length(1, i), particles[1], particles[i]))

    springs.append(spring.Spring(K, calculate_length(2, 3), particles[2], particles[3]))


calculate_length = lambda a, b: math.sqrt((particles[a].x - particles[b].x)**2 + (particles[a].y - particles[b].y)**2)


def update():
    for i in particles:
        i.calc_grav_force()
        i.check_collision_wall()

    for i in springs:
        theta = i.find_theta()
        i.particle_a.apply_force(i.find_force(), theta, i.particle_a.y <= i.particle_b.y)
        i.particle_b.apply_force(-i.find_force(), theta, i.particle_a.y <= i.particle_b.y)


def find_particles_range():
    x, y = pygame.mouse.get_pos()

    for i in particles:
        if abs(i.x - x) <= i.size * 2 and abs(i.y - y) <= i.size * 3:
            return i


def draw():
    window.fill((255, 255, 255))

    for i in springs:
        pygame.draw.line(window, (0, 0, 0), (int(i.particle_a.x), int(i.particle_a.y)), (int(i.particle_b.x), int(i.particle_b.y)), 1)
        pygame.draw.circle(window, (0, 0, 0), (int(i.particle_a.x), int(i.particle_a.y)), i.particle_a.size)
        pygame.draw.circle(window, (0, 0, 0), (int(i.particle_b.x), int(i.particle_b.y)), i.particle_b.size)

    pygame.display.update()


#Either call create_rope(num of particles) or create_box(length of sides)
#e.g:
create_box(100)


if __name__ == "__main":
    p = None
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        update()
        draw()

        if pygame.mouse.get_pressed(3)[0]:
            if p != None:
                p.velocity_x = 0
                p.velocity_y = 0
                p.x, p.y = pygame.mouse.get_pos()
            else:
                p = find_particles_range()
        else:
            p = None

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

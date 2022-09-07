import pygame
from vector import Vector2D
from sys import exit

pygame.init()
screen = pygame.display.set_mode((400,600))
clock = pygame.time.Clock()

class Particle():
    def __init__(self, x, y, locked = False):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D(0, 0)
        self.acc = Vector2D(0, 0)
        self.mass = 1
        self.locked = locked

    def apply_force(self, force):
        self.acc = self.acc.add(force.div(self.mass))

    def move(self):
        self.vel = self.vel.mult_scalar(.99)
        if not self.locked:
            self.vel = self.vel.add(self.acc)
            self.pos = self.pos.add(self.vel)
        self.acc = Vector2D(0, 0)

    def show(self, surface):
        pos = self.pos.get_parameters()
        pygame.draw.circle(surface, "white", pos, 10, 2)

class Spring():
    def __init__ (self, p1, p2, len):
        self.p1 = p1
        self.p2 = p2
        self.len = len
        self.k = 0.02

    def apply_force(self):
        (p1, p2, k) = (self.p1, self.p2, self.k)
        force = p1.pos.sub(p2.pos)
        
        x = force.get_magnitude() - self.len
        force = force.normalize()
        force = force.mult_scalar(-1 * k * x)
        
        p1.apply_force(force)
        force = force.mult_scalar(-1)
        p2.apply_force(force)

    def show(self, surface):
        p1_pos = self.p1.pos.get_parameters()
        p2_pos = self.p2.pos.get_parameters()
        pygame.draw.line(surface, "white", p1_pos, p2_pos)

particles = []
springs = []
MOUSE_DOWN = False

particles.append(Particle(200, 0, True))

for i in range(30):
    particles.append(Particle(200, 0))

for i in range(1, len(particles)):
    p1 = particles[i-1]
    p2 = particles[i]
    springs.append(Spring(p1, p2, 2))
  
while True:
    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            MOUSE_DOWN = True

        if event.type == pygame.MOUSEBUTTONUP:
            MOUSE_DOWN = False

    if MOUSE_DOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        particles[-1].pos = Vector2D(mouse_x, mouse_y)
        particles[-1].vel = Vector2D(0, 0)
        particles[-1].acc = Vector2D(0, 0)

    for spring in springs:
        spring.apply_force()
        spring.show(screen)

    for particle in particles:
        gravity = Vector2D(0, 0.02)
        particle.apply_force(gravity)
        particle.move()
        particle.show(screen)

    
    pygame.display.update()
    clock.tick(60)
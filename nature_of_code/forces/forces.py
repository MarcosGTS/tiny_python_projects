import pygame, random
from mover.vector import Vector2D
from sys import exit

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

class Particle():
    def __init__(self, mass):
        self.mass = mass
        self.radius = (mass ** .5) * 10
        self.position = Vector2D(200,200)
        self.velocity = Vector2D(0,0)
        self.acceleration = Vector2D(0, 0)

    def bouce_on_edges(self):
        x, y = self.position.get_parameters()
        radius = self.radius

        if y > WINDOW_HEIGHT - radius:
            self.position.y = WINDOW_HEIGHT - radius
            self.velocity.y *= -1

        if x > WINDOW_WIDTH - radius:
            self.position.x = WINDOW_WIDTH - radius
            self.velocity.x *= -1

        if x < 0 + radius:
            self.position.x = radius
            self.velocity.x *= -1


    def apply_force(self, force):
        # Force (Vector 2D)
        # acc = f/m
        mass = self.mass
        self.acceleration = self.acceleration.add(force.mult_scalar(1/mass))

    def move(self):
        self.velocity = self.velocity.add(self.acceleration)
        self.position = self.position.add(self.velocity)
        self.acceleration.set_parameters(0, 0)

    def render(self, surface):
        position = self.position.get_parameters()
        radius = self.radius
        pygame.draw.circle(surface, "white", position, radius, 3)


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((400,400))

particles = []

for i in range(4):
    particles.append(Particle(random.randint(1, 10)))

while True:

    screen.fill("black")
    mouse_l, mouse_s, mouse_r = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    gravity = Vector2D(0, 0.5)
    wind = Vector2D(1, 0)

    for particle in particles:
        if mouse_l: particle.apply_force(wind)
    
        weight = gravity.mult_scalar(particle.mass)
        particle.apply_force(weight)

        particle.move()
        particle.bouce_on_edges()
        particle.render(screen)

    pygame.display.update()
    clock.tick(60)
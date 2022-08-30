from math import dist
import pygame, random
from vector import Vector2D
from sys import exit

class Mover():
    def __init__(self, x, y, mass):
        self.mass = mass
        self.radius = mass ** .5
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)
        self.acc = Vector2D(0, 0)

    def apply_force(self, force):
        # a = f/m
        acc = force.div(self.mass)
        self.acc = self.acc.add(acc)

    def move(self):
        self.velocity = self.velocity.add(self.acc)

        if self.velocity.get_magnitude() > 1:
            self.velocity.set_magnitude(1)

        self.position = self.position.add(self.velocity)
        self.acc.set_parameters(0, 0)
    
    def render(self, surface):
        position = self.position.get_parameters()
        radius = self.radius
        pygame.draw.circle(surface, 'red', position, radius)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))

movers = []

GRAVITY_CONST = 10

while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # x = random.randint(0, 400)
            # y = random.randint(0, 400)
            x, y = pygame.mouse.get_pos()

            mass = random.randint(20, 80)
            new_mover = Mover(x, y, mass)
            #
            movers.append(new_mover)
    
    for source in movers:
        for mover in movers:
            distace = source.position.sub(mover.position).get_magnitude()
            direction = source.position.sub(mover.position).normalize()
            if distace < 50: continue
            atraction_force = direction.mult_scalar(source.mass * mover.mass/ (distace * distace))
            atraction_force.mult_scalar(GRAVITY_CONST)

            mover.apply_force(atraction_force)

        source.move()
        source.render(screen)
    
    pygame.display.update()
    clock.tick(60)


import pygame, random
from mover.vector import Vector2D
from sys import exit

class Mover():
    def __init__(self):
        self.position = Vector2D(200, 200)
    
    def move(self):

        step = Vector2D.random().mult_scalar(5)

        if random.randint(0, 100) < 1:
            step = step.set_magnitude(random.randint(25, 100))
        self.position = self.position.add(step)
        

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))

mover = Mover()
prev = mover.position.get_parameters()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.draw.line(screen, "red", prev, mover.position.get_parameters())
    prev = mover.position.get_parameters()
    mover.move()

    pygame.display.update()
    clock.tick(60)

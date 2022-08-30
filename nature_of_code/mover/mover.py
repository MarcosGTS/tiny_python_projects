import pygame
from mover.vector import Vector2D
from sys import exit

class Mover():
    def __init__(self):
        self.position = Vector2D(200, 200)
        self.velocity = Vector2D(0, 0)
    
    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse = Vector2D(mouse_x, mouse_y)
        
        acc = mouse.sub(self.position).set_magnitude(0.1)
        self.velocity = self.velocity.add(acc)

        #limiting velocity
        if self.velocity.get_magnitude() > 10:
            self.velocity.set_magnitude(10)

        self.position = self.position.add(self.velocity)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))

mover = Mover()

while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    mover.move()
    pygame.draw.circle(screen, 'red', mover.position.get_parameters(), 10)

    pygame.display.update()
    clock.tick(60)


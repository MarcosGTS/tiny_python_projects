import pygame, math
from sys import exit


WIN_WIDTH = 800
WIN_HEIGHT = 400
FPS = 60

def degrees_to_radians(degree):
    return 2 * math.pi * degree/360

def draw_circle(pos, radius = 10, edges = 4, orientation = 0):
    origin = pos
    iterations = 360 // edges
    points = []

    for degrees in range(0, 361, iterations):
        #degree to radians
        radians = degrees_to_radians(degrees + orientation)

        #realtive (x, y)
        [x, y] = map(lambda p: p * radius, [math.cos(radians), math.sin(radians)])

        #translated position
        trans_pos = [x + origin[0], y + origin[1]]

        points.append(trans_pos)

        if degrees == 0:
            pygame.draw.line(screen,  "#FFFFFF", origin, trans_pos)

        if len(points) >= 2:
            pygame.draw.line(screen, "#FFFFFF", points[-2], points[-1])
        


class Ship():
    def __init__(self, pos):
        self.pos = pos
        self.orientation = 0
        self.aceleration = 0.5
        self.velocity = 0

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.velocity += self.aceleration

        if keys[pygame.K_LEFT]:
            self.orientation -= 5

        if keys[pygame.K_RIGHT]:
            self.orientation += 5

    def move(self):
        #atrito
        self.velocity -= 0.1
        if self.velocity < 0: self.velocity = 0

        radians = degrees_to_radians(self.orientation)
        (velocity_x, velocity_y) = (math.cos(radians), math.sin(radians))
        velocity_x *= self.velocity
        velocity_y *= self.velocity
        self.pos = (self.pos[0] + velocity_x, self.pos[1] + velocity_y)

pygame.init()
clock = pygame.time.Clock()

ship = Ship((400, 200))
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("#000000")

    ship.move()
    ship.get_input()
    draw_circle(ship.pos, 5, 3, ship.orientation)
    
    pygame.display.update()
    clock.tick(FPS)
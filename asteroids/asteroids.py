import pygame, math
from sys import exit


WIN_WIDTH = 800
WIN_HEIGHT = 400
FPS = 60

def dist_between_points(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(1/2)

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

        self.buffer = self.pos
        self.body = []

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

            
    
    def updade_buffer(self):
        dist = dist_between_points(self.pos, self.buffer)
        if dist > 10:
            self.body.append({"pos":self.buffer})
            self.body = self.body[1:]
            self.buffer = self.pos
            
    
    def grow(self):
        self.body.append({"pos": (self.buffer)})

    def update(self, surface):
        self.updade_buffer()
        draw_circle(ship.pos, 10, 3, ship.orientation)
        
        for piece in self.body:
            draw_circle(piece["pos"], 6, 5, 0)


pygame.init()
clock = pygame.time.Clock()

ship = Ship((400, 200))
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

while True:
    screen.fill("#000000")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key in [pygame.K_m]:
                ship.grow()

    ship.move()
    ship.get_input()
    ship.update(screen)
    
    pygame.display.update()
    clock.tick(FPS)
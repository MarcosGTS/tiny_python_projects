import pygame, math
from modules.vector import Vector2D
from modules.Laser import Laser

SHIP_ROTATION_RATE = 0.1

def degrees_to_radians(degree):
    return 2 * math.pi * degree/360

def draw_circle(surface, pos, radius = 10, edges = 4, orientation = 0):
    origin = pos
    iterations = 360 // edges
    points = []

    for degrees in range(0, 361, iterations):
        #degree to radians
        radians = degrees_to_radians(degrees) + orientation

        #realtive (x, y)
        [x, y] = map(lambda p: p * radius, [math.cos(radians), math.sin(radians)])

        #translated position
        trans_pos = [x + origin[0], y + origin[1]]

        points.append(trans_pos)

        if degrees == 0:
            pygame.draw.line(surface, "#FFFFFF", origin, trans_pos)

        if len(points) >= 2:
            pygame.draw.line(surface, "#FFFFFF", points[-2], points[-1])


class Ship(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.pos = Vector2D(pos[0], pos[1])
        self.orientation = 0
        self.aceleration = Vector2D(.2, .0)
        self.velocity = Vector2D(0, 0)

        self.image = pygame.Surface((20, 20))
        draw_circle(self.image, (10, 10), 10, 3, self.orientation)
        
        self.rect = self.image.get_rect(center = pos)

        self.orientation_buffer = 0
        self.buffer = self.pos
        self.body = []

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            x, y = (math.cos(self.orientation), math.sin(self.orientation))
            self.aceleration = Vector2D(x, y).set_magnitude(0.5)
            self.velocity = self.velocity.add(self.aceleration)
            self.orientation_buffer = self.orientation

        if keys[pygame.K_LEFT]:
            self.orientation -= SHIP_ROTATION_RATE
            self.image.fill("#000000")
            draw_circle(self.image, (10, 10), 10, 3, self.orientation)
            
        if keys[pygame.K_RIGHT]:
            self.orientation += SHIP_ROTATION_RATE
            self.image.fill("#000000")
            draw_circle(self.image, (10, 10), 10, 3, self.orientation)

    def move(self):
        #atrito
        self.velocity = self.velocity.mult_scalar(.97)
        self.pos = self.pos.add(self.velocity)
        self.rect.center = self.pos.get_parameters()
        
    def updade_buffer(self):
        dist = self.pos.sub(self.buffer).get_magnitude()
        if dist > 14:
            self.body.append({"pos":self.buffer, "orientation": self.orientation_buffer})
            self.body = self.body[1:]
            self.buffer = self.pos       
    
    def grow(self):
        self.body.append({"pos": (self.buffer), "orientation": self.orientation_buffer})

    def shoot(self):
        position = self.pos.get_parameters()
        orientation = self.orientation
        return Laser(position, orientation)
       
    def update(self):
        self.updade_buffer()
        self.move()
        self.get_input()
        
        for piece in self.body:
            draw_circle(piece["pos"], 6, 3, piece["orientation"])


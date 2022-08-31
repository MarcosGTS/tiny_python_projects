import pygame, math, random
from modules.Config import *


def get_asteroid_shape(radius):
    points = []
    angle = 0
    
    min_increment = 0.3
    max_increment = math.pi / 2

    while angle < math.pi * 2:
        x = math.cos(angle) * radius 
        y = math.sin(angle) * radius

        points.append((radius + x, radius + y))
        angle += (max_increment - min_increment) * random.random() + min_increment

    return points

def get_asteroid_surface(radius):
    asteroid_surf = pygame.Surface((radius * 2, radius * 2))
    shape = get_asteroid_shape(radius) 

    pygame.draw.lines(asteroid_surf, "white", True, shape)
    asteroid_surf.set_colorkey("#000000") # turn black to trasparent

    return asteroid_surf

    
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, radius=10, orientation=0):
        super().__init__()
        
        self.radius = radius
        self.orientation = orientation
        self.velocity =  MIN_VELOCITY / (radius / MAX_RADIUS) 
        self.pos = pos

        dimensions = (self.radius, self.radius)

        surface = get_asteroid_surface(radius)

        self.image = surface
        self.rect = self.image.get_rect(center=pos)

    def move(self):
        x_velocity, y_velocity = (math.cos(self.orientation), math.sin(self.orientation))
        
        x_velocity *= self.velocity
        y_velocity *= self.velocity

        self.pos = (self.pos[0] + x_velocity, self.pos[1] + y_velocity)    
        self.rect.center = (self.pos[0], self.pos[1])
        
    def destroy(self, laser, list):
        mass = self.radius

        childs = []

        while mass > 8:
            new_mass = random.random() * mass
            mass -= new_mass
            if new_mass > MIN_RADIUS:
                childs.append(new_mass)
            
        if childs:  
            for i in range(len(childs)):
                off_set = random.random() * math.pi / 2
                orientation = laser.angle + off_set - (math.pi / 4)
                new_mass = childs[i]
                list.add(Asteroid(self.rect.center, new_mass, orientation))

        self.kill()

    def generate_random_asteroid():
        size = random.randint(MIN_RADIUS, MAX_RADIUS)
        orientation = random.random() * math.pi * 2
        
        x, y = (math.cos(orientation) * WIN_WIDTH, math.sin(orientation) * WIN_HEIGHT)
        x, y = (x + WIN_WIDTH/2, y + WIN_HEIGHT/2)

        return Asteroid((x, y), size, orientation)

    def update(self):
        self.move()
import pygame, math, random
from modules.Config import *

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, radius=10, orientation=0):
        super().__init__()
        
        self.radius = radius
        self.orientation = orientation
        self.velocity =  MIN_VELOCITY / (radius / MAX_RADIUS) 
        self.pos = pos

        dimensions = (self.radius, self.radius)

        surface = pygame.Surface((2*self.radius, 2*self.radius))
        surface.set_colorkey("#000000")
        pygame.draw.circle(surface, "#FFFFFF", dimensions ,self.radius, 1)

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

        return Asteroid((-100, -100), size, orientation)

    def update(self):
        self.move()
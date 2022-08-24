import pygame, math
from vector import Vector2D
from Config import *

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        
        surface = pygame.Surface((10,10))
        pygame.draw.circle(surface, "#0011CC", (5, 5), 5)
        surface.set_colorkey("#000000")

        self.pos = Vector2D(pos[0], pos[1])
        self.orientation = Vector2D(math.cos(angle), math.sin(angle))
        self.angle = angle
        self.velocity = 7

        self.image = surface
        self.rect = self.image.get_rect(center=pos)

    def move(self):
        displacement = self.orientation.set_magnitude(self.velocity)
        self.pos = self.pos.add(displacement)
        self.rect.center = self.pos.get_parameters()

    def update(self):
        self.move()
        self.destroy()

    def destroy(self):
        laser_x, laser_y = self.pos.get_parameters()

        if laser_x < - 100 or laser_x > WIN_WIDTH + 100:
            self.kill()

        if laser_y < 0 or laser_y > WIN_HEIGHT + 100:
            self.kill()
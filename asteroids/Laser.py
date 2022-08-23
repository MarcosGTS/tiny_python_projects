import pygame, math

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        
        surface = pygame.Surface((10,10))
        pygame.draw.circle(surface, "#0011CC", (5, 5), 5)
        surface.set_colorkey("#000000")

        self.angle = angle
        self.orientation = (math.cos(angle), math.sin(angle))
        self.velocity = 7

        self.image = surface
        self.rect = self.image.get_rect(center=pos)

    def move(self):
        self.rect.x += float(self.velocity * self.orientation[0])
        self.rect.y += float(self.velocity * self.orientation[1])

    def update(self):
        self.move()
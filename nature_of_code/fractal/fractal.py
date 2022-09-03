import pygame, math
from sys import exit
from vector import Vector2D

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
WINDOW_DIM = (WINDOW_WIDTH, WINDOW_HEIGHT)

BG_COLOR = "black"

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_DIM)

class Segment():
    def __init__(self, pos, angle, mag, height = 3):
        self.origin = Vector2D(pos[0], pos[1])
        self.mag = mag
        self.angle = angle
        self.height = height
        self.segment = Vector2D.get_polar_vector(angle, mag)
        self.childs = []

    def get_end(self):
        self.segment = Vector2D.get_polar_vector(self.angle, self.mag)
        end_pos = self.origin.add(self.segment).get_parameters()
        return end_pos

    def grow(self, off_set):
        if self.height > 0:
            self.childs = []
            
            new_mag = self.mag * 0.8
            new_height = self.height - 1

            self.childs.append(Segment(self.get_end(), self.angle - off_set, new_mag, new_height))
            self.childs.append(Segment(self.get_end(), self.angle + off_set, new_mag, new_height))

        for child in self.childs:
            child.grow(off_set)
  
    def move(self):
        self.angle += 0.01

    def render(self, surface):
        start_pos = self.origin.get_parameters()
        end_pos = self.get_end()

        for child in self.childs:
            child.render(surface)

        pygame.draw.line(surface, "white", start_pos, end_pos)

seg = Segment((WINDOW_WIDTH/2, WINDOW_HEIGHT), -math.pi/2, 60, 10)

direction = 1
angle = 0

while True:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if abs(angle) > math.pi / 4: direction *= -1
    
    seg.grow(angle)
    seg.render(screen)

    angle += 0.005 * direction

    pygame.display.update()
    clock.tick(60)


    
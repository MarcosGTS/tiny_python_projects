import pygame
from sys import exit 
from vector import Vector2D

LIFE_TIME = 50

pygame.init()
screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

class Particle():
    def __init__(self, x, y):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D.random()
        self.acc = Vector2D(0, 0)
        self.rad = 25
        self.life_time = LIFE_TIME

    def apply_force(self, force):
        self.acc = self.acc.add(force)

    def move(self):
        self.vel = self.vel.add(self.acc)
        self.pos = self.pos.add(self.vel)
        self.acc = Vector2D(0, 0)
    
    def check_life_time(self):
        return self.life_time < 0

    def show(self, surface):
        size = self.rad * (1 - self.life_time / LIFE_TIME) + 1
        pos = self.pos.get_parameters()
        
        circle = pygame.Surface((size, size))
        pygame.draw.circle(circle, "white", (size/2, size/2), size/2)
        circle.set_alpha(255 * self.life_time/LIFE_TIME)
        circle.set_colorkey("black")
        surface.blit(circle, pos)

    def update(self, surface):
        self.show(surface)
        self.move()

        self.life_time -= 1
        
class Emiter():
    def __init__(self, x, y):
        self.pos = Vector2D(x, y)
        self.particles = []
        self.force = Vector2D(0, -0.1)

    def insert_particles(self, num):
        x, y = self.pos.get_parameters()
        for i in range(10):
            self.particles.append(Particle(x, y))

    def show(self, surface):
        for p in self.particles:
            p.apply_force(self.force)
            p.update(surface)
            if p.check_life_time():
                self.particles.remove(p)

emiter = Emiter(200, 200)
while True:
    screen.fill("black")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    emiter.pos = Vector2D(mouse_x, mouse_y)
    emiter.insert_particles(5)
    emiter.show(screen)

    pygame.display.update()
    clock.tick(60)
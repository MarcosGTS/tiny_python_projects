import pygame, random
from sys import exit
from vector import Vector2D

WIDTH = 400
HEIGHT = 400

G = 10
MAX_GRAVITY_FORCE = 100

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Particle():
    def __init__(self, x, y, mass):
        self.position = Vector2D(x, y)
        self.vel = Vector2D(0, 0)
        self.acc = Vector2D(0, 0)
        self.mass = mass
        self.rad = self.mass ** .5

    def apply_force(self, force):
        self.acc = self.acc.add(force)

    def move(self):
        self.vel = self.vel.add(self.acc)
        self.position = self.position.add(self.vel)
        self.acc = Vector2D(0, 0)
    
    def render(self, surface, color = "red"):
        position = self.position.get_parameters()
        radius = self.rad
        pygame.draw.circle(surface, color, position, radius, 4)


class Attractor (Particle):
    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.rad = 10

    def apply_force(self, particle):
        #get direction
        force = self.position.sub(particle.position)
        #set magnitude
        if force.get_magnitude() > self.rad:
            return force.set_magnitude(particle.mass / (force.get_magnitude() ** 2) * G)

        return Vector2D(0, 0)

class Repulsor (Attractor):
    def __init__(self, x, y):
        super().__init__(x, y)

    def apply_force(self, particle):
        #invert force
        return super().apply_force(particle).mult_scalar(-1)

    def render(self, surface):
        super().render(surface, "green")

attractors = []
particles = []

particle_event = pygame.USEREVENT + 1

pygame.time.set_timer(particle_event, 1000)

while True:
    screen.fill("black")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == particle_event:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mass = random.randint(10, 30)
            particle = Particle(mouse_x, mouse_y, mass)

            # particle.vel = Vector2D(0, .5)
            particles.append(particle)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_l, mouse_m, mouse_r = pygame.mouse.get_pressed()
            
            if mouse_l:
                attractor = Attractor(mouse_x, mouse_y)
                attractors.append(attractor)
            elif mouse_r:
                repulsor = Repulsor(mouse_x, mouse_y)
                attractors.append(repulsor)

    for attractor in attractors:
        for p in particles:
            force = attractor.apply_force(p)
            if force.get_magnitude() > MAX_GRAVITY_FORCE: force.set_magnitude(MAX_GRAVITY_FORCE)
            p.apply_force(force)
            
        attractor.render(screen)

    for p in particles:
        p.move()
        p.render(screen) 

    pygame.display.update()
    clock.tick(60)


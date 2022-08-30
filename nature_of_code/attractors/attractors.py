import pygame, random
from sys import exit
from vector import Vector2D

WIDTH = 400
HEIGHT = 400

G = .5
MAX_GRAVITY_FORCE = 10

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
    
    def render(self, surface):
        position = self.position.get_parameters()
        radius = self.rad
        pygame.draw.circle(surface, "red", position, radius, 4)


attractors = [Particle(WIDTH/2, HEIGHT/2, 50)]
particles = []

particle_event = pygame.USEREVENT + 1

pygame.time.set_timer(particle_event, 2000)

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

            particle.vel = Vector2D(0, .5)
            particles.append(particle)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            attractor = Particle(mouse_x, mouse_y, 50)
            attractors.append(attractor)

            
    for attractor in attractors:
        attractor.render(screen)
        
        for p in particles:

            dif_vector = attractor.position.sub(p.position)
            distance = dif_vector.get_magnitude()
            direction = dif_vector.normalize()
            force = Vector2D(0, 0)
            
            if distance > 50:
                force = direction.set_magnitude(attractor.mass * p.mass /(distance ** 2))
                force = force.mult_scalar(G)
                if force.get_magnitude() > MAX_GRAVITY_FORCE: force.set_magnitude(MAX_GRAVITY_FORCE)
        
            p.apply_force(force)
            p.move()
            p.render(screen) 

    pygame.display.update()
    clock.tick(60)


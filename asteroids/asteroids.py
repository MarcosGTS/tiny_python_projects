import pygame, math, random
from sys import exit


WIN_WIDTH = 800
WIN_HEIGHT = 400
FPS = 60

MENU_STATE = 0
GAME_STATE = 1
GAME_OVER_STATE = 2

MIN_RADIUS = 10
MAX_RADIUS = 80
MIN_VELOCITY = 0.4

def dist_between_points(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(1/2)

def degrees_to_radians(degree):
    return 2 * math.pi * degree/360

def draw_circle(surface, pos, radius = 10, edges = 4, orientation = 0):
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
            pygame.draw.line(surface,  "#FFFFFF", origin, trans_pos)

        if len(points) >= 2:
            pygame.draw.line(surface, "#FFFFFF", points[-2], points[-1])

class Ship(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.pos = pos
        self.orientation = 0
        self.aceleration = 0.2
        self.velocity = 0

        self.image = pygame.Surface((20, 20))
        draw_circle(self.image, (10, 10), 10, 3, self.orientation)
        
        self.rect = self.image.get_rect(center = pos)

        self.orientation_buffer = 0
        self.buffer = self.pos
        self.body = []

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.velocity += self.aceleration
            self.orientation_buffer = self.orientation

        if keys[pygame.K_LEFT]:
            self.orientation -= 5
            self.image.fill("#000000")
            draw_circle(self.image, (10, 10), 10, 3, self.orientation)
            
        if keys[pygame.K_RIGHT]:
            self.orientation += 5
            self.image.fill("#000000")
            draw_circle(self.image, (10, 10), 10, 3, self.orientation)

    def move(self):
        #atrito
        self.velocity -= self.velocity * 0.01
        if self.velocity < 0: self.velocity = 0

        radians = degrees_to_radians(self.orientation_buffer)
        (velocity_x, velocity_y) = (math.cos(radians), math.sin(radians))
        velocity_x *= self.velocity
        velocity_y *= self.velocity
        self.pos = (self.pos[0] + velocity_x, self.pos[1] + velocity_y)

        self.rect.center = self.pos
        
    
    def updade_buffer(self):
        dist = dist_between_points(self.pos, self.buffer)
        if dist > 14:
            self.body.append({"pos":self.buffer, "orientation": self.orientation_buffer})
            self.body = self.body[1:]
            self.buffer = self.pos       
    
    def grow(self):
        self.body.append({"pos": (self.buffer), "orientation": self.orientation_buffer})

    def update(self):
        self.updade_buffer()
        self.move()
        self.get_input()
        
        for piece in self.body:
            draw_circle(piece["pos"], 6, 3, piece["orientation"])
        
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

    def update(self):
        self.move()

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

pygame.init()
clock = pygame.time.Clock()

ship = pygame.sprite.GroupSingle()
ship.add(Ship((400, 200)))
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

lasers = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

asteroid_event = pygame.USEREVENT + 1
pygame.time.set_timer(asteroid_event, 5000)

game_state = MENU_STATE

while True:
    screen.fill("#000000")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_state == GAME_STATE:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key in [pygame.K_m]:
                    ship.grow()

                if key in [32, pygame.K_SPACE]:
                    radians = degrees_to_radians(ship.sprite.orientation)
                    lasers.add(Laser(ship.sprite.pos, radians))

                    for cell in ship.sprite.body:
                        cell_orientation = degrees_to_radians(cell["orientation"])
                        lasers.add(Laser(cell["pos"], cell_orientation + math.pi / 2))
                        lasers.add(Laser(cell["pos"], cell_orientation - math.pi / 2))

            if event.type == asteroid_event:
                size = random.randint(MIN_RADIUS, MAX_RADIUS)
                orientation = random.random() * math.pi * 2

                asteroids.add(Asteroid((-100, -100), size, orientation))
        
        elif game_state == MENU_STATE:
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key in [32, 13, pygame.K_KP_ENTER]:
                    game_state = GAME_STATE



    if game_state == GAME_STATE:
        # matem nave na tela
        if ship.sprite.pos[0] > WIN_WIDTH: ship.sprite.pos = (0, ship.sprite.pos[1])
        if ship.sprite.pos[1] > WIN_HEIGHT: ship.sprite.pos = (ship.sprite.pos[0], 0)
        if ship.sprite.pos[0] < 0: ship.sprite.pos = (WIN_WIDTH, ship.sprite.pos[1])
        if ship.sprite.pos[1] < 0: ship.sprite.pos = (ship.sprite.pos[0], WIN_HEIGHT)

        # manter asteroids na tela
        for asteroid in asteroids:
            if asteroid.rect.left > WIN_WIDTH: asteroid.pos = (0, asteroid.pos[1])
            if asteroid.rect.top  > WIN_HEIGHT: asteroid.pos = (asteroid.pos[0], 0)
            if asteroid.rect.right  < 0: asteroid.pos = (WIN_WIDTH, asteroid.pos[1])
            if asteroid.rect.bottom < 0: asteroid.pos = (asteroid.pos[0], WIN_HEIGHT)

        ship.draw(screen)
        ship.update()

        lasers.draw(screen)
        lasers.update()

        asteroids.draw(screen)
        asteroids.update()

        for laser in lasers:
            asteroid = pygame.sprite.spritecollideany(laser, asteroids)
            if asteroid:
                asteroid.destroy(laser, asteroids)
                laser.kill()

        #game over
        
    elif game_state == MENU_STATE:
        screen.fill("red")
    
    pygame.display.update()
    clock.tick(FPS)
import pygame, math, random
from Ship import Ship
from Laser import Laser
from Asteroid import Asteroid
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

def degrees_to_radians(degree):
    return 2 * math.pi * degree/360
        
# class Asteroid(pygame.sprite.Sprite):
#     def __init__(self, pos, radius=10, orientation=0):
#         super().__init__()
        
#         self.radius = radius
#         self.orientation = orientation
#         self.velocity =  MIN_VELOCITY / (radius / MAX_RADIUS) 
#         self.pos = pos

#         dimensions = (self.radius, self.radius)

#         surface = pygame.Surface((2*self.radius, 2*self.radius))
#         surface.set_colorkey("#000000")
#         pygame.draw.circle(surface, "#FFFFFF", dimensions ,self.radius, 1)

#         self.image = surface
#         self.rect = self.image.get_rect(center=pos)

#     def move(self):
#         x_velocity, y_velocity = (math.cos(self.orientation), math.sin(self.orientation))
        
#         x_velocity *= self.velocity
#         y_velocity *= self.velocity

#         self.pos = (self.pos[0] + x_velocity, self.pos[1] + y_velocity)    
#         self.rect.center = (self.pos[0], self.pos[1])
        
#     def destroy(self, laser, list):
#         mass = self.radius

#         childs = []

#         while mass > 8:
#             new_mass = random.random() * mass
#             mass -= new_mass
#             if new_mass > MIN_RADIUS:
#                 childs.append(new_mass)
            
#         if childs:  
#             for i in range(len(childs)):
#                 off_set = random.random() * math.pi / 2
#                 orientation = laser.angle + off_set - (math.pi / 4)
#                 new_mass = childs[i]
#                 list.add(Asteroid(self.rect.center, new_mass, orientation))

#         self.kill()

#     def update(self):
#         self.move()

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
font = pygame.font.Font(None, 50)

ship = pygame.sprite.GroupSingle()
ship.add(Ship((400, 200)))
lasers = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

asteroid_event = pygame.USEREVENT + 1
pygame.time.set_timer(asteroid_event, 5000)

game_state = MENU_STATE
score = 0

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
                    laser_pos = ship.sprite.pos.get_parameters()
                    radians = degrees_to_radians(ship.sprite.orientation)
                    lasers.add(Laser(laser_pos, radians))

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
                if event.key in [32, 13, pygame.K_KP_ENTER]:
                    game_state = GAME_STATE

        elif game_state == GAME_OVER_STATE:
            if event.type == pygame.KEYDOWN:
                game_state = MENU_STATE

    if game_state == GAME_STATE:
        ship_pos = ship.sprite.pos.get_parameters()
        
        # keep ship on screen
        if ship_pos[0] > WIN_WIDTH: ship.sprite.pos.set_parameters(0, ship_pos[1])
        if ship_pos[1] > WIN_HEIGHT: ship.sprite.pos.set_parameters(ship_pos[0], 0)
        if ship_pos[0] < 0: ship.sprite.pos.set_parameters(WIN_WIDTH, ship_pos[1])
        if ship_pos[1] < 0: ship.sprite.pos.set_parameters(ship_pos[0], WIN_HEIGHT)

        # keep asteroids on screen
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

        #check collisions  
        if pygame.sprite.spritecollideany(ship.sprite, asteroids): 
            game_state = GAME_OVER_STATE

        for laser in lasers:
            asteroid = pygame.sprite.spritecollideany(laser, asteroids)
            if asteroid:
                score += MAX_RADIUS - int(asteroid.radius) + 10
                asteroid.destroy(laser, asteroids)
                laser.kill()

        score_text = font.render(f'{score}', False, "#FFFFFF")
        score_surf = score_text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT * .1))
        screen.blit(score_text, score_surf)

    elif game_state == MENU_STATE:
        # reset values
        ship.empty()
        ship.add(Ship((400, 200)))
        
        asteroids.empty()
        lasers.empty()

        score = 0
        screen.fill("red")

    elif game_state == GAME_OVER_STATE:
        screen.fill("green")
    
    pygame.display.update()
    clock.tick(FPS)
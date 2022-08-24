from email.mime import base
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

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
font_title = pygame.font.Font(None, 50)
font_simple = pygame.font.Font(None, 25)

bg_music = pygame.mixer.Sound("./bgm_action_3.mp3")
laser_sound = pygame.mixer.Sound("./laser1.wav")
hit_sound = pygame.mixer.Sound("./hit01.wav")

base_volume = bg_music.get_volume()
bg_music.play(-1)
bg_music.set_volume(base_volume * 0.4)

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
                    laser_sound.play()

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
                game_state = GAME_STATE

        elif game_state == GAME_OVER_STATE:
            if event.type == pygame.KEYDOWN:
                key = event.key 
                if key in [pygame.K_RETURN]:
                    game_state = MENU_STATE

    if game_state == GAME_STATE:
        bg_music.set_volume(base_volume)
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
                hit_sound.play()
                laser.kill()

        score_text = font_title.render(f'{score}', False, "#FFFFFF")
        score_surf = score_text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT * .1))
        screen.blit(score_text, score_surf)

    elif game_state == MENU_STATE:
        bg_music.set_volume(base_volume * 0.4)

        # reset values
        ship.empty()
        ship.add(Ship((400, 200)))
        
        asteroids.empty()
        lasers.empty()

        score = 0

        screen.fill("#000000")
        game_title = font_title.render("ASTEROIDS", False, "#FFFFFF")
        game_title_surf = game_title.get_rect(center=(WIN_WIDTH/2, 50))

        menu_msg = font_simple.render("Press any button", False, "#FFFFFF")
        menu_msg_surf = menu_msg.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT - 50))
        
        screen.blit(game_title, game_title_surf)
        screen.blit(menu_msg, menu_msg_surf)

    elif game_state == GAME_OVER_STATE:
        bg_music.set_volume(base_volume * 0.4)
        gameover_msg = font_title.render(f"Final Score: {score}", False, "#FFFFFF")
        gameover_msg_surf = gameover_msg.get_rect(center=(WIN_WIDTH/2, 50))
        
        restart_msg = font_simple.render("Enter to restart", False, "#FFFFFF")
        restart_msg_surf = restart_msg.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT - 25))

        screen.fill("#000000")
        screen.blit(gameover_msg, gameover_msg_surf)
        screen.blit(restart_msg, restart_msg_surf)
        
    
    pygame.display.update()
    clock.tick(FPS)
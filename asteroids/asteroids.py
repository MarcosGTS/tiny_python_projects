import pygame, math
from modules.Ship import Ship
from modules.Laser import Laser
from modules.Asteroid import Asteroid
from sys import exit

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

WINDOW_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
WINDOW_TOP_CENTER = (WINDOW_WIDTH / 2, 50)
WINDOW_BOT_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)

BACKGROUND_COLOR = "#000000"

FONT_COLOR = "#FFFFFF"
FONT_TITLE_SIZE = 50
FONT_SIMPLE_SIZE = 25

FPS = 60

MENU_STATE = 0
GAME_STATE = 1
GAME_OVER_STATE = 2

MIN_RADIUS = 10
MAX_RADIUS = 80
MIN_VELOCITY = 0.4

ASTEROID_SPAWN_DELAY = 5 * 1000

def degrees_to_radians(degree):
    return 2 * math.pi * degree/360

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
font_title = pygame.font.Font(None, FONT_TITLE_SIZE)
font_simple = pygame.font.Font(None, FONT_SIMPLE_SIZE)

bg_music = pygame.mixer.Sound("./assets/bgm_action_3.mp3")
laser_sound = pygame.mixer.Sound("./assets/laser1.wav")
hit_sound = pygame.mixer.Sound("./assets/hit01.wav")

base_volume = bg_music.get_volume()
bg_music.play(-1)
bg_music.set_volume(base_volume * 0.4)

ship = pygame.sprite.GroupSingle()
lasers = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

asteroid_event = pygame.USEREVENT + 1
pygame.time.set_timer(asteroid_event, ASTEROID_SPAWN_DELAY)

game_state = MENU_STATE
score = 0

while True:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_state == GAME_STATE:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key in [pygame.K_m]:
                    ship.sprite.grow()

                if key in [32, pygame.K_SPACE]:
                    laser = ship.sprite.shoot()
                    lasers.add(laser)
                    laser_sound.play()

                    for cell in ship.sprite.body:
                        cell_orientation = degrees_to_radians(cell["orientation"])
                        lasers.add(Laser(cell["pos"], cell_orientation + math.pi / 2))
                        lasers.add(Laser(cell["pos"], cell_orientation - math.pi / 2))

            if event.type == asteroid_event:
                random_asteroid = Asteroid.generate_random_asteroid()
                asteroids.add(random_asteroid)
        
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
        if ship_pos[0] > WINDOW_WIDTH: ship.sprite.pos.set_parameters(0, ship_pos[1])
        if ship_pos[1] > WINDOW_HEIGHT: ship.sprite.pos.set_parameters(ship_pos[0], 0)
        if ship_pos[0] < 0: ship.sprite.pos.set_parameters(WINDOW_WIDTH, ship_pos[1])
        if ship_pos[1] < 0: ship.sprite.pos.set_parameters(ship_pos[0], WINDOW_HEIGHT)

        # keep asteroids on screen
        for asteroid in asteroids:
            if asteroid.rect.left > WINDOW_WIDTH: asteroid.pos = (0, asteroid.pos[1])
            if asteroid.rect.top  > WINDOW_HEIGHT: asteroid.pos = (asteroid.pos[0], 0)
            if asteroid.rect.right  < 0: asteroid.pos = (WINDOW_WIDTH, asteroid.pos[1])
            if asteroid.rect.bottom < 0: asteroid.pos = (asteroid.pos[0], WINDOW_HEIGHT)

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

        score_text = font_title.render(f'{score}', False, FONT_COLOR)
        score_surf = score_text.get_rect(center=WINDOW_TOP_CENTER)
        screen.blit(score_text, score_surf)

    elif game_state == MENU_STATE:
        bg_music.set_volume(base_volume * 0.4)

        # reset values
        ship.empty()
        ship.add(Ship(WINDOW_CENTER))
        
        asteroids.empty()
        lasers.empty()

        score = 0

        screen.fill(BACKGROUND_COLOR)
        game_title = font_title.render("ASTEROIDS", False, FONT_COLOR)
        game_title_surf = game_title.get_rect(center=WINDOW_TOP_CENTER)

        menu_msg = font_simple.render("Press any button", False, FONT_COLOR)
        menu_msg_surf = menu_msg.get_rect(center=WINDOW_BOT_CENTER)
        
        screen.blit(game_title, game_title_surf)
        screen.blit(menu_msg, menu_msg_surf)

    elif game_state == GAME_OVER_STATE:
        bg_music.set_volume(base_volume * 0.4)
        gameover_msg = font_title.render(f"Final Score: {score}", False, FONT_COLOR)
        gameover_msg_surf = gameover_msg.get_rect(center=WINDOW_TOP_CENTER)
        
        restart_msg = font_simple.render("Enter to restart", False, FONT_COLOR)
        restart_msg_surf = restart_msg.get_rect(center=WINDOW_BOT_CENTER)

        screen.fill(BACKGROUND_COLOR)
        screen.blit(gameover_msg, gameover_msg_surf)
        screen.blit(restart_msg, restart_msg_surf)
        
    
    pygame.display.update()
    clock.tick(FPS)
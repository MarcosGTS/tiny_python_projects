import pygame
from sys import exit
from vector import Vector2D

W_WIDTH = 400
W_HEIGTH = 400

P_RADIUS = 10

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((W_WIDTH, W_HEIGTH))

def cubic_bezier(surface, point_list):
    t = 0

    def get_point(point_list, t):
        if len(point_list) <= 1:
            return point_list[0]
        
        new_list = []
        for i in range(len(point_list) - 1):
            p0, p1 = point_list[i:i+2]
            new_list.append(Vector2D.lerp(p0, p1, t))

        return get_point(new_list, t)
    
    while t < 1 :
        new_point = get_point(point_list, t)
        pygame.draw.circle(surface, "#ffff00", new_point.get_parameters(), 1)
        t += 0.001

point_list = [
Vector2D(10, 20),
Vector2D(0, 0),
Vector2D(300, 80),
Vector2D(250, 20)]
    
selected_point = None

while True:
    screen.fill("#000000")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    cubic_bezier(screen, point_list)

    left_click = pygame.mouse.get_pressed()[0]
    
    if left_click:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_vec = Vector2D(mouse_x, mouse_y)

        aux = None
        for point in point_list:
            dist = mouse_vec.sub(point).get_magnitude()

            if dist <= P_RADIUS:
                aux = point

        if selected_point == aux:
            selected_point = None
        else:
            selected_point = aux

    pygame.draw.line(screen, "#ffffff", point_list[0].get_parameters(), point_list[1].get_parameters())
    pygame.draw.line(screen, "#ffffff", point_list[-1].get_parameters(), point_list[-2].get_parameters())

    for point in point_list:
        if point == selected_point:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selected_point.set_parameters(mouse_x, mouse_y)
            pygame.draw.circle(screen, "#ffffff", point.get_parameters(), P_RADIUS)
        else:
            pygame.draw.circle(screen, "#00ffff", point.get_parameters(), P_RADIUS)
 
    pygame.display.update()
    clock.tick(60)


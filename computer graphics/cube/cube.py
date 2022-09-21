import pygame
from sys import exit 

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Edge():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
A = Point(1, 1, 1)
B = Point(-1, 1, 1)
C = Point(1, -1, 1)
D = Point(-1, -1, 1)
E = Point(1, 1, -1)
F = Point(-1, 1, -1)
G = Point(1, -1, -1)
H = Point(-1, -1, -1)

points = [A, B, C, D, E, F, G, H]

cube = [
    Edge(A,B),
    Edge(C,D),
    Edge(E,F),
    Edge(G,H),
    Edge(A,C),
    Edge(B,D),
    Edge(E,G),
    Edge(F,H),
    Edge(A,E),
    Edge(C,G),
    Edge(B,F),
    Edge(D,H)
]

camera_x = 0
camera_y = 0

def convert_point(point):
    u = 200 + (camera_x + point.x) / point.z * 50
    v = 200 + (camera_y + point.y) / point.z * 50

    return (u, v)



while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                camera_x += 1
            if event.key == pygame.K_LEFT:
                camera_x -= 1
            if event.key == pygame.K_UP:
                for point in points:
                    point.z += 0.05
            if event.key == pygame.K_DOWN:
                for point in points:
                    point.z -= 0.05

    for edge in cube:
        p1 = convert_point(edge.p1)
        p2 = convert_point(edge.p2)

        pygame.draw.line(screen, "white", p1, p2)
    

    pygame.display.update()
    clock.tick(60)
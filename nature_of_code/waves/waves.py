import pygame, math, random
from sys import exit

WIDTH = 400
HEIGHT = 400

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Wave():
    def __init__(self, freq, amp, fase = 0):
        self.freq = freq
        self.amp = amp
        self.fase = fase

    def evalueate(self, x):
        return math.sin(self.fase + self.freq * 2 * math.pi * x / WIDTH) * self.amp

    def update(self):
        self.fase += random.randint(1, 8) / 5000

# Wave parameters
radius = 3
number_of_points = int(WIDTH / radius)

points = []
waves = []

for i in range(5):
    wave = Wave(random.randint(1, 6), random.randint(5, 30))
    waves.append(wave)

for i in range(number_of_points):
    x = i / number_of_points * WIDTH
    points.append(x)
    
while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    for i in range(len(points)):
        y = 0
        for wave in waves:
            y += wave.evalueate(points[i])
            wave.update()
        pygame.draw.circle(screen, "white", (points[i], y + HEIGHT/2), radius)
    
    pygame.display.update()
    clock.tick(60)
    

    
import random

class Vector2D ():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_parameters(self):
        return (self.x, self.y)

    def get_magnitude(self):
        return (self.x**2 + self.y**2)**(1/2)

    def set_parameters(self, x, y):
        self.x = x
        self.y = y

    def set_magnitude(self, mag):
        return self.normalize().mult_scalar(mag)

    def add(self, vector):
        # vector: Vector2D
        x, y = vector.get_parameters()
        return Vector2D(self.x + x, self.y + y)
    
    def sub(self, vector):
        # vector: Vector2D
        x, y = vector.get_parameters()
        return Vector2D(self.x - x, self.y - y)
    
    def mult_scalar(self, num):
        #num: scalar
        x, y = (num * self.x, num * self.y)
        return Vector2D(x, y)

    def normalize(self):
        mag = self.get_magnitude()
        x, y = (self.x / mag, self.y / mag)
        return Vector2D(x, y)

    def lerp(p0, p1, t):
        # p0, p1 (Vector2D)
        # t : 1 <= t <= 0
        # p0 + (p1 - p0)*t
        return p0.add(p1.sub(p0).mult_scalar(t))

    def random():
        x = random.random() * 2 - 1
        y = random.random() * 2 - 1

        return Vector2D(x, y).normalize()
    
    def copy(self):
        return Vector2D(self.x, self.y)
    
    def __repr__(self):
        return f'({self.x}, {self.y})'

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

    
    def __repr__(self):
        return f'({self.x}, {self.y})'

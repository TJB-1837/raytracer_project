class Sphere:
    center:tuple
    radius:int
    color:tuple
    specular:int

    def __init__(self, center, radius, color, specular=-1):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular
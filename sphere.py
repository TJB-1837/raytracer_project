class Sphere:
    center:tuple
    radius:int
    color:tuple
    specular:int
    reflective:float

    def __init__(self, center, radius, color, specular=-1, reflective=0.0):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular
        self.reflective = reflective
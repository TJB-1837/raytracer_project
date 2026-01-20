from pyray import Vector3
from utils import vector_normalize, cross_product

class Rectangle:
    def __init__(self, center, normal, width, height, color, specular, reflective):
        self.center = center
        self.normal = vector_normalize(normal)
        self.width = width
        self.height = height
        self.color = color
        self.specular = specular
        self.reflective = reflective

        # Choix d’un vecteur non colinéaire
        if abs(self.normal.y) < 0.9:
            tmp = Vector3(0, 1, 0)
        else:
            tmp = Vector3(1, 0, 0)

        self.u = vector_normalize(cross_product(tmp, self.normal))  # vecteur u de la base locale
        self.v = cross_product(self.normal, self.u)                 # vecteur v de la base locale
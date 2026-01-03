import pyray as pr
import numpy as np
import math
from pyray import Vector3
from PIL import Image

BACKGROUND_COLOR = (255,255,255)
inf = math.inf
Cw = 1920
Ch = 1080

Vw=1
Vh=Vw * Ch / Cw
d=1

class Sphere:
    def __init__(self,center,radius,color):
        self.center = center
        self.radius = radius
        self.color = color


class Canva:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.pixels = [
            [(0, 0, 0) for _ in range(width)]
            for _ in range(height)
        ]

    def putPixel(self,x,y,color):
        Sx = Cw//2 + x
        Sy = Ch//2 -y
        if (0 <= Sx < self.width and 0 <= Sy < self.height):
            self.pixels[Sy][Sx] = color

    def savePNG(self, filename):
        # Crée une image vide
        img = Image.new("RGB", (self.width, self.height))
        
        # Remplit l'image pixel par pixel
        for y in range(self.height):
            for x in range(self.width):
                img.putpixel((x, y), self.pixels[y][x])
        
        # Sauvegarde en PNG
        img.save(filename)
    

def cross_product(A, B):
    """Calcule le produit vectoriel entre deux vecteurs A et B."""
    result = Vector3(A.y*B.z - A.z*B.y, A.z*B.x - A.x*B.z,A.x*B.y - A.y*B.x)
    return result

def vector_length(vector):
    """Calcule la longueur d'un vecteur."""
    return math.sqrt(dot_product(vector))

def vector_normalize(vector):
    """Normalise un vecteur pour obtenir un vecteur de longueur 1."""   
    length = vector_length(vector)
    return Vector3(vector.x / length,vector.y/length,vector.z/length)

def dot_product(A, B):
    """Calcule le produit scalaire entre deux vecteurs A et B."""
    result = A.x*B.x + A.y*B.y + A.z*B.z
    return result


def CanvasToViewport(x, y) :
    return Vector3(x*Vw/Cw, y*Vh/Ch, d) #calcule le vecteur directeur caméra / fenetre d affichage

def IntersectRaySphere(O, D, sphere) :
    r = sphere.radius
    CO = Vector3(O.x - sphere.center.x,
             O.y - sphere.center.y,
             O.z - sphere.center.z)

    a = dot_product(D, D)
    b = 2*dot_product(CO, D)
    c = dot_product(CO, CO) - r*r

    discriminant = b*b - 4*a*c
    if (discriminant < 0) :
        return inf, inf
    

    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)
    return t1, t2



def TraceRay(O, D, t_min, t_max,scene) :
    closest_t = inf
    closest_sphere = None
    for sphere in scene :
        t1, t2 = IntersectRaySphere(O, D, sphere)
        if (t_min <= t1 <= t_max and t1 < closest_t ):
            closest_t = t1
            closest_sphere = sphere
        
        if (t_min <= t2 <= t_max and t2 < closest_t) :
            closest_t = t2
            closest_sphere = sphere
        
    if (closest_sphere == None) :
        return BACKGROUND_COLOR
    
    return closest_sphere.color


def main():
    canvas = Canva(Cw,Ch)
    sphere1 =  Sphere(Vector3(0, -1, 3), 1, (255, 0, 0)) #Red
    sphere2 =  Sphere(Vector3(2, 0, 4),1,(0, 0, 255))  # Blue
    sphere3 =  Sphere(Vector3(-2, 0, 4),1,(0, 255, 0))  # Blue
    scene = [sphere1,sphere2,sphere3]
    
    print("Hello from raytracer-project!")
    O = Vector3(0, 0, 0)
    for i in range(-Cw//2 , Cw//2) : 
        for j in range (-Ch//2 , Ch//2):
            D = CanvasToViewport(i, j)
            color = TraceRay(O, D, 1, inf,scene)
            canvas.putPixel(i, j, color)
    canvas.savePNG("output.png")
    print("Image saved as output.png")    

if __name__ == "__main__":
    main()

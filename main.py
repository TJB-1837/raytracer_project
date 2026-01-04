import pyray as pr
import numpy as np
import math
from pyray import Vector3
from PIL import Image


inf = math.inf
Cw = 1920
Ch = 1080

Vw=1
Vh=Vw * Ch / Cw
d=1

class Sphere:
    def __init__(self,center,radius,color,specular,reflective):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular
        self.reflective = reflective

class Light: 
    def __init__(self,type,intensity,position,direction):
        self.type = type
        self.intensity = intensity
        self.position = position
        self.direction = direction

class Color:
    def __init__(self,r,g,b):
        self.r=r
        self.g=g
        self.b=b

    def to_tuple(self):
        return (
            min(255, max(0, int(self.r))),
            min(255, max(0, int(self.g))),
            min(255, max(0, int(self.b)))
        )
    def __mul__(self, k):
        return Color(self.r*k, self.g*k, self.b*k)
    
    def __add__(self,color):
        return Color(self.r+color.r, self.g+color.g, self.b+color.b)
    
BACKGROUND_COLOR = Color(0,0,0)

class Canva:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.pixels = [
            [(0, 0, 0) for _ in range(width)]
            for _ in range(height)
        ]

    def putPixel(self,x,y,color_tuple):
        Sx = Cw//2 + x
        Sy = Ch//2 -y
        if (0 <= Sx < self.width and 0 <= Sy < self.height):
            self.pixels[Sy][Sx] = color_tuple

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
    return math.sqrt(dot_product(vector,vector))

def vector_normalize(vector):
    """Normalise un vecteur pour obtenir un vecteur de longueur 1."""   
    length = vector_length(vector)
    if (vector_length(vector) ==0):
        return vector
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

def ReflectRay(R,N):
    return Vector3(2 * N.x * dot_product(N, R) - R.x,2 * N.y * dot_product(N, R) - R.y,2 * N.z * dot_product(N, R) - R.z)

def ComputeLighting(P, N,V,lights,s,scene):
    i = 0.0
    for light in lights :
        if (light.type == "ambient"):
            i += light.intensity
        else: 
            if (light.type == "point"):
                #L = light.position - P
                L= Vector3( light.position.x - P.x, light.position.y -P.y, light.position.z - P.z)
                t_max = 1
                L = vector_normalize(L)
            else:
                L = vector_normalize(light.direction)
                t_max = inf
            # Shadow check
            shadow_sphere, shadow_t = ClosestIntersection(P, L, 0.001, t_max,scene)
            if (shadow_sphere != None) :
                continue
            
            # Diffuse
            n_dot_l = dot_product(N, L)
            if (n_dot_l > 0):
                i += light.intensity * n_dot_l/(vector_length(N) * vector_length(L))

            # Specular
            if (s != -1) : #for matte shapes
                R = ReflectRay(L,N)
                r_dot_v = dot_product(R, V)
                if r_dot_v > 0 :
                    i += light.intensity * math.pow(r_dot_v/(vector_length(R) * vector_length(V)), s)
    return min(1,i)


def TraceRay(O, D, t_min, t_max,scene,lights, recursion_depth) :
    closest_sphere, closest_t = ClosestIntersection(O, D, t_min, t_max, scene)   
    if (closest_sphere == None) :
        return BACKGROUND_COLOR
    
    #P = O + closest_t * D  # Compute intersection
    P = Vector3(O.x + closest_t *  D.x,
             O.y + closest_t * D.y,
             O.z + closest_t * D.z)
    #N = P - closest_sphere.cente
    N = Vector3(P.x - closest_sphere.center.x,
             P.y - closest_sphere.center.y,
             P.z - closest_sphere.center.z)  # Compute sphere normal at intersection
        
    N = vector_normalize(N)
    V = Vector3(-D.x, -D.y, -D.z)
    i = ComputeLighting(P, N, V,lights,closest_sphere.specular,scene)
    local_color = closest_sphere.color * i 

    #If we hit the recursion limit or the object is not reflective, we're done
    r = closest_sphere.reflective
    if(recursion_depth <= 0 or r <= 0):
        return local_color

    # Compute the reflected color
    R = ReflectRay(V, N)
    reflected_color = TraceRay(P, R, 0.001, inf, scene, lights, recursion_depth - 1)
    
    return local_color * (1 - r) + reflected_color * r     
    
def ClosestIntersection(O, D, t_min, t_max,scene) :
    closest_t = inf
    closest_sphere = None
    for sphere in scene :
        t1, t2 = IntersectRaySphere(O, D, sphere)
        if (t_min <= t1 <= t_max and t1 < closest_t) :
            closest_t = t1
            closest_sphere = sphere
        
        if (t_min <= t2 <= t_max and t2 < closest_t) :
            closest_t = t2
            closest_sphere = sphere
    
    return closest_sphere, closest_t



def main():
    canvas = Canva(Cw,Ch)
    sphere1 =  Sphere(Vector3(0, -1, 3), 1, Color(255, 0, 0),500, 0.2) #Red (Shiny and a bit reflective) 
    sphere2 =  Sphere(Vector3(2, 0, 4),1,Color(0, 0, 255)  ,500, 0.3)  # Blue (Shinyand a bit more reflective)
    sphere3 =  Sphere(Vector3(-2, 0, 4),1,Color(0, 255, 0),10, 0.4)  # Blue (somewhat shiny and even more reflective)
    sphere4 =  Sphere(Vector3(0, -5001, 0),5000 ,Color(255, 255, 0), 1000, 0.5)  # Yellow (very shiny and half reflective)
    scene = [sphere1, sphere2, sphere3,sphere4]
    light1 = Light("ambient", 0.2,None,None)
    light2 = Light("point", 0.6, Vector3(2, 1, 0), None) 
    light3 = Light("directional", 0.2, None, Vector3(1, 4, 4)) 
    lights = [light1,light2,light3]
    
    print("Hello from raytracer-project!")
    O = Vector3(0, 0, 0)
    for i in range(-Cw//2 , Cw//2) : 
        for j in range (-Ch//2 , Ch//2):
            D = CanvasToViewport(i, j)
            color = TraceRay(O, D, 1, inf,scene,lights, 3)
            canvas.putPixel(i, j, color.to_tuple())
    canvas.savePNG("output.png")
    print("Image saved as output.png")    

if __name__ == "__main__":
    main()

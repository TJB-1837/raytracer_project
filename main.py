import pyray as pr
import numpy as np
import math
from pyray import Vector3

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

        self.u = vector_normalize(cross_product(tmp, self.normal))
        self.v = cross_product(self.normal, self.u)

    
class Scene:
    def __init__(self,spheres,rectangles,lights):
        self.spheres = spheres
        self.rectangles = rectangles
        self.lights = lights
        

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

    def savePPM(self, filename):
        with open(filename, "w") as f:
            # Header
            f.write("P3\n")                                 #Précision du type (ici ASCII)
            f.write(f"{self.width} {self.height}\n")        #Précision du format
            f.write("255\n")                                #précision valeur max

            # Pixels
            for y in range(self.height):            #parcours des lignes
                for x in range(self.width):         #parcours des colonnes
                    r, g, b = self.pixels[y][x]     #extraction du tuple
                    f.write(f"{r} {g} {b} ")        #écriture dans le fichier
                f.write("\n")                       #fin de la lignes --> ligne suivante
    

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


def rotation_matrix(axis, theta):
    """Génère une matrice de rotation autour d'un axe arbitraire."""
    # TODO : mettre en œuvre 
    axis = vector_normalize(axis)

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    nx = axis.x
    ny = axis.y
    nz = axis.z

    R = np.array([
        [(1 - cos_theta)*nx*nx + cos_theta,     (1 - cos_theta)*nx*ny - sin_theta*nz,  (1 - cos_theta)*nx*nz + sin_theta*ny],
        [(1 - cos_theta)*nx*ny + sin_theta*nz,  (1 - cos_theta)*ny*ny + cos_theta,     (1 - cos_theta)*ny*nz - sin_theta*nx],
        [(1 - cos_theta)*nx*nz - sin_theta*ny,  (1 - cos_theta)*ny*nz + sin_theta*nx,  (1 - cos_theta)*nz*nz + cos_theta   ]
    ])
    return R 

def np_to_vec3(a):
    return Vector3(a[0], a[1], a[2])

def vec3_to_np(v):
    return np.array([v.x, v.y, v.z])



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


def IntersectRayRectangle(O, D, rect):
    denom = dot_product(rect.normal, D)
    if abs(denom) < 1e-6:
        return inf

    t = dot_product(
        rect.normal,
        Vector3(
            rect.center.x - O.x,
            rect.center.y - O.y,
            rect.center.z - O.z
        )
    ) / denom

    if (t <= 0):
        return inf
    
    # Calcul du point d'intersection P = O+t*D 
    P = Vector3(O.x + t*D.x, O.y + t*D.y, O.z + t*D.z)

    # Vérifier si P est à l'intérieur du rectangle
    v = Vector3(P.x - rect.center.x, P.y - rect.center.y, P.z - rect.center.z)
    u_dist = dot_product(v, rect.u)
    v_dist = dot_product(v, rect.v)
    if abs(u_dist) > rect.width / 2 or abs(v_dist) > rect.height / 2:
        return inf

    return t


def ReflectRay(R,N):
    return Vector3(2 * N.x * dot_product(N, R) - R.x,2 * N.y * dot_product(N, R) - R.y,2 * N.z * dot_product(N, R) - R.z)

def ComputeLighting(P, N,V,s,scene):
    i = 0.0
    for light in scene.lights :
        if (light.type == "ambient"):
            i += light.intensity
        else: 
            if (light.type == "point"):
                #L = light.position - P
                L= Vector3( light.position.x - P.x, light.position.y -P.y, light.position.z - P.z)
                t_max = 1
                #L = vector_normalize(L)
            else:
                L = vector_normalize(light.direction)
                t_max = inf
            # Shadow check
            shadow_obj, shadow_t = ClosestIntersection(P, L, 0.001, t_max,scene)
            if (shadow_obj != None) :
                continue
            
            L = vector_normalize(L)
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


def TraceRay(O, D, t_min, t_max,scene, recursion_depth) :
    closest_obj, closest_t = ClosestIntersection(O, D, t_min, t_max, scene)   
    if (closest_obj == None) :
        return BACKGROUND_COLOR

    #P = O + closest_t * D  # Compute intersection
    P = Vector3(O.x + closest_t *  D.x,
             O.y + closest_t * D.y,
             O.z + closest_t * D.z)
    

    if isinstance(closest_obj, Sphere):
        N = vector_normalize(Vector3(P.x - closest_obj.center.x,            #N = P - closest_sphere.center
                                    P.y - closest_obj.center.y,
                                    P.z - closest_obj.center.z))            # Compute sphere normal at intersection
        i= ComputeLighting(P, N, Vector3(-D.x,-D.y,-D.z), closest_obj.specular, scene)
        local_color = closest_obj.color * i
        r = closest_obj.reflective
    elif isinstance(closest_obj, Rectangle):
        N = closest_obj.normal
        i = ComputeLighting(P, N, Vector3(-D.x,-D.y,-D.z), closest_obj.specular, scene)
        local_color = closest_obj.color * i
        r = closest_obj.reflective

    #If we hit the recursion limit or the object is not reflective, we're done
    if(recursion_depth <= 0 or r <= 0):
        return local_color

    # Compute the reflected color
    R = ReflectRay(Vector3(-D.x,-D.y,-D.z), N)
    reflected_color = TraceRay(P, R, 0.001, inf, scene, recursion_depth - 1)
    
    return local_color * (1 - r) + reflected_color * r     
    
def ClosestIntersection(O, D, t_min, t_max,scene) :
    closest_t = inf
    closest_obj = None
    for sphere in scene.spheres :
        t1, t2 = IntersectRaySphere(O, D, sphere)
        if (t_min <= t1 <= t_max and t1 < closest_t) :
            closest_t = t1
            closest_obj = sphere
        
        if (t_min <= t2 <= t_max and t2 < closest_t) :
            closest_t = t2
            closest_obj = sphere

    for rect in scene.rectangles:
        t = IntersectRayRectangle(O, D, rect)
        if t_min <= t <= t_max and t < closest_t:
            closest_t = t
            closest_obj = rect

    return closest_obj, closest_t



def main():
    canvas = Canva(Cw,Ch)

    sphere1 =  Sphere(Vector3(0, -1, 3), 1, Color(255, 0, 0),500, 0.2) #Red (Shiny and a bit reflective) 
    sphere2 =  Sphere(Vector3(2, 0, 4),1,Color(0, 0, 255)  ,500, 0.3)  # Blue (Shinyand a bit more reflective)
    sphere3 =  Sphere(Vector3(-2, 0, 4),1,Color(0, 255, 0),10, 0.4)  # Blue (somewhat shiny and even more reflective)
    #sphere4 =  Sphere(Vector3(0, -5001, 0),5000 ,Color(255, 255, 0), 1000, 0.5)  # Yellow (very shiny and half reflective)
    spheres = [sphere1, sphere2, sphere3,]

    rectangle1 = Rectangle(Vector3(0, 0, 10), Vector3(0, 0, -1), 20, 20, Color(200, 200, 200), 100, 0.1)#backwall
    rectangle2 = Rectangle(Vector3(0, -2, 5), Vector3(0, 1, 0), 20, 20, Color(255, 230, 150), 100, 0.1) #floor
    rectangle3 = Rectangle(Vector3(0, 10, 5), Vector3(0, -1, 0), 20, 20, Color(245, 245, 245), 100, 0.1) #ceiling
    rectangle4 = Rectangle(Vector3(-6, 2, 5), Vector3(1, 0, 0), 20, 20, Color(150, 180, 255), 100, 0.1)#left wall
    rectangle5 = Rectangle(Vector3(6, 2, 5), Vector3(-1, 0, 0), 20, 20, Color(150, 180, 255), 100, 0.1) #right yellow wall
    rectangles=[rectangle1,rectangle2,rectangle3,rectangle4,rectangle5]

    light1 = Light("ambient", 0.1,None,None)
    light2 = Light("point", 0.6, Vector3(2, 6, 0), None) 
    light3 = Light("directional", 0.3, None, Vector3(1, 4, -4)) 
    lights = [light1,light2,light3] 

    scene = Scene(spheres, rectangles, lights) 
    print("Hello from raytracer-project!")
    O = Vector3(0, 2, -20)                                        #Position de la caméra
    pi = math.pi
    R = rotation_matrix(Vector3(0,0,1),pi/10000)
    for i in range(-Cw//2 , Cw//2) : 
        for j in range (-Ch//2 , Ch//2):
            D_np = R @ vec3_to_np(CanvasToViewport(i, j))
            D = np_to_vec3(D_np)
            color = TraceRay(O, D, 1, inf,scene, 3)
            canvas.putPixel(i, j, color.to_tuple())
    canvas.savePPM("output.ppm")
    print("Image saved as output.ppm")    

if __name__ == "__main__":
    main()

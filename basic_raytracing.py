from PIL import Image
from sphere import Sphere
from light import Light
from scene import Scene
from utils import dot, vector_sub, vector_add, length, vector_mul, normalize
import math

# Configuration de la scène 
WIDTH = 500
HEIGHT = 500

# Viewport (dans l’espace 3D)
VWIDTH = 1
VHEIGHT = 1
DISTANCE_TO_VIEWPORT = 1

# Couleur de fond
BACKGROUND_COLOR = (240, 240, 240)

# Scène : 3 sphères de Gambetta 
scene = Scene([
    Sphere((0, -1, 3), 1, (255, 0, 0),500),   # rouge
    Sphere((2, 0, 4), 1, (0, 0, 255),500),    # bleu
    Sphere((-2, 0, 4), 1, (0, 255, 0),10),   # vert
    Sphere((0, -5001, 0),5000,(255, 255, 0),1000) # jaune
    ],
    [
    Light("ambient",0.2,(0,0,0),(0,0,0)),
    Light("point",0.6,(2,1,0),(0,0,0)),
    Light("directionnal",0.2,(0,0,0),(1,4,4))
    ]

)

# Fonctions du raytracer
def computeLighting(P, N, V, s):
    i = 0.0
    for light in scene.lights:
        if light.type == "ambient":
           i += light.intensity
        else:
            if light.type == "point":
               L = vector_sub(light.position,P)
               t_max = 1
            else:
               L = light.direction
               t_max = math.inf

            shadow_sphere, shadow_t = closestIntersection(P, L, 0.001, t_max)
            if shadow_sphere != None:
                continue
            
            # diffuse lightning
            n_dot_l = dot(N, L)
            if n_dot_l > 0:
               i += light.intensity * n_dot_l/(length(N) * length(L))
            
            # specular lightning
            if s != -1:
                R = vector_sub(vector_mul(N,2*dot(N,L)),L)
                r_dot_v = dot(R, V)
                if r_dot_v > 0 :
                    i += light.intensity * pow(r_dot_v/(length(R) * length(V)), s)


    return i


def closestIntersection(O, D, t_min, t_max):
    closest_t = math.inf
    closest_sphere = None
    for sphere in scene.spheres:
        t1, t2 = intersect_ray_sphere(O, D, sphere)
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere

        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere
        
    return closest_sphere, closest_t

def canvas_to_viewport(x, y):
    vx = x * VWIDTH / WIDTH
    vy = y * VHEIGHT / HEIGHT
    return (vx, vy, DISTANCE_TO_VIEWPORT)

def intersect_ray_sphere(origin, direction, sphere):
    # calculer intersection rayon-sphère
    CO = vector_sub(origin, sphere.center)

    a = dot(direction, direction)
    b = 2 * dot(CO, direction)
    c = dot(CO, CO) - sphere.radius * sphere.radius

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return math.inf, math.inf

    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)
    return t1, t2

def trace_ray(origin, direction, t_min, t_max):

    closest_sphere, closest_t = closestIntersection(origin, direction, t_min, t_max)
    if closest_sphere == None:
        return BACKGROUND_COLOR
    
    P = vector_add(origin, vector_mul(direction, closest_t))
    N = vector_sub(P,closest_sphere.center)
    N = normalize(N)
    direction_inv = (-direction[0],-direction[1],-direction[2])
    color = vector_mul(closest_sphere.color, computeLighting(P,N,direction_inv,closest_sphere.specular))
    
    return (int(color[0]),int(color[1]),int(color[2]))
    

# Rendu
image = Image.new("RGB", (WIDTH, HEIGHT))
pixels = image.load()

camera_origin = (0, 0, 0)

for x in range(-WIDTH//2, WIDTH//2):
    for y in range(-HEIGHT//2, HEIGHT//2):
        # point sur le viewport
        direction = canvas_to_viewport(x, y)

        # lancer le rayon
        color = trace_ray(camera_origin, direction, 1, math.inf)

        # dessiner pixel
        px = x + WIDTH//2
        py = HEIGHT//2 - y - 1
        pixels[px, py] = color

# Sauvegarder l’image
image.save("render.png")
print("Image générée : render.png")

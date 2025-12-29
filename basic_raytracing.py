from PIL import Image
from sphere import Sphere
from utils import dot, vector_sub
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
scene = [
    Sphere((0, -1, 3), 1, (255, 0, 0)),   # rouge
    Sphere((2, 0, 4), 1, (0, 0, 255)),    # bleu
    Sphere((-2, 0, 4), 1, (0, 255, 0))    # vert
]

# Fonctions du raytracer

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
    closest_t = math.inf
    closest_sphere = None

    for sphere in scene:
        t1, t2 = intersect_ray_sphere(origin, direction, sphere)
        
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        
        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere
    
    if closest_sphere is None:
        return BACKGROUND_COLOR
    
    return closest_sphere.color

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

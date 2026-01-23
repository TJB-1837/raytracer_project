import pyray as pr
import numpy as np
import math
from pyray import Vector3
from sphere import Sphere
from rectangle import Rectangle
from scene import Scene , load_scene_json
from light import Light
from color import Color
from canva import Canva, Cw, Ch
from utils import dot_product, vector_length, vector_normalize, cross_product, rotation_matrix, vec3_to_np, np_to_vec3

# Définition de variables globales
inf = math.inf
Vw=1
Vh=Vw * Ch / Cw
d=1
BACKGROUND_COLOR = Color(0,0,0)

def CanvasToViewport(x, y) :
    return Vector3(x*Vw/Cw, y*Vh/Ch, d) #calcule le vecteur directeur "caméra vers fenetre d affichage"

def IntersectRaySphere(O, D, sphere) :
    r = sphere.radius
    CO = Vector3(O.x - sphere.center.x,    # Vecteur entre la sphère et la caméra (O)
             O.y - sphere.center.y,
             O.z - sphere.center.z)

    # calculs des points d'intersections entre le rayon et une sphère
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
    denom = dot_product(rect.normal, D) #On veut savoir si on regarde le rectangle depuis une tranche 
    if abs(denom) < 1e-6:
        return inf

    #Calculs de la distance entre la caméra et le rectangle
    t = dot_product(
        rect.normal,
        Vector3(
            rect.center.x - O.x,
            rect.center.y - O.y,
            rect.center.z - O.z
        )
    ) / denom

    # pas d'affichage si le rectangle est derrière la caméra
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
    # 2 * N * <N:R> - R
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
            if (s != -1) : # For matte shapes
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

def ChoseAngleAndAXis():
    theta = float(input("Chose the rotation angle of the camera (strings not accepted) : "))
    axisInput = input("Chose the rotation axis [x, y or z ONLY] : ")
    if axisInput == 'x' :
        axis = Vector3(1,0,0)
    elif axeInput == 'y' : 
        axis = Vector3(0,1,0)
    elif axeInput == 'z' :
        axis = Vector3(0,0,1) 
    else :
        print("You didn't chose a valid axis, no rotation will be applied")
        axis = Vector3(1,0,0) # Choix arbitraire
        theta = 0
    return axis, theta


def FillCanva(R,canvas,scene,O) : 
    for i in range(-Cw//2 , Cw//2) : 
        for j in range (-Ch//2 , Ch//2):
            D_np = vec3_to_np(CanvasToViewport(i, j)) @ R  #Conversion to numpy array pour appliquer un produit matriciel
            D = np_to_vec3(D_np)
            color = TraceRay(O, D, 1, inf,scene, 3)
            canvas.putPixel(i, j, color.to_tuple())


def RenderImage():
    axe, theta = ChoseAngleAndAXis()  #Axe et angle entrés par l'utilisateur
    scene, O = load_scene_json("scene.json") #Position de la caméra
    print("Rendering in progress...")
    canvas = Canva(Cw,Ch)                            
    R = rotation_matrix(axe,theta)
    FillCanva(R,canvas,scene,O)    
    canvas.savePPM("output.ppm")
    print("Image saved as output.ppm") 


def RenderAnimation() : 
    NB_FRAMES = 30
    radius = 2
    theta = 0
    scene, O = load_scene_json("scene.json") #Position de la caméra
    pointLight = scene.lights[1] # Récupération de la pointLight OBLIGATOIREMENT DEFINIE EN 2EME dans la scene json
    if(pointLight.type != "point"):
        print("This animation rotates a point light, please define one as your second light defined in your json scene !")
        return
    xLight = pointLight.position.x
    yLight = pointLight.position.y
    zLight = pointLight.position.z
    for frame in range(NB_FRAMES):
        print(f"Rendering frame {frame + 1} / {NB_FRAMES}")
        canvas = Canva(Cw,Ch)                                 
        theta += 2*math.pi / NB_FRAMES  # Incrémentation de l'angle 
        pointLight.position = Vector3 (  # Calcul de la nouvelle position de la pointLight
            xLight +radius *math.cos(theta), 
            yLight +radius * math.sin(theta),
            zLight
        )   
        R = rotation_matrix(Vector3(0,1,0),0)
        FillCanva(R,canvas,scene,O)
        canvas.savePPM(f"frame_{frame+1:02}.ppm")


def main():
    choice = input("Choisir le mode [i = image | a = animation] : ").strip().lower() # prise en compte du caractere ou de la string d'input

    if choice in ["i", "image"]:
        RenderImage()
    elif choice in ["a", "anim", "animation"]:
        RenderAnimation()
    else:
        print("Entrée invalide")
             

if __name__ == "__main__":
    main()

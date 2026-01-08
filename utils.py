import math
import numpy as np 

#Vecteurs au format tuple (x, y, z)
def vector_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def vector_add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def vector_mul(a, k):
    return (a[0] * k, a[1] *k, a[2] *k)

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def length(a):
    return math.sqrt(dot(a,a))

def normalize(a):
    l = length(a)
    if l == 0 : 
        return (0,0,0)
    return (a[0]/l, a[1]/l, a[2]/l)


def rotation_matrix(axis, theta):
    """Génère une matrice de rotation autour d'un axe arbitraire."""
    # TODO : mettre en œuvre 
    axis = normalize(axis)

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    nx = axis[0]
    ny = axis[1]
    nz = axis[2]

    R = np.array([
        [(1 - cos_theta)*nx*nx + cos_theta,     (1 - cos_theta)*nx*ny - sin_theta*nz,  (1 - cos_theta)*nx*nz + sin_theta*ny],
        [(1 - cos_theta)*nx*ny + sin_theta*nz,  (1 - cos_theta)*ny*ny + cos_theta,     (1 - cos_theta)*ny*nz - sin_theta*nx],
        [(1 - cos_theta)*nx*nz - sin_theta*ny,  (1 - cos_theta)*ny*nz + sin_theta*nx,  (1 - cos_theta)*nz*nz + cos_theta   ]
    ])

    return R 
import numpy as np
import math 
from pyray import Vector3


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
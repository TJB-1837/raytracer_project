import math

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
    return (a[0]/l, a[1]/l, a[2]/l)
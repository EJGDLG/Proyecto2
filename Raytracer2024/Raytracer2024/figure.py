from intercep import Intercep
from math import sin, cos, tan, asin, acos, atan, atan2, pi, sqrt, isclose

from MathLib import *

def vector_subtract(v1, v2):
    return [v1[i] - v2[i] for i in range(len(v1))]

def vector_add(v1, v2):
    return [v1[i] + v2[i] for i in range(len(v1))]

def vector_multiply(v, scalar):
    return [v[i] * scalar for i in range(len(v))]

def vector_dot(v1, v2):
    return sum(v1[i] * v2[i] for i in range(len(v1)))

def vector_norm(v):
    return sqrt(sum(v[i] ** 2 for i in range(len(v))))

def normalize(v):
    norm = vector_norm(v)
    return [v[i] / norm for i in range(len(v))]

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"
    
    def ray_intersect(self, orig, dir):
        return None
    

class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"
        
    def ray_intersect(self, orig, dir):
        L = vector_subtract(self.position, orig)
        tca = vector_dot(L, dir)
        d = sqrt(vector_dot(L, L) - tca ** 2)
        
        if d > self.radius:
            return None
        
        thc = sqrt(self.radius ** 2 - d ** 2)
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        P = vector_add(orig, vector_multiply(dir, t0))
        normal = vector_subtract(P, self.position)
        normal = normalize(normal)

        u = (atan2(normal[2], normal[0])) / (2 * pi) + 0.5
        v = acos(-normal[1]) / pi

        return Intercep(point=P, normal=normal, distance=t0, texCoords=[u, v], rayDirection=dir, obj=self)

class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = normalize(normal)
        self.type = "Plane"

    def ray_intersect(self, orig, dir):
        denom = vector_dot(dir, self.normal)
        if isclose(denom, 0):
            return None
        num = vector_dot(vector_subtract(self.position, orig), self.normal)
        t = num / denom

        if t < 0:
            return None

        P = vector_add(orig, vector_multiply(dir, t))
        return Intercep(point=P, normal=self.normal, distance=t, texCoords=None, rayDirection=dir, obj=self)

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"

    def ray_intersect(self, orig, dir):
        plane_intercept = super().ray_intersect(orig, dir)
        if plane_intercept is None:
            return None

        contact = vector_subtract(plane_intercept.point, self.position)
        contact_length = vector_norm(contact)

        # Verificar si el punto de contacto está dentro del radio del disco
        if contact_length > self.radius:
            return None

        # Cálculo de coordenadas de textura (u, v) en el disco
        u = (contact[0] / self.radius) * 0.5 + 0.5  # Centro en 0.5
        v = (contact[1] / self.radius) * 0.5 + 0.5  # Centro en 0.5

        # Limitar las coordenadas UV para que estén en el rango [0, 1]
        u = min(0.999, max(0, u))
        v = min(0.999, max(0, v))

        # Agregar las coordenadas de textura a la intersección
        return Intercep(
            point=plane_intercept.point,
            normal=plane_intercept.normal,
            distance=plane_intercept.distance,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )



class SquarePlane(Plane):
    def __init__(self, position, normal, size, material):
        super().__init__(position, normal, material)
        self.size = size
        self.type = "SquarePlane"

    def ray_intersect(self, orig, dir):
        plane_intercept = super().ray_intersect(orig, dir)
        if plane_intercept is None:
            return None

        contact = vector_subtract(plane_intercept.point, self.position)
        if abs(contact[0]) > self.size / 2 or abs(contact[1]) > self.size / 2:
            return None

        return plane_intercept

class AABB(Shape):
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"
        self.planes = []

        right_plane = Plane([position[0] + sizes[0] / 2, position[1], position[2]], [1, 0, 0], material)
        left_plane = Plane([position[0] - sizes[0] / 2, position[1], position[2]], [-1, 0, 0], material)
        up_plane = Plane([position[0], position[1] + sizes[1] / 2, position[2]], [0, 1, 0], material)
        down_plane = Plane([position[0], position[1] - sizes[1] / 2, position[2]], [0, -1, 0], material)
        front_plane = Plane([position[0], position[1], position[2] + sizes[2] / 2], [0, 0, 1], material)
        back_plane = Plane([position[0], position[1], position[2] - sizes[2] / 2], [0, 0, -1], material)

        self.planes.extend([right_plane, left_plane, up_plane, down_plane, front_plane, back_plane])

        epsilon = 0.001
        self.bounds_min = [position[i] - (epsilon + sizes[i] / 2) for i in range(3)]
        self.bounds_max = [position[i] + (epsilon + sizes[i] / 2) for i in range(3)]

    def ray_intersect(self, orig, dir):
        intercept = None
        t = float("inf")

        for plane in self.planes:
            plane_intercept = plane.ray_intersect(orig, dir)
            if plane_intercept is not None:
                plane_point = plane_intercept.point
                if all(self.bounds_min[i] <= plane_point[i] <= self.bounds_max[i] for i in range(3)):
                    if plane_intercept.distance < t:
                        t = plane_intercept.distance
                        intercept = plane_intercept

        if intercept is None:
            return None

        u, v = 0, 0
        if abs(intercept.normal[0]) > 0:
            u = (intercept.point[1] - self.bounds_min[1]) / self.sizes[1]
            v = (intercept.point[2] - self.bounds_min[2]) / self.sizes[2]
        elif abs(intercept.normal[1]) > 0:
            u = (intercept.point[0] - self.bounds_min[0]) / self.sizes[0]
            v = (intercept.point[2] - self.bounds_min[2]) / self.sizes[2]
        elif abs(intercept.normal[2]) > 0:
            u = (intercept.point[0] - self.bounds_min[0]) / self.sizes[0]
            v = (intercept.point[1] - self.bounds_min[1]) / self.sizes[1]

        u = min(0.999, max(0, u))
        v = min(0.999, max(0, v))

        return Intercep(point=intercept.point, normal=intercept.normal, distance=t, texCoords=[u, v], rayDirection=dir, obj=self)

class Triangle(Shape):
    def __init__(self, A, B, C, material):
        super().__init__(None, material)
        self.A = A
        self.B = B
        self.C = C
        self.type = "Triangle"

    def ray_intersect(self, orig, dir):
        # Normal del triángulo
        edge1 = subtract(self.B, self.A)
        edge2 = subtract(self.C, self.A)
        h = vector_cross(dir, edge2)
        a = dot(edge1, h)
        
        if isclose(a, 0):
            return None

        f = 1.0 / a
        s = subtract(orig, self.A)
        u = f * dot(s, h)
        
        if u < 0.0 or u > 1.0:
            return None
        
        q = vector_cross(s, edge1)
        v = f * dot(dir, q)
        
        if v < 0.0 or u + v > 1.0:
            return None

        t = f * dot(edge2, q)
        
        if t > 0.001:  # Un pequeño margen para evitar intersecciones cercanas
            P = vector_add(orig, multiply(t, dir))
            normal = normalize(vector_cross(edge1, edge2))
            # Cálculo de las coordenadas de textura
            texCoords = [u, v]
            return Intercep(point=P, normal=normal, distance=t, texCoords=texCoords, rayDirection=dir, obj=self)
        
        return None

class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "Cylinder"

    def ray_intersect(self, orig, dir):
        # Ecuaciones para intersección con un cilindro infinito
        oc = subtract(orig, self.position)
        a = dir[0]**2 + dir[2]**2
        b = 2 * (oc[0] * dir[0] + oc[2] * dir[2])
        c = oc[0]**2 + oc[2]**2 - self.radius**2
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            return None

        t0 = (-b - sqrt(discriminant)) / (2 * a)
        t1 = (-b + sqrt(discriminant)) / (2 * a)

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        P = vector_add(orig, multiply(t0, dir))
        y = P[1] - self.position[1]

        if y < 0 or y > self.height:
            return None
        
        normal = [P[0] - self.position[0], 0, P[2] - self.position[2]]
        normal = normalize(normal)

        # Cálculo de las coordenadas de textura
        u = (atan2(normal[2], normal[0]) + pi) / (2 * pi)
        v = (y / self.height)

        return Intercep(point=P, normal=normal, distance=t0, texCoords=[u, v], rayDirection=dir, obj=self)


class Ellipsoid(Shape):
    def __init__(self, position, radii, material):
        super().__init__(position, material)
        self.radii = radii
        self.type = "Ellipsoid"

    def ray_intersect(self, orig, dir):
        # Vector desde el origen del rayo hacia el centro del elipsoide
        L = vector_subtract(orig, self.position)
        
        # Ajustar la dirección del rayo y el vector L
        dir = [dir[i] / (self.radii[i] ** 2) for i in range(3)]
        L = [L[i] / (self.radii[i] ** 2) for i in range(3)]
        
        # Coeficientes de la ecuación cuadrática
        a = vector_dot(dir, dir)
        b = 2 * vector_dot(L, dir)
        c = vector_dot(L, L) - 1
        
        # Cálculo del discriminante
        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return None  # No hay intersección
        
        # Calcular las soluciones de la ecuación cuadrática
        t0 = (-b - sqrt(discriminant)) / (2 * a)
        t1 = (-b + sqrt(discriminant)) / (2 * a)

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None  # Ambas intersecciones están detrás del origen del rayo
        
        # Punto de intersección
        P = vector_add(orig, vector_multiply(dir, t0))
        
        # Calcular la normal en el punto de intersección
        normal = vector_subtract(P, self.position)
        normal = normalize([normal[i] / (self.radii[i] ** 2) for i in range(3)])
        
        # Cálculo de las coordenadas de textura
        u = 0.5 + (atan2(normal[2], normal[0]) / (2 * pi))
        v = 0.5 - (asin(normal[1]) / pi)

        return Intercep(point=P, normal=normal, distance=t0, texCoords=[u, v], rayDirection=dir, obj=self)


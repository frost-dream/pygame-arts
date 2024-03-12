from PIL import Image
from math import tan, pi
class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    def cross_product(self, other):
        return Vector(self.y * other.z - self.z * other.y,self.z * other.x - self.x * other.z,self.x * other.y - self.y * other.x)
    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    def normalize(self):
        return self / self.dot_product(self) ** 0.5
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, other):
        return Vector(self.x * other, self.y * other, self.z * other)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other, self.z / other)
class ImageCanvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height))
        self.draw = self.image.load()
    def set_pixel(self, x, y, col):
        self.draw[x, y] = (int(col.x * 255), int(col.y * 255), int(col.z * 255))
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()
class RenderEngine:
    MAX_DEPTH = 5
    MIN_DISPLACE = 0.0001
    def render(self, scene):
        f = (scene.target - scene.camera).normalize()
        r = f.cross_product(scene.up).normalize()
        u = r.cross_product(f).normalize()
        angle = tan(pi * 0.5 * scene.fov / 180)
        canvas = ImageCanvas(scene.width, scene.height)
        for j in range(0, scene.height, 3):
            for i in range(0, scene.width, 3):
                canvas.set_pixel(i, j, self.ray_trace(Ray(scene.camera, (r * ((2 * (i + 0.5) / scene.width - 1) * angle * scene.width / scene.height) + u * ((1 - 2 * (j + 0.5) / scene.height) * angle) + f).normalize()), scene))
        return canvas.image
    def ray_trace(self, ray, scene, depth=0):
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_hit):
                dist_hit = dist
                obj_hit = obj
        if obj_hit is None:
            return Vector()
        hit_pos = ray.origin + ray.direction * dist_hit
        normal = obj_hit.normal(hit_pos)
        material = obj_hit.material
        color = Vector()
        color2 = material.ambient * Vector(1,1,1)
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos).direction
            color2 += (material.color* material.diffuse* max(normal.dot_product(to_light), 0)) + (light.color* material.specular* max(normal.dot_product((to_light + scene.camera - hit_pos).normalize()), 0) ** 50)
        if depth < self.MAX_DEPTH:
            return color + color2 + (self.ray_trace(Ray((hit_pos + normal * self.MIN_DISPLACE), (ray.direction - 2 * ray.direction.dot_product(normal) * normal)), scene, depth + 1) * obj_hit.material.reflection)
        return color + color2
class Light:
    def __init__(self, position, color=Vector(1,1,1)):
        self.position = position
        self.color = color
class Material:
    def __init__(self,color=Vector(1,1,1),ambient=0.05,diffuse=1.0,specular=1.0,reflection=0.5,):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    def intersects(self, ray):
        sphere_to_ray = ray.origin - self.center
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius
        discriminant = b * b - 4 * c
        if discriminant >= 0:
            dist = (-b - discriminant ** 0.5) / 2
            if dist > 0:
                return dist
    def normal(self, surface_point):
        return (surface_point - self.center).normalize()
class Scene:
    def __init__(self, camera, target, up, objects, lights, width, height, fov):
        self.camera = camera
        self.target = target
        self.up = up
        self.objects = objects
        self.lights = lights
        self.width = width
        self.height = height
        self.fov = fov
import pygame
from pygame.locals import *
from math import sin,cos,radians
pygame.init()
screen = pygame.display.set_mode((300,300))
mouse_down = False
xx = 0
yy = 0
from_x = 0
from_y = 0
from_z = 0
at_x = -1
at_y = 0
at_z = 1
while True:
    for event in pygame.event.get((MOUSEBUTTONUP,MOUSEBUTTONDOWN)):
        if event.type == MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            xcoor = pygame.mouse.get_pos()
    if mouse_down and (pygame.mouse.get_pos()[0] - xcoor[0] != 0 or pygame.mouse.get_pos()[1] - xcoor[1]):
        xx += pygame.mouse.get_pos()[0] - xcoor[0]
        yy += pygame.mouse.get_pos()[1] - xcoor[1]
        xcoor = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        from_x += sin(radians(xx)) * cos(radians(yy)) * .1
        from_y += sin(radians(yy)) * .1
        from_z += cos(radians(xx)) * cos(radians(yy)) * .1
    if keys[K_DOWN]:
        from_x -= sin(radians(xx)) * cos(radians(yy)) * .1
        from_y -= sin(radians(yy)) * .1
        from_z -= cos(radians(xx)) * cos(radians(yy)) * .1
    if keys[K_LEFT]:
        from_x += sin(radians(xx) - pi / 2) * .1
        from_z += cos(radians(xx) - pi / 2) * .1
    if keys[K_RIGHT]:
        from_x -= sin(radians(xx) - pi / 2) * .1
        from_z -= cos(radians(xx) - pi / 2) * .1
    at_x = from_x + sin(radians(xx)) * cos(radians(yy))
    at_y = from_y + sin(radians(yy))
    at_z = from_z + cos(radians(xx)) * cos(radians(yy))
    img = RenderEngine().render(Scene(Vector(from_x, from_y, from_z),Vector(at_x, at_y, at_z),Vector(0, -1, 0), [Sphere(Vector(0, 10000.5, 1),10000.0,Material(Vector(.1,1,1))),Sphere(Vector(0.75, -0.1, 1), 0.6, Material(Vector(0,0,1))),Sphere(Vector(-0.75, -0.1, 2.25), 0.6, Material(Vector(.5,.2,.5)))], [Light(Vector(1.5, -0.5, -10), Vector(1,1,1)),Light(Vector(-0.5, -10.5, 0), Vector(.9,.9,.9))], 300, 300, 90))
    screen.blit(pygame.image.fromstring(img.tobytes(), img.size, img.mode), (0, 0))
    pygame.display.flip()
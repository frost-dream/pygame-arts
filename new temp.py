# note that only this code is required pillow and numpy (will be only pygame soon)
import pygame
from PIL import Image
import numpy
pygame.init()
width, height = 500, 300
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, v):
        return vec3(self.x + v.x, self.y + v.y, self.z + v.z)
    def __sub__(self, v):
        return vec3(self.x - v.x, self.y - v.y, self.z - v.z)
    def __mul__(self, v):
        if isinstance(v, vec3):
            return vec3(self.x * v.x , self.y *  v.y , self.z * v.z )
        return vec3(self.x * v, self.y * v, self.z * v)
    def __rtruediv__(self, v):
        return vec3(v / self.x, v / self.y, v / self.z)
    def matmul(self, matrix):
        return vec3(*numpy.tensordot(matrix,numpy.array([self.x , self.y , self.z]) , axes=([1,0])))
    def dot(self, v):
        return self.x*v.x + self.y*v.y + self.z*v.z
    def cross(self, v):
        return vec3(self.y*v.z - self.z*v.y, -self.x*v.z + self.z*v.x,  self.x*v.y - self.y*v.x)
    def normalize(self):
        mag = numpy.sqrt(self.dot(self))
        return self * (1.0 / numpy.where(mag == 0, 1, mag))
    def __eq__(self, other):
        return (self.x == other.x)  &  (self.y == other.y) & (self.z == other.z)
class SkyBox_Material:
    def __init__(self, cubemap):
        img_array = numpy.asarray(Image.open(cubemap))/256.
        self.texture = numpy.where( img_array <= 0.03928,  img_array / 12.92,  numpy.power((img_array + 0.055) / 1.055,  2.4))
        self.repeat = 1.0
        self.center = vec3(0.,0.,0.)
        self.width = 2*SKYBOX_DISTANCE
        self.height = 2*SKYBOX_DISTANCE
        self.length = 2*SKYBOX_DISTANCE
        self.lb_local_basis = self.center - vec3(self.width / 2, self.height / 2, self.length / 2)
        self.rt_local_basis = self.center + vec3(self.width / 2, self.height / 2, self.length / 2)
        self.ax_w = vec3(1., 0., 0.)
        self.ax_h = vec3(0., 1., 0.)
        self.ax_l = vec3(0., 0., 1.)
        self.inverse_basis_matrix = numpy.array([[self.ax_w.x, self.ax_h.x, self.ax_l.x],[self.ax_w.y, self.ax_h.y, self.ax_l.y],[self.ax_w.z, self.ax_h.z, self.ax_l.z]])
        self.basis_matrix = self.inverse_basis_matrix.T
UPDOWN = -1
UPWARDS = 1
FARAWAY = 1e+39
SKYBOX_DISTANCE = 10
angle = -0.47123889803846897
camera = [vec3(2.5 * numpy.sin(angle), 0.25, 2.5 * numpy.cos(angle) - 1.5),vec3(0., 0.25, -3.),width,height,90.,0.,1.]
skybox = SkyBox_Material(cubemap = r'c:\Users\lenovo\Downloads\Compressed\Python-Raytracer-master\sightpy\backgrounds\lake.png')
running = True
mouse_down = False
xx = yy = xcoor = ycoor = 0
camera_width = numpy.tan(camera[4] * numpy.pi / 180 / 2.) * 2.
camera_height = camera_width / (camera[2] / camera[3])
xxxx = numpy.linspace(-camera_width / 2., camera_width / 2., camera[2])
yyyy = numpy.linspace(camera_height / 2., -camera_height / 2., camera[3])
xxx, yyy = numpy.meshgrid(xxxx, yyyy)
xxxx = xxx.flatten()
yyyy = yyy.flatten()
x = xxxx + (numpy.random.rand(len(xxxx)) - 0.5) * camera_width / (camera[2])
y = yyyy + (numpy.random.rand(len(yyyy)) - 0.5) * camera_height / (camera[3])
def cfov():
    camera[1].x = camera[0].x + numpy.sin(numpy.radians(xx)) * numpy.cos(numpy.radians(yy))
    camera[1].y = camera[0].y + numpy.sin(numpy.radians(yy))
    camera[1].z = camera[0].z + numpy.cos(numpy.radians(xx)) * numpy.cos(numpy.radians(yy))
while running:
    for event in pygame.event.get((pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN,pygame.QUIT)):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            xcoor = pygame.mouse.get_pos()
        else:
            running = False
    if mouse_down and (pygame.mouse.get_pos()[0] - xcoor[0] != 0 or pygame.mouse.get_pos()[1] - xcoor[1]):
        xx += (pygame.mouse.get_pos()[0] - xcoor[0]) * .1
        yy += (pygame.mouse.get_pos()[1] - xcoor[1]) * .1
        xcoor = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        camera[0].x += numpy.sin(numpy.radians(xx)) * numpy.cos(numpy.radians(yy)) * .3
        camera[0].y += numpy.sin(numpy.radians(yy)) * .3
        camera[0].z += numpy.cos(numpy.radians(xx)) * numpy.cos(numpy.radians(yy)) * .3
    if keys[pygame.K_DOWN]:
        camera[0].x -= numpy.sin(numpy.radians(xx)) * numpy.cos(numpy.radians(yy)) * .3
        camera[0].y -= numpy.sin(numpy.radians(yy)) * .3
        camera[0].z -= numpy.cos(numpy.radians(xx)) * numpy.cos(numpy.radians(yy)) * .3
    if keys[pygame.K_LEFT]:
        camera[0].x += numpy.sin(numpy.radians(xx) - pi / 2) * .3
        camera[0].z += numpy.cos(numpy.radians(xx) - pi / 2) * .3
    if keys[pygame.K_RIGHT]:
        camera[0].x -= numpy.sin(numpy.radians(xx) - pi / 2) * .3
        camera[0].z -= numpy.cos(numpy.radians(xx) - pi / 2) * .3
    cfov()
    cameraFwd = (camera[1] - camera[0]).normalize()
    cameraRight = (cameraFwd.cross(vec3(0., 1., 0.))).normalize()
    cameraUp = cameraRight.cross(cameraFwd)
    ray_origin = camera[0] + cameraRight * x * .1 + cameraUp * y * .1
    dir = (camera[0] + cameraUp * y * camera[6] +cameraRight * x * camera[6] +cameraFwd * camera[6] - ray_origin).normalize()
    O_local_basis = ray_origin.matmul(skybox.basis_matrix)
    D_local_basis = dir.matmul(skybox.basis_matrix)
    dirfrac = 1.0 / D_local_basis
    t1 = (skybox.lb_local_basis.x - O_local_basis.x) * dirfrac.x
    t2 = (skybox.rt_local_basis.x - O_local_basis.x) * dirfrac.x
    t3 = (skybox.lb_local_basis.y - O_local_basis.y) * dirfrac.y
    t4 = (skybox.rt_local_basis.y - O_local_basis.y) * dirfrac.y
    t5 = (skybox.lb_local_basis.z - O_local_basis.z) * dirfrac.z
    t6 = (skybox.rt_local_basis.z - O_local_basis.z) * dirfrac.z
    tmin = numpy.maximum(numpy.maximum(numpy.minimum(t1, t2), numpy.minimum(t3, t4)), numpy.minimum(t5, t6))
    tmax = numpy.minimum(numpy.minimum(numpy.maximum(t1, t2), numpy.maximum(t3, t4)), numpy.maximum(t5, t6))
    distances = [numpy.select([(tmax < 0) | (tmin > tmax), tmin < 0, True], [FARAWAY, [tmax, numpy.tile(UPDOWN, tmin.shape)],[tmin, numpy.tile(UPWARDS, tmin.shape)]])[0]]
    nearest = numpy.minimum.reduce(distances)
    hit_check = (nearest != FARAWAY) & (distances == nearest)
    point = ray_origin + dir * numpy.extract(hit_check, distances)
    P = (point - skybox.center).matmul(skybox.basis_matrix)
    absP = vec3(1. / skybox.width, 1. / skybox.height, 1. / skybox.length) * vec3(numpy.abs(P.x),numpy.abs(P.y),numpy.abs(P.z))
    Pmax = numpy.maximum(numpy.maximum(absP.x, absP.y), absP.z)
    P.x = numpy.where(Pmax == absP.x, numpy.sign(P.x), 0.)
    P.y = numpy.where(Pmax == absP.y, numpy.sign(P.y), 0.)
    P.z = numpy.where(Pmax == absP.z, numpy.sign(P.z), 0.)
    N = P.matmul(skybox.inverse_basis_matrix)
    M_C = point - skybox.center
    BOTTOM = N == vec3(0., -1., 0.)
    TOP = N == vec3(0., 1., 0.)
    RIGHT = N == vec3(1., 0., 0.)
    LEFT = N == vec3(-1., 0., 0.)
    FRONT = N == vec3(0., 0., 1.)
    BACK = N == vec3(0., 0., -1.)
    u = numpy.select([BOTTOM, TOP, RIGHT, LEFT, FRONT, BACK],[((skybox.ax_w.dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 1),((skybox.ax_w.dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 1),((skybox.ax_l.dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 2),(((skybox.ax_l * -1).dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 0),(((skybox.ax_w * -1).dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 3),((skybox.ax_w.dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 1)])
    v = numpy.select([BOTTOM, TOP, RIGHT, LEFT, FRONT, BACK],[(((skybox.ax_l * -1).dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 0),((skybox.ax_l.dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 2),((skybox.ax_h.dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 1),(((skybox.ax_h).dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 1),(((skybox.ax_h).dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 1),((skybox.ax_h.dot(M_C) / skybox.width * 2 * 0.985 + 1) / 2 + 1)])
    color_RGBlinear = vec3(*skybox.texture[-((v/3 * skybox.texture.shape[0]*skybox.repeat ).astype(int)% skybox.texture.shape[0]) , (u/4   * skybox.texture.shape[1]*skybox.repeat).astype(int) % skybox.texture.shape[1]].T)
    r = vec3(numpy.zeros(hit_check.shape), numpy.zeros(hit_check.shape), numpy.zeros(hit_check.shape))
    numpy.place(r.x, hit_check, color_RGBlinear.x)
    numpy.place(r.y, hit_check, color_RGBlinear.y)
    numpy.place(r.z, hit_check, color_RGBlinear.z)
    rgb_linear = numpy.array([r.x , r.y , r.z])
    rgb = numpy.where( rgb_linear <= 0.00304,  12.92 * rgb_linear,  1.055 * numpy.power(rgb_linear, 1.0/2.4) - 0.055)
    rgb_max =  numpy.amax(rgb, axis=0)
    screen.blit(pygame.image.fromstring(Image.merge("RGB", [Image.fromarray((255 * numpy.clip(c, 0, 1).reshape((camera[2], camera[3]))).astype(numpy.uint8), "L") for c in numpy.where(rgb_max > 1, rgb * 1 / (rgb_max), rgb)]).tobytes(), (width, height), 'RGB'), (0, 0))
    pygame.display.flip()
    clock.tick(100)
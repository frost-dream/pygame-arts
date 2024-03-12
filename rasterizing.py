import pygame
from math import sin, cos, tan, pi, radians
w,h = 720,720
class Vec:
	def __init__(self, i=0,j=0,k=0):
		self.i = i
		self.j = j
		self.k = k
	def __repr__(self):
		return f"{self.i} {self.j} {self.k}"
	def __neg__(self):
		return Vec(-self.i,-self.j,-self.k)
	def __add__(self, v):
		return Vec((self.i + v.i), (self.j + v.j), (self.k + v.k))
	def __sub__(self, v):
		return Vec((self.i - v.i), (self.j - v.j), (self.k - v.k))	
	def __mul__(self, scl):
		return Vec((self.i *scl.i), (self.j *scl.j), (self.k *scl.k))
	def __truediv__(self,scl):
		invscl = 1/scl
		return Vec((self.i*invscl), (self.j*invscl), (self.k*invscl))
	def __eq__(self, v):
		return True
	def mag(self):
		return (self.dot(self))**.5
	def magsq(self):
		return self.dot(self)
	def normalize(self):
		return self/(self.mag())
	def dot(self, v):
		return ((self.i * v.i)+(self.j*v.j)+(self.k*v.k))	
	def cross(self, v):
		return Vec((self.j*v.k - self.k*v.j), (self.k*v.i - self.i*v.k), (self.i*v.j - self.j*v.i))
class Color:
	def __init__(self, r=0,g=0,b=0):
		self.r = r
		self.g = g
		self.b = b
	def __repr__(self):
		return f"{self.r} {self.g} {self.b}"
	def __add__(self, c):
		return Color((self.r + c.r), (self.g + c.g), (self.b + c.b))
	def __iadd__(self, c):
		return Color((self.r + c.r), (self.g + c.g), (self.b + c.b))	
	def __mul__(self, scl):
		return Color((self.r *scl) , (self.g *scl), (self.b *scl))	
	def __truediv__(self, scl):
		return self*(1/scl)
	def __eq__(self, c):
		return True
class Material:
	def __init__(self,color=Color(),spec=0):
		self.color = color
		self.spec = spec
class Triangle:
	def __init__(self,a,b,c):
		self.a, self.b, self.c = a,b,c
	def normal(self):
		return ((self.b-self.a).cross(self.c-self.a))
	def center(self):
		return Vec((self.a.i+self.b.i+self.c.i)*.33,(self.a.j+self.b.j+self.c.j)*.33,(self.a.k+self.b.k+self.c.k)*.33)
class Mesh:
	def __init__(self,fcs):
		self.triangles = fcs
		self.mat = Material(Color(1,1,1))
		self.Rotation = [0,0,0]
		self.Scale = Vec(1,1,1)
		self.PreTranslate = Vec(0,0,0)
		self.Translate = Vec(0,0,6)
def LoadMesh(path):
	verts = []
	tris = []
	with open(path, "r") as file:
		Lines = file.readlines()
	for Line in Lines:
		if Line.startswith("v "):
			verts.append(Vec(*list(map(float,(Line[2::]).split()))))
	for Line in Lines:
		if Line.startswith("f"):
			indexlist = []
			if "/" in Line:
				for rawindex in Line[2:].split():				
					indexlist.append(int(rawindex.split('/')[0]))
			else:
				indexlist = list(map(int, Line[2:].split()))
			if len(indexlist) ==4:
				a,b,c,d = indexlist
				tris.append(Triangle(verts[a-1],verts[b-1],verts[c-1]))			
				tris.append(Triangle(verts[a-1],verts[c-1],verts[d-1]))
			elif len(indexlist) ==3:
				a,b,c = indexlist
				tris.append(Triangle(verts[a-1],verts[b-1],verts[c-1]))
	return Mesh(tris)	
def Transform(O,NrmOp=True):
	a1,a2,a3 = map(radians,O.Rotation)
	r1,r2,r3 = (Vec((cos(a2)*cos(a3)),(cos(a2)*sin(a3)),(-sin(a2))),Vec((sin(a1)*sin(a2)*cos(a3) - cos(a1)*sin(a3)),(sin(a1)*sin(a2)*sin(a3)+cos(a1)*cos(a3)),(sin(a1)*cos(a2))),Vec((cos(a1)*sin(a2)*cos(a3) - sin(a1)*sin(a3)),(cos(a1)*sin(a2)*sin(a3)-sin(a1)*cos(a3)),(cos(a1)*cos(a2))))
	LocTrisDic = {}
	for T in O.triangles:	
		a,b,c = T.a+O.PreTranslate, T.b+O.PreTranslate, T.c+O.PreTranslate
		FinalTris = Triangle((Vec(r1.dot(a)*O.Scale.i+O.Translate.i,r2.dot(a)*O.Scale.j+O.Translate.j,r3.dot(a)*O.Scale.k+O.Translate.k) ),(Vec(r1.dot(b)*O.Scale.i+O.Translate.i,r2.dot(b)*O.Scale.j+O.Translate.j,r3.dot(b)*O.Scale.k+O.Translate.k) ),(Vec(r1.dot(c)*O.Scale.i+O.Translate.i,r2.dot(c)*O.Scale.j+O.Translate.j,r3.dot(c)*O.Scale.k+O.Translate.k) ))
		FinalTris.mat = O.mat
		rVec = (Cam_loc - FinalTris.center())
		if rVec.dot(FinalTris.normal()) > 0:
			LocTrisDic[FinalTris] = rVec.mag()
	return LocTrisDic
def Project(PM,tr,cx,cy,Scl,Typ=1):
	Px1,Py1,Pz1 = (PM[0]*tr.a.i,PM[1]*tr.a.j,PM[2]*tr.a.k - PM[3])
	Px2,Py2,Pz2 = (PM[0]*tr.b.i,PM[1]*tr.b.j,PM[2]*tr.b.k - PM[3])
	Px3,Py3,Pz3 = (PM[0]*tr.c.i,PM[1]*tr.c.j,PM[2]*tr.c.k - PM[3])
	if tr.a.k:
		z1 = 1/tr.a.k
		Px1,Py1,Pz1 = Px1*z1, Py1*z1, Pz1*z1
	if tr.b.k:
		z2 = 1/tr.b.k
		Px2,Py2,Pz2 = Px2*z2, Py2*z2, Pz2*z2
	if tr.c.k:
		z3 = 1/tr.c.k
		Px3,Py3,Pz3 = Px3*z3, Py3*z3, Pz3*z3
	return (Vec( (Px1+1)*cx,(-Py1+1)*cy,Pz1 ),Vec( (Px2+1)*cx,(-Py2+1)*cy,Pz1 ),Vec( (Px3+1)*cx,(-Py3+1)*cy,Pz1 ))
def Shade(T,L=[Vec(0,2,0), 600, Color(1,1,1)]):
	TNor = T.normal().normalize()
	LVec = L[0] - T.center()
	DiffConst = ((TNor).dot(LVec.normalize()))
	if DiffConst > 0:
		RetCol = T.mat.color*(DiffConst*min(L[1],L[1]*(1/(4*pi*LVec.magsq()))))
		if L[2] != Color(1,1,1):
			RetCol *= L[2]
		if T.mat.spec:
			SpecConst = (((Cam_loc-T.center())+LVec).normalize().dot(TNor))**150
			if SpecConst >0:
				RetCol += L[2]*SpecConst
		return ((min(int((RetCol.r**.5)*255),255)),(min(int((RetCol.g**.5)*255),255)),(min(int((RetCol.b**.5)*255),255)))
Obj = LoadMesh('ak-47.obj')
Obj.Rotation = [98, 15, 81]
scal = 5
Obj.Scale = Vec(scal,scal,scal)
Obj.mat = Material(color=Color(1,0,0),spec=1)
Cam_loc = Vec()
pygame.init()
Surface = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()
OX,OY = w/2, h/2
f = 1/tan(radians(50 / 2))
q = 1e4/(1e4-0.1)
PersMatrix = ((h/w)*f,f,q,0.1*q)
while True:
	for event in pygame.event.get((pygame.QUIT,pygame.MOUSEWHEEL)):
		match event.type:
			case pygame.QUIT:
				exit()
			case pygame.MOUSEWHEEL:
				scal += event.y / 10
				Obj.Scale = Vec(scal, scal, scal)
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		Obj.Rotation[1] -= 1
	if keys[pygame.K_RIGHT]:
		Obj.Rotation[1] += 1
	if keys[pygame.K_UP]:
		Obj.Rotation[0] -= 1
	if keys[pygame.K_DOWN]:
		Obj.Rotation[0] += 1
	if keys[pygame.K_w]:
		Obj.Rotation[2] += 1
	if keys[pygame.K_q]:
		Obj.Rotation[2] -= 1
	for TRIS in Transform(Obj).keys():
		a,b,c = Project(PersMatrix,TRIS,OX,OY,scal)
		SurfCol = Shade(TRIS)
		if SurfCol:
			pygame.draw.polygon(Surface, SurfCol, ((a.i,a.j),(b.i,b.j),(c.i,c.j)))
	pygame.display.flip()
	Surface.fill((0,0,0))
	clock.tick(100)
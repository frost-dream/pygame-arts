import numpy as np
class AABB():
  def __init__(self, botleft, topright):
    self.botleft = botleft
    self.topright = topright
class BVHNode():
  def __init__(self, aabb, triangles, vernormals, triindices, child1, child2):
    self.aabb = aabb
    self.triangles = triangles
    self.vernormals = vernormals
    self.triindices = triindices
    self.child1 = child1
    self.child2 = child2
def buildBVH(triangles, vernormals, triindices):
  if(triangles.shape[0] <= 64):
    return BVHNode(AABB(triangles.min(axis=1).min(axis=0), triangles.max(axis=1).max(axis=0)), triangles, vernormals, triindices, None, None)
  else:
    minaxis = -1
    minsplit = -1      
    centroids = np.mean(triangles, axis=1)
    for axis in range(3):
      sortedtris = triangles[np.argsort(centroids[:, axis])]
      leftaabb = AABB(np.ones((3,), dtype=np.float32) * np.inf,np.ones((3,), dtype=np.float32) * -np.inf)
      leftcost = np.zeros((len(sortedtris),), dtype=np.float32)
      for i, tri in enumerate(sortedtris):
        leftaabb.botleft = np.minimum(leftaabb.botleft, tri.min(axis=0))
        leftaabb.topright = np.maximum(leftaabb.topright, tri.max(axis=0))
        diag = np.abs(leftaabb.topright - leftaabb.botleft)
        left_index = i
        leftcost[left_index] = (diag[0] * diag[1] + diag[1] * diag[2] + diag[2] * diag[0]) * i
      rightaabb = AABB(np.ones((3,), dtype=np.float32) * np.inf,np.ones((3,), dtype=np.float32) * -np.inf)
      rightcost = np.zeros((len(sortedtris),), dtype=np.float32)
      for i, tri in enumerate(sortedtris[::-1]):
        rightaabb.botleft = np.minimum(rightaabb.botleft, tri.min(axis=0))
        rightaabb.topright = np.maximum(rightaabb.topright, tri.max(axis=0))
        diag = np.abs(rightaabb.topright - rightaabb.botleft)
        right_index = len(sortedtris) - 1 - i
        rightcost[right_index] = (diag[0] * diag[1] + diag[1] * diag[2] + diag[2] * diag[0]) * i 
      if((leftcost + rightcost).min() < np.inf):
        mincost = (leftcost + rightcost).min()
        minaxis = axis
        minsplit = np.argmin(leftcost + rightcost)
    sortedindices = np.argsort(centroids[:, minaxis])
    sortedtriindices = triindices[sortedindices]
    sortedtris = triangles[sortedindices]
    sortedvern = vernormals[sortedindices]
    node1 = buildBVH(sortedtris[:minsplit], sortedvern[:minsplit], sortedtriindices[:minsplit])
    node2 = buildBVH(sortedtris[minsplit:], sortedvern[minsplit:], sortedtriindices[minsplit:])
    return BVHNode(AABB(triangles.min(axis=1).min(axis=0), triangles.max(axis=1).max(axis=0)),np.zeros((0, 3, 3), dtype=np.float32),np.zeros((0, 3, 3), dtype=np.float32),np.zeros((0,), dtype=np.int32), node1, node2)
class SerialBVHNode():
  def __init__(self, aabb, tristart, ntris):
    self.aabb = aabb
    self.tristart = tristart
    self.ntris = ntris
    self.child1 = -1
    self.child2 = -1
def create_box(nodelist):
  botleft = nodelist.aabb.botleft
  topright = nodelist.aabb.topright
  vertex = np.zeros((8, 3), dtype=np.float32)
  vertex[0] = botleft
  vertex[1] = [botleft[0], topright[1], botleft[2]]
  vertex[2] = [topright[0], topright[1], botleft[2]]
  vertex[3] = [topright[0], botleft[1], botleft[2]]
  vertex[4] = [botleft[0], botleft[1], topright[2]]
  vertex[5] = [botleft[0], topright[1], topright[2]]
  vertex[6] = topright
  vertex[7] = [topright[0], botleft[1], topright[2]]
  return vertex, np.array([[0, 4, 1],[1, 4, 5],[4, 7, 5],[5, 7, 6],[3, 7, 6],[2, 3, 6],[0, 2, 3],[0 ,1, 2],[1, 6, 2],[1, 5, 6],[0, 7, 4],[0, 3, 7]])
vertices = []
triangles = []
normals = []
with open('bunny.obj', 'r') as f:
  for line in f:
    if line[0] == '#':
      continue
    pieces = line.split(' ')
    if pieces[0] == 'v':
      vertices.append([float(x) for x in pieces[1:4]])      
    elif pieces[0] == 'f':
      if pieces[1] == '':
          triangles.append([int(x.split('/')[0]) - 1 for x in pieces[2:]])
      else: 
          triangles.append([int(x.split('/')[0]) - 1 for x in pieces[1:]])
    elif pieces[0] == 'vn':
      normals.append([float(x) for x in pieces[1:]])
vertices, triangles = (np.array(vertices, dtype=np.float32),np.array(triangles, dtype=np.int32))
eps = 1e-10
vn = np.zeros(vertices.shape, dtype=np.float32)
v = [vertices[triangles[:, 0], :],vertices[triangles[:, 1], :],vertices[triangles[:, 2], :]]
for i in range(3):
  v0 = v[i]
  v1 = v[(i + 1) % 3]
  v2 = v[(i + 2) % 3]
  e1 = v1 - v0
  e2 = v2 - v0
  e1_len = np.linalg.norm(e1, axis=-1)
  e2_len = np.linalg.norm(e2, axis=-1)
  side_a = e1 / (np.reshape(e1_len, (-1, 1)) + eps)
  side_b = e2 / (np.reshape(e2_len, (-1, 1)) + eps)
  if(i == 0):
    fn = np.cross(side_a, side_b)
    fn = fn / (np.reshape(np.linalg.norm(fn, axis=-1), (-1, 1)) + eps)
  angle = np.where(np.sum(side_a *side_b, axis=-1) < 0,np.pi - 2.0 * np.arcsin(np.around(0.5 * np.linalg.norm(side_a + side_b, axis=-1))),2.0 * np.arcsin(np.around(0.5 * np.linalg.norm(side_b - side_a, axis=-1))))
  sin_angle = np.sin(angle)
  contrib = fn * np.reshape(sin_angle / ((e1_len * e2_len) + eps), (-1, 1))
  index = triangles[:, i]
  for i in range(index.shape[0]):
    vn[index[i], :] += contrib[i, :]
queue = []
nodelist = []  
queue.append(buildBVH(np.copy(vertices[triangles.ravel()]).reshape((-1, 3, 3)), np.copy((vn / (np.reshape(np.linalg.norm(vn, axis=-1), (-1, 1)) + eps))[triangles.ravel()]).reshape((-1, 3, 3)), np.array(range(triangles.shape[0]))))  
while(len(queue) > 0):
  front = queue.pop(-1)
  nodelist.append(front)    
  if(front.child1 is not None):
    queue.append(front.child1)
  if(front.child2 is not None):
    queue.append(front.child2)  
for node in nodelist:
  node.parent = None  
serialnodelist = []
serialtrilist = np.zeros((0, 3, 3), dtype=np.float32)
for i, node in enumerate(nodelist):
  serialnodelist.append(SerialBVHNode(node.aabb,serialtrilist.shape[0],node.triangles.shape[0]))      
  if(node.child1 is not None):
    node.child1.parent = serialnodelist[-1]
  if(node.child2 is not None):
    node.child2.parent = serialnodelist[-1]
  serialtrilist = np.vstack((serialtrilist, node.triangles))
for i, node, snode in zip(range(len(nodelist)), nodelist, serialnodelist):
  if(node.parent is not None):
    if(node.parent.child1 == -1):
      node.parent.child1 = i
      continue
    if(node.parent.child2 == -1):
      node.parent.child2 = i
      continue
bvhnodelist, bvhtrilist = serialnodelist, serialtrilist
layer = 1
a = [0]
def return_child(node, a):
  new_list = []
  for i in a:
    child1 = node[i].child1
    child2 = node[i].child2
    if(child1 != -1):
      new_list.append(child1)
    if(child2 != -1):
      new_list.append(child2)
    if(child1 == -1 and child2 == -1):
      new_list.append(i)
  return (new_list,len(new_list))
prev = -1
a = return_child(bvhnodelist, a)
while a[1] != prev:
  prev = a[1]
  for i, index in enumerate(a[0]):
    temp_v, temp_f = create_box(bvhnodelist[index])
    if(i == 0):
      layer_v = temp_v
      layer_f = temp_f
    else:
      layer_v = np.vstack((layer_v, temp_v))
      layer_f = np.vstack((layer_f, temp_f+(8*i)))
  with open(f'layer_{layer}.obj', "w") as f:
    for i in range(layer_v.shape[0]):
      f.write("v {} {} {}\n".format(layer_v[i, 0], layer_v[i, 1], layer_v[i, 2]))
    for i in range(layer_f.shape[0]):
      f.write("f {} {} {}\n".format(layer_f[i, 0] + 1, layer_f[i, 1] + 1, layer_f[i, 2] + 1))
  layer += 1
  a = return_child(bvhnodelist, a[0])
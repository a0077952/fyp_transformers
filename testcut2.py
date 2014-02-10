import maya.cmds as mc
import maya.mel as mm
import random 

mc.select(all=True)
mc.delete()

cube1 = mc.polyCube(sx=1, sy=1, sz=1, h=3, w=3, d=3)
#cube1 = mc.polySphere(r=5, sx=20, sy=20, ax=[0,1,0])
#cube1 = mc.polyCylinder(r=3, h=5, sx=20, sy=1, ax=[0,1,0])
#cube1 = mc.polyCone(r=1, h=2, ax=[0,1,0])
#cube1 = mc.polyPyramid()
mesh = cube1[0]
# part0 = [2, 2, 3, 1, 2]
# part1 = [1, 2, 3, 0]
# part2 = [1, 2, 3, 0]
# part3 = [1, 1, 3, 0]

part0 = [-1, -1, -1.5, 1, 1, 1.5]
part1 = [-0.5, -1, -1.5, 0.5, 1, 1.5]
part2 = [-0.5, -1, -1.5, 0.5, 1, 1.5]
part3 = [-0.5, -0.5, -1.5, 0.5, 0.5, 1.5]

# part is defined by bbox and center
def cut_part(mesh, bbox, center):
	cutmesh = cmds.duplicate(mesh)
	#cutmesh = mesh
	minx, miny, minz, maxx, maxy, maxz = bbox
	cx, cy, cz = center
	cmds.select(cutmesh)
	cmds.polyCut(pc = (minx + cx, 0, 0), ro = (0, 90,0), df =1, ch=0 )
	cmds.polyCloseBorder(ch=0)
	cmds.polyCut(pc = (maxx + cx, 0, 0), ro = (0, -90,0), df = 1, ch=0)
	cmds.polyCloseBorder(ch=0)
	cmds.polyCut(pc = (0, 0, minz + cz), ro = (0, 0,0), df =1, ch=0 )
	cmds.polyCloseBorder(ch=0)
	cmds.polyCut(pc = (0, 0, maxz + cz), ro = (0, 180,0), df = 1, ch=0)
	cmds.polyCloseBorder(ch=0)
	cmds.polyCut(pc = (0, miny + cy, 0), ro = (-90, 0,0), df =1,ch=0 )
	cmds.polyCloseBorder(ch=0)
	cmds.polyCut(pc = (0, maxy + cy, 0), ro = (90, 0,0), df = 1, ch=0)
	cmds.polyCloseBorder(ch=0)
	cmds.select(cutmesh)

# get a random center for cutting
def rand_center(bbox):
	minx, miny, minz, maxx, maxy, maxz = bbox
	x = minx + (maxx - minx) * random.random()
	y = miny + (maxy - miny) * random.random()
	z = minz + (maxz - minz) * random.random()
	return [x, y, z]

bbox = mc.exactWorldBoundingBox(obj)

c = [-1.5,1.5,1.5]
print c
minx, miny, minz, maxx, maxy, maxz = bbox
cx, cy, cz = c
cmds.select(mesh)
cmds.polyCut(pc = (minx + cx, 0, 0), ro = (0, 90,0), ef=1)
cmds.polyCloseBorder()
cmds.polyCut(pc = (maxx + cx, 0, 0), ro = (0, -90,0), ef=1)
cmds.polyCloseBorder()
cmds.polyCut(pc = (0, 0, minz + cz), ro = (0, 0,0), ef=1)
cmds.polyCloseBorder()
cmds.polyCut(pc = (0, 0, maxz + cz), ro = (0, 180,0), ef=1)
cmds.polyCloseBorder()
cmds.polyCut(pc = (0, miny + cy, 0), ro = (-90, 0,0), ef=1)
cmds.polyCloseBorder()
cmds.polyCut(pc = (0, maxy + cy, 0), ro = (90, 0,0), ef=1)
cmds.polyCloseBorder()
cmds.select(cutmesh)
import maya.cmds as mc
import maya.mel as mm

mc.select(all=True)
mc.delete()

cube1 = mc.polyCube(sx=1, sy=1, sz=1, h=3, w=3, d=3)
#cube1 = mc.polySphere(r=5, sx=20, sy=20, ax=[0,1,0])
#cube1 = mc.polyCylinder(r=3, h=5, sx=20, sy=1, ax=[0,1,0])
#cube1 = mc.polyCone(r=1, h=2, ax=[0,1,0])
#cube1 = mc.polyPyramid()
obj = cube1[0]
part0 = [2, 2, 3, 1, 2]
part1 = [1, 2, 3, 0]
part2 = [1, 2, 3, 0]
part3 = [1, 1, 3, 0]

bbox = mc.exactWorldBoundingBox(obj)
print 'bbox', bbox

# yz
pyz = {'pc': [part0[0], 0, 0], 'ro': [0, 90, 0]}
# xz
pxz = {'pc': [0, part0[1], 0], 'ro': [-90, 0, 0]}
# xy
pxy = {'pc': [0, 0, part0[2]], 'ro': [0, 0, 0]}
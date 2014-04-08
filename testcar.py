import maya.cmds as cmds
import maya.mel as mel

def move_obj_center(obj, new_center):
	center = cmds.objectCenter(obj)
	translation = [x1 - x2 for (x1, x2) in zip(new_center, center)]
	cmds.move(translation[0], translation[1], translation[2], obj, r=1)
	return cmds.objectCenter(obj)

def move_lower_left_back_corner_to(obj, new_corner):
	bbox = cmds.exactWorldBoundingBox(obj)
	llb = [bbox[0], bbox[1], bbox[2]]
	translation = [x1 - x2 for (x1, x2) in zip(new_corner, llb)]
	cmds.move(translation[0], translation[1], translation[2], obj, r=1)
	return

def percet2loc(obj, perc):
	minx, miny, minz, maxx, maxy, maxz = cmds.exactWorldBoundingBox(obj)
	x = minx + (maxx - minx) * perc[0]
	y = miny + (maxy - miny) * perc[1]
	z = minz + (maxz - minz) * perc[2]
	return [x, y, z]

def create_part_by_shape(obj, shape, pivot):
	ow, oh, od = percet2loc(obj, shape)
	part = cmds.polyCube(h=oh, w=ow, d=od)[0]

	px, py, pz = percet2loc(obj, pivot)
	move_lower_left_back_corner_to(part, [px, py+0.1, pz])
	return part

def cut_by_part(obj, part):
	dup_obj = cmds.duplicate(obj)[0]
	new_cut = cmds.polyBoolOp(dup_obj, part, op=3, useThresholds=1, preserveColor=1)[0]
	return new_cut

def create_joints_and_bind(obj, joints):
	x1, y1, z1 = percet2loc(obj, joints[0])
	x2, y2, z2 = percet2loc(obj, joints[1])

	cmds.select(cl=1)
	j1 = cmds.joint(p=(x1, y1, z1), rad =0.5)
	j2 = cmds.joint(p=(x2, y2, z2), rad =0.5)
	cmds.joint(j1, e=True, zso=True, oj='xyz', sao='yup')
	cmds.select(obj, j1, r=1)
	cmds.bindSkin()
	return j1, j2


#####################################################################################
#cmds.select(all=True)
#cmds.delete()

# init
rem = 'transform47'
# map from part id to the mesh
partdict = dict()
# joint info contains 4 3-tuples, parent pos, child pos, parent translation, parent rotation
jointinfodict = dict()
jointdict = dict()
partid = []
shapes = []
pivots = []
num_parts = 0

# read all input
with open('D:\\FYP\\fyp_transformers\\template_brick', 'r') as f:
	fin = f.readlines()
# number of parts
num_parts = int(fin[0])

####################
# read each part
for i in xrange(1, num_parts + 1):
	line = fin[i].split()
	partid.append(line[0])
	shapes.append([float(line[4]), float(line[5]), float(line[6])])
	pivots.append([float(line[1]), float(line[2]), float(line[3])])

# move box's llb corner to the origin
move_lower_left_back_corner_to(rem, [0, 0, 0])
# cut all parts out
for i in xrange(num_parts):
	# create shape and move to pivot
	part = create_part_by_shape(rem, shapes[i], pivots[i])
	# do boolean op
	mesh = cut_by_part(rem, part)
	partdict[partid[i]] = mesh

# delete original object
cmds.delete(rem)

###################
# read each joint info
for i in xrange(num_parts + 1, 2*num_parts + 1):
	line = fin[i].split()
	jointid = line[0]
	jointinfodict[jointid] = [[float(line[1]), float(line[2]), float(line[3])], [float(line[4]), float(line[5]), float(line[6])], \
								[float(line[7]), float(line[8]), float(line[9])], [float(line[10]), float(line[11]), float(line[12])]]

# create joints and bind skin
for p in partid:
	parent, child = create_joints_and_bind(partdict[p], jointinfodict[p])
	jointdict[p] = [parent, child]

###################
# read parent info
for i in xrange(2*num_parts + 1, len(fin)):
	line = fin[i].split()
	p1, j1, p2, j2 = line[0], line[1], line[2], line[3]
	cmds.parent(jointdict[p2][int(j2)], jointdict[p1][int(j1)])

##################
# move and rotate each part
for p in partid:
	x, y, z = jointinfodict[p][2]
	rx, ry, rz = jointinfodict[p][3]
	cmds.move(x, y, z, jointdict[p][0], r=1)
	cmds.rotate(rx, ry, rz, jointdict[p][0], r=1, os=1)
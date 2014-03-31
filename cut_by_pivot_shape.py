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

def create_part_by_shape(obj, shape, pivot):
	minx, miny, minz, maxx, maxy, maxz = cmds.exactWorldBoundingBox(obj)
	ow = (maxx - minx) * shape[0]
	oh = (maxy - miny) * shape[1]
	od = (maxz - minz) * shape[2]
	part = cmds.polyCube(h=oh, w=ow, d=od)[0]

	px = (maxx - minx) * pivot[0]
	py = (maxy - miny) * pivot[1]
	pz = (maxz - minz) * pivot[2]
	move_lower_left_back_corner_to(part, [px, py, pz])
	return part

def cut_by_part(obj, part):
	dup_obj = cmds.duplicate(obj)[0]
	new_cut = cmds.polyBoolOp(dup_obj, part, op=3)[0]
	return new_cut

cmds.select(all=True)
cmds.delete()

# init
rem = cmds.polyCube(w = 3, h = 6, d = 2)[0]
shapes = []
pivots = []

# read input
with open('D:\\FYP\\fyp_transformers\\template_brick', 'r') as f:
	fin = f.readlines()
for i in xrange(len(fin)):
	line = fin[i].split()
	shapes.append([float(line[3]), float(line[4]), float(line[5])])
	pivots.append([float(line[0]), float(line[1]), float(line[2])])

# move box's llb corner to the origin
move_lower_left_back_corner_to(rem, [0, 0, 0])

# for each shape
for i in xrange(len(fin)):
	# create shape and move to pivot
	part = create_part_by_shape(rem, shapes[i], pivots[i])
	# do boolean op
	cut_by_part(rem, part)

# delete original object
cmds.delete(rem)

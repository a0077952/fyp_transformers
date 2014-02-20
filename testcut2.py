import maya.cmds as cmds
import maya.mel as mel
import random 

# create a cuboid, return its name
def create_part(part):
	minx, miny, minz, maxx, maxy, maxz = part
	return cmds.polyCube(w=maxx-minx, h=maxy-miny, d=maxz-minz)[0]

# get a random center for cutting
def rand_center(mesh):
	minx, miny, minz, maxx, maxy, maxz = cmds.exactWorldBoundingBox(mesh)
	x = minx + (maxx - minx) * random.random()
	y = miny + (maxy - miny) * random.random()
	z = minz + (maxz - minz) * random.random()
	return [x, y, z]

def move_obj_center(obj, new_center):
	center = cmds.objectCenter(obj)
	translation = [x1 - x2 for (x1, x2) in zip(new_center, center)]
	cmds.move(translation[0], translation[1], translation[2], obj, r=1)
	return cmds.objectCenter(obj)

def volume(mesh):
	return mel.eval('meshVolume(\"' + mesh + '\")')

# return number of vertices of bbox2 outside bbox1
def vertices_outside(bbox1, bbox2):
	minx, miny, minz, maxx, maxy, maxz = bbox1
	cminx, cminy, cminz, cmaxx, cmaxy, cmaxz = bbox2

	def vertex_inside_bbox(v):
		xin = v[0] > minx and v[0] < maxx
		yin = v[1] > miny and v[1] < maxy
		zin = v[2] > minz and v[2] < maxz
		return xin and yin and zin

	sum = 0
	# 8 vertices of cutpart's bbox
	for x in [cminx, cmaxx]:
		for y in [cminy, cmaxy]:
			for z in [cminz, cmaxz]:
				sum = sum + vertex_inside_bbox([x, y, z])

	return 8 - sum

def rec(remaining, part, move):
	print 'enter step', (move-5)/3

	# last part
	if len(part) == 1: 
		print 'done'
		return True
		# print 'last part!'
		# vol_rem = volume(remaining)
		# vol_part = volume(part)
		# ratio = vol_rem / vol_part
		# if ratio < 15 and ratio > 0.6:
		# 	print 'last part going to return true'
		# 	return True
		# else:
		# 	print 'last part going to return false'
		# 	cmds.delete(remaining)
		# 	return False

	backup_rem = cmds.duplicate(remaining)
	bbox_rem = cmds.exactWorldBoundingBox(remaining)
	for j in range(30):
		# get the cutpart at right position
		cutpart = create_part(part[0])
		cutcenter = rand_center(remaining)
		move_obj_center(cutpart, cutcenter)

		vol_part = volume(cutpart)
		bbox_cut = cmds.exactWorldBoundingBox(cutpart)

		# percentage inside check
		pi = vertices_outside(bbox_rem, bbox_cut)
		if pi < 5:
			cmds.delete(cutpart)
			continue

		# volumn check
		dum_rem = cmds.duplicate(remaining)
		dum_cut = cmds.duplicate(cutpart)
		new_cut = cmds.polyBoolOp(dum_rem, dum_cut, op=3)[0]
		new_rem = cmds.polyBoolOp(remaining, cutpart, op=2)[0]
		vol_cut = volume(new_cut)
		if vol_cut / vol_part > 0.6:
			# this part might work
			result = rec(new_rem, part[1:], move + 3)
			if result == True:
				print 'sol found, return to upper lv'
				cmds.move(move, 0, 0, new_cut, r=1)
				cmds.delete(backup_rem)
				return True
			else:
				cmds.delete(new_cut)
				remaining = cmds.duplicate(backup_rem)
				print 'try again in step', move
		else:
			cmds.delete(new_cut)
			cmds.delete(new_rem)
			remaining = cmds.duplicate(backup_rem)

	print 'fail in step', (move-5)/3
	cmds.delete(backup_rem)
	cmds.delete(remaining)
	return False

	

cmds.select(all=True)
cmds.delete()

remaining = cmds.polyCube(h=3, w=3, d=3)[0]
#remaining = cmds.polyCylinder(r=3, h=3, ax=[0,1,0])[0]
#remaining = cmds.polyCone(r=3, h=3, ax=[0,1,0])[0]
#cube1 = cmds.polyPyramid()
part0 = [-1, -1, -1, 1, 1, 1]
part1 = [-0.5, -1, -1.5, 0.5, 1, 1.5]
part2 = [-0.5, -1, -1.5, 0.5, 1, 1.5]
part3 = [-0.5, -0.5, -1.5, 0.5, 0.5, 1.5]
part = [part0, part1, part2, part3]
rec(remaining, part[:4], 5)

# cutpart = create_part(part0)
# vp = volume(cutpart)
# cutcenter = [1,1,0]
# move_obj_center(cutpart, cutcenter)

# minx, miny, minz, maxx, maxy, maxz = cmds.exactWorldBoundingBox(remaining)
# cminx, cminy, cminz, cmaxx, cmaxy, cmaxz = cmds.exactWorldBoundingBox(cutpart)

# print percentage_inside_check(cmds.exactWorldBoundingBox(cutpart), cmds.exactWorldBoundingBox(remaining))

# dup_rem = cmds.duplicate(remaining)
# dup_cut = cmds.duplicate(cutpart)
# new_rem = cmds.polyBoolOp(remaining, cutpart, op=2)[0]
# new_cut = cmds.polyBoolOp(dup_rem, dup_cut, op=3)[0]


# reunion
# ew_rem = cmds.polyBoolOp(new_rem, new_cut, op=1)[0]








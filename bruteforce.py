import maya.cmds as cmds
import maya.mel as mel
import random 

# create a cuboid, return its name
def create_part(part):
	minx, miny, minz, maxx, maxy, maxz = part
	return cmds.polyCube(w=maxx-minx, h=maxy-miny, d=maxz-minz)[0]

# create a cuboid based on w, h, d, centered in origin
def part_by_aspect(asp):
	return cmds.polyCube(w=asp[0], h=asp[1], d=asp[2])[0]

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

def volume_with_bbox(bbox):
	minx, miny, minz, maxx, maxy, maxz = bbox
	return abs((maxx - minx) * (maxy - miny) * (maxz - minz))

# return number of vertices of bbox2 outside bbox1
def vertices_outside(bbox1, bbox2):
	minx, miny, minz, maxx, maxy, maxz = bbox1
	cminx, cminy, cminz, cmaxx, cmaxy, cmaxz = bbox2

	def vertex_inside_bbox(v):
		xin = v[0] >= minx and v[0] <= maxx
		yin = v[1] >= miny and v[1] <= maxy
		zin = v[2] >= minz and v[2] <= maxz
		return xin and yin and zin

	sum = 0
	# 8 vertices of cutpart's bbox
	for x in [cminx, cmaxx]:
		for y in [cminy, cmaxy]:
			for z in [cminz, cmaxz]:
				sum = sum + vertex_inside_bbox([x, y, z])

	return 8 - sum

# get center from bbox of mesh and its axis percentage
def center_with_sub_index(bbox, xp, yp, zp):
	minx, miny, minz, maxx, maxy, maxz = bbox
	x = minx + (maxx - minx) * xp
	y = miny + (maxy - miny) * yp
	z = minz + (maxz - minz) * zp
	return [x, y, z]

def rec(remaining, part, move):
	print 'enter step', (move-5)/3

	if len(part) == 0: 
		print 'done', remaining
		return True

	backup_rem = cmds.duplicate(remaining)
	bbox_rem = cmds.exactWorldBoundingBox(remaining)

	# for all possible centers
	# center must be inside the bounding box
	# here we consider centers lies on one subdivision of axis
	nn = 20
	xsub = nn
	ysub = nn
	zsub = nn
	sum = 0
	for x in xrange(xsub):
		for y in xrange(ysub):
			for z in xrange(zsub):
				# for all possible orientations
				# create part
				cutpart = part_by_aspect(part[0])
				# move part to this center
				cutcenter = center_with_sub_index(bbox_rem, x/float(xsub), y/float(ysub), z/float(zsub))
				move_obj_center(cutpart, cutcenter)

				# store volume
				bbox_cut = cmds.exactWorldBoundingBox(cutpart)
				vol_part = volume_with_bbox(bbox_cut)

				# percentage of vertex outside check
				pi = vertices_outside(bbox_rem, bbox_cut)
				if pi < 6:
					cmds.delete(cutpart)
					continue

				# cut the part out from remaining
				dum_rem = cmds.duplicate(remaining)
				dum_cut = cmds.duplicate(cutpart)
				new_cut = cmds.polyBoolOp(dum_rem, dum_cut, op=3)[0]
				new_rem = cmds.polyBoolOp(remaining, cutpart, op=2)[0]

				# shell check
				# make sure that new_cut contains one single object
				if cmds.polyEvaluate(new_cut, shell = True) != 1:
					cmds.delete(new_rem)
					cmds.delete(new_cut)
					remaining = cmds.duplicate(backup_rem)
					continue

				# volume check
				vol_cut = volume(new_cut)
				if vol_cut / vol_part  > 0.4:
					# this part might work
					result = rec(new_rem, part[1:], move + 3)
					if result == True:
						sum = sum + 1
						print 'sol found, return to upper lv', vol_cut, vol_part
						cmds.move(move, 0, 0, new_cut, r=1)
						cmds.delete(backup_rem)
						return True
				else:
					print vol_cut / vol_part 

					cmds.delete(new_rem)
					cmds.delete(new_cut)
					remaining = cmds.duplicate(backup_rem)
			
	# no solusion after tried all
	print 'fail in step', (move-5)/3, 'try', sum
	cmds.delete(backup_rem)
	cmds.delete(remaining)
	return False

	

cmds.select(all=True)
cmds.delete()

remaining = cmds.polyCube(h=5, w=5, d=5)[0]
part0 = [1, 1, 1]
part = [part0, part0, part0, part0, part0, part0, part0, part0, part0]
rec(remaining, part, 5)







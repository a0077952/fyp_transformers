import maya.cmds
import maya.mel
import random 

# part is defined by bbox and center
# def cut_part(mesh, bbox, center):
# 	cutmesh = cmds.duplicate(mesh)
# 	#cutmesh = mesh
# 	minx, miny, minz, maxx, maxy, maxz = bbox
# 	cx, cy, cz = center
# 	cmds.select(cutmesh)
# 	cmds.polyCut(pc = (minx + cx, 0, 0), ro = (0, 90,0), df =1, ch=0 )
# 	cmds.polyCloseBorder(ch=0)
# 	cmds.polyCut(pc = (maxx + cx, 0, 0), ro = (0, -90,0), df = 1, ch=0)
# 	cmds.polyCloseBorder(ch=0)
# 	cmds.polyCut(pc = (0, 0, minz + cz), ro = (0, 0,0), df =1, ch=0 )
# 	cmds.polyCloseBorder(ch=0)
# 	cmds.polyCut(pc = (0, 0, maxz + cz), ro = (0, 180,0), df = 1, ch=0)
# 	cmds.polyCloseBorder(ch=0)
# 	cmds.polyCut(pc = (0, miny + cy, 0), ro = (-90, 0,0), df =1,ch=0 )
# 	cmds.polyCloseBorder(ch=0)
# 	cmds.polyCut(pc = (0, maxy + cy, 0), ro = (90, 0,0), df = 1, ch=0)
# 	cmds.polyCloseBorder(ch=0)
# 	cmds.select(cutmesh)

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


# minx, miny, minz, maxx, maxy, maxz = bbox
# cx, cy, cz = c
# cmds.select(mesh)
# cmds.polyCut(pc = (minx + cx, 0, 0), ro = (0, 90,0), ef=1)
# cmds.polyCloseBorder()
# cmds.polyCut(pc = (maxx + cx, 0, 0), ro = (0, -90,0), ef=1)
# cmds.polyCloseBorder()
# cmds.polyCut(pc = (0, 0, minz + cz), ro = (0, 0,0), ef=1)
# cmds.polyCloseBorder()
# cmds.polyCut(pc = (0, 0, maxz + cz), ro = (0, 180,0), ef=1)
# cmds.polyCloseBorder()
# cmds.polyCut(pc = (0, miny + cy, 0), ro = (-90, 0,0), ef=1)
# cmds.polyCloseBorder()
# cmds.polyCut(pc = (0, maxy + cy, 0), ro = (90, 0,0), ef=1)
# cmds.polyCloseBorder()
# cmds.select(cutmesh)

def volume(mesh):
	return mm.eval('meshVolume(\"' + mesh + '\")')

def rec(remaining, part, move):
	print 'enter step', move
	cmds.select(remaining, r=1)
	cmds.polyCloseBorder()

	# last part
	if len(part) == 1: 
		print 'last part!'
		vol_rem = volume(remaining)
		vol_part = volume(part)
		ratio = vol_rem / vol_part
		if ratio < 1.5 and ratio > 0.6:
			return True
		else:
			return False


	# 10 tries each depth
	# for i in range(10):
		# select a part (1st one)
	cutpart = create_part(part[0])
	vol_part = volume(cutpart)
	for j in range(10):
		# 10 tries for a suitable part
		cutcenter = rand_center(remaining)
		move_obj_center(cutpart, cutcenter)
		dup_rem = cmds.duplicate(remaining)
		dup_cut = cmds.duplicate(cutpart)

		new_rem = cmds.polyBoolOp(remaining, cutpart, op=2)[0]
		new_cut = cmds.polyBoolOp(dup_rem, dup_cut, op=3)[0]
		vol_cut = volume(new_cut)
		if vol_cut / vol_part > 0.7:
			# this part might work
			move = move + 3
			result = rec(new_rem, part[1:], move)
			if result == True:
				print 'fuck', new_cut
				cmds.move(move, 0, 0, new_cut, r=1)
				return True

		remaining = cmds.polyBoolOp(new_rem, new_cut, op=1)[0]
		cmds.select(remaining, r=1)
		cmds.polyCloseBorder()
		cutpart = create_part(part[0])
	return False

	

cmds.select(all=True)
cmds.delete()

remaining = cmds.polyCube(h=3, w=3, d=3)[0]
part0 = [-1, -1, -1, 1, 1, 1]
part1 = [-0.5, -1, -1.5, 0.5, 1, 1.5]
part2 = [-0.5, -1, -1.5, 0.5, 1, 1.5]
part3 = [-0.5, -0.5, -1.5, 0.5, 0.5, 1.5]
part = [part0, part1, part2, part3]
rec(remaining, part, 5)

# cutpart = create_part(part0)
# vp = volume(cutpart)
# cutcenter = [0,0,0]
# move_obj_center(cutpart, cutcenter)
# dup_rem = cmds.duplicate(remaining)
# dup_cut = cmds.duplicate(cutpart)
# new_rem = cmds.polyBoolOp(remaining, cutpart, op=2)[0]
# new_cut = cmds.polyBoolOp(dup_rem, dup_cut, op=3)[0]
# vc = volume(new_cut)
# print vc/vp

# reunion
# ew_rem = cmds.polyBoolOp(new_rem, new_cut, op=1)[0]








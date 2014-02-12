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

def rec(remaining, part, move):
	print 'enter step', move

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
	for j in range(100):
		# 100 tries for a suitable part
		cutpart = create_part(part[0])
		vol_part = volume(cutpart)
		cutcenter = rand_center(remaining)
		move_obj_center(cutpart, cutcenter)

		new_cut = cmds.polyBoolOp(cmds.duplicate(remaining), cmds.duplicate(cutpart), op=3)[0]
		new_rem = cmds.polyBoolOp(remaining, cutpart, op=2)[0]
		vol_cut = volume(new_cut)
		if vol_cut / vol_part > 0.9:
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
				print 'shit try again'
		else:
			cmds.delete(new_cut)
			cmds.delete(new_rem)
			remaining = cmds.duplicate(backup_rem)

	print 'oh no fail 100 times in step', move
	cmds.delete(backup_rem)
	cmds.delete(remaining)
	return False

	

cmds.select(all=True)
cmds.delete()

remaining = cmds.polyCube(h=3, w=3, d=3)[0]
part0 = [-1, -1, -1, 1, 1, 1]
part1 = [-0.5, -1, -1.5, 0.5, 1, 1.5]
part2 = [-0.5, -1, -1.5, 0.5, 1, 1.5]
part3 = [-0.5, -0.5, -1.5, 0.5, 0.5, 1.5]
part = [part0, part1, part2, part3]
rec(remaining, part[:4], 5)

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








import maya.cmds as mc
import maya.mel as mm
import random

kMoveAwayXDistance = 20

def form_cutting_planes_for_object(obj, num):
	"num = number of separations in each direction, result in num - 1 planes"
	res = []
	bbox = mc.exactWorldBoundingBox(obj)
	xmin = bbox[0]
	ymin = bbox[1]
	zmin = bbox[2]
	xmax = bbox[3]
	ymax = bbox[4]
	zmax = bbox[5]
	# yz planes 
	for i in range(1, num):
		x = xmin + i * ((xmax - xmin) / num)
		# todo add randomness in rotation
		p = {'pc': [x, 0, 0], 'ro': [0, 90, 0]}
		res.append(p)
	# xz planes
	for j in range(1, num):
		y = ymin + j *((ymax - ymin) / num)
		p = {'pc': [0, y, 0], 'ro': [90, 0, 0]}
		res.append(p)
	# xy planes
	for k in range(1, num):
		z = zmin + k * ((zmax - zmin) / num)
		p = {'pc': [0, 0, z], 'ro': [0, 0, 0]}
		res.append(p)
	return res


# input: one object, total volume, generated cutting planes, list of ratios interested, error threshold
# return: on success, return a list of separated parts moved kMoveAwayXDistance in x direction
#	on failure, return a dictionary contains key 'bad_cut_objs' -> list of object that cannot 
#	match any ratios, and 'ratios_remaining' -> list of remaining ratios, 
# 	and 'good_cut_objs' -> list of objects found
def cut_object_with_planes_and_ratios(obj, volume_total, planes, ratios, threshold):
	# create a list of booleans indicating ratios found or not
	ratio_found = []
	for r in ratios: ratio_found.append(0)
	ratios.sort()
	results = []
	# a list of objects that volume cannot be match anymore
	bad_cut_objs = []
	all_found = False
	# initially we have only one object to cut
	objs_to_cut = [obj]

	# loop all cut planes
	for plane in planes:
		# store all object result from this cut
		objs_for_next_plane_iteration = []
		# for each object in world
		for i in range(len(objs_to_cut)):
			#print 'cut object: ' + objs_to_cut[i]
			mc.select(objs_to_cut[i], r = True)
			# cut
			mc.polyCut(pc = plane['pc'], ro = plane['ro'], ef = True, eo = [0, 0, 0])
			# fill hole
			mc.select(objs_to_cut[i], r = True)
			mc.polyCloseBorder()
			# separate
			# if number of pieces < 2, means the plane and the object did not have intersection
			if mc.polyEvaluate(objs_to_cut[i], shell = True) < 2:
				# add back this object
				objs_for_next_plane_iteration.append(objs_to_cut[i])
				# continue with other objs_to_cut
				continue
			parts = mc.polySeparate(objs_to_cut[i])
			# add these parts to future objs to cut
			objs_for_next_plane_iteration.extend(parts[0:-1])
			# for each parts
			for j in range(len(parts) - 1):
				this_volume_ratio = mm.eval('meshVolume(\"' + parts[j] + '\")') / volume_total
				# check volume
				first_unfound_volume = True
				for k in range(len(ratios)):
					if ratio_found[k] == 0:
						# this part's volume is less than the smallest volume unfound
						if first_unfound_volume and this_volume_ratio + threshold < ratios[k]:
							print 'bad volume found, save', this_volume_ratio
							objs_for_next_plane_iteration.remove(parts[j])
							bad_cut_objs.append(parts[j])
							break
						# got match
						elif abs(this_volume_ratio - ratios[k]) < threshold:
							print 'volume found: ', this_volume_ratio
							# dup the object
							temp = mc.duplicate(parts[j])
							mc.select(temp[0], r = True)
							# move away the duplication
							mc.move(kMoveAwayXDistance, 0, 0, temp[0])
							# add it to the result list
							results.append(temp[0])
							# remove the current object
							mc.delete(parts[j])
							objs_for_next_plane_iteration.remove(parts[j])
							# mark volume as found
							ratio_found[k] = 1
							# if all parts found
							if ratio_found.count(0) == 0:
								all_found = True
							break
						if first_unfound_volume:
							first_unfound_volume = False
				if all_found: break
			if all_found: break
		objs_to_cut = objs_for_next_plane_iteration
		if all_found:
			# todo move back all result obj
			print 'FFFFFFFFFFFFFFFFFFFFFFFFUUUUUUUUUUUUUUUUUUUUUUUUUU'
			return results
		elif len(objs_to_cut) == 0:
			# no more cuttings but not all_found
			break

	# objs_to_cut might be empty due to insufficient planes OR empty
	if len(objs_to_cut) != 0:
		bad_cut_objs.extend(objs_to_cut)
	ratios_remaining = []
	for i in range(len(ratio_found)):
		if ratio_found[i] == 0:
			ratios_remaining.append(ratios[i])
	return {'bad_cut_objs': bad_cut_objs, 'ratios_remaining': ratios_remaining, 'good_cut_objs': results}

# object should not contain more than one shell
def rec(object_name, volume_total, cut_planes, volume_ratios, threshold, result, loop_num):
	# base cases
	if loop_num == 0:
		print 'insert more coins to continue'
		return False
	elif mc.polyEvaluate(object_name, shell = True) > 1:
		# more than one shell in object named 'object_name'
		print 'NO REDEMPTION'
		return False
	elif len(volume_ratios) == 1:
		# check ratio matches
		this_ratio = mm.eval('meshVolume(\"' + object_name + '\")') / volume_total
		# since its last one, might have more errors
		if abs(this_ratio - volume_ratios[0]) < threshold * 4:
			# duplicate the object
			temp = mc.duplicate(object_name)
			mc.select(temp[0], r = True)
			# move away the duplication
			mc.move(kMoveAwayXDistance, 0, 0, temp[0])
			# remove the current object
			mc.delete(object_name)
			print 'DONE with last object!'
			result.append(temp[0])
			print result
			return True
		else:
			print 'last object did NOT match last ratio!', this_ratio, volume_ratios[0]
			return False

	# recursive step
	random.shuffle(cut_planes)
	result_from_cutting = cut_object_with_planes_and_ratios(object_name, volume_total, cut_planes, volume_ratios, threshold)
	if isinstance(result_from_cutting, list):
		# this list contains all successfully cut objects and we are done
		result.extend(result_from_cutting)
		print 'lucky!'
		print result
		return True
	else:
		print 'Enter recursive step'
		# dictionary returned
		# extend result list with what we have now
		result.extend(result_from_cutting['good_cut_objs'])
		# merge the remaining objects into one
		bad_cut_objs = result_from_cutting['bad_cut_objs']
		if mc.polyEvaluate(bad_cut_objs, shell = True) > 1:
			united_objects = mc.polyUnite(bad_cut_objs)[0]
			mc.polyMergeVertex(united_objects)
		else:
			united_objects = bad_cut_objs[0]
		# get list of ratios un-resolved
		ratios_remaining = result_from_cutting['ratios_remaining']
		recursion_result = rec(united_objects, volume_total, cut_planes, ratios_remaining, threshold, result, loop_num-1)
		return recursion_result






mc.select(all=True)
mc.delete()
cube1 = mc.polyCube(sx=1, sy=1, sz=1, h=5, w=5, d=5)
object_name = cube1[0]
volume_total = mm.eval('meshVolume(\"' + object_name + '\")')
volume_ratios = [0.2, 0.4, 0.4]
threshold = 0.03
#print mc.objectCenter(cube1[0])
# LOOP A
cut_planes = form_cutting_planes_for_object(object_name, 10)
# LOOP B

rec(object_name, volume_total, cut_planes, volume_ratios, threshold, [], 10)

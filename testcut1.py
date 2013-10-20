import maya.cmds as mc
import maya.mel as mm
import random

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



def cut_object_with_planes_and_ratios(obj, planes, ratios, threshold):
	volume_total = mm.eval('meshVolume(\"' + obj + '\")')
	ratio_found = []
	for r in ratios: ratio_found.append(0)
	results = []
	all_found = False
	# initially we have only one object to cut
	objs_to_cut = [obj]

	# loop all cut planes
	for plane in planes:
		#print 'cut use plane: '
		#print plane
		# store all object result from this cut
		objs_for_next_iteration = []
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
			# if number of pieces < 2, means the plane and the object did not intersect
			if mc.polyEvaluate(shell = True) < 2:
				# add back this object
				objs_for_next_iteration.append(objs_to_cut[i])
				# continue with other objs_to_cut
				continue
			parts = mc.polySeparate(objs_to_cut[i])
			# add parts to future objs to cut
			objs_for_next_iteration.extend(parts[0:-1])
			# for each parts
			for j in range(len(parts) - 1):
				this_volume_ratio = mm.eval('meshVolume(\"' + parts[j] + '\")') / volume_total
				#print 'volume: ', this_volume_ratio
				# check volume
				for k in range(len(ratios)):
					if ratio_found[k] == 0 and abs(this_volume_ratio - ratios[k]) < threshold:
						print 'volume found: ', this_volume_ratio
						# dup the object
						temp = mc.duplicate(parts[j])
						mc.select(temp[0], r = True)
						# move away the duplication
						mc.move(20, 0, 0, temp[0])
						# add it to the result list
						results.append(temp[0])
						# remove the current object
						mc.delete(parts[j])
						objs_for_next_iteration.remove(parts[j])
						# mark volume as found
						ratio_found[k] = 1
						# if all parts found
						if ratio_found.count(0) == 0:
							all_found = True
						break
				if all_found: break
			if all_found: break
		objs_to_cut = objs_for_next_iteration
		if all_found:
			# todo move back all result obj
			print 'FFFFFFFFFFFFFFFFFFFFFFFFUUUUUUUUUUUUUUUUUUUUUUUUUU'
			return results

	return False


mc.select(all=True)
mc.delete()
cube1 = mc.polyCube(sx=1, sy=1, sz=1, h=5, w=5, d=5)
#print mc.objectCenter(cube1[0])
cut_planes = form_cutting_planes_for_object(cube1[0], 4)
random.shuffle(cut_planes)
volume_ratios = [0.25, 0.5, 0.25]
print cut_object_with_planes_and_ratios(cube1[0], cut_planes, volume_ratios, 0.05)



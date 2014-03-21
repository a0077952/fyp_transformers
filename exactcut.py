import maya.cmds as cmds
import maya.mel as mel

def volume(mesh):
	return mel.eval('meshVolume(\"' + mesh + '\")')

def cut_object(obj):
	xmin, ymin, zmin, xmax, ymax, zmax = cmds.exactWorldBoundingBox(obj)
	plane_body = []
	for j in range(1, 3):
		y = ymin + j *((ymax - ymin) / 3) + (-1)**j * (ymax - ymin) / 30
		p = {'pc': [0, y, 0], 'ro': [-90, 0, 0]}
		plane_body.append(p)

	plane_legs = []
	for i in xrange(1, 4):
		x = xmin + i * ((xmax - xmin) / 4) + (2-i)**i * (xmax - xmin) / 30
		p = {'pc': [x, 0, 0], 'ro': [0, 90, 0]}
		plane_legs.append(p)

	plane_heads = []
	for i in xrange(1, 3):
		x = xmin + i * ((xmax - xmin) / 3)
		p = {'pc': [x, 0, 0], 'ro': [0, 90, 0]}
		plane_heads.append(p)

	plane_arms = []
	for i in xrange(1, 3):
		x = xmin + i * ((xmax - xmin) / 3) + (-1)**i * (xmax - xmin) / 20
		p = {'pc': [x, 0, 0], 'ro': [0, 90, 0]}
		plane_arms.append(p)

	plane_hands = []
	for i in xrange(1, 2):
		z = zmin + i * ((zmax - zmin) / 2) - (zmax - zmin) / 7
		p = {'pc': [0, 0, z], 'ro': [0, 0, 0]}
		plane_hands.append(p)

	# cut body
	body = cut_by_planes(obj, plane_body)
	for i in xrange(2):
		cmds.select(body[i], r=True)
		cmds.move(0, (-1)**i * (0.3), 0, r=True)

	# cut legs
	legs = cut_by_planes(body[1], plane_legs)
	for i in xrange(2):
		cmds.select(legs[i], r=True)
		cmds.move((-1)**i * (0.5), 0, 0, r=True)
	for i in xrange(2, 4):
		cmds.select(legs[i], r=True)
		cmds.move((-1)**i * (0.2), 0, 0, r=True)

	# cut heads
	heads = cut_by_planes(body[0], plane_heads)
	for i in xrange(1, 3):
		cmds.select(heads[i], r=True)
		cmds.move((-1)**i * (0.3), 0, 0, r=True)

	# cut arms
	arms = cut_by_planes(body[2], plane_arms)
	for i in xrange(2):
		cmds.select(arms[i], r=True)
		cmds.move((-1)**i * (-0.3), 0, 0, r=True)

	# cut right_hand
	cmds.select(arms[0], r=True)
	cmds.move(0, 0, -0.3, r=True)
	right_hand = cut_by_planes(arms[0], plane_hands)
	cmds.select(right_hand[0], r=True)
	cmds.move(0, 0, -0.3, r=True)

	# cut left_hand
	cmds.select(arms[1], r=True)
	cmds.move(0, 0, -0.3, r=True)
	left_hand = cut_by_planes(arms[1], plane_hands)
	cmds.select(left_hand[0], r=True)
	cmds.move(0, 0, -0.3, r=True)

	return

def cut_by_planes(obj, planes):
	cmds.select(obj, r=True)
	for plane in planes:
		cmds.polyCut(pc = plane['pc'], ro = plane['ro'], ef = True, eo = [0,0,0])
		cmds.polyCloseBorder()

	res = cmds.polySeparate(obj)
	return res;

def print_cut_planes(planes):
	for p in planes:
		temp = cmds.polyPlane(ax = [0, 0, 1], h = 5, w = 5)
		cmds.move(p['pc'][0], p['pc'][1], p['pc'][2], temp)
		cmds.rotate(p['ro'][0], p['ro'][1], p['ro'][2], temp)
	return




# mc.select(all=True)
# mc.delete()
cut_object("transform1")


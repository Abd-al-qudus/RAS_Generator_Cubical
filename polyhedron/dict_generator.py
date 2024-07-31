import csv
from abaqus import *
from abaqusConstants import *
import numpy as np
import os
import __main__

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior


csvPath = r"C:\Users\engin\Desktop" #path storing the polygon data
os.chdir(csvPath)

keydict = {}
hulldict = {}


with open('testp.csv') as fob:
    lines = csv.reader(fob)
    next(lines)
    for line in lines:
        intl = list(map(float, line))
        if not keydict.get(intl[0]):
            keydict[intl[0]] = []
        keydict[intl[0]].append(intl[1:])


with open('testh.csv') as fob:
    lines = csv.reader(fob)
    next(lines)
    for line in lines:
        intl = list(map(int, line))
        if not hulldict.get(intl[0]):
            hulldict[intl[0]] = []
        hulldict[intl[0]].append(intl[1:])


def checkWire(index, wireSet):
	for i in wireSet:
		if i == index:
			return True
		else:
			return False

			
def isCollinear(point, pointA,pointB): #points are tuple
	MA = np.sqrt((point[0]-pointA[0])**2+(point[1]-pointA[1])**2+(point[2]-pointA[2])**2)
	BM = np.sqrt((pointB[0]-point[0])**2+(pointB[1]-point[1])**2+(pointB[2]-point[2])**2)
	BA = np.sqrt((pointB[0]-pointA[0])**2+(pointB[1]-pointA[1])**2+(pointB[2]-pointA[2])**2)
	if abs(MA+BM-BA) < 1e-9:
		return True
	else:
		return False


for k, h in zip(keydict, hulldict):
    data = keydict[k]
    convexHull = hulldict[h]

    # create coordinate reference and supress
    p = mdb.models['Model-1'].Part(name='Part-{}'.format(int(k)), dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p.ReferencePoint(point=(0.0, 0.0, 0.0))	
    p.features['RP'].suppress()

    for item in data:
        p.DatumPointByCoordinate(coords=(item[0], item[1], item[2]))
        
    d1 = p.datums;

    # join datum for edges
    for hull in convexHull:
	v1 = int(hull[0]) + 2 if int(hull[0]) + 2 <= max(d1.keys()) else max(d1.keys())
	v2 = int(hull[1]) + 2 if int(hull[1]) + 2 <= max(d1.keys()) else max(d1.keys())
	v3 = int(hull[2]) + 2 if int(hull[2]) + 2 <= max(d1.keys()) else max(d1.keys())
        p.WirePolyLine(points=((d1[v1], d1[v2]),), mergeType=IMPRINT, meshable=ON)
        p.WirePolyLine(points=((d1[v2], d1[v3]),), mergeType=IMPRINT, meshable=ON)
        p.WirePolyLine(points=((d1[v3], d1[v1]),), mergeType=IMPRINT, meshable=ON)
        
    eg = p.edges

    # create faces
    for p in convexHull:
	v1 = int(p[0]) + 2 if int(p[0]) + 2 <= max(d1.keys()) else max(d1.keys())
	v2 = int(p[1]) + 2 if int(p[1]) + 2 <= max(d1.keys()) else max(d1.keys())
	v3 = int(p[2]) + 2 if int(p[2]) + 2 <= max(d1.keys()) else max(d1.keys())
        seq = []
        wireSet = []
        for edge in eg:
            point = edge.pointOn[0]
            if isCollinear(point, d1[v1].pointOn,d1[v2].pointOn):	
                if checkWire(1,wireSet):
                    continue
                else:
                    seq.append(edge)
                    wireSet.append(1)
            if isCollinear(point, d1[v2].pointOn,d1[v3].pointOn):
                if checkWire(2,wireSet):
                    continue
                else:
                    seq.append(edge)
                    wireSet.append(2)
            if isCollinear(point, d1[v3].pointOn,d1[v1].pointOn):
                if checkWire(3,wireSet):
                    continue
                else:
                    seq.append(edge)
                    wireSet.append(3)
            if len(seq) == 3:
                p = mdb.models['Model-1'].parts['Part-{}'.format(int(k))]
                p.CoverEdges(edgeList = seq, tryAnalytical=True)
                break
                
    # create solid
    p = mdb.models['Model-1'].parts['Part-{}'.format(int(k))]
    f = p.faces
    p.AddCells(faceList = f)

mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
for i in range(len(keydict.keys())):
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-{}-1'.format(i + 1), part=mdb.models['Model-1'].parts['Part-{}'.format(i + 1)])

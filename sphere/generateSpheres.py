from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import math as mt
import csv
import os

csvPath = r"C:\Users\engin\Downloads\data"  # path storing the polygon data
os.chdir(csvPath)

sphere_dict = {}

with open('spheres40%.csv') as fob:
    lines = csv.reader(fob)
    next(lines)
    for line in lines:
        intl = list(map(float, line))
        if not sphere_dict.get(intl[0]):
            sphere_dict[intl[0]] = []
        sphere_dict[intl[0]].append(intl[1:])

for k in sphere_dict.keys():
    sphere = sphere_dict[k][0]
    
    # Create a sketch and define the profile for the sphere
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=mdb.models['Model-1'].sketches['__profile__'].geometry[2])
    mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(center=(0, 0), direction=CLOCKWISE, point1=(0, sphere[3]), point2=(0, -sphere[3]))
    mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=mdb.models['Model-1'].sketches['__profile__'].vertices[2], entity2=mdb.models['Model-1'].sketches['__profile__'].geometry[2])
    mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=mdb.models['Model-1'].sketches['__profile__'].vertices[0], entity2=mdb.models['Model-1'].sketches['__profile__'].geometry[2])
    mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(addUndoState=False, entity1=mdb.models['Model-1'].sketches['__profile__'].vertices[1], entity2=mdb.models['Model-1'].sketches['__profile__'].geometry[2])
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, sphere[3]), point2=(0, -sphere[3]))
    mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=False, entity=mdb.models['Model-1'].sketches['__profile__'].geometry[4])
    mdb.models['Model-1'].sketches['__profile__'].PerpendicularConstraint(addUndoState=False, entity1=mdb.models['Model-1'].sketches['__profile__'].geometry[3], entity2=mdb.models['Model-1'].sketches['__profile__'].geometry[4])
    mdb.models['Model-1'].sketches['__profile__'].move(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].geometry[2], 
    mdb.models['Model-1'].sketches['__profile__'].geometry[3], 
    mdb.models['Model-1'].sketches['__profile__'].geometry[4]), vector=(sphere[0], sphere[1]))

    # Create a 3D part by revolving the sketch
    part_name = 'Part-{}'.format(int(k))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name=part_name, type=DEFORMABLE_BODY)
    mdb.models['Model-1'].parts[part_name].BaseSolidRevolve(angle=360.0, flipRevolveDirection=OFF, sketch=mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']

    # create partition
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].DatumPlaneByPrincipalPlane(offset=0.0, 
    principalPlane=XYPLANE)
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].DatumPlaneByPrincipalPlane(offset=sphere[0], 
    principalPlane=YZPLANE)
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].DatumPlaneByPrincipalPlane(offset=sphere[1], 
    principalPlane=XZPLANE)

    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].PartitionFaceByDatumPlane(datumPlane=
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].datums[4], faces=
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].faces.getSequenceFromMask(('[#1 ]', 
    ), ))
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].PartitionFaceByDatumPlane(datumPlane=
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].datums[2], faces=
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].faces.getSequenceFromMask(('[#3 ]', 
    ), ))
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].PartitionFaceByDatumPlane(datumPlane=
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].datums[3], faces=
    mdb.models['Model-1'].parts['Part-{}'.format(int(k))].faces.getSequenceFromMask(('[#f ]', 
    ), ))


    # Translate the part to the specified center coordinates
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='{}-1'.format(part_name), part=mdb.models['Model-1'].parts[part_name])
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('{}-1'.format(part_name), ), vector=(0.0, 0.0, sphere[2]))

    # Meshing
    #if sphere[3] > 6.35 and sphere[3] <= 9.5:
    #    mdb.models['Model-1'].parts[part_name].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=2.0)
    #elif sphere[3] > 4.75 and sphere[3] <= 6.35:
    #    mdb.models['Model-1'].parts[part_name].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=1.0)
    #else:
    #    mdb.models['Model-1'].parts[part_name].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=0.50)
    #mdb.models['Model-1'].parts[part_name].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=2.0)
    #mdb.models['Model-1'].parts[part_name].setMeshControls(elemShape=TET, regions=mdb.models['Model-1'].parts[part_name].cells.getSequenceFromMask(('[#1 ]', ), ), technique=FREE)
    #mdb.models['Model-1'].parts[part_name].setElementType(elemTypes=(ElemType(elemCode=C3D20R, elemLibrary=STANDARD), ElemType(elemCode=C3D15, elemLibrary=STANDARD), ElemType(elemCode=C3D10, elemLibrary=STANDARD)), regions=(mdb.models['Model-1'].parts[part_name].cells.getSequenceFromMask(('[#1 ]', ), ), ))
    #mdb.models['Model-1'].parts[part_name].setElementType(elemTypes=(ElemType(elemCode=UNKNOWN_HEX, elemLibrary=EXPLICIT), ElemType(elemCode=UNKNOWN_WEDGE, elemLibrary=EXPLICIT), ElemType(elemCode=C3D10M, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT, elemDeletion=ON)), regions=(mdb.models['Model-1'].parts[part_name].cells.getSequenceFromMask(('[#1 ]', ), ), ))
    #mdb.models['Model-1'].parts[part_name].generateMesh()


"""
 * @Author: Mengsen.Wang
 * @Date: 2019-12-02 19:05:58
 * @Last Modified by:   Mengsen.Wang
 * @Last Modified time: 2019-12-05 19-27-56
"""
# coding = utf-8

from abaqus import *
from abaqusConstants import *
from caeModules import *
import math

# setting parameters
parameters = (
    ("Model Name:", "JinGuangZe_SheerWall"),
    ("Cover(mm):", "24"),
    ("Length(wall)(mm):", "1200"),
    ("Thickness(wall)(mm):", "240"),
    ("Height(wall)(mm):", "1050"),
    ("Diameter(tube)(mm):", "106"),
    ("Thickness(tube)(mm):", "4"),
    ("Diameter(longitudinal bar)(mm):", "10"),
    ("Diameter(transversal bar)(mm):", "6"),
    ("Length(foundation)(mm):", "3500"),
    ("Thickness(foundation)(mm):", "600"),
    ("Height(foundation)(mm):", "500"),
    ("Length(loadbeam)(mm):", "1200"),
    ("Thickness(loadbeam)(mm):", "300"),
    ("Height(loadbeam)(mm):", "300"),
    ("Yield stress(longitudinal bar)(N/mm):", "400"),
    ("Yield stress(transversal bar)(N/mm):", "500"),
    ("Yield stress(tube)(N/mm):", "325"),
    ("Displacement(maximum)(mm):", "35"),
    ("axial-load(KN):", "3450000"),
    ("offset(tube1)(mm):", "400"),
    ("offset(tube2)(mm):", "230"),
    ("Space between transversal bar", "100"),
    ("Mesh Size(mm):", "50"),
    ("Job Name:", "Job-ShearWall"),
)

# setting getInput parameters
modelname, cover, lwall, twall, hwall, dtube, ttube, dlbar, dtbar, lfd, tfd, hfd, lbl, tbl, hbl, fylbar, fytbar, fytube, dis, axld, offset1, offset2, space, meshsize, jobname = getInputs(
    fields=parameters, label="Please Input The Parameter", dialogTitle="Parameter Input"
)

session.viewports["Viewport: 1"].makeCurrent()
session.viewports["Viewport: 1"].maximize()
myModel = mdb.Model(name=modelname)
cover = float(cover)
lwall = float(lwall)
twall = float(twall)
hwall = float(hwall)
dtube = float(dtube)
ttube = float(ttube)
dlbar = float(dlbar)
dtbar = float(dtbar)
lfd = float(lfd)
tfd = float(tfd)
hfd = float(hfd)
lbl = float(lbl)
tbl = float(tbl)
hbl = float(hbl)
fylbar = float(fylbar)
fytbar = float(fytbar)
fytube = float(fytube)
dis = float(dis)
axld = float(axld)
offset1 = float(offset1)
offset2 = float(offset2)
meshsize = float(meshsize)
space = float(space)

# part
# wall

# Sketch for Wall
s = myModel.ConstrainedSketch(name=modelname, sheetSize=lwall)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-lwall / 2, -twall / 2), point2=(lwall / 2, twall / 2))
s.CircleByCenterPerimeter(center=(-offset1, 0),
                          point1=(-offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset1, 0), point1=(offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(-offset2, 0),
                          point1=(-offset2 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset2, 0), point1=(offset2 + dtube / 2, 0))

# Part for Wall
partwall = myModel.Part(
    name="wall", dimensionality=THREE_D, type=DEFORMABLE_BODY)
partwall = myModel.parts["wall"]
partwall.BaseSolidExtrude(sketch=s, depth=hwall)
p = myModel.parts["wall"]

# Partition cover for Wall
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=-lwall / 2 + cover)
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=lwall / 2 - cover)
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-twall / 2 + cover)
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=twall / 2 - cover)
c = p.cells
d = p.datums
pickedCells = c.findAt(((0, 0, 0),))
p.PartitionCellByDatumPlane(datumPlane=d[2], cells=pickedCells)
pickedCells = c.findAt(((0, 0, 0),))
p.PartitionCellByDatumPlane(datumPlane=d[3], cells=pickedCells)
pickedCells = c.findAt(((0, 0, 0),))
p.PartitionCellByDatumPlane(datumPlane=d[4], cells=pickedCells)
pickedCells = c.findAt(((0, 0, 0),))
p.PartitionCellByDatumPlane(datumPlane=d[5], cells=pickedCells)

# tube
s = myModel.ConstrainedSketch(name="tube", sheetSize=dtube)
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(0, 0), point1=(dtube / 2, 0))
s.CircleByCenterPerimeter(center=(0, 0), point1=(dtube / 2 - ttube, 0))
parttube = myModel.Part(
    name="tube", dimensionality=THREE_D, type=DEFORMABLE_BODY)
parttube = myModel.parts["tube"]
parttube.BaseSolidExtrude(sketch=s, depth=hwall + hbl + hfd)

# in-concrete
s = myModel.ConstrainedSketch(name="in-Concrete", sheetSize=dtube)
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(0, 0), point1=(dtube / 2 - ttube, 0))
partincon = myModel.Part(
    name="in-concrete", dimensionality=THREE_D, type=DEFORMABLE_BODY)
partincon = myModel.parts["in-concrete"]
partincon.BaseSolidExtrude(sketch=s, depth=hwall + hbl + hfd)

# foundation-concrete
s = myModel.ConstrainedSketch(name="foundation-Concrete", sheetSize=lfd)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-lfd / 2, -tfd / 2), point2=(lfd / 2, tfd / 2))
s.CircleByCenterPerimeter(center=(-offset1, 0),
                          point1=(-offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset1, 0), point1=(offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(-offset2, 0),
                          point1=(-offset2 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset2, 0), point1=(offset2 + dtube / 2, 0))
partfoundation = myModel.Part(
    name="foundation-Concrete", dimensionality=THREE_D, type=DEFORMABLE_BODY)
partfoundation = myModel.parts["foundation-Concrete"]
partfoundation.BaseSolidExtrude(sketch=s, depth=hfd)

# loadbeam-concrete
s = myModel.ConstrainedSketch(name="loadbeam-Concrete", sheetSize=lbl)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-lbl / 2, -tbl / 2), point2=(lbl / 2, tbl / 2))
s.CircleByCenterPerimeter(center=(-offset1, 0),
                          point1=(-offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset1, 0), point1=(offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(-offset2, 0),
                          point1=(-offset2 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset2, 0), point1=(offset2 + dtube / 2, 0))
partloadbeam = myModel.Part(
    name="loadbeam-Concrete", dimensionality=THREE_D, type=DEFORMABLE_BODY)
partloadbeam = myModel.parts["loadbeam-Concrete"]
partloadbeam.BaseSolidExtrude(sketch=s, depth=hbl)

# rebar
s = myModel.ConstrainedSketch(name="sheerwall-long-steel", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(hwall - 2 * cover, 0.0))
p = myModel.Part(name="shellwall-long-steel",
                 dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["shellwall-long-steel"]
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name="foundation-long-steel", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(lfd - 2 * cover, 0.0))
p = myModel.Part(name="foundation-long-steel",
                 dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["foundation-long-steel"]
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name="foundation-hoop", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0, 0), point2=(hfd - 2 * cover, tfd / 2 + dtube / 2))
p = myModel.Part(name="foundation-hoop",
                 dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["foundation-hoop"]
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name="loadbeam-long-steel", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(lbl - 2 * cover, 0.0))
p = myModel.Part(name="loadbeam-long-steel",
                 dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["loadbeam-long-steel"]
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name="loadbeam-hoop", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-(tbl / 2 - cover), -(hbl / 2 - cover)),
            point2=((tbl / 2 - cover), (hbl / 2 - cover)))
p = myModel.Part(name="loadbeam-hoop",
                 dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["loadbeam-hoop"]
p.BaseWire(sketch=s)

# size define of sheerwall hoop
hooplength = float(offset1 - offset2)
hoopwidth = float(twall - 2 * cover)
hooplength2 = float(3 * offset2 / 2 - offset1 / 2)

# hoop
s = myModel.ConstrainedSketch(name="sheerwall-hoop-1", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-hooplength / 2, -hoopwidth / 2),
            point2=(hooplength / 2, hoopwidth / 2))
p = myModel.Part(name="sheerwall-hoop-1",
                 dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["sheerwall-hoop-1"]
p.BaseWire(sketch=s)

# hoop
s = myModel.ConstrainedSketch(name="sheerwall-hoop-2", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-hooplength2 / 2, -hoopwidth / 2),
            point2=(hooplength2 / 2, hoopwidth / 2))
p = myModel.Part(name="sheerwall-hoop-2",
                 dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["sheerwall-hoop-2"]
p.BaseWire(sketch=s)

# material
myModel = mdb.models[modelname]
myModel.Material(name="In-Concrete")
myModel.materials["In-Concrete"].Elastic(table=((37500.0, 0.2), ))
myModel.materials["In-Concrete"].Density(table=((2.5e-09, ), ))
myModel.Material(name="Out-Concrete")
myModel.materials["Out-Concrete"].Elastic(table=((35500.0, 0.2), ))
myModel.materials["Out-Concrete"].Density(table=((2.5e-09, ), ))
myModel.Material(name="cover-concrete")
myModel.materials["cover-concrete"].Elastic(table=((35500.0, 0.2),))
myModel.materials["cover-concrete"].Density(table=((2.5e-09,),))
myModel.Material(name="rigid-body")
myModel.materials["rigid-body"].Elastic(table=((38000, 0.2),))
myModel.materials["rigid-body"].Density(table=((2.5e-09,),))
myModel.Material(name="tube")
myModel.materials["tube"].Density(table=((7.85e-09,),))
myModel.materials["tube"].Elastic(table=((200000, 0.3),))
myModel.materials["tube"].Plastic(table=((fytube, 0),))
myModel.Material(name="rebar-l")
myModel.materials["rebar-l"].Density(table=((7.85e-09,),))
myModel.materials["rebar-l"].Elastic(table=((200000, 0.3),))
myModel.materials["rebar-l"].Plastic(hardening=ISOTROPIC,
                                     table=((fylbar, 0.0),))
myModel.Material(name="rebar-t")
myModel.materials["rebar-t"].Density(table=((7.85e-09,),))
myModel.materials["rebar-t"].Elastic(table=((200000, 0.3),))
myModel.materials["rebar-t"].Plastic(hardening=ISOTROPIC,
                                     table=((fytbar, 0.0),))
myModel.Material(name="rebar-rigid")
myModel.materials["rebar-rigid"].Density(table=((7.85e-09,),))
myModel.materials["rebar-rigid"].Elastic(table=((200000, 0.3),))
myModel.materials["rebar-rigid"].Plastic(table=((400, 0.0),))

# section
myModel.HomogeneousSolidSection(
    name="in-con", material="in-concrete", thickness=None)
myModel.HomogeneousSolidSection(
    name="out-con", material="out-concrete", thickness=None)
myModel.HomogeneousSolidSection(
    name="cover-con", material="cover-concrete", thickness=None)
myModel.HomogeneousSolidSection(
    name="rigid-body", material="rigid-body", thickness=None)
myModel.HomogeneousSolidSection(name="tube", material="tube", thickness=None)
myModel.TrussSection(name="rebar-l", material="rebar-l",
                     area=3.1415926 / 4 * dlbar * dlbar)
myModel.TrussSection(name="rebar-t", material="rebar-t",
                     area=3.1415926 / 4 * dtbar * dtbar)
myModel.TrussSection(name="rebar-rigid", material="rebar-rigid", area=100)

# property
# foundation-Concrete
p = mdb.models[modelname].parts["foundation-Concrete"]
region = regionToolset.Region(cells=p.cells[:])
p.SectionAssignment(
    region=region,
    sectionName="rigid-body",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# loadbeam-Concrete
p = mdb.models[modelname].parts["loadbeam-Concrete"]
region = regionToolset.Region(cells=p.cells[:])
p.SectionAssignment(
    region=region,
    sectionName="rigid-body",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# wall
p = mdb.models[modelname].parts["wall"]
c = p.cells.findAt(((0, 0, 0),))
region = regionToolset.Region(cells=c)
p.SectionAssignment(
    region=region,
    sectionName="out-con",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# wall-cover
cells = p.cells.findAt(
    ((1, twall / 2 - 1, 0), ),
    ((1, -twall / 2 + 1, 0), ),
    ((lwall / 2 - 1, 1, 0), ),
    ((-lwall / 2 + 1, 1, 0),),
)
region = regionToolset.Region(cells=cells)
p.SectionAssignment(
    region=region,
    sectionName="cover-con",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# tube
p = mdb.models[modelname].parts["tube"]
region = regionToolset.Region(cells=p.cells[:])
p.SectionAssignment(
    region=region,
    sectionName="tube",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# in-concrete
p = mdb.models[modelname].parts["in-concrete"]
region = regionToolset.Region(cells=p.cells[:])
p.SectionAssignment(
    region=region,
    sectionName="in-con",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# sheerwall-long-steel
p = mdb.models[modelname].parts["shellwall-long-steel"]
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(
    region=region,
    sectionName="rebar-l",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# sheerwall-hoop-1
p = mdb.models[modelname].parts["sheerwall-hoop-1"]
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(
    region=region,
    sectionName="rebar-t",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# sheerwall-hoop-2
p = mdb.models[modelname].parts["sheerwall-hoop-2"]
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(
    region=region,
    sectionName="rebar-t",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# foundation-long-steel
p = mdb.models[modelname].parts["foundation-long-steel"]
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(
    region=region,
    sectionName="rebar-rigid",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# loadbeam-long-steel
p = mdb.models[modelname].parts["loadbeam-long-steel"]
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(
    region=region,
    sectionName="rebar-rigid",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# foundation-hoop
p = mdb.models[modelname].parts["foundation-hoop"]
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(
    region=region,
    sectionName="rebar-rigid",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# loadbeam-hoop
p = mdb.models[modelname].parts["loadbeam-hoop"]
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(
    region=region,
    sectionName="rebar-rigid",
    offset=0.0,
    offsetType=MIDDLE_SURFACE,
    offsetField="",
    thicknessAssignment=FROM_SECTION,
)

# assembly
a = myModel.rootAssembly
#session.viewports["Viewport: 1"].setValues(displayedObject=a)
a.DatumCsysByDefault(CARTESIAN)

p = myModel.parts["wall"]
a.Instance(name="wall", part=p, dependent=ON)

p = myModel.parts["foundation-Concrete"]
a.Instance(name="foundation-Concrete", part=p, dependent=ON)

p = myModel.parts["loadbeam-Concrete"]
a.Instance(name="loadbeam-Concrete", part=p, dependent=ON)

p = myModel.parts["tube"]
a.Instance(name="tube1", part=p, dependent=ON)
a.Instance(name="tube2", part=p, dependent=ON)
a.Instance(name="tube3", part=p, dependent=ON)
a.Instance(name="tube4", part=p, dependent=ON)

p = myModel.parts["in-concrete"]
a.Instance(name="in-concrete1", part=p, dependent=ON)
a.Instance(name="in-concrete2", part=p, dependent=ON)
a.Instance(name="in-concrete3", part=p, dependent=ON)
a.Instance(name="in-concrete4", part=p, dependent=ON)

p = myModel.parts["shellwall-long-steel"]
for i in range(1, 15):
    i = str(i)
    a.Instance(name="sheerwall-long-steel-" + i, part=p, dependent=ON)

hoopnum = int((hwall - 2 * cover) / space) + 1
p = myModel.parts["sheerwall-hoop-1"]
for i in range(1, hoopnum + 1):
    a.Instance(name="sheerwall-hoop-11-" + str(i), part=p, dependent=ON)
    a.Instance(name="sheerwall-hoop-12-" + str(i), part=p, dependent=ON)
    a.Instance(name="sheerwall-hoop-13-" + str(i), part=p, dependent=ON)
    a.Instance(name="sheerwall-hoop-14-" + str(i), part=p, dependent=ON)
p = myModel.parts["sheerwall-hoop-2"]
for i in range(1, hoopnum + 1):
    a.Instance(name="sheerwall-hoop-21-" + str(i), part=p, dependent=ON)
    a.Instance(name="sheerwall-hoop-22-" + str(i), part=p, dependent=ON)

lhoopnum = int((lbl / 2 - offset1 - dtube / 2 - 2 * cover) / 50) + 1
fhoopnum = int((lfd / 2 - offset1 - dtube / 2 - 2 * cover) / 50) + 1
midhoopnum = int((2 * offset2 - dtube - 2 * cover) / 50) + 1

p = myModel.parts["loadbeam-hoop"]
for i in range(1, lhoopnum + 1):
    a.Instance(name="loadbeam-hoop-1-" + str(i), part=p, dependent=ON)
    a.Instance(name="loadbeam-hoop-2-" + str(i), part=p, dependent=ON)
for i in range(1, midhoopnum + 1):
    a.Instance(name="loadbeam-hoop-3-" + str(i), part=p, dependent=ON)
p = myModel.parts["foundation-hoop"]
for i in range(1, fhoopnum + 1):
    a.Instance(name="foundation-hoop-1-" + str(i), part=p, dependent=ON)
    a.Instance(name="foundation-hoop-2-" + str(i), part=p, dependent=ON)
    a.Instance(name="foundation-hoop-3-" + str(i), part=p, dependent=ON)
    a.Instance(name="foundation-hoop-4-" + str(i), part=p, dependent=ON)
for i in range(1, midhoopnum + 1):
    a.Instance(name="foundation-hoop-5-" + str(i), part=p, dependent=ON)
    a.Instance(name="foundation-hoop-6-" + str(i), part=p, dependent=ON)

for i in range(1, midhoopnum + 1):
    a = mdb.models[modelname].rootAssembly
    a.rotate(
        instanceList=("loadbeam-hoop-3-" + str(i),),
        axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1, 0.0),
        angle=-90.0,
    )
    a.rotate(
        instanceList=("foundation-hoop-5-" + str(i),),
        axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1, 0.0),
        angle=90.0,
    )
    a.rotate(
        instanceList=("foundation-hoop-6-" + str(i),),
        axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1, 0.0),
        angle=90.0,
    )

for i in range(1, lhoopnum + 1):
    a = mdb.models[modelname].rootAssembly
    a.rotate(
        instanceList=("loadbeam-hoop-1-" + str(i),),
        axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1, 0.0),
        angle=-90.0,
    )
    a.rotate(
        instanceList=("loadbeam-hoop-2-" + str(i),),
        axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1, 0.0),
        angle=-90.0,
    )

for i in range(1, fhoopnum + 1):
    a = mdb.models[modelname].rootAssembly
    a.rotate(
        instanceList=("foundation-hoop-1-" + str(i),),
        axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1, 0.0),
        angle=90.0,
    )
    a.rotate(
        instanceList=("foundation-hoop-2-" + str(i),),
        axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1, 0.0),
        angle=90.0,
    )
    a.rotate(
        instanceList=("foundation-hoop-3-" + str(i),),
        axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1, 0.0),
        angle=90.0,
    )
    a.rotate(
        instanceList=("foundation-hoop-4-" + str(i),),
        axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1, 0.0),
        angle=90.0,
    )

p = myModel.parts["foundation-long-steel"]
for i in range(1, 9):
    a.Instance(name="foundation-long-steel-" + str(i), part=p, dependent=ON)
p = myModel.parts["loadbeam-long-steel"]
for i in range(1, 5):
    a.Instance(name="loadbeam-long-steel-" + str(i), part=p, dependent=ON)

# install
a.translate(instanceList=("foundation-Concrete",), vector=(0.0, 0.0, -hfd))
a.translate(instanceList=("loadbeam-Concrete",), vector=(0.0, 0.0, hwall))
a.translate(instanceList=("tube1",), vector=(offset1, 0.0, -hfd))
a.translate(instanceList=("tube2",), vector=(-offset1, 0.0, -hfd))
a.translate(instanceList=("tube3",), vector=(offset2, 0.0, -hfd))
a.translate(instanceList=("tube4",), vector=(-offset2, 0.0, -hfd))
a.translate(instanceList=("in-concrete1",), vector=(offset1, 0.0, -hfd))
a.translate(instanceList=("in-concrete2",), vector=(-offset1, 0.0, -hfd))
a.translate(instanceList=("in-concrete3",), vector=(offset2, 0.0, -hfd))
a.translate(instanceList=("in-concrete4",), vector=(-offset2, 0.0, -hfd))
for i in range(1, 15):
    i = str(i)
    a.rotate(
        instanceList=("sheerwall-long-steel-" + i,),
        axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1, 0.0),
        angle=-90.0,
    )

a.translate(
    instanceList=("sheerwall-long-steel-1",),
    vector=(-(offset1 * 1.5 - offset2 / 2), twall / 2 - cover, cover),
)
a.translate(
    instanceList=("sheerwall-long-steel-2",),
    vector=(offset1 * 1.5 - offset2 / 2, twall / 2 - cover, cover),
)
a.translate(
    instanceList=("sheerwall-long-steel-3",),
    vector=(-(offset1 * 1.5 - offset2 / 2), -(twall / 2 - cover), cover),
)
a.translate(
    instanceList=("sheerwall-long-steel-4",),
    vector=(offset1 * 1.5 - offset2 / 2, -(twall / 2 - cover), cover),
)

a.translate(
    instanceList=("sheerwall-long-steel-5",),
    vector=(-(offset1 + offset2) / 2, twall / 2 - cover, cover),
)
a.translate(
    instanceList=("sheerwall-long-steel-6",),
    vector=((offset1 + offset2) / 2, twall / 2 - cover, cover),
)
a.translate(
    instanceList=("sheerwall-long-steel-7",),
    vector=(-(offset1 + offset2) / 2, -(twall / 2 - cover), cover),
)
a.translate(
    instanceList=("sheerwall-long-steel-8",),
    vector=((offset1 + offset2) / 2, -(twall / 2 - cover), cover),
)

a.translate(
    instanceList=("sheerwall-long-steel-9",),
    vector=(-(offset2 * 1.5 - offset1 / 2), twall / 2 - cover, cover),
)
a.translate(
    instanceList=("sheerwall-long-steel-10",),
    vector=(offset2 * 1.5 - offset1 / 2, twall / 2 - cover, cover),
)
a.translate(
    instanceList=("sheerwall-long-steel-11",),
    vector=(-(offset2 * 1.5 - offset1 / 2), -(twall / 2 - cover), cover),
)
a.translate(
    instanceList=("sheerwall-long-steel-12",),
    vector=(offset2 * 1.5 - offset1 / 2, -(twall / 2 - cover), cover),
)

a.translate(
    instanceList=("sheerwall-long-steel-13",),
    vector=(0, twall / 2 - cover, cover)
)
a.translate(
    instanceList=("sheerwall-long-steel-14",),
    vector=(0, -(twall / 2 - cover), cover)
)

for i in range(1, hoopnum + 1):
    a.translate(
        instanceList=("sheerwall-hoop-11-" + str(i),), 
        vector=(offset1, 0, cover + (i - 1) * space)
    )
    a.translate(
        instanceList=("sheerwall-hoop-12-" + str(i),),
        vector=(-offset1, 0, cover + (i - 1) * space + dtbar),
    )
    a.translate(
        instanceList=("sheerwall-hoop-13-" + str(i),),
        vector=(offset2, 0, cover + (i - 1) * space + dtbar),
    )
    a.translate(
        instanceList=("sheerwall-hoop-14-" + str(i),),
        vector=(-offset2, 0, cover + (i - 1) * space),
    )
    a.translate(
        instanceList=("sheerwall-hoop-21-" + str(i),),
        vector=((hooplength2) / 2, 0, cover + (i - 1) * space),
    )
    a.translate(
        instanceList=("sheerwall-hoop-22-" + str(i),),
        vector=(-(hooplength2) / 2, 0, cover + (i - 1) * space + dtbar),
    )

for i in range(1, fhoopnum + 1):
    a.translate(
        instanceList=("foundation-hoop-1-" + str(i),),
        vector=(lfd / 2 - cover - (i - 1) * 50, -(tfd / 2 - cover), -cover),
    )
    a.translate(
        instanceList=("foundation-hoop-2-" + str(i),),
        vector=(lfd / 2 - cover - (i - 1) * 50, -(dtube / 2 + cover), -cover),
    )
    a.translate(
        instanceList=("foundation-hoop-3-" + str(i),),
        vector=(-(lfd / 2 - cover - (i - 1) * 50), -(tfd / 2 - cover), -cover),
    )
    a.translate(
        instanceList=("foundation-hoop-4-" + str(i),),
        vector=(-(lfd / 2 - cover - (i - 1) * 50), -
                (dtube / 2 + cover), -cover),
    )

for i in range(1, lhoopnum + 1):
    a.translate(
        instanceList=("loadbeam-hoop-1-" + str(i),),
        vector=(lbl / 2 - cover - (i - 1) * 50, 0, hwall + hbl / 2),
    )
    a.translate(
        instanceList=("loadbeam-hoop-2-" + str(i),),
        vector=(-(lbl / 2 - cover - (i - 1) * 50), 0, hwall + hbl / 2),
    )
for i in range(1, midhoopnum + 1):
    a.translate(
        instanceList=("loadbeam-hoop-3-" + str(i),),
        vector=(((-1) ** i) * (int(i / 2)) * 50, 0, hwall + hbl / 2),
    )
    a.translate(
        instanceList=("foundation-hoop-5-" + str(i),),
        vector=(((-1) ** i) * (int(i / 2)) * 50, -(dtube / 2 + cover), -cover),
    )
    a.translate(
        instanceList=("foundation-hoop-6-" + str(i),),
        vector=(((-1) ** i) * (int(i / 2)) * 50, -(tfd / 2 - cover), -cover),
    )

a.translate(
    instanceList=("foundation-long-steel-1",), vector=(-lfd / 2 + cover, tfd / 2 - cover, -cover)
)
a.translate(
    instanceList=("foundation-long-steel-2",), vector=(-lfd / 2 + cover, -(tfd / 2 - cover), -cover)
)
a.translate(
    instanceList=("foundation-long-steel-3",),
    vector=(-lfd / 2 + cover, -(tfd / 2 - cover), -hfd + cover),
)
a.translate(
    instanceList=("foundation-long-steel-4",),
    vector=(-lfd / 2 + cover, tfd / 2 - cover, -hfd + cover),
)
a.translate(
    instanceList=("foundation-long-steel-5",),
    vector=(-lfd / 2 + cover, -(dtube / 2 + cover), -cover),
)
a.translate(
    instanceList=("foundation-long-steel-6",),
    vector=(-lfd / 2 + cover, dtube / 2 + cover, -cover)
)
a.translate(
    instanceList=("foundation-long-steel-7",),
    vector=(-lfd / 2 + cover, dtube / 2 + cover, -hfd + cover),
)
a.translate(
    instanceList=("foundation-long-steel-8",),
    vector=(-lfd / 2 + cover, -(dtube / 2 + cover), -hfd + cover),
)

a.translate(
    instanceList=("loadbeam-long-steel-1",),
    vector=(-lbl / 2 + cover, -(tbl / 2 - cover), hwall + hbl - cover),
)
a.translate(
    instanceList=("loadbeam-long-steel-2",),
    vector=(-lbl / 2 + cover, tbl / 2 - cover, hwall + hbl - cover),
)
a.translate(
    instanceList=("loadbeam-long-steel-3",),
    vector=(-lbl / 2 + cover, -(tbl / 2 - cover), hwall + cover),
)
a.translate(
    instanceList=("loadbeam-long-steel-4",),
    vector=(-lbl / 2 + cover, tbl / 2 - cover, hwall + cover),
)

# merge-rebar & embedd rebar
ins = (a.instances["sheerwall-long-steel-1"],)
for i in range(2, 15):
    ins = ins + (a.instances["sheerwall-long-steel-" + str(i)],)
for i in range(1, hoopnum + 1):
    ins = ins + (a.instances["sheerwall-hoop-11-" + str(i)],)
    ins = ins + (a.instances["sheerwall-hoop-12-" + str(i)],)
    ins = ins + (a.instances["sheerwall-hoop-13-" + str(i)],)
    ins = ins + (a.instances["sheerwall-hoop-14-" + str(i)],)
    ins = ins + (a.instances["sheerwall-hoop-21-" + str(i)],)
    ins = ins + (a.instances["sheerwall-hoop-22-" + str(i)],)
a.InstanceFromBooleanMerge(
    name="merge-rebar", instances=ins, originalInstances=DELETE, domain=GEOMETRY
)
e = a.instances["merge-rebar-1"].edges
region1 = regionToolset.Region(edges=e[:])
mdb.models[modelname].EmbeddedRegion(
    name="steel-embed",
    embeddedRegion=region1,
    hostRegion=None,
    weightFactorTolerance=1e-06,
    absoluteTolerance=0.0,
    fractionalTolerance=0.05,
    toleranceMethod=BOTH,
)

ins = (a.instances["loadbeam-long-steel-1"],)
for i in range(2, 5):
    ins = ins + (a.instances["loadbeam-long-steel-" + str(i)],)
for i in range(1, lhoopnum + 1):
    ins = ins + (a.instances["loadbeam-hoop-1-" + str(i)],)
    ins = ins + (a.instances["loadbeam-hoop-2-" + str(i)],)
for i in range(1, midhoopnum + 1):
    ins = ins + (a.instances["loadbeam-hoop-3-" + str(i)],)
a.InstanceFromBooleanMerge(
    name="merge-rebar-l", instances=ins, originalInstances=DELETE, domain=GEOMETRY
)
e = a.instances["merge-rebar-l-1"].edges
region1 = regionToolset.Region(edges=e[:])
mdb.models[modelname].EmbeddedRegion(
    name="l-steel-embed",
    embeddedRegion=region1,
    hostRegion=None,
    weightFactorTolerance=1e-06,
    absoluteTolerance=0.0,
    fractionalTolerance=0.05,
    toleranceMethod=BOTH,
)

ins = (a.instances["foundation-long-steel-1"],)
for i in range(2, 9):
    ins = ins + (a.instances["foundation-long-steel-" + str(i)],)
for i in range(1, fhoopnum + 1):
    ins = ins + (a.instances["foundation-hoop-1-" + str(i)],)
    ins = ins + (a.instances["foundation-hoop-2-" + str(i)],)
    ins = ins + (a.instances["foundation-hoop-3-" + str(i)],)
    ins = ins + (a.instances["foundation-hoop-4-" + str(i)],)
for i in range(1, midhoopnum + 1):
    ins = ins + (a.instances["foundation-hoop-5-" + str(i)],)
    ins = ins + (a.instances["foundation-hoop-6-" + str(i)],)
a.InstanceFromBooleanMerge(
    name="merge-rebar-f", instances=ins, originalInstances=DELETE, domain=GEOMETRY
)
e = a.instances["merge-rebar-f-1"].edges
region1 = regionToolset.Region(edges=e[:])
mdb.models[modelname].EmbeddedRegion(
    name="f-steel-embed",
    embeddedRegion=region1,
    hostRegion=None,
    weightFactorTolerance=1e-06,
    absoluteTolerance=0.0,
    fractionalTolerance=0.05,
    toleranceMethod=BOTH,
)

# interaction
# a1 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a1.instances["wall"].faces
# side1Faces1 = s1.findAt(
#     ((1, 1, hwall),),
#     ((1, twall / 2 - 1, hwall),),
#     ((1, -twall / 2 + 1, hwall),),
#     ((lwall / 2 - 1, 1, hwall),),
#     ((-lwall / 2 + 1, 1, hwall),),
# )
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a1 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a1.instances["loadbeam"].faces
# side1Faces1 = s1.findAt(((1, 1, hwall),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="wall-loadbeam",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a2 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a2.instances["foundation"].faces
# side1Faces1 = s1.findAt(((1, 1, 0),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a2 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a2.instances["wall"].faces
# side1Faces1 = s1.findAt(
#     ((1, 1, 0),),
#     ((1, twall / 2 - 1, 0),),
#     ((1, -twall / 2 + 1, 0),),
#     ((lwall / 2 - 1, 1, 0),),
#     ((-lwall / 2 + 1, 1, 0),),
# )
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="wall-foundation",
#     master=region2,
#     slave=region1,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube1"].faces
# side1Faces1 = s1.findAt(((offset1 + dtube / 2, 0, hwall - 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["wall"].faces
# side1Faces1 = s1.findAt(((offset1 + dtube / 2, 0, hwall - 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="wall-tube1",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube2"].faces
# side1Faces1 = s1.findAt(((-offset1 + dtube / 2, 0, hwall - 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["wall"].faces
# side1Faces1 = s1.findAt(((-offset1 + dtube / 2, 0, hwall - 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="wall-tube2",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube3"].faces
# side1Faces1 = s1.findAt(((offset2 + dtube / 2, 0, hwall - 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["wall"].faces
# side1Faces1 = s1.findAt(((offset2 + dtube / 2, 0, hwall - 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="wall-tube3",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube4"].faces
# side1Faces1 = s1.findAt(((-offset2 + dtube / 2, 0, hwall - 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["wall"].faces
# side1Faces1 = s1.findAt(((-offset2 + dtube / 2, 0, hwall - 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="wall-tube4",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube1"].faces
# side1Faces1 = s1.findAt(((offset1 + dtube / 2, 0, -1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["foundation"].faces
# side1Faces1 = s1.findAt(((offset1 + dtube / 2, 0, -1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="fd-tube1",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube2"].faces
# side1Faces1 = s1.findAt(((-offset1 + dtube / 2, 0, -1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["foundation"].faces
# side1Faces1 = s1.findAt(((-offset1 + dtube / 2, 0, -1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="fd-tube2",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube3"].faces
# side1Faces1 = s1.findAt(((offset2 + dtube / 2, 0, -1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["foundation"].faces
# side1Faces1 = s1.findAt(((offset2 + dtube / 2, 0, -1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="fd-tube3",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube4"].faces
# side1Faces1 = s1.findAt(((-offset2 + dtube / 2, 0, -1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["foundation"].faces
# side1Faces1 = s1.findAt(((-offset2 + dtube / 2, 0, -1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="fd-tube4",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube1"].faces
# side1Faces1 = s1.findAt(((offset1 + dtube / 2, 0, hwall + 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["loadbeam"].faces
# side1Faces1 = s1.findAt(((offset1 + dtube / 2, 0, hwall + 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="lb-tube1",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube2"].faces
# side1Faces1 = s1.findAt(((-offset1 + dtube / 2, 0, hwall + 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["loadbeam"].faces
# side1Faces1 = s1.findAt(((-offset1 + dtube / 2, 0, hwall + 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="lb-tube2",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube3"].faces
# side1Faces1 = s1.findAt(((offset2 + dtube / 2, 0, hwall + 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["loadbeam"].faces
# side1Faces1 = s1.findAt(((offset2 + dtube / 2, 0, hwall + 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="lb-tube3",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube4"].faces
# side1Faces1 = s1.findAt(((-offset2 + dtube / 2, 0, hwall + 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["loadbeam"].faces
# side1Faces1 = s1.findAt(((-offset2 + dtube / 2, 0, hwall + 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="lb-tube4",
#     master=region1,
#     slave=region2,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube1"].faces
# side1Faces1 = s1.findAt(((offset1 + dtube / 2 - ttube, 0, hwall - 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["in-concrete1"].faces
# side1Faces1 = s1.findAt(((offset1 + dtube / 2 - ttube, 0, hwall - 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="incon-tube1",
#     master=region2,
#     slave=region1,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube2"].faces
# side1Faces1 = s1.findAt(((-offset1 + dtube / 2 - ttube, 0, hwall - 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["in-concrete2"].faces
# side1Faces1 = s1.findAt(((-offset1 + dtube / 2 - ttube, 0, hwall - 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="incon-tube2",
#     master=region2,
#     slave=region1,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube3"].faces
# side1Faces1 = s1.findAt(((offset2 + dtube / 2 - ttube, 0, hwall - 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["in-concrete3"].faces
# side1Faces1 = s1.findAt(((offset2 + dtube / 2 - ttube, 0, hwall - 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="incon-tube3",
#     master=region2,
#     slave=region1,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )
#
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["tube4"].faces
# side1Faces1 = s1.findAt(((-offset2 + dtube / 2 - ttube, 0, hwall - 1),))
# region1 = regionToolset.Region(side1Faces=side1Faces1)
# a4 = mdb.models["Model-NewShearWall"].rootAssembly
# s1 = a4.instances["in-concrete4"].faces
# side1Faces1 = s1.findAt(((-offset2 + dtube / 2 - ttube, 0, hwall - 1),))
# region2 = regionToolset.Region(side1Faces=side1Faces1)
# mdb.models["Model-NewShearWall"].Tie(
#     name="incon-tube4",
#     master=region2,
#     slave=region1,
#     positionToleranceMethod=COMPUTED,
#     adjust=ON,
#     tieRotations=ON,
#     thickness=ON,
# )

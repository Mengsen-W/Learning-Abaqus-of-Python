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
## wall

### Sketch for Wall
s = myModel.ConstrainedSketch(name=modelname, sheetSize=lwall)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-lwall / 2, -twall / 2), point2=(lwall / 2, twall / 2))
s.CircleByCenterPerimeter(center=(-offset1, 0), point1=(-offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset1, 0), point1=(offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(-offset2, 0), point1=(-offset2 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset2, 0), point1=(offset2 + dtube / 2, 0))

### Part for Wall
partwall = myModel.Part(name="wall", dimensionality=THREE_D, type=DEFORMABLE_BODY)
partwall = myModel.parts["wall"]
partwall.BaseSolidExtrude(sketch=s, depth=hwall)
p = myModel.parts["wall"]

### Partition cover for Wall
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=-lwall / 2 + cover)
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=lwall / 2 - cover)
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=-twall / 2 + cover)
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=twall / 2 - cover)
c = p.cells
d = p.datums
pickedCells = c.findAt(((0, 0, 1),))
p.PartitionCellByDatumPlane(datumPlane=d[2], cells=pickedCells)
pickedCells = c.findAt(((0, 0, 1),))
p.PartitionCellByDatumPlane(datumPlane=d[3], cells=pickedCells)
pickedCells = c.findAt(((0, 0, 1),))
p.PartitionCellByDatumPlane(datumPlane=d[4], cells=pickedCells)
pickedCells = c.findAt(((0, 0, 1),))
p.PartitionCellByDatumPlane(datumPlane=d[5], cells=pickedCells)

##tube
s = myModel.ConstrainedSketch(name="tube", sheetSize=dtube)
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(0, 0), point1=(dtube / 2, 0))
s.CircleByCenterPerimeter(center=(0, 0), point1=(dtube / 2 - ttube, 0))
parttube = myModel.Part(name="tube", dimensionality=THREE_D, type=DEFORMABLE_BODY)
parttube = myModel.parts["tube"]
parttube.BaseSolidExtrude(sketch=s, depth=hwall + hbl + hfd)

## in-concrete
s = myModel.ConstrainedSketch(name="in-Concrete", sheetSize=dtube)
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(0, 0), point1=(dtube / 2 - ttube, 0))
partincon = myModel.Part(name="in-concrete", dimensionality=THREE_D, type=DEFORMABLE_BODY)
partincon = myModel.parts["in-concrete"]
partincon.BaseSolidExtrude(sketch=s, depth=hwall + hbl + hfd)

## foundation-concrete
s = myModel.ConstrainedSketch(name="foundation-Concrete", sheetSize=lfd)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-lfd / 2, -tfd / 2), point2=(lfd / 2, tfd / 2))
s.CircleByCenterPerimeter(center=(-offset1, 0), point1=(-offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset1, 0), point1=(offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(-offset2, 0), point1=(-offset2 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset2, 0), point1=(offset2 + dtube / 2, 0))
partfoundation = myModel.Part(name="foundation-Concrete", dimensionality=THREE_D, type=DEFORMABLE_BODY)
partfoundation = myModel.parts["foundation-Concrete"]
partfoundation.BaseSolidExtrude(sketch=s, depth=hfd)

##loadbeam-concrete
s = myModel.ConstrainedSketch(name="loadbeam-Concrete", sheetSize=lbl)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-lbl / 2, -tbl / 2), point2=(lbl / 2, tbl / 2))
s.CircleByCenterPerimeter(center=(-offset1, 0), point1=(-offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset1, 0), point1=(offset1 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(-offset2, 0), point1=(-offset2 + dtube / 2, 0))
s.CircleByCenterPerimeter(center=(offset2, 0), point1=(offset2 + dtube / 2, 0))
partloadbeam = myModel.Part(name="loadbeam-Concrete", dimensionality=THREE_D, type=DEFORMABLE_BODY)
partloadbeam = myModel.parts["loadbeam-Concrete"]
partloadbeam.BaseSolidExtrude(sketch=s, depth=hbl)

##rebar
s = myModel.ConstrainedSketch(name="sheerwall-long-steel", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(hwall - 2 * cover, 0.0))
p = myModel.Part(name="shellwall-long-steel", dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["shellwall-long-steel"]
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name="foundation-long-steel", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(lfd - 2 * cover, 0.0))
p = myModel.Part(name="foundation-long-steel", dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["foundation-long-steel"]
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name="foundation-hoop", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0, 0), point2=(hfd - 2 * cover, tfd / 2 + dtube / 2))
p = myModel.Part(name="foundation-hoop", dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["foundation-hoop"]
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name="loadbeam-long-steel", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(lbl - 2 * cover, 0.0))
p = myModel.Part(name="loadbeam-long-steel", dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["loadbeam-long-steel"]
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name="loadbeam-hoop", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-(tbl / 2 - cover), -(hbl / 2 - cover)), point2=((tbl / 2 - cover), (hbl / 2 - cover)))
p = myModel.Part(name="loadbeam-hoop", dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["loadbeam-hoop"]
p.BaseWire(sketch=s)

# size define of sheerwall hoop
hooplength = float(offset1 - offset2)
hoopwidth = float(twall - 2 * cover)
hooplength2 = float(3 * offset2 / 2 - offset1 / 2)

##hoop
s = myModel.ConstrainedSketch(name="sheerwall-hoop-1", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-hooplength / 2, -hoopwidth / 2), point2=(hooplength / 2, hoopwidth / 2))
p = myModel.Part(name="sheerwall-hoop-1", dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["sheerwall-hoop-1"]
p.BaseWire(sketch=s)

##hoop
s = myModel.ConstrainedSketch(name="sheerwall-hoop-2", sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-hooplength2 / 2, -hoopwidth / 2), point2=(hooplength2 / 2, hoopwidth / 2))
p = myModel.Part(name="sheerwall-hoop-2", dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts["sheerwall-hoop-2"]
p.BaseWire(sketch=s)

# material
myModel = mdb.models[modelname]
myModel.Material(name = "In-Concrete")
myModel.materials["In-Concrete"].Elastic(table = ((37500.0, 0.2), ))
myModel.materials["In-Concrete"].Density(table = ((2.5e-09, ), ))
myModel.Material(name = "Out-Concrete")
myModel.materials["Out-Concrete"].Elastic(table = ((35500.0, 0.2), ))
myModel.materials["Out-Concrete"].Density(table = ((2.5e-09, ), ))
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
myModel.materials["rebar-l"].Plastic(hardening=ISOTROPIC, table=((fylbar, 0.0),))
myModel.Material(name="rebar-t")
myModel.materials["rebar-t"].Density(table=((7.85e-09,),))
myModel.materials["rebar-t"].Elastic(table=((200000, 0.3),))
myModel.materials["rebar-t"].Plastic(hardening=ISOTROPIC, table=((fytbar, 0.0),))
myModel.Material(name="rebar-rigid")
myModel.materials["rebar-rigid"].Density(table=((7.85e-09,),))
myModel.materials["rebar-rigid"].Elastic(table=((200000, 0.3),))
myModel.materials["rebar-rigid"].Plastic(table=((400, 0.0),))

# section
myModel.HomogeneousSolidSection(name="in-con", material="in-concrete", thickness=None)
myModel.HomogeneousSolidSection(name="out-con", material="out-concrete", thickness=None)
myModel.HomogeneousSolidSection(name="cover-con", material="cover-concrete", thickness=None)
myModel.HomogeneousSolidSection(name="rigid-body", material="rigid-body", thickness=None)
myModel.HomogeneousSolidSection(name="tube", material="tube", thickness=None)
myModel.TrussSection(name="rebar-l", material="rebar-l", area=3.1415926 / 4 * dlbar * dlbar)
myModel.TrussSection(name="rebar-t", material="rebar-t", area=3.1415926 / 4 * dtbar * dtbar)
myModel.TrussSection(name="rebar-rigid", material="rebar-rigid", area=100)

# property
# p = mdb.models["Model-NewShearWall"].parts["foundation"]
# region = regionToolset.Region(cells=p.cells[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="rigid-body",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["loadbeam"]
# region = regionToolset.Region(cells=p.cells[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="rigid-body",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["wall"]
# c = p.cells
# cells = c.findAt(((1, 1, 0),))
# region = regionToolset.Region(cells=cells)
# p.SectionAssignment(
#     region=region,
#     sectionName="out-con",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
# cells = c.findAt(
#     ((1, twall / 2 - 1, 0),),
#     ((1, -twall / 2 + 1, 0),),
#     ((lwall / 2 - 1, 1, 0),),
#     ((-lwall / 2 + 1, 1, 0),),
# )
# region = regionToolset.Region(cells=cells)
# p.SectionAssignment(
#     region=region,
#     sectionName="cover-con",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["tube"]
# region = regionToolset.Region(cells=p.cells[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="tube",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["in-concrete"]
# region = regionToolset.Region(cells=p.cells[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="in-con",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["lsteel"]
# region = regionToolset.Region(edges=p.edges[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="rebar-l",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["hoop1"]
# region = regionToolset.Region(edges=p.edges[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="rebar-t",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["hoop2"]
# region = regionToolset.Region(edges=p.edges[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="rebar-t",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["f-lsteel"]
# region = regionToolset.Region(edges=p.edges[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="rebar-rigid",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["l-lsteel"]
# region = regionToolset.Region(edges=p.edges[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="rebar-rigid",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["f-hoop"]
# region = regionToolset.Region(edges=p.edges[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="rebar-rigid",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
#
# p = mdb.models["Model-NewShearWall"].parts["l-hoop"]
# region = regionToolset.Region(edges=p.edges[:])
# p.SectionAssignment(
#     region=region,
#     sectionName="rebar-rigid",
#     offset=0.0,
#     offsetType=MIDDLE_SURFACE,
#     offsetField="",
#     thicknessAssignment=FROM_SECTION,
# )
# assembly

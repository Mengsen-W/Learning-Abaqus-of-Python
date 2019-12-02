"""
 * @Author: Mengsen.Wang
 * @Date: 2019-12-02 19:05:58
 * @Last Modified by:   Mengsen.Wang
 * @Last Modified time: 2019-12-02 19:05:58
"""
# coding = utf-8

# import module for abaqus
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


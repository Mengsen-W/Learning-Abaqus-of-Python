'''
 * @Author: Mengsen.Wang
 * @Date: 2019-12-15 09:56:27
 * @Last Modified by:   Mengsen.Wang
 * @Last Modified time: 2019-12-17 18:06:07
'''
# coding=utf-8
from abaqus import *
from abaqusConstants import *
from caeModules import *
import math


class MyModel:
    """MyModel Class"""
    """init public members"""
    modelName = "SheerWall"
    coverFoundation = 20.0
    longFoundation = 1200.0
    highFoundation = 600.0
    thicknessFoundation = 600.0
    coverSheerWall = 20.0
    longSheerWall = 800.0
    highSheerWall = 1200.0
    thicknessSheerWall = 200.0
    coverLoadBeam = 20.0
    longLoadBeam = 1000.0
    highLoadBeam = 600.0
    thicknessLoadBeam = 600.0
    diameterLongitudinalBar = 10
    betweenLongitudinalBar = 80
    diameterTransversalBar = 8
    betweenTransversalBar = 80
    yieldStressLongitudinalBar = 400
    yieldStressTransversalBar = 300
    displacement = 35
    axialLoad = 3000000
    meshSize = 50
    jobName = 'SheerWall-Job'

    """setting parameters fot private"""
    parameters = (
        ("Model Name:", "ShearWall"),
        ("Cover(wall)(mm):", "20"),
        ("Length(wall)(mm):", "800"),
        ("Thickness(wall)(mm):", "200"),
        ("Height(wall)(mm):", "1200"),
        ("Diameter(longitudinal bar)(mm):", "10"),
        ("Diameter(transversal bar)(mm):", "8"),
        ("Length(foundation)(mm):", "1200"),
        ("Thickness(foundation)(mm):", "600"),
        ("Height(foundation)(mm):", "600"),
        ("Cover(foundation)(mm):", "20"),
        ("Length(loadbeam)(mm):", "1000"),
        ("Thickness(loadbeam)(mm):", "300"),
        ("Height(loadbeam)(mm):", "600"),
        ("Cover(loadbeam)(mm):", "20"),
        ("Yield stress(longitudinal bar)(N/mm):", "400"),
        ("Space between longitudinal bar", "80"),
        ("Yield stress(transversal bar)(N/mm):", "300"),
        ("Space between transversal bar", "80"),
        ("Displacement(maximum)(mm):", "35"),
        ("axial-load(KN):", "3000000"),
        ("Mesh Size(mm):", "50"),
        ("Job Name:", "Job-NewShearWall-01"),
    )

    def __init__(self):
        self.Input()

    def Input(self):
        """Input Parameters"""
        (modelName,
         coverFoundation, longFoundation, thicknessFoundation, highFoundation,
         coverSheerWall, longSheerWall, highSheerWall, thicknessSheerWall,
         coverLoadBeam, longLoadBeam, highLoadBeam, thicknessLoadBeam,
         diameterLongitudinalBar, betweenLongitudinalBar,
         diameterTransversalBar, betweenTransversalBar,
         yieldStressLongitudinalBar, yieldStressTransversalBar,
         displacement, axialLoad, meshSize, jobName,
         ) = getInputs(
            fields=self.parameters, label="Please Input The Parameter", dialogTitle="Parameter Input"
        )
        myModel = mdb.Model(name=modelName)
        self.coverFoundation = float(coverFoundation)
        self.longFoundation = float(longFoundation)
        self.thicknessFoundation = float(thicknessFoundation)
        self.highFoundation = float(highFoundation)
        self.coverSheerWall = float(coverSheerWall)
        self.longSheerWall = float(longSheerWall)
        self.highSheerWall = float(highSheerWall)
        self.thicknessSheerWall = float(thicknessSheerWall)
        self.coverLoadBeam = float(coverLoadBeam)
        self.longLoadBeam = float(longLoadBeam)
        self.highLoadBeam = float(highLoadBeam)
        self.thicknessLoadBeam = float(thicknessLoadBeam)
        self.diameterLongitudinalBar = float(diameterLongitudinalBar)
        self.betweenLongitudinalBar = float(betweenLongitudinalBar)
        self.diameterTransversalBar = float(diameterTransversalBar)
        self.betweenTransversalBar = float(betweenTransversalBar)
        self.yieldStressLongitudinalBar = float(yieldStressLongitudinalBar)
        self.yieldStressTransversalBar = float(yieldStressTransversalBar)
        self.displacement = float(displacement)
        self.axialLoad = float(axialLoad)
        self.meshSize = float(meshSize)
        self.jobName = 'SheerWall-Job'


class Foundation(MyModel):
    pass


class SheerWall(MyModel):
    pass


class LoadBeam(MyModel):
    pass


class InteractionInstance:
    pass


class StepMyModel:
    pass


class BoundaryLoad:
    pass


class MashMyModel:
    pass


class JobMyModel:
    pass

sheerwall = MyModel()



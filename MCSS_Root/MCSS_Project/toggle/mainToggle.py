from ..helpers import helpersMain
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import maya.OpenMaya as om
import json

#################################################################################################
# Module Description:
# This module holds all toggle relate functions to execute as scripts in custom shelf
#
#
#################################################################################################
#
#


def ToggleHistory(*args, **kwargs):

    historyNode = 'historyHolderNode'
    #
    if cmds.objExists(historyNode):
        historyData = cmds.getAttr(historyNode + '.historyData')

        # restore
        converted = json.loads(historyData)

        for itm, value in converted.items():
            cmds.setAttr(itm + ".isHistoricallyInteresting", value)

        cmds.delete(historyNode)
        om.MGlobal.displayInfo(" History Restored ")
        return

    else:
        cmds.createNode('transform', n=historyNode)
        cmds.addAttr(historyNode, ln='historyData', dt='string')
        cmds.setAttr(historyNode + '.template', 1)
        cmds.setAttr(historyNode + '.hiddenInOutliner', 1)

        allObjects = cmds.ls()
        dictTemp = {}

        for itm in allObjects:
            dictTemp[itm] = cmds.getAttr(itm + ".isHistoricallyInteresting")
            cmds.setAttr(itm + ".isHistoricallyInteresting", 0)

        jsonformat = json.dumps(dictTemp)
        cmds.setAttr(historyNode + '.historyData', jsonformat, type='string')
        cmds.select(clear=True)
        om.MGlobal.displayInfo(" History Hidden ")

#################################################################################################


def ToggleGeos(*args, **kwargs):
    meshes = cmds.ls(type="mesh")
    [cmds.setAttr(obj + '.overrideDisplayType', 2) for obj in meshes]
    [cmds.setAttr(obj + '.ove', not(cmds.getAttr(obj + '.ove'))) for obj in meshes]


#################################################################################################

def ToggleJoints(*args, **kwargs):
    joints = cmds.ls(type="joint")
    #
    if any([True for obj in joints if cmds.getAttr(obj + ".drawStyle") == 0]):
        [cmds.setAttr(obj + '.drawStyle', 2) for obj in joints]

    else:
        [cmds.setAttr(obj + '.drawStyle', 0) for obj in joints]


#################################################################################################

def ToggleAxis(*args, **kwargs):
    dagObjs = cmds.ls(dag=True, type='transform')
    if any([True for obj in dagObjs if cmds.getAttr(obj + '.displayLocalAxis') == 1]):
        [cmds.setAttr(obj + '.displayLocalAxis', 0) for obj in dagObjs]
        return

    [cmds.setAttr(obj + '.displayLocalAxis', not(cmds.getAttr(obj + '.displayLocalAxis'))) for obj in dagObjs]

###################################################################################################


def ToggleAffected(*args, **kwargs):
    # display affected or not ?? - fuck it all!
    checker = cmds.displayPref(q=True, da=True)
    cmds.displayPref(displayAffected=not(checker))


###################################################################################################

def ToggleFocal(*args, **kwargs):

    focalLength = cmds.getAttr("perspShape.focalLength")
    lockedCamera = cmds.getAttr("perspShape.focalLength", lock=True)

    if lockedCamera:
        cmds.warning("camera is locked")
        return

    if focalLength > 12:
        cmds.setAttr("perspShape.focalLength", 12)
        cmds.setAttr("perspShape.nearClipPlane", 0.01)

    elif focalLength == 12:
        cmds.setAttr("perspShape.focalLength", 8)
        cmds.setAttr("perspShape.nearClipPlane", 0.001)

    else:
        cmds.setAttr("perspShape.focalLength", 35)
        cmds.setAttr("perspShape.nearClipPlane", 0.1)

###################################################################################################
#
###################################################################################################

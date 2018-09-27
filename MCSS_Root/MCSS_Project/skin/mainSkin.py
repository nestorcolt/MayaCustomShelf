from ..helpers import helpersMain
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import maya.OpenMaya as om

#################################################################################################
# Module Description:
# This module holds all skinning relate functions to execute as scripts in custom shelf
#
#
#################################################################################################
#
#


def MigrateSkin(*args, **kwargs):
    sel = cmds.ls(sl=True)

    if sel == None or len(sel) == 0:
        cmds.warning('Not executed, please check selected items')
        return

    mainSkin = [item for item in cmds.listHistory(
                sel[0]) if cmds.objectType(item, isType='skinCluster')][0]

    jntList = [itm for itm in cmds.skinCluster(mainSkin, q=1, inf=1)]

    if any([itm for itm in jntList if ':' in itm]):
        jntList = [itm.split(':')[-1] for itm in jntList]

    print('SkinCluster: %s' % mainSkin)
    print('JOINTS: %s' % jntList)

    cmds.select(clear=True)
    skinCl = cmds.skinCluster(jntList, sel[1], bm=0)
    cmds.copySkinWeights(ss=mainSkin, ds=skinCl[0], noMirror=True)
    cmds.select(clear=True)

#################################################################################################
#
#


def RemoveUnusedInfluence(*args, **kwargs):

    # Get shift key
    mods = cmds.getModifiers()
    shift = (mods & 1) > 0
    boleanCheck = False
    #
    if shift:
        boleanCheck = True
    #

    def unused_influence(object=''):
        #
        mainSkin = [item for item in cmds.listHistory(
            object) if cmds.objectType(item, isType='skinCluster')]

        if len(mainSkin) == 0:
            return

        jntList = set([itm for itm in cmds.skinCluster(mainSkin[0], q=1, inf=1)])
        weigthedList = set([itm for itm in cmds.skinCluster(mainSkin[0], q=1, wi=1)])
        non_weigthed = list(jntList.difference(weigthedList))
        cmds.skinCluster(mainSkin[0], edit=True, ri=non_weigthed)
        print('Removed from Skin: {} :: {} '.format(mainSkin[0], non_weigthed))

    if boleanCheck:
        [unused_influence(obj) for obj in cmds.ls(type='mesh')]
    else:
        [unused_influence(obj) for obj in cmds.ls(sl=True)]


#################################################################################################
#
#

def ResetSkinCluster(*args, **kwargs):
    selection = cmds.ls(sl=True)

    for obj in selection:
        skinCluster = mel.eval('findRelatedSkinCluster ' + obj)

        if not skinCluster:
            return

        nInf = len(cmds.listConnections('%s.matrix' % skinCluster, destination=False))

        for idx in range(nInf):
            slotNJoint = cmds.listConnections('%s.matrix[ %d ]' % (skinCluster, idx), destination=False)

            if slotNJoint is not None:
                matrixAsStr = cmds.getAttr('%s.worldInverseMatrix' % slotNJoint[0])
                cmds.setAttr('%s.bindPreMatrix[ %d ]' % (skinCluster, idx), matrixAsStr, type="matrix")

                for dPose in cmds.listConnections(skinCluster, d=False, type='dagPose') or []:
                    cmds.dagPose(slotNJoint[0], reset=True, n=dPose)


#################################################################################################
#
#

def LabelJoints(*args, **kwargs):

    sel = cmds.ls(sl=True)
    #
    if sel is None or len(sel) == 0:
        cmds.warning('Not executed, please check selected mesh')
        return

    mainSkin = [item for item in cmds.listHistory(sel[0]) if cmds.objectType(item, isType='skinCluster')][0]
    jntList = [itm for itm in cmds.skinCluster(mainSkin, q=1, inf=1)]

    tempJDict = helpersMain.match_strings(jntList, filter='_L_', replace='_R_')
    helpersMain.rename_sibilings(tempJDict)

    jntList = [itm for itm in cmds.skinCluster(mainSkin, q=1, inf=1)]

    if any([itm for itm in jntList if ':' in itm]):
        jntList = [itm.split(':')[-1] for itm in jntList]

    for jnt in jntList:
        prefix = jnt.split('_')[0]
        cmds.setAttr(jnt + '.type', 18)
        cmds.setAttr(jnt + '.otherType', prefix, type='string')

        if '_L_' in jnt:
            cmds.setAttr(jnt + '.side', 1)

        elif '_R_' in jnt:
            cmds.setAttr(jnt + '.side', 2)

        else:
            cmds.setAttr(jnt + '.side', 0)

    #
    om.MGlobal.displayInfo("Labeling Done")


#################################################################################################

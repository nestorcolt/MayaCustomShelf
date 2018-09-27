from ..helpers import helpersMain
from string import ascii_uppercase
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import maya.OpenMaya as om
import json

#################################################################################################
# Module Description:
# This module holds all create relate functions to execute as scripts in custom shelf
#
#
#################################################################################################
#
#


def CreateOffset(*args, **kwargs):

    selection = cmds.ls(sl=True)
    offset = "Offset"

    if len(selection) < 1:
        cmds.warning("Please select at least one transform node")
        return

    for node in selection:
        word_array = node.split("_")
        prefix = word_array[0]
        suffix = "GRUP"
        tag = "A"
        off_temp = ""

        if len(word_array) > 1:
            suffix = word_array[1:]

            if "CTRL" in suffix:
                index = suffix.index("CTRL")
                suffix.insert(index, "GRUP")
                suffix.pop(index + 1)
            else:
                suffix.insert(-1, "GRUP")

            #
            suffix = "_".join(suffix)

        if offset in prefix:
            off_temp = prefix[prefix.index(offset):]
            prefix = prefix[:prefix.index(offset)]
            last_offset_letter = off_temp[-1]

            if last_offset_letter.isupper() and last_offset_letter != tag:
                tag = ascii_uppercase[last_offset_letter + 1]

        new_name = prefix + offset + tag + '_' + suffix

        group = cmds.group(name=new_name, em=True)
        cmds.matchTransform(group, node)

        # get parent if exist
        parent = cmds.listRelatives(node, p=True)

        # parent node to group
        cmds.parent(node, group)

        if parent is not None:
            cmds.parent(group, parent[0])

###################################################################################################

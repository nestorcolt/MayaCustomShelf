from difflib import SequenceMatcher
from functools import partial
from collections import OrderedDict
from runpy import run_path
# PyQt
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
# API
import maya.OpenMaya as om
import maya.OpenMayaUI as mui
import shiboken2 as shi
# Comands
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
# Python
import inspect
import os
import sys
import re
import json

###################################################################################################
# Globals:

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ICON_DIR = os.path.join(ROOT_DIR, "icons")
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
TOOLS_DIR = os.path.join(ROOT_DIR, "tools")
#
SHELF_LAYOUT = cmds.shelfTabLayout('ShelfLayout', q=True, fpn=True)
SHELF_NAME = "CustomShelf"

###################################################################################################


def get_maya_shelf(shelf_layout):
    """

        Description: Find the control of the shelf, or the shelf it self from maya UI

    """
    tabSwing = mui.MQtUtil.findControl(shelf_layout)
    myShelfLayout = shi.wrapInstance(long(tabSwing), QtWidgets.QTabWidget)

    for itm in myShelfLayout.children():
        if isinstance(itm, QtWidgets.QTabWidget):
            return itm

###################################################################################################


def kill_Shelf(function):
    """

        Description: Decorator to search and destroy Old shelf before base Class __init__ method

    """

    if cmds.shelfLayout(SHELF_NAME, ex=1):
        cmds.deleteUI(SHELF_NAME)
        print("Tinker Shelf Deleted")

    def wrapper_function(*args, **kwars):
        # runs decorated function
        function_exec = function(*args, **kwars)

        return function_exec

    return wrapper_function


###################################################################################################

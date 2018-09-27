from PySide2 import QtGui
from PySide2 import QtWidgets
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken2

###################################################################################################


def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(pointer), QtWidgets.QWidget)

###################################################################################################


def createLayout(attribute, parentLayout):

    # create and add the horizontal layout
    layout = QtWidgets.QHBoxLayout()
    parentLayout.addLayout(layout)

    # create label
    label = QtWidgets.QLabel(attribute)
    layout.addWidget(label)

    # create font and assign
    font = QtGui.QFont()
    font.setPointSize(11)
    font.setBold(True)
    label.setFont(font)

    # add spacer
    spacer = QtWidgets.QSpacerItem(30, 0)
    layout.addSpacerItem(spacer)

    #  loop through attribiutes and creates checkbox at each one
    for attr in ["X", "Y", "Z"]:
        checkBox = QtWidgets.QCheckBox(attr)
        objectName = attribute.partition(":")[0] + attr + "_cmCheckbox"
        checkBox.setObjectName(objectName)
        checkBox.setChecked(False)
        layout.addWidget(checkBox)
        checkBox.setMinimumWidth(30)
        checkBox.setMaximumWidth(30)

    # create spacer and maintain offset
    spacer50 = QtWidgets.QSpacerItem(50, 0)
    layout.addSpacerItem(spacer50)

    showAllCheckBox = QtWidgets.QCheckBox("Show Attributes ")
    objectName = attribute.partition(":")[0] + "_cmCheckbox_showAll"
    showAllCheckBox.setObjectName(objectName)
    layout.addWidget(showAllCheckBox)


def executeFunction():
    # get selection
    selection = cmds.ls(sl=True)

    # get checkbox value
    for attribute in ["Translate", "Rotate", "Scale"]:
        doList = []

        for attr in ["X", "Y", "Z"]:
            if cmds.control(attribute + attr + "_cmCheckbox", q=1, exists=True):
                ptr = mui.MQtUtil.findControl(attribute + attr + "_cmCheckbox")
                checkBox = shiboken.wrapInstance(long(ptr), QtWidgets.QCheckBox)
                value = checkBox.isChecked()
                if value == True:
                    doList.append(attr.lower())

        # showAll
        showAll = []
        if cmds.control(attribute + "_cmCheckbox_showAll", q=1, exists=True):
            ptr = mui.MQtUtil.findControl(attribute + "_cmCheckbox_showAll")
            checkBox = shiboken.wrapInstance(long(ptr), QtWidgets.QCheckBox)
            showAll = checkBox.isChecked()

        Order = showAll

        if len(doList) > 0:
            for obj in selection:
                for att in doList:
                    if attribute == "Translate":
                        cmds.setAttr("{}.t{}".format(obj, att), l=Order, k=Order, cb=Order)
                    if attribute == "Rotate":
                        cmds.setAttr("{}.r{}".format(obj, att), l=Order, k=Order, cb=Order)
                    if attribute == "Scale":
                        cmds.setAttr("{}.s{}".format(obj, att), l=Order, k=Order, cb=Order)


def unlockAll():
    selection = cmds.ls(sl=True)
    coordenadas = ["x", "y", "z"]
    attributo = ["t", "r", "s"]

    for obj in selection:
        for cor, attr in[(cor, attr) for cor in coordenadas for attr in attributo]:
            cmds.setAttr("{}.{}{}".format(obj, attr, cor), l=False, k=True)

###################################################################################################


def modificarAtributos():

    # check for open Window first
    winName = "HideAttrMasterWin"
    if cmds.window(winName, exists=1):
        cmds.deleteUI(winName, wnd=True)

    # create a window
    parent = getMayaWindow()
    window = QtWidgets.QMainWindow(parent)
    window.setObjectName(winName)
    window.setWindowOpacity(0.95)
    window.setWindowTitle("Show - Hide Attributes Tool 1.2")
    window.setMinimumSize(420, 125)
    window.setMaximumSize(420, 125)

    # create the main widget
    mainWidget = QtWidgets.QWidget()
    window.setCentralWidget(mainWidget)

    # create or main vertical layout
    verticalLayout = QtWidgets.QVBoxLayout(mainWidget)

    # loop through the attributes, create layouts
    for attribute in ["Translate:", "Rotate:", "Scale:"]:
        createLayout(attribute, verticalLayout)

    # create the "Show Hide" button
    Button = QtWidgets.QPushButton("Show / Hide Attributes")
    verticalLayout.addWidget(Button)
    font = QtGui.QFont()
    font.setPointSize(10)
    Button.setFont(font)
    Button.clicked.connect(executeFunction)

    # create the "unlock" button
    Button2 = QtWidgets.QPushButton("Unlock All ")
    verticalLayout.addWidget(Button2)
    Button2.setFont(font)
    Button2.clicked.connect(unlockAll)

    # show the window
    window.show()


###################################################################################################
#
modificarAtributos()

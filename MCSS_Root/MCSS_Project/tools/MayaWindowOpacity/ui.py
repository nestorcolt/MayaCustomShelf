from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance as wrapI
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import os


#---------------------------------------------------------------------------------#
GlobalTweener = None
windowTitle = "Maya Window Opacity"
windowObject = "WindowOpacity"


#---------------------------------------------------------------------------------#


def deleteFromGlobal():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapI(long(mayaMainWindowPtr), QtWidgets.QMainWindow)  # Important that it's QMainWindow, and not QWidget
    # Go through main window's children to find any previous instances
    for obj in mayaMainWindow.children():
        if obj.objectName() == windowObject:
            obj.setParent(None)
            obj.deleteLater()
            print('Object Deleted')

#####################################################################################################

# Get Maya Window Pointer


def getMayaWindow():
    mainWinPtr = omui.MQtUtil.mainWindow()
    return wrapI(long(mainWinPtr), QtWidgets.QWidget)


class WindowOpacityUI(QtWidgets.QDialog):

    parent = getMayaWindow()

    def __init__(self, parent=parent):
        super(WindowOpacityUI, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # check for open Window first
        winName = windowTitle
        if cmds.window(winName, exists=1):
            cmds.deleteUI(winName, wnd=True)

        self.setObjectName(windowObject)
        self.setWindowTitle(windowTitle)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setMinimumWidth(350)
        self.setMinimumHeight(100)
        # self.setGeometry(690, 335, 350, 150)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(10)
        self.layout().setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        labelLayout = QtWidgets.QVBoxLayout()
        labelLayout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        sliderLayout = QtWidgets.QHBoxLayout()
        sliderLayout.setContentsMargins(8, 5, 8, 5)
        sliderLayout.setSpacing(5)

        buttonsLayout = QtWidgets.QHBoxLayout()
        buttonsLayout.setContentsMargins(10, 10, 10, 10)
        buttonsLayout.setSpacing(10)

        self.layout().addLayout(labelLayout)
        verticalSpacer = QtWidgets.QSpacerItem(15, 15, QtWidgets.QSizePolicy.Minimum)
        verticalSpacer2 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Maximum)
        self.layout().addItem(verticalSpacer)
        self.layout().addLayout(sliderLayout)
        self.layout().addItem(verticalSpacer2)
        self.layout().addLayout(buttonsLayout)

        self.topLabel = QtWidgets.QLabel('< Use this slider to set the opacity amount >')
        self.topLabel.setContentsMargins(0, 10, 0, 0)
        self.zeroLabel = QtWidgets.QLabel('0 -')
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setFixedHeight(22)
        self.hundredLabel = QtWidgets.QLabel('- 100')

        self.CloseBtn = QtWidgets.QPushButton('Close')
        self.ResetBtn = QtWidgets.QPushButton('Reset')

        labelLayout.addWidget(self.topLabel)
        sliderLayout.addWidget(self.zeroLabel)
        sliderLayout.addWidget(self.slider)
        sliderLayout.addWidget(self.hundredLabel)

        buttonsLayout.addWidget(self.CloseBtn)
        buttonsLayout.addWidget(self.ResetBtn)
        self.slider.setValue(100)
#---------------------------------------------------------------------------------#

        self.CloseBtn.clicked.connect(self.closeNOW)
        self.ResetBtn.clicked.connect(lambda: self.slider.setValue(100))
        self.slider.valueChanged.connect(lambda: self.windowOpacity(self.slider.value()))


#---------------------------------------------------------------------------------#
    def windowOpacity(self, value):
        formated_value = float(value / 100.0)
        self.parent.setWindowOpacity(formated_value)
#---------------------------------------------------------------------------------#

    def closeEvent(self, event):
        deleteFromGlobal()

    def closeNOW(self):
        self.close()

#---------------------------------------------------------------------------------#


def OpaUIRun():
    deleteFromGlobal()
    global GlobalTweener

    try:
        Tweener.close()
        Tweener.deleteLater()
    except:
        pass

    if GlobalTweener is None:
        Tweener = WindowOpacityUI()
        Tweener.show()


#---------------------------------------------------------------------------------#
if __name__ == '__main__':
    OpaUIRun()

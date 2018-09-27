from file_version_finder.Qt import __binding__
from file_version_finder.Qt import QtWidgets as qw
from file_version_finder.Qt import QtCore as qc
from file_version_finder.Qt import QtGui as qg

#
if __binding__ in ('PySide2', 'PyQt5'):
    print('Qt5 binding available')
    import shiboken2 as shi


elif __binding__ in ('PySide', 'PyQt4'):
    print('Qt4 binding available.')
    import shiboken as shi


else:
    print('No Qt binding available.')

import os
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
from file_version_finder import finder

reload(finder)

# TIP:
# Must be selected the current workspace over the project/pipeline options

#---------------------------------------------------------------------------------#
# GLOBALS:
Finder_UI = None
CONTROL_VERSION_UI = 2.001

WORKSPACE_PATH = os.path.abspath(os.path.join(os.path.abspath(os.path.join(cmds.workspace(q=True, fn=True), os.pardir)), os.pardir))


windowTitle = "Colt File Finder - CFF"
windowObject = "FileFinderUiTool"

# print('ControlVerUI: {} - ControlVerEngine: {}'.format(CONTROL_VERSION_UI, RelocationEngine.CONTROL_VERSION_ENGINE ))
#---------------------------------------------------------------------------------#


###################################################################################

# Get Maya Window Pointer
def getMayaWindow():
    mainWinPtr = omui.MQtUtil.mainWindow()
    return shi.wrapInstance(long(mainWinPtr), qw.QWidget)


class FileFinderUI(qw.QDialog):

    parent = getMayaWindow()

    def __init__(self, parent=parent):
        super(FileFinderUI, self).__init__(parent)
        self.initUI()

    def initUI(self):

        # check for open Window first
        winName = windowTitle
        if cmds.window(winName, exists=1):
            cmds.deleteUI(winName, wnd=True)

        # call engine
        self.engine = finder.LatestFileFinderEngine()

        objectName = windowTitle
        self.setObjectName(objectName)
        self.setWindowTitle(windowTitle)
        self.setWindowFlags(qc.Qt.Tool)
        self.setAttribute(qc.Qt.WA_DeleteOnClose)

        self.setMinimumWidth(600)
        self.setMaximumHeight(300)

        self.setLayout(qw.QVBoxLayout())

        self.layout().setContentsMargins(2, 20, 2, 5)
        self.layout().setSpacing(10)
        self.layout().setAlignment(qc.Qt.AlignVCenter | qc.Qt.AlignHCenter)

        labelLayout = qw.QVBoxLayout()
        labelLayout.setAlignment(qc.Qt.AlignVCenter | qc.Qt.AlignHCenter)

        sliderLayout = qw.QHBoxLayout()
        sliderLayout.setContentsMargins(8, 5, 8, 5)
        sliderLayout.setSpacing(5)

        buttonsLayout = qw.QHBoxLayout()
        buttonsLayout.setContentsMargins(10, 0, 10, 10)
        buttonsLayout.setSpacing(10)

        # file path widgets
        #
        filePath_lyt = qw.QHBoxLayout()
        filePath_lyt.setContentsMargins(5, 0, 5, 0)

        self.path_le = qw.QLineEdit()
        self.path_btn = qw.QPushButton('Path')

        filePath_lyt.addWidget(self.path_le)
        filePath_lyt.addWidget(self.path_btn)

        # checkBox type of find
        #
        checks_lyt = qw.QHBoxLayout()
        checks_lyt.setAlignment(qc.Qt.AlignCenter)
        checks_lyt.setSpacing(50)

        self.date_chckBox = qw.QCheckBox('Last Modified')
        self.serial_chckBox = qw.QCheckBox('Name Serial')

        self.rig_high = qw.QCheckBox('RigHigh')
        self.rig_Low = qw.QCheckBox('RigLow')

        checks_lyt.addWidget(self.date_chckBox)
        checks_lyt.addWidget(self.serial_chckBox)
        checks_lyt.addWidget(qw.QWidget())
        checks_lyt.addWidget(self.rig_high)
        checks_lyt.addWidget(self.rig_Low)

        # Filters line edits
        #

        filter_lyt = qw.QHBoxLayout()
        filter_lyt.setContentsMargins(60, 0, 25, 0)
        filter_lyt.setSpacing(15)
        self.user_folder_filter_le = qw.QLineEdit()
        self.hint_filter_le = qw.QLineEdit()

        filter_folder_lb = qw.QLabel('User')
        hint_lb = qw.QLabel('Hint')

        filter_lyt.addWidget(filter_folder_lb)
        filter_lyt.addWidget(self.user_folder_filter_le)
        filter_lyt.addWidget(hint_lb)
        filter_lyt.addWidget(self.hint_filter_le)

        # Data LCD
        #
        lcd_label_lyt = qw.QHBoxLayout()
        lcd_label_lyt.setContentsMargins(5, 0, 5, 0)
        self.lcd_label = qw.QLabel()
        self.lcd_label.setStyleSheet("""background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(200, 200, 200,40), stop:1 rgba(34, 34, 34, 20));
                                        color: rgba(225,80,80,250);
                                        font-family:calibri;
                                        font-size:14px;
                                        font-weight:400;
                                        border-radius: 10px;
                                        padding: 0px;
                                        padding-left: -25px;
                                        marging:0px;""")

        lcd_label_lyt.addWidget(self.lcd_label)
        self.lcd_label.setFixedHeight(120)
        self.lcd_label.setIndent(0)
        self.lcd_label.setMargin(0)
        self.lcd_label.setAlignment(qc.Qt.AlignLeft)
        self.lcd_label.setWordWrap(True)

        # add layouts to main widget UI
        self.layout().addLayout(labelLayout)
        self.layout().addLayout(filePath_lyt)
        self.layout().addLayout(checks_lyt)
        self.layout().addLayout(filter_lyt)
        self.layout().addLayout(lcd_label_lyt)
        self.layout().addLayout(buttonsLayout)

        self.topLabel = qw.QLabel(' Maya Lastest File Version Finder ')
        self.topLabel.setStyleSheet('color: rgba(225,80,80,250); font-family:calibri; font-size:18px; font-weight:600;')

        self.find_btn = qw.QPushButton('Find')
        self.open_Btn = qw.QPushButton('Open')

        labelLayout.addWidget(self.topLabel)

        buttonsLayout.addWidget(self.find_btn)
        buttonsLayout.addWidget(self.open_Btn)

        # toogle checkboxes
        self._toggle = True
        self.date_chckBox.setChecked(self._toggle)
        self.serial_chckBox.setChecked(not self._toggle)
        self.date_chckBox.clicked.connect(self.toggle)
        self.serial_chckBox.clicked.connect(self.toggle)

        # toogle checkboxes
        self.rig_high.clicked.connect(self.toggle_rig)
        self.rig_high.setObjectName('rigHigh')
        self.rig_Low.clicked.connect(self.toggle_rig)
        self.rig_Low.setObjectName('rigLow')

        # button connection
        self.path_btn.clicked.connect(self.getPath)
        self.find_btn.clicked.connect(self.findOperation)
        self.open_Btn.clicked.connect(self.openScene)

        # call methods
        self.populate_lcd()
        self.populate_path_lineEdit()
        self.path_le.deselect()

        for itm in self.findChildren(qw.QLineEdit):
            itm.setReadOnly(True)
            itm.installEventFilter(self)

        self.installEventFilter(self)
        self.lineEdits = self.findChildren(qw.QLineEdit)

        # checks rigs checkboxes handable variable

        self.block_check_bug = 0
#---------------------------------------------------------------------------------#

    def eventFilter(self, obj, event):
        if isinstance(obj, qw.QLineEdit):
            if event.type() == qc.QEvent.MouseButtonPress:
                obj.setReadOnly(False)
                event.accept()
                return True

        elif event.type() == qc.QEvent.MouseButtonPress:
            if obj == self:
                for itm in self.lineEdits:
                    itm.clearFocus()
                    itm.setReadOnly(True)
                    event.accept()

                return True

        return False
    # populates the LCD screen with object file data to show to user
    #

    def populate_lcd(self, json={}):
        label = self.lcd_label
        dummie = '*** empty field ***'

        text = """
               Scene Data:\n
               \t\t\tUser: {}
               \t\t\tFile Name: {}
               \t\t\tDate: {}
               """

        if json and self.engine.success:
            label.setText(text.format(json['user'].capitalize(),
                                      os.path.basename(os.path.normpath(json['scene'])),
                                      json['date']
                                      ))
        else:
            label.setText(text.format(dummie, dummie, dummie))

    #################################################
    # checks and unchecks checkboxes
    #
    def toggle(self):
        self._toggle = not self._toggle
        self.date_chckBox.setChecked(self._toggle)
        self.serial_chckBox.setChecked(not self._toggle)

    def toggle_rig(self):
        array_checks = [self.rig_high, self.rig_Low]
        array_checks.remove(self.sender())

        if array_checks[0].isChecked():
            array_checks[0].setChecked(False)

    ###################################################
    def closeEvent(self, event):
        print('File finder closed')

    ####################################################
    # populates path line edit with path info
    #
    def populate_path_lineEdit(self, path=''):

        if not path:
            rawPath = WORKSPACE_PATH
            self.path_le.setText(rawPath)

        else:
            self.path_le.setText(path)

    #####################################################
    # open maya window for select rute
    #

    def getPath(self):
        singleFilter = "Directories"
        pathTo = cmds.fileDialog2(startingDirectory=WORKSPACE_PATH, fileFilter=singleFilter, dialogStyle=2, fileMode=3, okCaption='Go')
        self.populate_path_lineEdit(path=pathTo[0])
        self.path_le.deselect()

    #######################################################
    # find button operation
    #
    def findOperation(self):

        rig_checks = [itm for itm in [self.rig_Low, self.rig_high] if itm.isChecked()]
        clue = self.hint_filter_le.text()
        user_filter = self.user_folder_filter_le.text()

        if len(rig_checks) > 0:
            rig_filter = rig_checks[0].objectName()
            self.engine.finder(rootPath=self.path_le.text(),
                               date=self.date_chckBox.checkState(), serial=self.serial_chckBox.checkState(),
                               userFilter=user_filter, hint=clue, rigFilter=rig_filter)
        else:
            self.engine.finder(rootPath=self.path_le.text(),
                               date=self.date_chckBox.checkState(), serial=self.serial_chckBox.checkState(),
                               userFilter=user_filter, hint=clue)

        self.engine.returnDataToUser()
        self.populate_lcd(self.engine.latestUserData)

    ########################################################
    # open scene
    #
    def openScene(self):
        path = self.engine.latestUserData.get('file', None),
        print(path)
        print(len(path))

        if not path or path[0] is None:
            cmds.warning('No File Path Found')
            return

        cmds.file(force=True, new=True)
        cmds.file(path, open=True, f=True)

#-----------------------------------------------------------------------------------------------#


def finder_Ui_Run():
    global Finder_UI
    try:
        FileFinderUI.close()
        FileFinderUI.deleteLater()
    except:
        pass

    if Finder_UI is None:
        finderUI = FileFinderUI()

        finderUI.show()


#---------------------------------------------------------------------------------#
###########################
if __name__ == '__main__':
    finder_Ui_Run()

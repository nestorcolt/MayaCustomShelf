from MCSS_Project.main.imports_and_globals import *
from MCSS_Project.helpers import get_modules_data
from MCSS_Project.main import shelfBase

"""

    Description: This module holds the object from the actual T-M shelf


"""

###################################################################################################
# Globals
# Getters from Module 'get_modules_data'
MODULES_DATA = get_modules_data.MODULES_STRUCT
SCRIPTS_DATA = get_modules_data.SCRIPTS_DATA
TOOLS_DATA = get_modules_data.TOOLS_DATA

###################################################################################################


class CustomSmartShelf(shelfBase.CustomShelfBase):
    """ CustomSmartShelf shelf object inherit from shelfBase.CustomShelfBase  """

    def __init__(self, name=SHELF_NAME):
        super(CustomSmartShelf, self).__init__(name)

        #
        print("Init : %s" % self.__class__)

        # public members
        self.labels = []
        self.buttons = []
        self.separators = []
        self.name = name

        self.modules = MODULES_DATA
        self.scripts = SCRIPTS_DATA
        self.tools = TOOLS_DATA

        # private members
        self._parent = get_maya_shelf(SHELF_LAYOUT)

        #
        # call methods ---------------------------------------------------------------------------------

        # Set initial Reload Button by default build shelf and insert it in first tab widget index
        self.QShelf_tab, self.QShelf_layout = self.do_insertShelf(shelfObj=self._parent, index=0, tabName=self.name)

        # Init the Reload button at start
        self.addButon(icon=os.path.join(self.iconPath, "reload.png"), command=self.do_reloadShelf)
        self.addSeparator()

        # Build shelf widgets
        self.build()

        self._parent.currentChanged.connect(self.do_trackTabChange)

        # fix a problem that was clearing momentanously the other shelf when this one was inserted at first index
        # maya is a dick.
        for idx in range(self._parent.count()):
            self._parent.setCurrentIndex(idx)

        self._parent.setCurrentIndex(0)

    ###################################################################################################
    # This method is in charge of build and reload the shelf structure after
    # the reload buttons that comes by default on Class Init
    #

    def build(self):

        # create pop ups menus
        self.do_label(text=" Popups ")
        self.do_popups()
        #

        # Create Scrips area
        sep_2 = self.addSeparator()
        self.do_label(text=" Buttons ")
        self.do_scripts()

        # Create Tools area
        sep_3 = self.addSeparator()
        self.do_label(text=" Tools ")
        self.do_tools()

        # set style for shelf elements (this fix the problem that prevent the width to be set at label init)
        self.do_labelWidth()

        self.separators.append(sep_2)
        self.separators.append(sep_3)

    ###################################################################################################
    # Get the Icon if exist for the created button
    #

    def do_get_icons(self, name=''):
        icon = "commandButton.png"
        iconRute = [img for img in os.listdir(ICON_DIR) if os.path.splitext(img)[0].lower() == name.lower()]

        if iconRute:
            icon = os.path.join(ICON_DIR, iconRute[0])

        return icon

    ###################################################################################################
    # Fetch the tools to the shelf
    #

    def do_tools(self):
        for name, path in sorted(self.tools.items()):
            pre_loaded_func = partial(run_path, path)
            button = self.addButon(command=pre_loaded_func, annotation=name, icon=self.do_get_icons(name))
            self.buttons.append(button)

    ###################################################################################################
    # Fetch the scripts to the shelf
    #

    def do_scripts(self):
        for name, path in sorted(self.scripts.items()):
            pre_loaded_func = partial(run_path, path)
            button = self.addButon(command=pre_loaded_func, annotation=name, icon=self.do_get_icons(name))
            self.buttons.append(button)

    ###################################################################################################
    # Fetch the popup menus to the shelf
    #

    def do_popups(self):

        for name, data in sorted(self.modules.items()):
            button = self.addButon(label=name, icon=self.do_get_icons(name))
            popUpMenu = cmds.popupMenu(parent=button, button=1)
            self.buttons.append(button)

            for function, path in sorted(data.items()):
                command = partial(path)
                self.addMenuItem(parent=popUpMenu, label=function, command=command)

    ###################################################################################################
    # When shelf is created, find the TabBar widget from Qt, and insert this shelf obj
    # in the index 0 - First shelf on Tabbar
    #

    def do_insertShelf(self, shelfObj='', index=0, tabName=''):

        tabsCount = shelfObj.count()
        filteredTab = [shelfObj.widget(idx) for idx in range(tabsCount) if shelfObj.widget(idx).objectName() == tabName]

        if filteredTab:
            shelfObj.insertTab(index, filteredTab[0], tabName)
            shelfObj.setCurrentIndex(index)

            return filteredTab[0], filteredTab[0].layout()

    ###################################################################################################
    # Create a label with a Area name on the shelf [Popup - Buttons - Tools]
    #

    def do_label(self, text=''):

        label = QtWidgets.QLabel(text)
        label.setObjectName(text)
        label.setStyleSheet("""background-color: qlineargradient( x1:0, y1:0, x2:0.5, y2:1, stop:0 #007e7e, stop:1 lightgray);
                            width: 150px; color:black; border-radius: 5px; padding-left:1px; padding-right:1px;""")

        label.setAlignment(QtCore.Qt.AlignCenter)
        self.QShelf_layout.addWidget(label)
        self.labels.append(label)

        return label

    ###################################################################################################
    # Re-adjust the width of each QLabel because for some weird reason is lost after reload
    #

    def do_labelWidth(self, width=60):

        for label in self.labels:
            label.setFixedWidth(width)

    ###################################################################################################
    # Reload method. it is self explanatory
    #

    def do_reloadShelf(self):

        shelf_widgets = []
        shelf_widgets.extend(self.buttons)
        shelf_widgets.extend(self.separators)
        shelf_widgets.extend(self.labels)

        for widget in shelf_widgets:
            if not isinstance(widget, QtCore.QObject):
                widget = self.do_get_widget(widget)
            #
            widget.deleteLater()

        # # reload the shelf widgets
        reload(get_modules_data)

        self.modules = get_modules_data.MODULES_STRUCT
        self.scripts = get_modules_data.SCRIPTS_DATA
        self.tools = get_modules_data.TOOLS_DATA
        #
        self.labels = []
        self.buttons = []
        self.separators = []

        # Re-build the shelf structure
        self.build()

    ###################################################################################################
    # Basicaly this is a getter method, will take a string name and will look for the swinger c++ object to
    # get the Pyqt widget
    #

    def do_get_widget(self, controler):
        """

            Description: Find the control of the shelf, or the shelf it self from maya UI
            @Param controler: String name of maya controler
            @Return: Pyqt widget

        """
        swinger = mui.MQtUtil.findControl(controler)
        widget = None

        if "button" in controler.split("|")[-1].lower():
            widget = shi.wrapInstance(long(swinger), QtWidgets.QPushButton)

        elif "separator" in controler.split("|")[-1].lower():
            widget = shi.wrapInstance(long(swinger), QtWidgets.QWidget)

        return widget

    ###################################################################################################
    # fix the spacing in the Tab between icons because is lose after tab changes,
    # so this method set it again at 12

    def do_trackTabChange(self):
        """

            Description: Try to do this, if the shelf doesn't exist for some reason will ignore it

        """
        try:
            cmds.shelfLayout(self.name, e=True, spa=10)
        except:
            pass

##########################################################################


if __name__ == '__main__':
    instanceShelf = CustomSmartShelf()

from MCSS_Project.main.imports_and_globals import *

###################################################################################################


class CustomShelfBase(object):
    '''A simple class to build shelves in maya. Since the build method is empty,
    it should be extended by the derived class to build the necessary shelf elements.
    By default it creates an empty shelf called "customShelf".'''

    # Decorator that checks before init if a shelf exist in maya to delete it first
    @kill_Shelf
    def __init__(self, name="CustomShelf", iconPath=ICON_DIR):

        # Public Members
        self.name = name
        self.iconPath = iconPath
        self.labelBackground = (1, 1, 1, 0.5)
        self.labelColour = (.1, .1, .1)
        #
        self._cleanOldShelf()
        cmds.setParent(self.name)

        # set the spacing
        cmds.shelfLayout(name, e=True, spa=10)

    #################################################################################################
    # This method should be overwritten in derived classes to actually build the shelf
    # elements. Otherwise, nothing is added to the shelf

    def build(self):
        pass

    #################################################################################################
    # Adds a shelf button with the specified label, command, double click command and image
    #

    def addButon(self, label='', icon="commandButton.png", annotation='', command="'ShelfButton'", doubleCommand="'ShelfButton'"):

        cmds.setParent(self.name)

        if icon:
            icon = icon

        button = cmds.shelfButton(width=37, height=37, image=icon, label=label, command=command, annotation=annotation,
                                  dcc=doubleCommand, imageOverlayLabel=label, olb=self.labelBackground, olc=self.labelColour)

        return button

    #################################################################################################
    # Adds menu item
    #

    def addMenuItem(self, parent, label, command="'ButtonItem'", icon=""):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        if icon:
            icon = self.iconPath + icon
        return cmds.menuItem(p=parent, label=label, c=command, i="")

    #################################################################################################
    # Add a sub menu to menu item
    #

    def addSubMenu(self, parent, label, icon=None):
        '''Adds a sub menu item with the specified label and icon to the specified parent popup menu.'''
        if icon:
            icon = self.iconPath + icon
        return cmds.menuItem(p=parent, label=label, i=icon, subMenu=1)

    #################################################################################################
    # Maya shelf separator
    #

    def addSeparator(self, long=True):

        return cmds.separator(p=self.name, enable=1, width=12, height=35, preventOverride=0, manage=1, highlightColor=(0.321569, 0.521569, 0.65098),
                              horizontal=False, style="shelf", visible=1, enableBackground=0, backgroundColor=(0, 0, 0))

    #################################################################################################
    # Checks if the shelf exists and empties it if it does or creates it if it does not
    #

    def _cleanOldShelf(self):

        if cmds.shelfLayout(self.name, ex=1):
            if cmds.shelfLayout(self.name, q=1, ca=1):
                for each in cmds.shelfLayout(self.name, q=1, ca=1):
                    cmds.deleteUI(each)
        else:
            cmds.shelfLayout(self.name, p="ShelfLayout")

###################################################################################################

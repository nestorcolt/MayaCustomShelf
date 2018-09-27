import os
import sys

###################################################################################################

"""

    Description: Init and load the shelf module  - add tools module to python path to find the tools easily

"""

###################################################################################################


def loadModule():
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #
    if DIR not in sys.path:
        sys.path.append(os.path.join(DIR, "MCSS_Project", "tools"))
        sys.path.append(DIR)
        print('\nCURRENT DIR: %s' % DIR)

    return DIR


###################################################################################################
loadModule()
from MCSS_Project.main import SmartShelf
SmartShelf.CustomSmartShelf()
###################################################################################################

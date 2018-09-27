import maya.mel as mel
import os
#
###################################################################################################
melScriptPath = os.path.join(os.path.dirname(__file__), "mel", "TMTools.mel")
# Launch the tool
mel.eval('source "%s"' % melScriptPath)
####################################################################################################

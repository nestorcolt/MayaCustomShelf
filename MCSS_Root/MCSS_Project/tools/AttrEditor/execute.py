import maya.mel as mel
import os
#
###################################################################################################
melScriptPath = os.path.join(os.path.dirname(__file__), "ntAttrEditor_v0.06.mel")
# Launch the tool
mel.eval('source "%s"' % melScriptPath)
####################################################################################################

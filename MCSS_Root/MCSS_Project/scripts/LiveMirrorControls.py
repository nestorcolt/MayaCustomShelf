import maya.cmds as cmds
#
# will temporaly connect the right side controls to the left side to mirror motions to check skinning
#
# Get shift key
mods = cmds.getModifiers()
shift = (mods & 1) > 0
boleanCheck = True
#
if shift:
    boleanCheck = False
#


def mirrorTempControls(obj, plug=True):

    attributes = []
    #
    allAttrs = cmds.listAttr(obj)
    cbAttrs = cmds.listAnimatable(obj)
    if allAttrs and cbAttrs:
        orderedAttrs = [attr for attr in allAttrs for cb in cbAttrs if cb.endswith(attr)]
    if u'visibility' in orderedAttrs:
        orderedAttrs.remove(u'visibility')
        orderedAttrs.append(u'visibility')
    attributes.extend(orderedAttrs)
    # print attributes

    node = obj.replace('_L_', '_R_')
    for attr in attributes:
        #
        if plug:
            if cmds.objExists(obj + '.%s' % attr) and cmds.objExists(node + '.%s' % attr):
                if not cmds.isConnected(obj + '.%s' % attr, node + '.%s' % attr):
                    cmds.connectAttr(obj + '.%s' % attr, node + '.%s' % attr, f=True)

        else:
            if cmds.objExists(obj + '.%s' % attr) and cmds.objExists(node + '.%s' % attr):
                if cmds.isConnected(obj + '.%s' % attr, node + '.%s' % attr):
                    cmds.disconnectAttr(obj + '.%s' % attr, node + '.%s' % attr)


###################################################
# Execute logic
#
controls_left = [itm for itm in cmds.ls('*CTRL') if '_L_' in itm]
for control in controls_left:
    mirrorTempControls(control, plug=boleanCheck)

###################################################

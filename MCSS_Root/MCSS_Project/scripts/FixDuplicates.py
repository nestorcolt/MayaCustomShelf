import pymel.core as pm
from string import ascii_uppercase

###################################################################################################
#


objectsList = [pm.ls(itm) for itm in list(set([obj.split('|')[-1] for obj in pm.ls() if len(pm.ls(obj.split('|')[-1])) > 1]))]
#


def hierchy_check(array):
    newOrder = []

    for ar_1, ar_2 in [(ar_1, ar_2) for ar_1 in array for ar_2 in array]:
        if ar_2 == ar_1:
            continue

        decendents = pm.listRelatives(ar_1, ad=True, f=True)

        if decendents is not None:
            if ar_2 in decendents:
                newOrder.append([ar_1, ar_2])

    if len(newOrder) > 0:
        # print(newOrder[0])
        return newOrder[0]

    else:
        False

###################################################################################################


fixedItems = []


def fixNames(objects, noShapes=True):

    for array in objects:
        orderedItems = hierchy_check(array)

        if orderedItems:
            array = orderedItems

        for idx, obj in enumerate(array):
            node = pm.PyNode(obj)
            splitted = node.name().split('|')[-1]
            prefixArr = splitted.split('_')
            name = ''

            if noShapes:
                if not isinstance(node, pm.nodetypes.NurbsCurve):

                    if len(prefixArr) > 1:
                        prefix = prefixArr[0]
                        name = prefix + ascii_uppercase[idx] + splitted[len(prefix):]
                    else:
                        name = node.name().split('|')[-1] + ascii_uppercase[idx]

                    newObject = pm.rename(node, name)
                    fixedItems.append(newObject)

            else:
                if isinstance(node, pm.nodetypes.NurbsCurve):
                    parent = node.getParent().split('|')[-1]

                    if parent in fixedItems:
                        continue

                    if len(prefixArr) > 1:
                        prefix = prefixArr[0]
                        name = prefix + ascii_uppercase[idx] + splitted[len(prefix):]
                    else:
                        name = node.name().split('|')[-1] + ascii_uppercase[idx]

                    pm.rename(node, name)


###################################################################################################
# transforms objects
fixNames(objectsList)
# shape objects
fixNames(objectsList, noShapes=False)
print('*** Rename Duplicates Done ***')
#

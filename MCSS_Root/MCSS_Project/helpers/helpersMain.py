from MCSS_Project.main.imports_and_globals import *


#################################################################################################
# Globals:

#################################################################################################


#################################################################################################
# Helper function to match string names by tolerance
# handy to match joints names even if there is a bad spelling in object name
#

def match_strings(string_list=[], filter='', replace='', tolerance=0.85):
    """
    Param: string_list [object names array ex: joints list]
    Param: filter [reference to find '_L_']
    Param: replace [reference to replace with '_R_']
    Param: tolerance [if radius is > than tolerance value will match word]
    Return: RelationShip dictionary

    """
    sideOneArray = [itm for itm in string_list if filter in itm]
    sideTwoArray = [itm for itm in string_list if replace in itm]
    #
    unMatchedWords = []
    relationship_dict = {}

    for obj in sideOneArray:
        dummy = obj.replace(filter, replace)

        if dummy not in sideTwoArray:
            unMatchedWords.append(obj)
        else:
            relationship_dict[obj] = dummy
            sideTwoArray.remove(dummy)

    for aWord, bWord in [(aWord, bWord) for aWord in unMatchedWords for bWord in sideTwoArray]:
        value = SequenceMatcher(a=aWord, b=bWord).ratio()
        if value > tolerance:
            relationship_dict[aWord] = bWord

    return relationship_dict

#################################################################################################
# Rename the pair of joints of jnt hierchies
#


def rename_sibilings(jointsDictionary):
    """
    Param: jointsDictionary :: output from match_strings
    """
    for main, pair in jointsDictionary:
        name = main.replace('_L_', '_R_')
        node = pm.PyNode(pair)
        pm.rename(node, name)


#################################################################################################

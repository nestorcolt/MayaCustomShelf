from MCSS_Project.main.imports_and_globals import *

# Shelf project modules
from MCSS_Project.skin import mainSkin
from MCSS_Project.toggle import mainToggle
from MCSS_Project.create import mainCreate
from MCSS_Project import scripts
from MCSS_Project import tools

"""

    Description: This Module holds the logic behind getter methods to fecth the data about scripts and tools to the shelf

"""

###################################################################################################
# globals
"""

    Description: If a new module to feed a popup button is created, must be inserted into MODULES dictionary after import

"""

MODULES = {"Skin": mainSkin, "Toggle": mainToggle, "Create": mainCreate}
MODULES_STRUCT = OrderedDict({})

###################################################################################################
# For popups menus getter method


def get_file_members(module):
    """

        Description: Get all functions/members into a file
        @Param: Module file to check
        @Return: Dictionary with Function name as key and address in memory as value

    """

    # reload module to add / remove changes in the file

    module_name = inspect.getmodule(module).__name__
    module_path = inspect.getsourcefile(module)

    for itm, value in sys.modules.items():
        if module == value:
            # print("module: {} - path: {}".format(itm, value))
            del sys.modules[itm]

    sys.modules[module_name] = module
    reload(module)
    #

    func_dict = OrderedDict({})
    # print("Module : {}\n".format(module))

    # Get members of module
    functions_list = [obj for obj in inspect.getmembers(module) if inspect.isfunction(obj[1])]

    for func in functions_list:
        path = inspect.getmodule(module).__name__
        func_dict[func[0]] = func[1]
        # print('Function Name: {:25}   -   Address in memory: {:55}    -    Path: {}.{}'.format(func[0], func[1], path, func[0]))

    # print("\t\t\t\t-----------------------------------------------------------------------------------------------------------------------------------------------------")

    return func_dict


# Collect the info form each module in MODULES dictionary
for moduleName, module in MODULES.items():
    module_info = get_file_members(module)
    MODULES_STRUCT[moduleName] = module_info

###################################################################################################
# For scripts button getter method


def get_scripts_files():
    """

        Description: get all the script files from Scripts directory
        @Return: Dictionary with script name and script path

    """

    # reload scripts module to add any new script files
    reload(scripts)
    dict_o = {}
    script_path = [itm for itm in os.listdir(SCRIPTS_DIR) if "__init__" not in itm]

    for itm in script_path:
        path = os.path.join(SCRIPTS_DIR, itm)
        name = itm.split(".")[0]
        dict_o[name] = path

    return dict_o


SCRIPTS_DATA = get_scripts_files()

###################################################################################################
# For tools buttons getter method


def get_tools():
    """

        Description: get and fetch all the tools from tools directory
        @Return: Dictionary with tool name and tools execute file path

    """

    # reload tools module to add any new script files
    reload(tools)

    dict_o = {}
    tools_path = [itm for itm in os.listdir(TOOLS_DIR) if "__init__" not in itm]

    for itm in tools_path:
        tool_dir = os.listdir(os.path.join(TOOLS_DIR, itm))
        executable = [os.path.join(TOOLS_DIR, itm, file) for file in tool_dir if "execute" in file]

        if not executable:
            continue

        dict_o[itm] = executable[0]

    return dict_o


TOOLS_DATA = get_tools()

###################################################################################################

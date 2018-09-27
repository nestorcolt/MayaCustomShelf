from MCSS_Project.main.imports_and_globals import *


#############################################################################################################################
# This function clean all modules initialized from memory to make a fresh start when reloading and testing. this is equivalent
# to reload(*) function but globalized


def resetLoadedModules(userPath=None):
    if userPath is None:
        userPath = os.path.dirname(os.path.dirname(__file__))

    # Convert this to lower just for a clean comparison later
    userPath = userPath.lower()
    toDelete = []

    # Iterate over all the modules that are currently loaded
    for key, module in sys.modules.items():
        if module is None:
            continue

        # There's a few modules that are going to complain if you try to query them
        # so I've popped this into a try/except to keep it safe
        try:
            # Use the "inspect" library to get the moduleFilePath that the current module was loaded from
            moduleFilePath = inspect.getfile(module).lower()

            # Don't try and remove the startup script, that will break everything
            if moduleFilePath == __file__.lower():
                continue

            # If the module's filepath contains the userPath, add it to the list of modules to delete
            if moduleFilePath.startswith(userPath):
                print("Removing %s" % key)
                toDelete.append(key)

        except:
            pass

    # If we'd deleted the module in the loop above, it would have changed the size of the dictionary and
    # broken the loop. So now we go over the list we made and delete all the modules
    for module in toDelete:
        del (sys.modules[module])

###################################################################################################


if __name__ == '__main__':
    resetLoadedModules()

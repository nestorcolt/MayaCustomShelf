import os
import re
import collections
from datetime import datetime

###################################################################################################
# GLOBALS:
FILE_PATH = 'C:\\Users\\colt-desk\\Desktop\\finder_dummy'


###################################################################################################


class LatestFileFinderEngine(object):

    def __init__(self):

        print('Running Finder Object')
        print()

        self.latestUserData = {}
        self.success = False

    ###################################################################################################
    #  finds the latest file and store the data into a class property
    #

    def finder(self, rootPath='', date=True, serial=False, userFilter='', hint='', rigFilter=''):
        # checker to sett if the finder was successfull
        #
        self.success = False

        if rootPath is None:
            return

        if not os.path.exists(rootPath):
            return

        folders = os.listdir(rootPath)

        if userFilter:
            new_Path = os.path.join(rootPath, userFilter)
            if not os.path.exists(new_Path):
                print('User Given no Exist in Folder Path')
                return

            folders = [userFilter]

        userFiles = collections.defaultdict(list)
        latestDate = []
        latestFile = []

        for user in folders:
            listPath = ''
            newPath = os.path.join(rootPath, user)

            try:
                listPath = os.listdir(newPath)
            except:
                continue

            for fldr in listPath:
                if fldr == 'maya':
                    mayaPath = os.path.join(newPath, fldr)
                    mayaListPath = os.listdir(mayaPath)

                    for fl in mayaListPath:
                        if fl == 'scenes':
                            scenesPath = os.path.join(mayaPath, fl)
                            scenesListPath = [itm for itm in os.listdir(scenesPath) if itm.endswith('.mb') or itm.endswith('.ma')]

                            hint_filtered = []
                            rig_filtered = []

                            if rigFilter:
                                for scene in scenesListPath:
                                    match = re.search(r'(?:^|\B|[0-9]|_|[a-z]){}(?:\B|$|[0-9]|_|[a-z])'.format(rigFilter), scene, flags=re.I)

                                    if match is not None:
                                        rig_filtered.append(scene)

                                #
                                scenesListPath = rig_filtered

                            if hint:
                                for scene in scenesListPath:
                                    match = re.search(r'(?:^|\B|[0-9]|_|[a-z]){}(?:\B|$|[0-9]|_|[a-z])'.format(hint), scene, flags=re.I)

                                    if match is not None:
                                        hint_filtered.append(scene)

                                #
                                scenesListPath = hint_filtered

                            allFiles = []
                            allDates = []

                            # If len array with maya files is empty, continue loop
                            if len(scenesListPath) < 1:
                                continue

                            if serial:
                                rawSceneNames = [os.path.splitext(scn)[0] for scn in scenesListPath]
                                digitedScene = [str(itm) for itm in rawSceneNames if itm[-1].isdigit()]

                                if len(digitedScene) == 0:
                                    continue

                                latestSuffix = max([itm.split('_')[-1] for itm in digitedScene])

                                latestFile = [itm for itm in digitedScene if itm.endswith(latestSuffix)]
                                userFiles[user].append([[os.path.join(scenesPath, itm) for itm in scenesListPath if latestFile[0] in itm], latestFile[0]])

                            if date:
                                for file in scenesListPath:
                                    filePath = os.path.join(scenesPath, file)
                                    modified = datetime.fromtimestamp(os.stat(filePath).st_mtime)

                                    allFiles.append(filePath)
                                    allDates.append(modified)
                                    latestDate.append(modified)
                                    # print('FileName: %s - Date: %s' % (file, datetime.fromtimestamp(modified)))

                                latest = max([date for date in allDates])
                                sceneFile = [itm for itm in allFiles if latest == datetime.fromtimestamp(os.stat(itm).st_mtime)]
                                userFiles[user].append([sceneFile[0], latest])

        #
        latestFileData = {}

        if date:
            if len(latestDate) == 0:
                print('No match with given hint, path or user ...')
                return

            # yield the latest date file from dates array

            yieldDate = max(latestDate)
            latestFileData = {}

            for user, sceneData in userFiles.items():
                if sceneData[0][1] == yieldDate:
                    latestFileData['user'] = user
                    latestFileData['file'] = sceneData[0][0]
                    latestFileData['date'] = sceneData[0][1]
                    latestFileData['scene'] = sceneData[0][0]
                    break

            # data stored into class property
            self.latestUserData = latestFileData
            self.success = True

        if serial:
            latestNumber = []
            outputArray = []

            for user, data in userFiles.items():
                fileName = data[0][1]
                latestNumber.append(data[0][1].split('_')[-1])

            number = max(latestNumber)

            for user, data in userFiles.items():
                # print(user, data[0][0])
                pre_output_array = []
                files_array = data[0][0]

                for itm in files_array:
                    name = os.path.splitext(os.path.basename(os.path.normpath(itm)))[0]
                    # print(name)
                    if name.endswith(number):
                        singleScene = itm
                        fileName = data[0][1]
                        date = datetime.fromtimestamp(os.stat(singleScene).st_mtime)
                        outputArray.append([user, singleScene, date, fileName])

            if len(outputArray) > 1:
                print('More than two matches found, try filter by date instead')
                return

            else:
                to_dict_Array = outputArray[0]
                latestFileData['user'] = to_dict_Array[0]
                latestFileData['file'] = to_dict_Array[1]
                latestFileData['date'] = to_dict_Array[2]
                latestFileData['scene'] = to_dict_Array[3]

                # data stored into class property
                self.latestUserData = latestFileData
                self.success = True

    ###################################################################################################
    # returns data to user to print, find, open or import
    #

    def returnDataToUser(self):
        if self.latestUserData is None or len(self.latestUserData) < 1:
            return

        if self.success:
            print('User:\n%s' % self.latestUserData['user'].capitalize())
            print('SceneName:\n%s' % os.path.basename(os.path.normpath(self.latestUserData['scene'])))
            print('LatestDate:\n%s' % self.latestUserData['date'])
            print('FilePath:\n%s' % self.latestUserData['file'])
            print()

###################################################################################################



###################################################################################################
#
if __name__ == '__main__':
    finderObject = LatestFileFinderEngine()
    finderObject.finder(rootPath=FILE_PATH, serial=True, userFilter='', hint='')
    finderObject.returnDataToUser()

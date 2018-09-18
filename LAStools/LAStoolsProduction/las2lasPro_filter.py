# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2lasPro_filter.py
    ---------------------
    Date                 : October 2014, May 2016 and August 2018
    Copyright            : (C) 2014 by Martin Isenburg
    Email                : martin near rapidlasso point com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Martin Isenburg'
__date__ = 'October 2014'
__copyright__ = '(C) 2014, Martin Isenburg'

import os

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class las2lasPro_filter(LAStoolsAlgorithm):

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParametersFilter1ReturnClassFlagsGUI()
        self.addParametersFilter2ReturnClassFlagsGUI()
        self.addParametersFilter1CoordsIntensityGUI()
        self.addParametersFilter2CoordsIntensityGUI()
        self.addParametersPointOutputGUI()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2las.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2las")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersFilter1ReturnClassFlagsCommands(parameters, context, commands)
        self.addParametersFilter2ReturnClassFlagsCommands(parameters, context, commands)
        self.addParametersFilter1CoordsIntensityCommands(parameters, context, commands)
        self.addParametersFilter2CoordsIntensityCommands(parameters, context, commands)
        self.addParametersPointOutputCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'las2lasPro_filter'

    def displayName(self):
        return 'las2lasPro_filter'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return las2lasPro_filter()

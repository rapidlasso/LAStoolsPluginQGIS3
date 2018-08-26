# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasgroundPro.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : April 2014
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum


class lasgroundPro(LAStoolsAlgorithm):

    NO_BULGE = "NO_BULGE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasgroundPro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParametersHorizontalAndVerticalFeetGUI()
        self.addParameter(ParameterBoolean(lasgroundPro.NO_BULGE,
                                           self.tr("no triangle bulging during TIN refinement"), False))
        self.addParameter(ParameterSelection(lasgroundPro.TERRAIN,
                                             self.tr("terrain type"), lasgroundPro.TERRAINS, 1))
        self.addParameter(ParameterSelection(lasgroundPro.GRANULARITY,
                                             self.tr("preprocessing"), lasgroundPro.GRANULARITIES, 1))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersHorizontalAndVerticalFeetCommands(parameters, context, commands)
        if (self.getParameterValue(lasgroundPro.NO_BULGE)):
            commands.append("-no_bulge")
        method = self.getParameterValue(lasgroundPro.TERRAIN)
        if (method != 1):
            commands.append("-" + lasgroundPro.TERRAINS[method])
        granularity = self.getParameterValue(lasgroundPro.GRANULARITY)
        if (granularity != 1):
            commands.append("-" + lasgroundPro.GRANULARITIES[granularity])
        self.addParametersCoresCommands(parameters, context, commands)
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszipPro'

    def displayName(self):
        return 'laszipPro'

    def group(self):
        return 'folder - conversion'

    def groupId(self):
        return 'folder - conversion'

    def createInstance(self):
        return laszipPro()
	

# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasgridPro.py
    ---------------------
    Date                 : October 2014 and August 2018
    Copyright            : (C) 2013 by Martin Isenburg
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

from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean


class lasgridPro(LAStoolsAlgorithm):

    ATTRIBUTE = "ATTRIBUTE"
    METHOD = "METHOD"
    ATTRIBUTES = ["elevation", "intensity", "rgb", "classification"]
    METHODS = ["lowest", "highest", "average", "stddev"]
    USE_TILE_BB = "USE_TILE_BB"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasgridPro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParametersPointInputMergedGUI()
        self.addParametersFilter1ReturnClassFlagsGUI()
        self.addParametersStepGUI()
        self.addParameter(ParameterSelection(lasgridPro.ATTRIBUTE,
                                             self.tr("Attribute"), lasgridPro.ATTRIBUTES, 0))
        self.addParameter(ParameterSelection(lasgridPro.METHOD,
                                             self.tr("Method"), lasgridPro.METHODS, 0))
        self.addParameter(ParameterBoolean(lasgridPro.USE_TILE_BB,
                                           self.tr("use tile bounding box (after tiling with buffer)"), False))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersRasterOutputFormatGUI()
        self.addParametersRasterOutputGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasgrid")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersPointInputMergedCommands(parameters, context, commands)
        self.addParametersFilter1ReturnClassFlagsCommands(parameters, context, commands)
        self.addParametersStepCommands(parameters, context, commands)
        attribute = self.getParameterValue(lasgridPro.ATTRIBUTE)
        if attribute != 0:
            commands.append("-" + lasgridPro.ATTRIBUTES[attribute])
        method = self.getParameterValue(lasgridPro.METHOD)
        if method != 0:
            commands.append("-" + lasgridPro.METHODS[method])
        if (self.getParameterValue(lasgridPro.USE_TILE_BB)):
            commands.append("-use_tile_bb")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersRasterOutputFormatCommands(parameters, context, commands)
        self.addParametersRasterOutputCommands(parameters, context, commands)
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
	

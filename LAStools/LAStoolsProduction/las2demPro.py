# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2demPro.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : September 2013
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class las2demPro(LAStoolsAlgorithm):

    ATTRIBUTE = "ATTRIBUTE"
    PRODUCT = "PRODUCT"
    ATTRIBUTES = ["elevation", "slope", "intensity", "rgb", "edge_longest", "edge_shortest"]
    PRODUCTS = ["actual values", "hillshade", "gray", "false"]
    USE_TILE_BB = "USE_TILE_BB"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParametersFilter1ReturnClassFlagsGUI()
        self.addParametersStepGUI()
        self.addParameter(QgsProcessingParameterEnum(las2demPro.ATTRIBUTE, "Attribute", las2demPro.ATTRIBUTES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(las2demPro.PRODUCT, "Product", las2demPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterBoolean(las2demPro.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersRasterOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2dem")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersFilter1ReturnClassFlagsCommands(parameters, context, commands)
        self.addParametersStepCommands(parameters, context, commands)
        attribute = self.parameterAsInt(parameters, las2demPro.ATTRIBUTE, context)
        if (attribute != 0):
            commands.append("-" + las2demPro.ATTRIBUTES[attribute])
        product = self.parameterAsInt(parameters, las2demPro.PRODUCT, context)
        if (product != 0):
            commands.append("-" + las2demPro.PRODUCTS[product])
        if (self.parameterAsBool(parameters, las2demPro.USE_TILE_BB, context)):
            commands.append("-use_tile_bb")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersRasterOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'las2demPro'

    def displayName(self):
        return 'las2demPro'

    def group(self):
        return 'folder - raster derivatives'

    def groupId(self):
        return 'folder - raster derivatives'

    def createInstance(self):
        return las2demPro()

# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2dem.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : September 2013 and August 2018
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

class las2dem(LAStoolsAlgorithm):

    ATTRIBUTE = "ATTRIBUTE"
    PRODUCT = "PRODUCT"
    ATTRIBUTES = ["elevation", "slope", "intensity", "rgb", "edge_longest", "edge_shortest"]
    PRODUCTS = ["actual values", "hillshade", "gray", "false"]
    USE_TILE_BB = "USE_TILE_BB"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParametersFilter1ReturnClassFlagsGUI()
        self.addParametersStepGUI()
        self.addParameter(QgsProcessingParameterEnum(las2dem.ATTRIBUTE, "Attribute", las2dem.ATTRIBUTES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(las2dem.PRODUCT, "Product", las2dem.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterBoolean(las2dem.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False))
        self.addParametersRasterOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2dem")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersFilter1ReturnClassFlagsCommands(parameters, context, commands)
        self.addParametersStepCommands(parameters, context, commands)
        attribute = self.parameterAsInt(parameters, las2dem.ATTRIBUTE, context)
        if (attribute != 0):
            commands.append("-" + las2dem.ATTRIBUTES[attribute])
        product = self.parameterAsInt(parameters, las2dem.PRODUCT, context)
        if (product != 0):
            commands.append("-" + las2dem.PRODUCTS[product])
        if (self.parameterAsBool(parameters, las2dem.USE_TILE_BB, context)):
            commands.append("-use_tile_bb")
        self.addParametersRasterOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'las2dem'

    def displayName(self):
        return 'las2dem'

    def group(self):
        return 'file - raster derivatives'

    def groupId(self):
        return 'file - raster derivatives'

    def createInstance(self):
        return las2dem()

# -*- coding: utf-8 -*-

"""
***************************************************************************
    blast2demPro.py
    ---------------------
    Date                 : October 2014 and August 2018
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

from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean


class blast2demPro(LAStoolsAlgorithm):

    ATTRIBUTE = "ATTRIBUTE"
    PRODUCT = "PRODUCT"
    ATTRIBUTES = ["elevation", "slope", "intensity", "rgb"]
    PRODUCTS = ["actual values", "hillshade", "gray", "false"]
    USE_TILE_BB = "USE_TILE_BB"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('blast2demPro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParametersPointInputMergedGUI()
        self.addParametersFilter1ReturnClassFlagsGUI()
        self.addParametersStepGUI()
        self.addParameter(ParameterSelection(blast2demPro.ATTRIBUTE,
                                             self.tr("Attribute"), blast2demPro.ATTRIBUTES, 0))
        self.addParameter(ParameterSelection(blast2demPro.PRODUCT,
                                             self.tr("Product"), blast2demPro.PRODUCTS, 0))
        self.addParameter(ParameterBoolean(blast2demPro.USE_TILE_BB,
                                           self.tr("Use tile bounding box (after tiling with buffer)"), False))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersRasterOutputFormatGUI()
        self.addParametersRasterOutputGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "blast2dem")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersPointInputMergedCommands(parameters, context, commands)
        self.addParametersFilter1ReturnClassFlagsCommands(parameters, context, commands)
        self.addParametersStepCommands(parameters, context, commands)
        attribute = self.getParameterValue(blast2demPro.ATTRIBUTE)
        if attribute != 0:
            commands.append("-" + blast2demPro.ATTRIBUTES[attribute])
        product = self.getParameterValue(blast2demPro.PRODUCT)
        if product != 0:
            commands.append("-" + blast2demPro.PRODUCTS[product])
        if (self.getParameterValue(blast2demPro.USE_TILE_BB)):
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
	

# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasoverlapPro.py
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
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasoverlapPro(LAStoolsAlgorithm):

    CHECK_STEP = "CHECK_STEP"
    ATTRIBUTE = "ATTRIBUTE"
    OPERATION = "OPERATION"
    ATTRIBUTES = ["elevation", "intensity", "number_of_returns", "scan_angle_abs", "density"]
    OPERATIONS = ["lowest", "highest", "average"]
    CREATE_OVERLAP_RASTER = "CREATE_OVERLAP_RASTER"
    CREATE_DIFFERENCE_RASTER = "CREATE_DIFFERENCE_RASTER"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParametersFilesAreFlightlinesGUI()
        self.addParametersFilter1ReturnClassFlagsGUI()
        self.addParameter(QgsProcessingParameterNumber(lasoverlapPro.CHECK_STEP, "size of grid used for overlap check", QgsProcessingParameterNumber.Double, 2.0, False, 0.001, 50.0))
        self.addParameter(QgsProcessingParameterEnum(lasoverlapPro.ATTRIBUTE, "attribute to check", lasoverlapPro.ATTRIBUTES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lasoverlapPro.OPERATION, "operation on attribute per cell", lasoverlapPro.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterBoolean(lasoverlapPro.CREATE_OVERLAP_RASTER, "create overlap raster", True))
        self.addParameter(QgsProcessingParameterBoolean(lasoverlapPro.CREATE_DIFFERENCE_RASTER, "create difference raster", True))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersRasterOutputFormatGUI()
        self.addParametersRasterOutputGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasoverlap")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersFilesAreFlightlinesCommands(parameters, context, commands)
        self.addParametersFilter1ReturnClassFlagsCommands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, lasoverlapPro.CHECK_STEP, context)
        if (step != 2.0):
            commands.append("-step")
            commands.append(unicode(step))
        commands.append("-values")
        attribute = self.parameterAsInt(parameters, lasoverlapPro.ATTRIBUTE, context)
        if (attribute != 0):
            commands.append("-" + lasoverlapPro.ATTRIBUTES[attribute])
        operation = self.parameterAsInt(parameters, lasoverlapPro.OPERATION, context)
        if (operation != 0):
            commands.append("-" + lasoverlapPro.OPERATIONS[operation])
        if (not self.parameterAsBool(parameters, lasoverlapPro.CREATE_OVERLAP_RASTER, context)):
            commands.append("-no_over")
        if (not self.parameterAsBool(parameters, lasoverlapPro.CREATE_DIFFERENCE_RASTER, context)):
            commands.append("-no_diff")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersRasterOutputFormatCommands(parameters, context, commands)
        self.addParametersRasterOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasoverlapPro'

    def displayName(self):
        return 'lasoverlapPro'

    def group(self):
        return 'folder - checking quality'

    def groupId(self):
        return 'folder - checking quality'

    def createInstance(self):
        return lasoverlapPro()

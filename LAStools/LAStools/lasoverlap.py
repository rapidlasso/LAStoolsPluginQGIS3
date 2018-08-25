# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasoverlap.py
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

__author__ = 'Martin Isenburg'
__date__ = 'September 2013'
__copyright__ = '(C) 2013, Martin Isenburg'


import os
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum


class lasoverlap(LAStoolsAlgorithm):

    CHECK_STEP = "CHECK_STEP"
    ATTRIBUTE = "ATTRIBUTE"
    OPERATION = "OPERATION"
    ATTRIBUTES = ["elevation", "intensity", "number_of_returns", "scan_angle_abs", "density"]
    OPERATIONS = ["lowest", "highest", "average"]
    CREATE_OVERLAP_RASTER = "CREATE_OVERLAP_RASTER"
    CREATE_DIFFERENCE_RASTER = "CREATE_DIFFERENCE_RASTER"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasoverlap')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParametersFilter1ReturnClassFlagsGUI()
        self.addParameter(QgsProcessingParameterNumber(lasoverlap.CHECK_STEP,
                                          self.tr("size of grid used for overlap check"), 0, None, 2.0))
        self.addParameter(QgsProcessingParameterEnum(lasoverlap.ATTRIBUTE,
                                             self.tr("attribute to check"), lasoverlap.ATTRIBUTES, 0))
        self.addParameter(QgsProcessingParameterEnum(lasoverlap.OPERATION,
                                             self.tr("operation on attribute per cell"), lasoverlap.OPERATIONS, 0))
        self.addParameter(QgsProcessingParameterBoolean(lasoverlap.CREATE_OVERLAP_RASTER,
                                           self.tr("create overlap raster"), True))
        self.addParameter(QgsProcessingParameterBoolean(lasoverlap.CREATE_DIFFERENCE_RASTER,
                                           self.tr("create difference raster"), True))
        self.addParametersRasterOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasoverlap")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersFilter1ReturnClassFlagsCommands(parameters, context, commands)
        step = self.parameterAsInt(parameters, lasoverlap.CHECK_STEP)
        if step != 0.0:
            commands.append("-step")
            commands.append(unicode(step))
        commands.append("-values")
        attribute = self.parameterAsInt(parameters, lasoverlap.ATTRIBUTE)
        if attribute != 0:
            commands.append("-" + lasoverlap.ATTRIBUTES[attribute])
        operation = self.parameterAsInt(parameters, lasoverlap.OPERATION)
        if operation != 0:
            commands.append("-" + lasoverlap.OPERATIONS[operation])
        if not self.parameterAsInt(parameters, lasoverlap.CREATE_OVERLAP_RASTER):
            commands.append("-no_over")
        if not self.parameterAsInt(parameters, lasoverlap.CREATE_DIFFERENCE_RASTER):
            commands.append("-no_diff")
        self.addParametersRasterOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszip'

    def displayName(self):
        return 'laszip'

    def group(self):
        return 'LAStools'

    def groupId(self):
        return 'LAStools'

    def createInstance(self):
        return laszip()
	
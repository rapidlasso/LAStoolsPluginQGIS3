# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2shp.py
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
from processing.core.outputs import OutputVector


class las2shp(LAStoolsAlgorithm):

    POINT_Z = "POINT_Z"
    RECORD_SIZE = "RECORD_SIZE"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('las2shp')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterBoolean(las2shp.POINT_Z,
                                           self.tr("use PointZ instead of MultiPointZ"), False))
        self.addParameter(QgsProcessingParameterNumber(las2shp.RECORD_SIZE,
                                          self.tr("number of points per record"), 0, None, 1024))
        self.addOutput(OutputVector(las2shp.OUTPUT,
                                    self.tr("Output SHP file")))
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2shp")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        if self.parameterAsInt(parameters, las2shp.POINT_Z):
            commands.append("-single_points")
        record_size = self.parameterAsInt(parameters, las2shp.RECORD_SIZE)
        if record_size != 1024:
            commands.append("-record_size")
            commands.append(unicode(record_size))
        commands.append("-o")
        commands.append(self.getOutputValue(las2shp.OUTPUT))
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
	
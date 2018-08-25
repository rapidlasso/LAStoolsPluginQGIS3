# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasclip.py
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
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from processing.core.parameters import ParameterVector
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum


class lasclip(LAStoolsAlgorithm):

    POLYGON = "POLYGON"
    INTERIOR = "INTERIOR"
    OPERATION = "OPERATION"
    OPERATIONS = ["clip", "classify"]
    CLASSIFY_AS = "CLASSIFY_AS"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasclip')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParameter(ParameterVector(lasclip.POLYGON,
                                          self.tr("Input polygon(s)"), ParameterVector.VECTOR_TYPE_POLYGON))
        self.addParameter(QgsProcessingParameterBoolean(lasclip.INTERIOR,
                                           self.tr("interior"), False))
        self.addParameter(QgsProcessingParameterEnum(lasclip.OPERATION,
                                             self.tr("what to do with points"), lasclip.OPERATIONS, 0))
        self.addParameter(QgsProcessingParameterNumber(lasclip.CLASSIFY_AS,
                                          self.tr("classify as"), 0, None, 12))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasclip")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        poly = self.parameterAsInt(parameters, lasclip.POLYGON)
        if poly is not None:
            commands.append("-poly")
            commands.append(poly)
        if self.parameterAsInt(parameters, lasclip.INTERIOR):
            commands.append("-interior")
        operation = self.parameterAsInt(parameters, lasclip.OPERATION)
        if operation != 0:
            commands.append("-classify")
            classify_as = self.parameterAsInt(parameters, lasclip.CLASSIFY_AS)
            commands.append(unicode(classify_as))
        self.addParametersPointOutputCommands(parameters, context, commands)
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
	
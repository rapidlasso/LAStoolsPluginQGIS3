# -*- coding: utf-8 -*-

"""
***************************************************************************
    lascontrol.py
    ---------------------
    Date                 : May 2016 and August 2018
    Copyright            : (C) 2016 by Martin Isenburg
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
__date__ = 'May 2016'
__copyright__ = '(C) 2016, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lascontrol(LAStoolsAlgorithm):

    PARSE_STRING = "PARSE_STRING"
    USE_POINTS = "USE_POINTS"
    USE_POINTS_LIST = ["all", "ground (2)", "ground (2) and keypoints (8)", "ground (2), buldings (6), and keypoints (8)"]
    ADJUST_Z = "ADJUST_Z"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParametersGenericInputGUI("ASCII text file of control points", "csv", False)
        self.addParameter(QgsProcessingParameterString(lascontrol.PARSE_STRING, "parse string marking which columns are xyz (use 's' for skip)", "sxyz"))
        self.addParameter(QgsProcessingParameterEnum(lascontrol.USE_POINTS, "which points to use for elevation checks", lascontrol.USE_POINTS_LIST, False, 0))
        self.addParameter(QgsProcessingParameterBoolean(lascontrol.ADJUST_Z, "adjust z elevation by translating away the average error", False))
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lascontrol")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersGenericInputCommandsfile(parameters, context, commands, "-cp")
        parse = self.parameterAsString(parameters, lascontrol.PARSE_STRING, context)
        if parse != "":
            commands.append("-parse")
            commands.append(parse)
        use_point = self.parameterAsInt(parameters, lascontrol.USE_POINTS, context)
        if use_point > 0:
            commands.append("-keep_class")
            commands.append(unicode(2))
            if use_point > 1:
                commands.append(unicode(8))
                if use_point > 2:
                    commands.append(unicode(6))
        if self.parameterAsBool(parameters, lascontrol.ADJUST_Z, context):
            commands.append("-adjust_z")
            commands.append("-odix _adjusted")
            commands.append("-olaz")
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lascontrol'

    def displayName(self):
        return 'lascontrol'

    def group(self):
        return 'file - checking quality'

    def groupId(self):
        return 'file - checking quality'

    def createInstance(self):
        return lascontrol()

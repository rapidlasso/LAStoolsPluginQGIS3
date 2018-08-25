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
from LAStoolsUtils import LAStoolsUtils
from LAStoolsAlgorithm import LAStoolsAlgorithm

from processing.core.parameters import ParameterFile
from processing.core.parameters import ParameterString
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum


class lascontrol(LAStoolsAlgorithm):

    CONTROL_POINT_FILE = "CONTROL_POINT_FILE"
    PARSE_STRING = "PARSE_STRING"
    USE_POINTS = "USE_POINTS"
    USE_POINTS_LIST = ["all", "ground (2)", "ground (2) and keypoints (8)", "ground (2), buldings (6), and keypoints (8)"]
    ADJUST_Z = "ADJUST_Z"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lascontrol')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParameter(ParameterFile(lascontrol.CONTROL_POINT_FILE,
                                        self.tr("ASCII text file of control points"), False, False))
        self.addParameter(ParameterString(lascontrol.PARSE_STRING,
                                          self.tr("parse string marking which columns are xyz (use 's' for skip)"), "sxyz", False, False))
        self.addParameter(QgsProcessingParameterEnum(lascontrol.USE_POINTS,
                                             self.tr("which points to use for elevation checks"), lascontrol.USE_POINTS_LIST, 0))
        self.addParameter(QgsProcessingParameterBoolean(lascontrol.ADJUST_Z,
                                           self.tr("adjust z elevation by translating away the average error"), False))
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lascontrol")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        file = self.parameterAsInt(parameters, lascontrol.CONTROL_POINT_FILE)
        if file is not None:
            commands.append("-cp")
            commands.append('"' + file + '"')
        parse = self.parameterAsInt(parameters, lascontrol.PARSE_STRING)
        if parse is not None:
            commands.append("-parse")
            commands.append(parse)
        use_point = self.parameterAsInt(parameters, lascontrol.USE_POINTS)
        if use_point > 0:
            commands.append("-keep_class")
            commands.append(unicode(2))
            if use_point > 1:
                commands.append(unicode(8))
                if use_point > 2:
                    commands.append(unicode(6))
        if self.parameterAsInt(parameters, lascontrol.ADJUST_Z):
            commands.append("-adjust_z")
            commands.append("-odix _adjusted")
            commands.append("-olaz")
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
	
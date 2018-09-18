# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2lasPro_transform.py
    ---------------------
    Date                 : October 2014, May 2016 and August 2018
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

from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class las2lasPro_transform(LAStoolsAlgorithm):

    OPERATION = "OPERATION"
    OPERATIONS = ["---", "set_point_type", "set_point_size", "set_version_minor", "set_version_major", "start_at_point", "stop_at_point", "remove_vlr", "week_to_adjusted", "adjusted_to_week", "auto_reoffset", "scale_rgb_up", "scale_rgb_down", "remove_all_vlrs", "remove_extra", "clip_to_bounding_box"]
    OPERATIONARG = "OPERATIONARG"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParametersTransform1CoordinateGUI()
        self.addParametersTransform2CoordinateGUI()
        self.addParametersTransform1OtherGUI()
        self.addParametersTransform2OtherGUI()
        self.addParameter(QgsProcessingParameterEnum(las2lasPro_transform.OPERATION, "operations (first 8 need an argument)", las2lasPro_transform.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterString(las2lasPro_transform.OPERATIONARG, "argument for operation"))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2las.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2las")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersTransform1CoordinateCommands(parameters, context, commands)
        self.addParametersTransform2CoordinateCommands(parameters, context, commands)
        self.addParametersTransform1OtherCommands(parameters, context, commands)
        self.addParametersTransform2OtherCommands(parameters, context, commands)
        operation = self.parameterAsInt(parameters, las2lasPro_transform.OPERATION, context)
        if (operation != 0):
            commands.append("-" + las2lasPro_transform.OPERATIONS[operation])
            if (operation > 8):
                commands.append(self.parameterAsString(parameters, las2lasPro_transform.OPERATIONARG, context))
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'las2lasPro_transform'

    def displayName(self):
        return 'las2lasPro_transform'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return las2lasPro_transform()

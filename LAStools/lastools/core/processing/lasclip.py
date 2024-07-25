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
    Copyright            : (C) 2013 by rapidlasso GmbH
    Email                : info near rapidlasso point de
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = "Victor Olaya"
__date__ = "August 2012"
__copyright__ = "(C) 2012, Victor Olaya"

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasClip(LastoolsAlgorithm):
    TOOL_NAME = "LasClip"
    LASTOOL = "lasclip"
    LICENSE = "c"
    LASGROUP = 3
    INTERIOR = "INTERIOR"
    OPERATION = "OPERATION"
    OPERATIONS = ["clip", "classify"]
    CLASSIFY_AS = "CLASSIFY_AS"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_generic_input_gui("input polygon(s)", "shp", False)
        self.addParameter(QgsProcessingParameterBoolean(LasClip.INTERIOR, "interior", False))
        self.addParameter(
            QgsProcessingParameterEnum(LasClip.OPERATION, "what to do with points", LasClip.OPERATIONS, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasClip.CLASSIFY_AS, "classify as", QgsProcessingParameterNumber.Integer, 12, False, 0, 255
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-poly")
        if self.parameterAsBool(parameters, LasClip.INTERIOR, context):
            commands.append("-interior")
        operation = self.parameterAsInt(parameters, LasClip.OPERATION, context)
        if operation != 0:
            commands.append("-classify")
            classify_as = self.parameterAsInt(parameters, LasClip.CLASSIFY_AS, context)
            commands.append(str(classify_as))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasClip()

    def name(self):
        return self.TOOL_NAME

    def displayName(self):
        return lastool_info[self.TOOL_NAME]["disp"]

    def group(self):
        return lasgroup_info[self.LASGROUP]["group"]

    def groupId(self):
        return lasgroup_info[self.LASGROUP]["group_id"]

    def helpUrl(self):
        return readme_url(self.LASTOOL)

    def shortHelpString(self):
        return lastool_info[self.TOOL_NAME]["help"] + help_string_help(self.LASTOOL, self.LICENSE)

    def shortDescription(self):
        return lastool_info[self.TOOL_NAME]["desc"]

    def icon(self):
        icon_file = licence[self.LICENSE]["path"]
        return QIcon(f"{paths['img']}{icon_file}")

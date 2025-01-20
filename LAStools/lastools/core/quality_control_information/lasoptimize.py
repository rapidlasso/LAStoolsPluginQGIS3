# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasoptimize.py
    ---------------------
    Date                 : January 2025
    Copyright            : (C) 2025 by rapidlasso GmbH
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

__author__ = "rapidlasso"
__date__ = "January 2025"
__copyright__ = "(C) 2025, rapidlasso GmbH"

import os

from PyQt5.QtGui import QIcon

# QgsProcessingParameterNumber, QgsProcessingParameterString, QgsProcessingParameterEnum,
from qgis.core import QgsProcessingParameterBoolean

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasOptimize(LastoolsAlgorithm):
    TOOL_NAME = "LasOptimize"
    LASTOOL = "lasoptimize"
    LICENSE = "f"
    LASGROUP = 2
    ARGAPPEND = "ARGAPPEND"
    ARGNOLAX = "ARGNOLAX"
    ARGNOFLU = "ARGNOFLU"
    ARGNOMEVL = "ARGNOMEVL"
    ARGNOREPA = "ARGNOREPA"
    ARGNOOFFS = "ARGNOOFFS"
    ARGNOZUD = "ARGNOZUD"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(self.ARGAPPEND, "append LAX index to existing file", False))
        self.addParameter(QgsProcessingParameterBoolean(self.ARGNOLAX, "do not create index file", False))
        self.addParameter(QgsProcessingParameterBoolean(self.ARGNOFLU, "do not eliminate point scale fluff", False))
        self.addParameter(QgsProcessingParameterBoolean(self.ARGNOMEVL, "do not move EVLRs", False))
        self.addParameter(QgsProcessingParameterBoolean(self.ARGNOREPA, "do not remove padding", False))
        self.addParameter(QgsProcessingParameterBoolean(self.ARGNOOFFS, "do not auto reoffset", False))
        self.addParameter(QgsProcessingParameterBoolean(self.ARGNOZUD, "do not zero user data", False))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.ARGAPPEND, context):
            commands.append("-append")
        if self.parameterAsBool(parameters, self.ARGNOLAX, context):
            commands.append("-do_not_create_lax")
        if self.parameterAsBool(parameters, self.ARGNOFLU, context):
            commands.append("-do_not_eliminate_fluff")
        if self.parameterAsBool(parameters, self.ARGNOMEVL, context):
            commands.append("-do_not_move_EVLRs")
        if self.parameterAsBool(parameters, self.ARGNOREPA, context):
            commands.append("-do_not_remove_padding")
        if self.parameterAsBool(parameters, self.ARGNOOFFS, context):
            commands.append("-do_not_set_nice_offset")
        if self.parameterAsBool(parameters, self.ARGNOZUD, context):
            commands.append("-do_not_zero_user_data")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasOptimize()

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

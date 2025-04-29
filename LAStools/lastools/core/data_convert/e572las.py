# -*- coding: utf-8 -*-
"""
***************************************************************************
    e572las.py
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


from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class e572las(LastoolsAlgorithm):
    TOOL_NAME = "e572las"
    LASTOOL = "e572las"
    LICENSE = "f"
    LASGROUP = 2
    SPLIT = "split"
    SCALE_FACTOR_XY = "SCALE_FACTOR_XY"
    SCALE_FACTOR_Z = "SCALE_FACTOR_Z"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.canGui = False
        self.add_parameters_generic_input_gui("Input ASCII file", "e57", False)
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SCALE_FACTOR_XY,
                "target scale of x and y coordinates",
                QgsProcessingParameterNumber.Double,
                0.001,
                False,
                0.001,
                1,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SCALE_FACTOR_Z,
                "target scale of z coordinate",
                QgsProcessingParameterNumber.Double,
                0.001,
                False,
                0.001,
                1,
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(self.SPLIT, "split output files by scan", False))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_generic_input_commands(parameters, context, commands, "-i")
        scale_factor_xy = self.parameterAsDouble(parameters, self.SCALE_FACTOR_XY, context)
        scale_factor_z = self.parameterAsDouble(parameters, self.SCALE_FACTOR_Z, context)
        if scale_factor_xy != 0.001 or scale_factor_z != 0.001:
            commands.append("-set_scale")
            commands.append(str(scale_factor_xy))
            commands.append(str(scale_factor_xy))
            commands.append(str(scale_factor_z))
        if self.parameterAsBool(parameters, self.SPLIT, context):
            commands.append("-split")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return e572las()

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

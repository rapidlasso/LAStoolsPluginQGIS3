# -*- coding: utf-8 -*-

"""
***************************************************************************
    lassplit.py
    ---------------------
    Date                 : January 2025
    Copyright            : (c) 2025 by rapidlasso GmbH
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
__copyright__ = "(c) 2025, rapidlasso GmbH"

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasSplit(LastoolsAlgorithm):
    TOOL_NAME = "LasSplit"
    LASTOOL = "lassplit"
    LICENSE = "c"
    LASGROUP = 3
    DIGITS = "DIGITS"
    OPERATION = "OPERATION"
    OPERATIONS = [
        "by_flightline",
        "by_classification",
        "by_gps_time_interval",
        "by_intensity_interval",
        "by_x_interval",
        "by_y_interval",
        "by_z_interval",
        "by_scan_angle_interval",
        "by_user_data_interval",
        "every_x_points",
        "recover_flightlines",
    ]
    INTERVAL = "INTERVAL"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DIGITS,
                "number of digits for file names",
                QgsProcessingParameterNumber.Integer,
                5,
                False,
                2,
                10,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.OPERATION, "how to split", self.OPERATIONS, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.INTERVAL,
                "interval or number",
                QgsProcessingParameterNumber.Double,
                5.0,
                False,
                0.00001,
                100000.0,
            )
        )
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
        digits = self.parameterAsInt(parameters, self.DIGITS, context)
        if digits != 5:
            commands.append("-digits")
            commands.append(str(digits))
        operation = self.parameterAsInt(parameters, self.OPERATION, context)
        if operation != 0:
            if operation == 9:
                commands.append("-split")
            else:
                commands.append("-" + self.OPERATIONS[operation])
        if 1 < operation < 10:
            interval = self.parameterAsDouble(parameters, self.INTERVAL, context)
            commands.append(str(interval))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasSplit()

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

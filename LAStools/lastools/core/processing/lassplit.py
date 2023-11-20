# -*- coding: utf-8 -*-

"""
***************************************************************************
    lassplit.py
    ---------------------
    Date                 : March 2014 and August 2018
    Copyright            : (C) 2023 by rapidlasso GmbH
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

__author__ = 'Martin Isenburg'
__date__ = 'March 2014'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_processing as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasSplit(LastoolsAlgorithm):
    TOOL_INFO = ('lassplit', 'LasSplit')
    DIGITS = "DIGITS"
    OPERATION = "OPERATION"
    OPERATIONS = ["by_flightline", "by_classification", "by_gps_time_interval", "by_intensity_interval",
                  "by_x_interval", "by_y_interval", "by_z_interval", "by_scan_angle_interval", "by_user_data_interval",
                  "every_x_points", "recover_flightlines"]
    INTERVAL = "INTERVAL"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterNumber(
            LasSplit.DIGITS, "number of digits for file names", QgsProcessingParameterNumber.Integer, 5, False, 2, 10
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasSplit.OPERATION, "how to split", LasSplit.OPERATIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasSplit.INTERVAL, "interval or number", QgsProcessingParameterNumber.Double, 5.0, False, 0.00001, 100000.0
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lassplit")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        digits = self.parameterAsInt(parameters, LasSplit.DIGITS, context)
        if digits != 5:
            commands.append("-digits")
            commands.append(str(digits))
        operation = self.parameterAsInt(parameters, LasSplit.OPERATION, context)
        if operation != 0:
            if operation == 9:
                commands.append("-split")
            else:
                commands.append("-" + LasSplit.OPERATIONS[operation])
        if 1 < operation < 10:
            interval = self.parameterAsDouble(parameters, LasSplit.INTERVAL, context)
            commands.append(str(interval))
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasSplit()

    def name(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["name"]

    def displayName(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["display_name"]

    def group(self):
        return descript_info["info"]["group"]

    def groupId(self):
        return descript_info["info"]["group_id"]

    def helpUrl(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["url_path"]

    def shortHelpString(self):
        return self.tr(descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_help_string"])

    def shortDescription(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_description"]

    def icon(self):
        img_path = 'licenced.png' \
            if descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence"] else 'open_source.png'
        return QIcon(f"{paths['img']}{img_path}")

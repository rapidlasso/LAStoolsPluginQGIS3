# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2shp.py
    ---------------------
    Date                 : November 2023
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

__author__ = "rapidlasso"
__date__ = "March 2024"
__copyright__ = "(C) 2024, rapidlasso GmbH"

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class Las2Shp(LastoolsAlgorithm):
    TOOL_NAME = "Las2Shp"
    LASTOOL = "las2shp"
    LICENSE = "c"
    LASGROUP = 2
    POINT_Z = "POINT_Z"
    RECORD_SIZE = "RECORD_SIZE"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(Las2Shp.POINT_Z, "use PointZ instead of MultiPointZ", False))
        self.addParameter(
            QgsProcessingParameterNumber(
                Las2Shp.RECORD_SIZE,
                "number of points per record",
                QgsProcessingParameterNumber.Integer,
                1024,
                False,
                0,
                65536,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_generic_output_gui("Output SHP file", "shp", True)

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2shp")]
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, Las2Shp.POINT_Z, context):
            commands.append("-single_points")
        record_size = self.parameterAsInt(parameters, Las2Shp.RECORD_SIZE, context)
        if record_size != 1024:
            commands.append("-record_size")
            commands.append(str(record_size))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return Las2Shp()

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

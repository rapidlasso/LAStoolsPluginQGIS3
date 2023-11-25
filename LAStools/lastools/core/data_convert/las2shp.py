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

__author__ = 'rapidlasso'
__date__ = 'September 2023'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber

from ..utils import LastoolsUtils, descript_data_convert as descript_info, paths
from ..algo import LastoolsAlgorithm


class Las2Shp(LastoolsAlgorithm):
    TOOL_INFO = ('las2shp', 'Las2Shp')
    POINT_Z = "POINT_Z"
    RECORD_SIZE = "RECORD_SIZE"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(
            Las2Shp.POINT_Z, "use PointZ instead of MultiPointZ", False
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Las2Shp.RECORD_SIZE, "number of points per record",
            QgsProcessingParameterNumber.Integer, 1024, False, 0, 65536
        ))
        self.add_parameters_generic_output_gui("Output SHP file", "shp", True)
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2shp")]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, Las2Shp.POINT_Z, context):
            commands.append("-single_points")
        record_size = self.parameterAsInt(parameters, Las2Shp.RECORD_SIZE, context)
        if record_size != 1024:
            commands.append("-record_size")
            commands.append(str(record_size))
        self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        self.add_parameters_additional_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2Shp()

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
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")

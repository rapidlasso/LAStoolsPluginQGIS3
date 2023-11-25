# -*- coding: utf-8 -*-

"""
***************************************************************************
    shp2las.py
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
from qgis.core import QgsProcessingParameterNumber

from ..utils import LastoolsUtils, descript_data_convert as descript_info, paths
from ..algo import LastoolsAlgorithm


class Shp2Las(LastoolsAlgorithm):
    TOOL_INFO = ('shp2las', 'Shp2Las')
    SCALE_FACTOR_XY = "SCALE_FACTOR_XY"
    SCALE_FACTOR_Z = "SCALE_FACTOR_Z"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui()
        self.add_parameters_generic_input_gui("Input SHP file", "shp", False)
        self.addParameter(QgsProcessingParameterNumber(
            Shp2Las.SCALE_FACTOR_XY, "resolution of x and y coordinate",
            QgsProcessingParameterNumber.Double, 0.01, False, 0.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Shp2Las.SCALE_FACTOR_Z, "resolution of z coordinate",
            QgsProcessingParameterNumber.Double, 0.01, False, 0.0
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "shp2las")]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-i")
        scale_factor_xy = self.parameterAsDouble(parameters, Shp2Las.SCALE_FACTOR_XY, context)
        scale_factor_z = self.parameterAsInt(parameters, Shp2Las.SCALE_FACTOR_Z, context)
        if scale_factor_xy != 0.01 or scale_factor_z != 0.01:
            commands.append("-set_scale_factor")
            commands.append(str(scale_factor_xy) + " " + str(scale_factor_xy) + " " + str(scale_factor_z))
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Shp2Las()

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

# -*- coding: utf-8 -*-
"""
***************************************************************************
    lasplanes.py
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


from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasPlanes(LastoolsAlgorithm):
    TOOL_NAME = "LasPlanes"
    LASTOOL = "lasplanes"
    LICENSE = "c"
    LASGROUP = 5

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_vector_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_vector_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasPlanes()

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

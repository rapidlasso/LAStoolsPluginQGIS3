# -*- coding: utf-8 -*-
"""
***************************************************************************
    self.py
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


from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasProbe(LastoolsAlgorithm):
    TOOL_NAME = "LasProbe"
    LASTOOL = "lasprobe"
    LICENSE = "o"
    LASGROUP = 6

    ARGPROBEX = "ARGPROBEX"
    ARGPROBEY = "ARGPROBEY"
    ARGSTEP = "ARGSTEP"
    ARGXYZ = "ARGXYZ"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ARGPROBEX, "probe at x pos", QgsProcessingParameterNumber.Double, 0.0, True
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ARGPROBEY, "probe at y pos", QgsProcessingParameterNumber.Double, 0.0, True
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(self.ARGSTEP, "step radius", QgsProcessingParameterNumber.Double, 5.0, False)
        )
        self.addParameter(QgsProcessingParameterBoolean(self.ARGXYZ, "output xyz value", False))
        self.add_parameters_generic_output_gui("Result file", "txt", True)
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        # xy pos
        commands.append(f"-probe {parameters['ARGPROBEX']} {parameters['ARGPROBEY']}")
        #
        commands.append(f"-step {parameters['ARGSTEP']}")
        if self.parameterAsBool(parameters, self.ARGXYZ, context):
            commands.append("-xyz")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        if self.parameterAsString(parameters, self.OUTPUT_GENERIC, context):
            self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasProbe()

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

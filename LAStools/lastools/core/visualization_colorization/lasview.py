"""
***************************************************************************
    lasview.py
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


from qgis.core import QgsProcessingParameterEnum, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasView(LastoolsAlgorithm):
    TOOL_NAME = "LasView"
    LASTOOL = "lasview"
    LICENSE = "c"
    LASGROUP = 8
    POINTS = "POINTS"
    SIZE = "SIZE"
    SIZES = ["1024 768", "800 600", "1200 900", "1200 400", "1550 900", "1550 1150"]
    COLORING = "COLORING"
    COLORINGS = ["default", "classification", "elevation1", "elevation2", "intensity", "return", "flightline", "rgb"]

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.POINTS,
                "max number of points sampled",
                QgsProcessingParameterNumber.Integer,
                5000000,
                False,
                100000,
                20000000,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.COLORING, "color by", self.COLORINGS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.SIZE, "window size (x y) in pixels", self.SIZES, False, 0))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context)]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        points = self.parameterAsInt(parameters, self.POINTS, context)
        commands.append("-points " + str(points))
        coloring = self.parameterAsInt(parameters, self.COLORING, context)
        if coloring != 0:
            commands.append("-color_by_" + self.COLORINGS[coloring])
        size = self.parameterAsInt(parameters, self.SIZE, context)
        if size != 0:
            commands.append("-win " + self.SIZES[size])
        self.add_parameters_additional_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasView()

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


class LasViewPro(LastoolsAlgorithm):
    TOOL_NAME = "LasViewPro"
    LASTOOL = "lasview"
    LICENSE = "c"
    LASGROUP = 8
    POINTS = "POINTS"
    SIZE = "SIZE"
    SIZES = ["1024 768", "800 600", "1200 900", "1200 400", "1550 900", "1550 1150"]
    COLORING = "COLORING"
    COLORINGS = ["default", "classification", "elevation1", "elevation2", "intensity", "return", "flightline", "rgb"]

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                LasViewPro.POINTS,
                "max number of points sampled",
                QgsProcessingParameterNumber.Integer,
                5000000,
                False,
                100000,
                20000000,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(LasViewPro.COLORING, "color by", LasViewPro.COLORINGS, False, 0))
        self.addParameter(
            QgsProcessingParameterEnum(LasViewPro.SIZE, "window size (x y) in pixels", LasViewPro.SIZES, False, 0)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context)]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        points = self.parameterAsInt(parameters, LasViewPro.POINTS, context)
        commands.append("-points " + str(points))
        coloring = self.parameterAsInt(parameters, LasViewPro.COLORING, context)
        if coloring != 0:
            commands.append("-color_by_" + LasViewPro.COLORINGS[coloring])
        size = self.parameterAsInt(parameters, LasViewPro.SIZE, context)
        if size != 0:
            commands.append("-win " + LasViewPro.SIZES[size])
        self.add_parameters_additional_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"": None}

    def createInstance(self):
        return LasViewPro()

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

# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasview.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : September 2013
    Copyright            : (C) 2013 by rapidlasso GmbH
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
__date__ = 'September 2013'
__copyright__ = '(C) 2013, rapidlasso GmbH'

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterNumber, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_visualization_colorization as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasView(LastoolsAlgorithm):
    TOOL_INFO = ('lasview', 'LasView')
    POINTS = "POINTS"
    SIZE = "SIZE"
    SIZES = ["1024 768", "800 600", "1200 900", "1200 400", "1550 900", "1550 1150"]
    COLORING = "COLORING"
    COLORINGS = ["default", "classification", "elevation1", "elevation2", "intensity", "return", "flightline", "rgb"]

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterNumber(
            LasView.POINTS, "max number of points sampled",
            QgsProcessingParameterNumber.Integer, 5000000, False, 100000, 20000000
        ))
        self.addParameter(QgsProcessingParameterEnum(LasView.COLORING, "color by", LasView.COLORINGS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(
            LasView.SIZE, "window size (x y) in pixels", LasView.SIZES, False, 0
        ))
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasview")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        points = self.parameterAsInt(parameters, LasView.POINTS, context)
        commands.append("-points " + str(points))
        coloring = self.parameterAsInt(parameters, LasView.COLORING, context)
        if coloring != 0:
            commands.append("-color_by_" + LasView.COLORINGS[coloring])
        size = self.parameterAsInt(parameters, LasView.SIZE, context)
        if size != 0:
            commands.append("-win " + LasView.SIZES[size])
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasView()

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


class LasViewPro(LastoolsAlgorithm):
    TOOL_INFO = ('lasview', 'LasViewPro')
    POINTS = "POINTS"
    SIZE = "SIZE"
    SIZES = ["1024 768", "800 600", "1200 900", "1200 400", "1550 900", "1550 1150"]
    COLORING = "COLORING"
    COLORINGS = ["default", "classification", "elevation1", "elevation2", "intensity", "return", "flightline", "rgb"]

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.addParameter(QgsProcessingParameterNumber(
            LasViewPro.POINTS, "max number of points sampled",
            QgsProcessingParameterNumber.Integer, 5000000, False, 100000, 20000000
        ))
        self.addParameter(QgsProcessingParameterEnum(LasViewPro.COLORING, "color by", LasViewPro.COLORINGS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(
            LasViewPro.SIZE, "window size (x y) in pixels", LasViewPro.SIZES, False, 0
        ))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasview")]
        self.add_parameters_verbose_commands(parameters, context, commands)
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

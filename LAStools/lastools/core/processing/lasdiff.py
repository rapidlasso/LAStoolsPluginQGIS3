# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasdiff.py
    ---------------------
    Date                 : May 2016 and August 2018
    Copyright            : (C) 2016 by rapidlasso GmbH
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
__date__ = 'May 2016'
__copyright__ = '(C) 2016, rapidlasso GmbH'

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_processing as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasDiff(LastoolsAlgorithm):
    TOOL_INFO = ('lasdiff', 'LasDiff')
    CREATE_DIFFERENCE_FILE = "CREATE_DIFFERENCE_FILE"
    SHUTUP = "SHUTUP"
    SHUTUP_AFTER = ["5", "10", "50", "100", "1000", "10000", "50000"]

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.add_parameters_generic_input_gui("other input LAS/LAZ file", "laz", False)
        self.addParameter(QgsProcessingParameterEnum(
            LasDiff.SHUTUP, "stop reporting difference after this many points", LasDiff.SHUTUP_AFTER, False, 0
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasDiff.CREATE_DIFFERENCE_FILE, "create elevation difference file (if points are in the same order)", False
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasdiff.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasdiff")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-i")
        shutup = self.parameterAsInt(parameters, LasDiff.SHUTUP, context)
        if shutup != 0:
            commands.append("-shutup")
            commands.append(LasDiff.SHUTUP_AFTER[shutup])
        if self.parameterAsBool(parameters, LasDiff.CREATE_DIFFERENCE_FILE, context):
            self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasDiff()

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

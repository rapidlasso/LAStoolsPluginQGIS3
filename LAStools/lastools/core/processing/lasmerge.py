# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasmerge.py
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
from qgis.core import QgsProcessingParameterFile

from ..utils import LastoolsUtils, descript_processing as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasMerge(LastoolsAlgorithm):
    TOOL_INFO = ('lasmerge', 'LasMerge')
    FILE2 = "FILE2"
    FILE3 = "FILE3"
    FILE4 = "FILE4"
    FILE5 = "FILE5"
    FILE6 = "FILE6"
    FILE7 = "FILE7"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_files_are_flightlines_gui()
        self.add_parameters_apply_file_source_id_gui()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterFile(
            LasMerge.FILE2, "2nd file", QgsProcessingParameterFile.File, "laz", None, True
        ))
        self.addParameter(QgsProcessingParameterFile(
            LasMerge.FILE3, "3rd file", QgsProcessingParameterFile.File, "laz", None, True
        ))
        self.addParameter(QgsProcessingParameterFile(
            LasMerge.FILE4, "4th file", QgsProcessingParameterFile.File, "laz", None, True
        ))
        self.addParameter(QgsProcessingParameterFile(
            LasMerge.FILE5, "5th file", QgsProcessingParameterFile.File, "laz", None, True
        ))
        self.addParameter(QgsProcessingParameterFile(
            LasMerge.FILE6, "6th file", QgsProcessingParameterFile.File, "laz", None, True
        ))
        self.addParameter(QgsProcessingParameterFile(
            LasMerge.FILE7, "7th file", QgsProcessingParameterFile.File, "laz", None, True
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasmerge.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasmerge")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        file2 = self.parameterAsString(parameters, LasMerge.FILE2, context)
        if file2 != '':
            commands.append("-i")
            commands.append(file2)
        file3 = self.parameterAsString(parameters, LasMerge.FILE3, context)
        if file3 != '':
            commands.append("-i")
            commands.append(file3)
        file4 = self.parameterAsString(parameters, LasMerge.FILE4, context)
        if file4 != '':
            commands.append("-i")
            commands.append(file4)
        file5 = self.parameterAsString(parameters, LasMerge.FILE5, context)
        if file5 != '':
            commands.append("-i")
            commands.append(file5)
        file6 = self.parameterAsString(parameters, LasMerge.FILE6, context)
        if file6 != '':
            commands.append("-i")
            commands.append(file6)
        file7 = self.parameterAsString(parameters, LasMerge.FILE7, context)
        if file7 != '':
            commands.append("-i")
            commands.append(file7)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        self.add_parameters_apply_file_source_id_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasMerge()

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


class LasMergePro(LastoolsAlgorithm):
    TOOL_INFO = ('lasmerge', 'LasMergePro')

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.add_parameters_apply_file_source_id_gui()
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasmerge.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasmerge")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        self.add_parameters_apply_file_source_id_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasMergePro()

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

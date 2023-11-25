# -*- coding: utf-8 -*-

"""
***************************************************************************
    laspublish.py
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
from qgis.core import QgsProcessingParameterEnum, QgsProcessingParameterBoolean, QgsProcessingParameterString

from ..utils import LastoolsUtils, descript_publishing as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasPublish(LastoolsAlgorithm):
    TOOL_INFO = ('laspublish', 'LasPublish')
    MODE = "MODE"
    MODES = ["3D only", "3D + download map", "download map only"]
    DIR = "DIR"
    SHOW_SKYBOX = "SHOW_SKYBOX"
    USE_EDL = "USE_EDL"
    MATERIAL = "MATERIAL"
    MATERIALS = ["elevation", "intensity", "return_number", "point_source", "rgb"]
    COPY_OR_MOVE = "COPY_OR_MOVE"
    COPY_OR_MOVE_OPTIONS = ["copy into portal dir", "move into portal dir", "neither"]
    PORTAL_DIRECTORY = "PORTAL_DIRECTORY"
    PORTAL_HTML_PAGE = "PORTAL_HTML_PAGE"
    OVERWRITE_EXISTING = "OVERWRITE_EXISTING"
    PORTAL_TITLE = "PORTAL_TITLE"
    PORTAL_DESCRIPTION = "PORTAL_DESCRIPTION"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterEnum(LasPublish.MODE, "type of portal", LasPublish.MODES, False, 1))
        self.addParameter(QgsProcessingParameterBoolean(LasPublish.USE_EDL, "use Eye Dome Lighting (EDL)", True))
        self.addParameter(QgsProcessingParameterBoolean(LasPublish.SHOW_SKYBOX, "show Skybox", True))
        self.addParameter(QgsProcessingParameterEnum(
            LasPublish.MATERIAL, "default material colors on start-up", LasPublish.MATERIALS, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasPublish.COPY_OR_MOVE, "copy or move source LiDAR files into portal (only for download portals)",
            LasPublish.COPY_OR_MOVE_OPTIONS, False, 2
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasPublish.OVERWRITE_EXISTING, "overwrite existing files", True
        ))
        self.addParameter(QgsProcessingParameterString(LasPublish.PORTAL_HTML_PAGE, "portal HTML page", "portal.html"))
        self.addParameter(QgsProcessingParameterString(LasPublish.PORTAL_TITLE, "portal title", "My LiDAR Portal"))
        self.addParameter(QgsProcessingParameterString(LasPublish.PORTAL_DESCRIPTION, "portal description", ""))
        self.add_parameters_output_directory_gui(optional_value=False)
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "laspublish")]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        mode = self.parameterAsInt(parameters, LasPublish.MODE, context)
        if mode == 0:
            commands.append("-only_3D")
        elif mode == 2:
            commands.append("-only_2D")
        material = self.parameterAsInt(parameters, LasPublish.MATERIAL, context)
        commands.append("-" + LasPublish.MATERIALS[material])
        if not self.parameterAsBool(parameters, LasPublish.USE_EDL, context):
            commands.append("-no_edl")
        if not self.parameterAsBool(parameters, LasPublish.SHOW_SKYBOX, context):
            commands.append("-no_skybox")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        copy_or_move = self.parameterAsInt(parameters, LasPublish.COPY_OR_MOVE, context)
        if copy_or_move == 0:
            commands.append("-copy_source_files")
        elif copy_or_move == 1:
            commands.append("-move_source_files")
            commands.append("-really_move")
        if self.parameterAsBool(parameters, LasPublish.OVERWRITE_EXISTING, context):
            commands.append("-overwrite")
        portal_html_page = self.parameterAsString(parameters, LasPublish.PORTAL_HTML_PAGE, context)
        if portal_html_page != "":
            commands.append("-o")
            commands.append('"' + portal_html_page + '"')
        title = self.parameterAsString(parameters, LasPublish.PORTAL_TITLE, context)
        if title != "":
            commands.append("-title")
            commands.append('"' + title + '"')
        description = self.parameterAsString(parameters, LasPublish.PORTAL_DESCRIPTION, context)
        if description != "":
            commands.append("-description")
            commands.append('"' + description + '"')
        commands.append("-olaz")
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasPublish()

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


class LasPublishPro(LastoolsAlgorithm):
    TOOL_INFO = ('laspublish', 'LasPublishPro')
    MODE = "MODE"
    MODES = ["3D only", "3D + download map", "download map only"]
    DIR = "DIR"
    SHOW_SKYBOX = "SHOW_SKYBOX"
    USE_EDL = "USE_EDL"
    MATERIAL = "MATERIAL"
    MATERIALS = ["elevation", "intensity", "return_number", "point_source", "rgb"]
    COPY_OR_MOVE = "COPY_OR_MOVE"
    COPY_OR_MOVE_OPTIONS = ["copy into portal dir", "move into portal dir", "neither"]
    PORTAL_DIRECTORY = "PORTAL_DIRECTORY"
    PORTAL_HTML_PAGE = "PORTAL_HTML_PAGE"
    OVERWRITE_EXISTING = "OVERWRITE_EXISTING"
    PORTAL_TITLE = "PORTAL_TITLE"
    PORTAL_DESCRIPTION = "PORTAL_DESCRIPTION"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui()
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterEnum(
            LasPublishPro.MODE, "type of portal", LasPublishPro.MODES, False, 1
        ))
        self.addParameter(QgsProcessingParameterBoolean(LasPublishPro.USE_EDL, "use Eye Dome Lighting (EDL)", True))
        self.addParameter(QgsProcessingParameterBoolean(LasPublishPro.SHOW_SKYBOX, "show Skybox", True))
        self.addParameter(QgsProcessingParameterEnum(
            LasPublishPro.MATERIAL, "default material colors on start-up", LasPublishPro.MATERIALS, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasPublishPro.COPY_OR_MOVE, "copy or move source LiDAR files into portal (only for download portals)",
            LasPublishPro.COPY_OR_MOVE_OPTIONS, False, 2
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasPublishPro.OVERWRITE_EXISTING, "overwrite existing files", True))
        self.addParameter(QgsProcessingParameterString(
            LasPublishPro.PORTAL_HTML_PAGE, "portal HTML page", "portal.html"
        ))
        self.addParameter(
            QgsProcessingParameterString(LasPublishPro.PORTAL_TITLE, "portal title", "My LiDAR Portal"))
        self.addParameter(QgsProcessingParameterString(LasPublishPro.PORTAL_DESCRIPTION, "portal description", ""))
        self.add_parameters_output_directory_gui(optional_value=False)
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "laspublish")]
        self.add_parameters_verbose_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        mode = self.parameterAsInt(parameters, LasPublishPro.MODE, context)
        if mode == 0:
            commands.append("-only_3D")
        elif mode == 2:
            commands.append("-only_2D")
        material = self.parameterAsInt(parameters, LasPublishPro.MATERIAL, context)
        commands.append("-" + LasPublishPro.MATERIALS[material])
        if not self.parameterAsBool(parameters, LasPublishPro.USE_EDL, context):
            commands.append("-no_edl")
        if not self.parameterAsBool(parameters, LasPublishPro.SHOW_SKYBOX, context):
            commands.append("-no_skybox")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        copy_or_move = self.parameterAsInt(parameters, LasPublishPro.COPY_OR_MOVE, context)
        if copy_or_move == 0:
            commands.append("-copy_source_files")
        elif copy_or_move == 1:
            commands.append("-move_source_files")
            commands.append("-really_move")
        if self.parameterAsBool(parameters, LasPublishPro.OVERWRITE_EXISTING, context):
            commands.append("-overwrite")
        portal_html_page = self.parameterAsString(parameters, LasPublishPro.PORTAL_HTML_PAGE, context)
        if portal_html_page != "":
            commands.append("-o")
            commands.append('"' + portal_html_page + '"')
        title = self.parameterAsString(parameters, LasPublishPro.PORTAL_TITLE, context)
        if title != "":
            commands.append("-title")
            commands.append('"' + title + '"')
        description = self.parameterAsString(parameters, LasPublishPro.PORTAL_DESCRIPTION, context)
        if description != "":
            commands.append("-description")
            commands.append('"' + description + '"')
        commands.append("-olaz")
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasPublishPro()

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

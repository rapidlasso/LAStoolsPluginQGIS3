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


from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum, QgsProcessingParameterString
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasPublish(LastoolsAlgorithm):
    TOOL_NAME = "LasPublish"
    LASTOOL = "laspublish"
    LICENSE = "c"
    LASGROUP = 7
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
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterEnum(self.MODE, "type of portal", self.MODES, False, 1))
        self.addParameter(QgsProcessingParameterBoolean(self.USE_EDL, "use Eye Dome Lighting (EDL)", True))
        self.addParameter(QgsProcessingParameterBoolean(self.SHOW_SKYBOX, "show Skybox", True))
        self.addParameter(
            QgsProcessingParameterEnum(self.MATERIAL, "default material colors on start-up", self.MATERIALS, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.COPY_OR_MOVE,
                "copy or move source LiDAR files into portal (only for download portals)",
                self.COPY_OR_MOVE_OPTIONS,
                False,
                2,
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(self.OVERWRITE_EXISTING, "overwrite existing files", True))
        self.addParameter(QgsProcessingParameterString(self.PORTAL_HTML_PAGE, "portal HTML page", "portal.html"))
        self.addParameter(QgsProcessingParameterString(self.PORTAL_TITLE, "portal title", "My LiDAR Portal"))
        self.addParameter(QgsProcessingParameterString(self.PORTAL_DESCRIPTION, "portal description", ""))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_output_directory_gui(optional_value=False)

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        mode = self.parameterAsInt(parameters, self.MODE, context)
        if mode == 0:
            commands.append("-only_3D")
        elif mode == 2:
            commands.append("-only_2D")
        material = self.parameterAsInt(parameters, self.MATERIAL, context)
        commands.append("-" + self.MATERIALS[material])
        if not self.parameterAsBool(parameters, self.USE_EDL, context):
            commands.append("-no_edl")
        if not self.parameterAsBool(parameters, self.SHOW_SKYBOX, context):
            commands.append("-no_skybox")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        copy_or_move = self.parameterAsInt(parameters, self.COPY_OR_MOVE, context)
        if copy_or_move == 0:
            commands.append("-copy_source_files")
        elif copy_or_move == 1:
            commands.append("-move_source_files")
            commands.append("-really_move")
        if self.parameterAsBool(parameters, self.OVERWRITE_EXISTING, context):
            commands.append("-overwrite")
        portal_html_page = self.parameterAsString(parameters, self.PORTAL_HTML_PAGE, context)
        if portal_html_page != "":
            commands.append("-o")
            commands.append('"' + portal_html_page + '"')
        title = self.parameterAsString(parameters, self.PORTAL_TITLE, context)
        if title != "":
            commands.append("-title")
            commands.append('"' + title + '"')
        description = self.parameterAsString(parameters, self.PORTAL_DESCRIPTION, context)
        if description != "":
            commands.append("-description")
            commands.append('"' + description + '"')
        commands.append("-olaz")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasPublish()

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


class LasPublishPro(LastoolsAlgorithm):
    TOOL_NAME = "LasPublishPro"
    LASTOOL = "laspublish"
    LICENSE = "c"
    LASGROUP = 7
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
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterEnum(LasPublishPro.MODE, "type of portal", LasPublishPro.MODES, False, 1)
        )
        self.addParameter(QgsProcessingParameterBoolean(LasPublishPro.USE_EDL, "use Eye Dome Lighting (EDL)", True))
        self.addParameter(QgsProcessingParameterBoolean(LasPublishPro.SHOW_SKYBOX, "show Skybox", True))
        self.addParameter(
            QgsProcessingParameterEnum(
                LasPublishPro.MATERIAL, "default material colors on start-up", LasPublishPro.MATERIALS, False, 0
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                LasPublishPro.COPY_OR_MOVE,
                "copy or move source LiDAR files into portal (only for download portals)",
                LasPublishPro.COPY_OR_MOVE_OPTIONS,
                False,
                2,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(LasPublishPro.OVERWRITE_EXISTING, "overwrite existing files", True)
        )
        self.addParameter(
            QgsProcessingParameterString(LasPublishPro.PORTAL_HTML_PAGE, "portal HTML page", "portal.html")
        )
        self.addParameter(QgsProcessingParameterString(LasPublishPro.PORTAL_TITLE, "portal title", "My LiDAR Portal"))
        self.addParameter(QgsProcessingParameterString(LasPublishPro.PORTAL_DESCRIPTION, "portal description", ""))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_output_directory_gui(optional_value=False)

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
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
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasPublishPro()

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

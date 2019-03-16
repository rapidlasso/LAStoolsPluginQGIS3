# -*- coding: utf-8 -*-

"""
***************************************************************************
    laspublishPro.py
    ---------------------
    Date                 : May 2016 and August 2018
    Copyright            : (C) 2016 by Martin Isenburg
    Email                : martin near rapidlasso point com
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
__copyright__ = '(C) 2016, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterString

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class laspublishPro(LAStoolsAlgorithm):

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

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI()
        self.addParametersPointInputFolderGUI()
        self.addParameter(QgsProcessingParameterEnum(laspublishPro.MODE, "type of portal", laspublishPro.MODES, False, 1))
        self.addParameter(QgsProcessingParameterBoolean(laspublishPro.USE_EDL, "use Eye Dome Lighting (EDL)", True))
        self.addParameter(QgsProcessingParameterBoolean(laspublishPro.SHOW_SKYBOX, "show Skybox", True))
        self.addParameter(QgsProcessingParameterEnum(laspublishPro.MATERIAL, "default material colors on start-up", laspublishPro.MATERIALS, False, 0))
        self.addParametersOutputDirectoryGUI()
        self.addParameter(QgsProcessingParameterEnum(laspublishPro.COPY_OR_MOVE, "copy or move source LiDAR files into portal (only for download portals)", laspublishPro.COPY_OR_MOVE_OPTIONS, False, 2))
        self.addParameter(QgsProcessingParameterBoolean(laspublishPro.OVERWRITE_EXISTING, "overwrite existing files", True))
        self.addParameter(QgsProcessingParameterString(laspublishPro.PORTAL_HTML_PAGE, "portal HTML page", "portal.html"))
        self.addParameter(QgsProcessingParameterString(laspublishPro.PORTAL_TITLE, "portal title", "My LiDAR Portal"))
        self.addParameter(QgsProcessingParameterString(laspublishPro.PORTAL_DESCRIPTION, "portal description", ""))
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "laspublish")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        mode = self.parameterAsInt(parameters, laspublishPro.MODE, context)
        if (mode == 0):
            commands.append("-only_3D")
        elif (mode == 2):
            commands.append("-only_2D")
        material = self.parameterAsInt(parameters, laspublishPro.MATERIAL, context)
        commands.append("-" + laspublishPro.MATERIALS[material])
        if (not self.parameterAsBool(parameters, laspublishPro.USE_EDL, context)):
            commands.append("-no_edl")
        if (not self.parameterAsBool(parameters, laspublishPro.SHOW_SKYBOX, context)):
            commands.append("-no_skybox")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        copy_or_move = self.parameterAsInt(parameters, laspublishPro.COPY_OR_MOVE, context)
        if (copy_or_move == 0):
            commands.append("-copy_source_files")
        elif (copy_or_move == 1):
            commands.append("-move_source_files")
            commands.append("-really_move")
        if (self.parameterAsBool(parameters, laspublishPro.OVERWRITE_EXISTING, context)):
            commands.append("-overwrite")
        portal_html_page = self.parameterAsString(parameters, laspublishPro.PORTAL_HTML_PAGE, context)
        if (portal_html_page != ""):
            commands.append("-o")
            commands.append('"' + portal_html_page + '"')
        title = self.parameterAsString(parameters, laspublishPro.PORTAL_TITLE, context)
        if (title != ""):
            commands.append("-title")
            commands.append('"' + title + '"')
        description = self.parameterAsString(parameters, laspublishPro.PORTAL_DESCRIPTION, context)
        if (description != ""):
            commands.append("-description")
            commands.append('"' + description + '"')
        commands.append("-olaz")
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laspublishPro'

    def displayName(self):
        return 'laspublishPro'

    def group(self):
        return 'folder - conversion'

    def groupId(self):
        return 'folder - conversion'

    def createInstance(self):
        return laspublishPro()

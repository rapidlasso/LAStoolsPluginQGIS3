# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasclip.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : September 2013 and August 2018
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_processing as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasClip(LastoolsAlgorithm):
    TOOL_INFO = ('lasclip', 'LasClip')
    INTERIOR = "INTERIOR"
    OPERATION = "OPERATION"
    OPERATIONS = ["clip", "classify"]
    CLASSIFY_AS = "CLASSIFY_AS"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_gui()
        self.add_parameters_generic_input_gui("Input polygon(s)", "shp", False)
        self.addParameter(QgsProcessingParameterBoolean(LasClip.INTERIOR, "interior", False))
        self.addParameter(QgsProcessingParameterEnum(
            LasClip.OPERATION, "what to do with points", LasClip.OPERATIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasClip.CLASSIFY_AS, "classify as", QgsProcessingParameterNumber.Integer, 12, False, 0, 255
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasclip")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-poly")
        if self.parameterAsBool(parameters, LasClip.INTERIOR, context):
            commands.append("-interior")
        operation = self.parameterAsInt(parameters, LasClip.OPERATION, context)
        if operation != 0:
            commands.append("-classify")
            classify_as = self.parameterAsInt(parameters, LasClip.CLASSIFY_AS, context)
            commands.append(str(classify_as))
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasClip()

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

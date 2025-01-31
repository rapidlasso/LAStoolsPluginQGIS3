"""
***************************************************************************
    self.py
    ---------------------
    Date                 : January 2025
    Copyright            : (C) 2025 by rapidlasso GmbH
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
__copyright__ = "(C) 2025, rapidlasso GmbH"

import os

from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasCopy(LastoolsAlgorithm):
    TOOL_NAME = "LasCopy"
    LASTOOL = "lascopy"
    LICENSE = "c"
    LASGROUP = 2
    MATCH_GPS_TIME = "MATCH_GPS_TIME"
    MATCH_RETURN_NUMBER = "MATCH_RETURN_NUMBER"
    MATCH_CLASSIFICATION = "MATCH_CLASSIFICATION"
    MATCH_INTENSITY = "MATCH_INTENSITY"
    MATCH_POINT_SOURCE_ID = "MATCH_POINT_SOURCE_ID"
    MATCH_USER_DATA = "MATCH_USER_DATA"
    MATCH_XY = "MATCH_XY"
    ARGXYDIST = "XY_DIST"
    ARGXYZDIST = "XYZ_DIST"
    MATCH_XYZ = "MATCH_XYZ"
    COPY_CLASSIFICATION = "COPY_CLASSIFICATION"
    COPY_ELEVATION = "COPY_ELEVATION"
    COPY_INTENSITY = "COPY_INTENSITY"
    COPY_RGB = "COPY_RGB"
    COPY_USER_DATA = "COPY_USER_DATA"
    COPY_RETURN_NUMBER = "COPY_RETURN_NUMBER"
    ZERO = "ZERO"
    UNMATCHED = "UNMATCHED"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(self.MATCH_GPS_TIME, "match by gps time (default)", True))
        self.addParameter(
            QgsProcessingParameterBoolean(self.MATCH_RETURN_NUMBER, "match by number of return (default)", True)
        )
        self.addParameter(QgsProcessingParameterBoolean(self.MATCH_CLASSIFICATION, "match by classification", False))
        self.addParameter(QgsProcessingParameterBoolean(self.MATCH_INTENSITY, "match by intensity", False))
        self.addParameter(QgsProcessingParameterBoolean(self.MATCH_POINT_SOURCE_ID, "match by point source", False))
        self.addParameter(QgsProcessingParameterBoolean(self.MATCH_USER_DATA, "match by user data field", False))
        self.addParameter(QgsProcessingParameterBoolean(self.MATCH_XY, "match by xy point distance", False))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ARGXYDIST,
                "maximum XY distance",
                QgsProcessingParameterNumber.Double,
                1,
                False,
                0,
                100,
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(self.MATCH_XYZ, "match by xyz point distance", False))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ARGXYZDIST,
                "maximum XYZ distance",
                QgsProcessingParameterNumber.Double,
                1,
                False,
                0,
                100,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.COPY_CLASSIFICATION, "copy classification (default)", False)
        )
        self.addParameter(QgsProcessingParameterBoolean(self.COPY_ELEVATION, "copy elevation", False))
        self.addParameter(QgsProcessingParameterBoolean(self.COPY_INTENSITY, "copy intensity", False))
        self.addParameter(QgsProcessingParameterBoolean(self.COPY_RGB, "copy color (RGB)", False))
        self.addParameter(QgsProcessingParameterBoolean(self.COPY_USER_DATA, "copy user data", False))
        self.addParameter(QgsProcessingParameterBoolean(self.COPY_RETURN_NUMBER, "copy return number", False))
        self.addParameter(QgsProcessingParameterBoolean(self.ZERO, "zero target if not found in source", False))
        self.addParameter(QgsProcessingParameterBoolean(self.UNMATCHED, "copy attributes by point order", False))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_point_input_commands(parameters, context, commands)

        if self.parameterAsBool(parameters, self.MATCH_GPS_TIME, context):
            commands.append("-match_gps_time")
        if self.parameterAsBool(parameters, self.MATCH_RETURN_NUMBER, context):
            commands.append("-match_return_number")
        if self.parameterAsBool(parameters, self.MATCH_CLASSIFICATION, context):
            commands.append("-match_classification")
        if self.parameterAsBool(parameters, self.MATCH_INTENSITY, context):
            commands.append("-match_intensity")
        if self.parameterAsBool(parameters, self.MATCH_POINT_SOURCE_ID, context):
            commands.append("-match_point_source_id")
        if self.parameterAsBool(parameters, self.MATCH_USER_DATA, context):
            commands.append("-match_user_data")
        if self.parameterAsBool(parameters, self.MATCH_XY, context):
            commands.append(f"-match_xy {parameters['ARGXYDIST']}")
        if self.parameterAsBool(parameters, self.MATCH_XYZ, context):
            commands.append(f"-match_xyz {parameters['ARGXYZDIST']}")
        if self.parameterAsBool(parameters, self.COPY_CLASSIFICATION, context):
            commands.append("-copy_classification")
        if self.parameterAsBool(parameters, self.COPY_ELEVATION, context):
            commands.append("-copy_elevation")
        if self.parameterAsBool(parameters, self.COPY_INTENSITY, context):
            commands.append("-copy_intensity")
        if self.parameterAsBool(parameters, self.COPY_RGB, context):
            commands.append("-copy_rgb")
        if self.parameterAsBool(parameters, self.COPY_USER_DATA, context):
            commands.append("-copy_user_data")
        if self.parameterAsBool(parameters, self.COPY_RETURN_NUMBER, context):
            commands.append("-copy_return_number")
        if self.parameterAsBool(parameters, self.ZERO, context):
            commands.append("-zero")
        if self.parameterAsBool(parameters, self.UNMATCHED, context):
            commands.append("-unmatched")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasCopy()

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

# -*- coding: utf-8 -*-
"""
***************************************************************************
    lasdistance.py
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


from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsProcessingParameterNumber,
)
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url

class LasDistance(LastoolsAlgorithm):
    TOOL_NAME = "LasDistance"
    LASTOOL = "lasdistance"
    LICENSE = "c"
    LASGROUP = 3
    DISTANCE_XY = "DISTANCE_XY"
    WEIGHT_FIELD = "WEIGHT_FIELD"
    CLASSIFY_AS = {
        "name": "CLASSIFY_AS",
        "options": [
            "default",
            "never classified (0)",
            "unclassified (1)",
            "ground (2)",
            "veg low (3)",
            "veg mid (4)",
            "veg high (5)",
            "buildings (6)",
            "noise (7)",
            "keypoint (8)",
            "water (9)",
            "rail (10)",
            "road surface (11)",
            "overlap (12)",
        ],
    }
    CSV_SEPARATOR = {
        "name": "CSV_SEPARATOR",
        "options": ["default", "comma", "tab", "dot", "colon", "semicolon", "hyphen", "space"],
    }
    REMOVE_POINT = "REMOVE_POINT"
    FLAG_AS_WITHHELD = "FLAG_AS_WITHHELD"
    FLAG_AS_KEYPOINT = "FLAG_AS_KEYPOINT"
    FLAG_AS_SYNTHETIC = "FLAG_AS_SYNTHETIC"
    ADDITIONAL_PARAM = "ADDITIONAL_PARAM"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.add_parameters_generic_input_gui("input polyline(s)/polygons", "shp", False)
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DISTANCE_XY,
                "Distance XY (m)",
                QgsProcessingParameterNumber.Integer,
                10,
                False,
                0,
                10000,
            )
        )
        # classify_as
        classify_as_param = QgsProcessingParameterEnum(
            self.CLASSIFY_AS["name"],
            "Classify as",
            self.CLASSIFY_AS["options"],
            False,
            0,
        )
        classify_as_param.setFlags(classify_as_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(classify_as_param)
        # remove point
        remove_point_param = QgsProcessingParameterBoolean(self.REMOVE_POINT, "Remove Point", False)
        remove_point_param.setFlags(remove_point_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(remove_point_param)
        # flag as withheld
        flag_as_withheld_param = QgsProcessingParameterBoolean(self.FLAG_AS_WITHHELD, "Flag as Withheld", False)
        flag_as_withheld_param.setFlags(flag_as_withheld_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(flag_as_withheld_param)
        # flag as keypoint
        flag_as_keypoint_param = QgsProcessingParameterBoolean(self.FLAG_AS_KEYPOINT, "Flag as Keypoint", False)
        flag_as_keypoint_param.setFlags(flag_as_keypoint_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(flag_as_keypoint_param)
        # flag as synthetic
        flag_as_synthetic_param = QgsProcessingParameterBoolean(self.FLAG_AS_SYNTHETIC, "Flag as Synthetic", False)
        flag_as_synthetic_param.setFlags(
            flag_as_synthetic_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced
        )
        self.addParameter(flag_as_synthetic_param)
        # csv options
        csv_sep_param = QgsProcessingParameterEnum(
            self.CSV_SEPARATOR["name"],
            "CSV Separator Options",
            self.CSV_SEPARATOR["options"],
            False,
            0,
        )
        # sep
        csv_sep_param.setFlags(csv_sep_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(csv_sep_param)
        #
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        # append poly
        self.add_parameters_generic_input_commands(parameters, context, commands, "-poly")
        # append -distance
        commands.append(f"-distance_xy {parameters['DISTANCE_XY']}")
        # append -classify_as
        if parameters["CLASSIFY_AS"] != 0:
            commands.append(f"-classify_as {parameters['CLASSIFY_AS'] - 1}")
        # advance tool
        if parameters["REMOVE_POINT"]:
            commands.append("-remove_points")
        if parameters["FLAG_AS_WITHHELD"]:
            commands.append("-flag_as_withheld")
        if parameters["FLAG_AS_KEYPOINT"]:
            commands.append("-flag_as_keypoint")
        if parameters["FLAG_AS_SYNTHETIC"]:
            commands.append("-flag_as_synthetic")
        # append -sep
        if parameters["CSV_SEPARATOR"] != 0:
            commands.append(f"-sep {self.CSV_SEPARATOR['options'][parameters['CSV_SEPARATOR']]}")
        #
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"command": commands}

    def createInstance(self):
        return LasDistance()

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

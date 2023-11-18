# -*- coding: utf-8 -*-

"""
***************************************************************************
    las3dpoly.py
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

from qgis._core import QgsProcessingParameterDefinition, QgsProcessingParameterBoolean, QgsProcessingParameterString, \
    QgsProcessingParameterFile, QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_processing as descript_info, paths
from ..algo import LastoolsAlgorithm
from PyQt5.QtGui import QIcon


class Las3dPolyRadialDistance(LastoolsAlgorithm):
    TOOL_INFO = ('las3dpoly', 'Las3dPolyRadialDistance')
    DISTANCE_RADIAL = "DISTANCE_RADIAL"
    WEIGHT_FIELD = 'WEIGHT_FIELD'
    CLASSIFY_AS = {
        "name": 'CLASSIFY_AS',
        "options": ["default", "never classified (0)", "unclassified (1)", "ground (2)", "veg low (3)", "veg mid (4)",
                    "veg high (5)", "buildings (6)", "noise (7)", "keypoint (8)", "water (9)", "rail (10)",
                    "road surface (11)", "overlap (12)"]
    }
    CSV_SEPARATOR = {
        "name": 'CSV_SEPARATOR',
        "options": ["default", "comma", "tab", "dot", "colon", "semicolon", "hyphen", "space"]
    }
    REMOVE_POINT = 'REMOVE_POINT'
    FLAG_AS_WITHHELD = 'FLAG_AS_WITHHELD'
    FLAG_AS_KEYPOINT = 'FLAG_AS_KEYPOINT'
    FLAG_AS_SYNTHETIC = 'FLAG_AS_SYNTHETIC'
    ADDITIONAL_PARAM = 'ADDITIONAL_PARAM'
    INPUT_POLYLINE_PATH = 'INPUT_POLYLINE_PATH'
    OUTPUT_LAS_PATH = 'OUTPUT_LAS_PATH'

    def initAlgorithm(self, config=None):
        # input verbose ans gui
        self.add_parameters_verbose_gui()
        # input las file
        self.add_parameters_point_input_gui()
        # input shp
        self.addParameter(QgsProcessingParameterFile(
            Las3dPolyRadialDistance.INPUT_POLYLINE_PATH, "Input polyline(s)/polygons SHP/CSV file",
            QgsProcessingParameterFile.File, "", None, False, None)
        )
        # radial distance
        self.addParameter(QgsProcessingParameterNumber(
            Las3dPolyRadialDistance.DISTANCE_RADIAL, "Radial Distance (m)",
            QgsProcessingParameterNumber.Integer, 10, False, 0, 10000)
        )
        # advance tools
        # classify_as
        classify_as_param = QgsProcessingParameterEnum(
            Las3dPolyRadialDistance.CLASSIFY_AS['name'], "Classify as",
            Las3dPolyRadialDistance.CLASSIFY_AS['options'], False, 0
        )
        classify_as_param.setFlags(classify_as_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(classify_as_param)
        # remove point
        remove_point_param = QgsProcessingParameterBoolean(Las3dPolyRadialDistance.REMOVE_POINT, "Remove Point", False)
        remove_point_param.setFlags(remove_point_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(remove_point_param)
        # flag as withheld
        flag_as_withheld_param = QgsProcessingParameterBoolean(
            Las3dPolyRadialDistance.FLAG_AS_WITHHELD, "Flag as Withheld", False
        )
        flag_as_withheld_param.setFlags(flag_as_withheld_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(flag_as_withheld_param)
        # flag as keypoint
        flag_as_keypoint_param = QgsProcessingParameterBoolean(
            Las3dPolyRadialDistance.FLAG_AS_KEYPOINT, "Flag as Keypoint", False
        )
        flag_as_keypoint_param.setFlags(flag_as_keypoint_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(flag_as_keypoint_param)
        # flag as synthetic
        flag_as_synthetic_param = QgsProcessingParameterBoolean(
            Las3dPolyRadialDistance.FLAG_AS_SYNTHETIC, "Flag as Synthetic", False
        )
        flag_as_synthetic_param.setFlags(
            flag_as_synthetic_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(flag_as_synthetic_param)
        # csv options
        csv_sep_param = QgsProcessingParameterEnum(
            Las3dPolyRadialDistance.CSV_SEPARATOR["name"], "CSV Separator Options",
            Las3dPolyRadialDistance.CSV_SEPARATOR["options"], False, 0
        )
        csv_sep_param.setFlags(csv_sep_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(csv_sep_param)
        # output las path
        self.addParameter(QgsProcessingParameterFileDestination(
            Las3dPolyRadialDistance.OUTPUT_LAS_PATH, "Output LAS/LAZ file", "*.laz *.las", "", False, False)
        )
        # additional parameters
        self.addParameter(QgsProcessingParameterString(
            Las3dPolyRadialDistance.ADDITIONAL_PARAM, "additional command line parameter(s)", ' ', False, False
        ))
        self.helpUrl()
        self.icon()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las3dpoly64")]
        # append -v and -gui
        self.add_parameters_verbose_commands(parameters, context, commands)
        # append -i
        commands.append(f"-i {parameters['INPUT_LASLAZ']}")
        # append poly
        commands.append(f"-poly {parameters['INPUT_POLYLINE_PATH']}")
        # append -distance
        commands.append(f"-distance {parameters['DISTANCE_RADIAL']}")
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
            commands.append(f"-sep {Las3dPolyRadialDistance.CSV_SEPARATOR['options'][parameters['CSV_SEPARATOR']]}")
        # append -o
        if parameters["OUTPUT_LAS_PATH"] != 'TEMPORARY_OUTPUT':
            commands.append(f"-o {parameters['OUTPUT_LAS_PATH']}")
        # append extra params
        commands.append(parameters['ADDITIONAL_PARAM'])
        LastoolsUtils.run_lastools(commands, feedback)
        return {"command": commands}

    def createInstance(self):
        return Las3dPolyRadialDistance()

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


class Las3dPolyHorizontalVerticalDistance(LastoolsAlgorithm):
    TOOL_INFO = ('las3dpoly', 'Las3dPolyHorizontalVerticalDistance')
    DISTANCE_HORIZONTAL = "DISTANCE_HORIZONTAL"
    DISTANCE_VERTICAL = "DISTANCE_VERTICAL"
    CLASSIFY_AS = {
        "name": 'CLASSIFY_AS',
        "options": ["default", "never classified (0)", "unclassified (1)", "ground (2)", "veg low (3)", "veg mid (4)",
                    "veg high (5)", "buildings (6)", "noise (7)", "keypoint (8)", "water (9)", "rail (10)",
                    "road surface (11)", "overlap (12)"]
    }
    CSV_SEPARATOR = {
        "name": 'CSV_SEPARATOR',
        "options": ["default", "comma", "tab", "dot", "colon", "semicolon", "hyphen", "space"]
    }
    REMOVE_POINT = 'REMOVE_POINT'
    FLAG_AS_WITHHELD = 'FLAG_AS_WITHHELD'
    FLAG_AS_KEYPOINT = 'FLAG_AS_KEYPOINT'
    FLAG_AS_SYNTHETIC = 'FLAG_AS_SYNTHETIC'
    ADDITIONAL_PARAM = 'ADDITIONAL_PARAM'
    INPUT_POLYLINE_PATH = 'INPUT_POLYLINE_PATH'
    OUTPUT_LAS_PATH = 'OUTPUT_LAS_PATH'

    def initAlgorithm(self, config=None):
        # input verbose ans gui
        self.add_parameters_verbose_gui()
        # input las file
        self.add_parameters_point_input_gui()
        # input shp
        self.addParameter(QgsProcessingParameterFile(
            Las3dPolyHorizontalVerticalDistance.INPUT_POLYLINE_PATH, "Input polyline(s)/polygons SHP/CSV file",
            QgsProcessingParameterFile.File, "", None, False, None)
        )
        # horizontal and vertical distance
        self.addParameter(QgsProcessingParameterNumber(
            Las3dPolyHorizontalVerticalDistance.DISTANCE_VERTICAL, "Vertical Distance (m)",
            QgsProcessingParameterNumber.Integer, 10, False, 0, 10000)
        )
        self.addParameter(QgsProcessingParameterNumber(
            Las3dPolyHorizontalVerticalDistance.DISTANCE_HORIZONTAL, "Horizontal Distance (m)",
            QgsProcessingParameterNumber.Integer, 10, False, 0, 10000)
        )
        # advance tools
        # classify_as
        classify_as_param = QgsProcessingParameterEnum(
            Las3dPolyHorizontalVerticalDistance.CLASSIFY_AS['name'], "Classify as",
            Las3dPolyHorizontalVerticalDistance.CLASSIFY_AS['options'], False, 0
        )
        classify_as_param.setFlags(classify_as_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(classify_as_param)
        # remove point
        remove_point_param = QgsProcessingParameterBoolean(Las3dPolyHorizontalVerticalDistance.REMOVE_POINT,
                                                           "Remove Point", False)
        remove_point_param.setFlags(remove_point_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(remove_point_param)
        # flag as withheld
        flag_as_withheld_param = QgsProcessingParameterBoolean(
            Las3dPolyHorizontalVerticalDistance.FLAG_AS_WITHHELD, "Flag as Withheld", False
        )
        flag_as_withheld_param.setFlags(flag_as_withheld_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(flag_as_withheld_param)
        # flag as keypoint
        flag_as_keypoint_param = QgsProcessingParameterBoolean(
            Las3dPolyHorizontalVerticalDistance.FLAG_AS_KEYPOINT, "Flag as Keypoint", False
        )
        flag_as_keypoint_param.setFlags(flag_as_keypoint_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(flag_as_keypoint_param)
        # flag as synthetic
        flag_as_synthetic_param = QgsProcessingParameterBoolean(
            Las3dPolyHorizontalVerticalDistance.FLAG_AS_SYNTHETIC, "Flag as Synthetic", False
        )
        flag_as_synthetic_param.setFlags(
            flag_as_synthetic_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(flag_as_synthetic_param)
        # csv options
        csv_sep_param = QgsProcessingParameterEnum(
            Las3dPolyHorizontalVerticalDistance.CSV_SEPARATOR["name"], "CSV Separator Options",
            Las3dPolyHorizontalVerticalDistance.CSV_SEPARATOR["options"], False, 0
        )
        csv_sep_param.setFlags(csv_sep_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(csv_sep_param)
        # output las path
        self.addParameter(QgsProcessingParameterFileDestination(
            Las3dPolyHorizontalVerticalDistance.OUTPUT_LAS_PATH, "Output LAS/LAZ file", "*.laz *.las", "", False, False)
        )
        # additional parameters
        self.addParameter(QgsProcessingParameterString(
            Las3dPolyHorizontalVerticalDistance.ADDITIONAL_PARAM, "additional command line parameter(s)", ' ', False,
            False
        ))
        self.helpUrl()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las3dpoly64")]
        # append -v and -gui
        self.add_parameters_verbose_commands(parameters, context, commands)
        # append -i
        self.add_parameters_point_input_commands(parameters, context, commands)
        # append -i
        commands.append(f"-i {parameters['INPUT_LASLAZ']}")
        # append poly
        commands.append(f"-poly {parameters['INPUT_POLYLINE_PATH']}")
        # append -distance
        commands.append(f"-distance {parameters['DISTANCE_VERTICAL']} {parameters['DISTANCE_HORIZONTAL']}")
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
            commands.append(
                f"-sep {Las3dPolyHorizontalVerticalDistance.CSV_SEPARATOR['options'][parameters['CSV_SEPARATOR']]}"
            )
        # append -o
        if parameters["OUTPUT_LAS_PATH"] != 'TEMPORARY_OUTPUT':
            commands.append(f"-o {parameters['OUTPUT_LAS_PATH']}")
        # append extra params
        commands.append(parameters['ADDITIONAL_PARAM'])
        LastoolsUtils.run_lastools(commands, feedback)
        return {"command": commands}

    def createInstance(self):
        return Las3dPolyHorizontalVerticalDistance()

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

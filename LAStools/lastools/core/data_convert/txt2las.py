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

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterNumber, QgsProcessingParameterString, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class Txt2Las(LastoolsAlgorithm):
    TOOL_NAME = "Txt2Las"
    LASTOOL = "txt2las"
    LICENSE = "o"
    LASGROUP = 2
    PARSE = "PARSE"
    SKIP = "SKIP"
    SCALE_FACTOR_XY = "SCALE_FACTOR_XY"
    SCALE_FACTOR_Z = "SCALE_FACTOR_Z"
    PROJECTION = "PROJECTION"
    EPSG_CODE = "EPSG_CODE"
    UTM = "UTM"
    SP = "SP"

    def initAlgorithm(self, config=None):
        self.add_parameters_generic_input_gui("Input ASCII file", "txt", False)
        self.addParameter(QgsProcessingParameterString(self.PARSE, "parse lines as", "xyz"))
        self.addParameter(
            QgsProcessingParameterNumber(self.SKIP, "skip the first n lines", QgsProcessingParameterNumber.Integer, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SCALE_FACTOR_XY,
                "resolution of x and y coordinate",
                QgsProcessingParameterNumber.Double,
                0.01,
                False,
                0.00000001,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SCALE_FACTOR_Z,
                "resolution of z coordinate",
                QgsProcessingParameterNumber.Double,
                0.01,
                False,
                0.00000001,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.PROJECTION, "projection", self.PROJECTIONS, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(self.EPSG_CODE, "EPSG code", QgsProcessingParameterNumber.Integer, 25832)
        )
        self.addParameter(QgsProcessingParameterEnum(self.UTM, "utm zone", self.UTM_ZONES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.SP, "state plane code", self.STATE_PLANES, False, 0))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_generic_input_commands(parameters, context, commands, "-i")
        parse_string = self.parameterAsString(parameters, self.PARSE, context)
        if parse_string != "xyz":
            commands.append("-parse")
            commands.append(parse_string)
        skip = self.parameterAsInt(parameters, self.SKIP, context)
        if skip != 0:
            commands.append("-skip")
            commands.append(str(skip))
        scale_factor_xy = self.parameterAsDouble(parameters, self.SCALE_FACTOR_XY, context)
        scale_factor_z = self.parameterAsDouble(parameters, self.SCALE_FACTOR_Z, context)
        if scale_factor_xy != 0.01 or scale_factor_z != 0.01:
            commands.append("-set_scale")
            commands.append(str(scale_factor_xy))
            commands.append(str(scale_factor_xy))
            commands.append(str(scale_factor_z))
        projection = self.parameterAsInt(parameters, self.PROJECTION, context)
        if projection != 0:
            if projection == 1:
                epsg_code = self.parameterAsInt(parameters, self.EPSG_CODE, context)
                if epsg_code != 0:
                    commands.append("-" + self.PROJECTIONS[projection])
                    commands.append(str(epsg_code))
            elif projection == 2:
                utm_zone = self.parameterAsInt(parameters, self.UTM, context)
                if utm_zone != 0:
                    commands.append("-" + self.PROJECTIONS[projection])
                    if utm_zone > 60:
                        commands.append(str(utm_zone - 60) + "south")
                    else:
                        commands.append(str(utm_zone) + "north")
            elif projection < 5:
                sp_code = self.parameterAsInt(parameters, self.SP, context)
                if sp_code != 0:
                    commands.append("-" + self.PROJECTIONS[projection])
                    commands.append(self.STATE_PLANES[sp_code])
            else:
                commands.append("-" + self.PROJECTIONS[projection])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return Txt2Las()

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


class Txt2LasPro(LastoolsAlgorithm):
    TOOL_NAME = "Txt2LasPro"
    LASTOOL = "txt2las"
    LICENSE = "o"
    LASGROUP = 2
    PARSE = "PARSE"
    SKIP = "SKIP"
    SCALE_FACTOR_XY = "SCALE_FACTOR_XY"
    SCALE_FACTOR_Z = "SCALE_FACTOR_Z"
    PROJECTIONS = ["---", "epsg", "utm", "sp83", "sp27", "longlat", "latlong", "ecef"]
    PROJECTION = "PROJECTION"
    EPSG_CODE = "EPSG_CODE"
    UTM = "UTM"
    SP = "SP"

    def initAlgorithm(self, config=None):
        self.add_parameters_generic_input_folder_gui("*.txt")
        self.addParameter(QgsProcessingParameterString(self.PARSE, "parse lines as", "xyz"))
        self.addParameter(
            QgsProcessingParameterNumber(self.SKIP, "skip the first n lines", QgsProcessingParameterNumber.Integer, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SCALE_FACTOR_XY,
                "resolution of x and y coordinate",
                QgsProcessingParameterNumber.Double,
                0.01,
                False,
                0.00000001,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SCALE_FACTOR_Z,
                "resolution of z coordinate",
                QgsProcessingParameterNumber.Double,
                0.01,
                False,
                0.00000001,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.PROJECTION, "projection", self.PROJECTIONS, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.EPSG_CODE, "EPSG code", QgsProcessingParameterNumber.Integer, 25832, False, 1, 65535
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.UTM, "utm zone", self.UTM_ZONES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.SP, "state plane code", self.STATE_PLANES, False, 0))
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        # TODO: check the output and use f string
        self.add_parameters_generic_input_folder_commands(parameters, context, commands)
        parse_string = self.parameterAsString(parameters, self.PARSE, context)
        if parse_string != "xyz":
            commands.append("-parse")
            commands.append(parse_string)
        skip = self.parameterAsInt(parameters, self.SKIP, context)
        if skip != 0:
            commands.append("-skip")
            commands.append(str(skip))
        scale_factor_xy = self.parameterAsDouble(parameters, self.SCALE_FACTOR_XY, context)
        scale_factor_z = self.parameterAsDouble(parameters, self.SCALE_FACTOR_Z, context)
        if scale_factor_xy != 0.01 or scale_factor_z != 0.01:
            commands.append("-set_scale")
            commands.append(str(scale_factor_xy))
            commands.append(str(scale_factor_xy))
            commands.append(str(scale_factor_z))
        projection = self.parameterAsInt(parameters, self.PROJECTION, context)
        if projection != 0:
            if projection == 1:
                epsg_code = self.parameterAsInt(parameters, self.EPSG_CODE, context)
                if epsg_code != 0:
                    commands.append("-" + self.PROJECTIONS[projection])
                    commands.append(str(epsg_code))
            elif projection == 2:
                utm_zone = self.parameterAsInt(parameters, self.UTM, context)
                if utm_zone != 0:
                    commands.append("-" + self.PROJECTIONS[projection])
                    if utm_zone > 60:
                        commands.append(str(utm_zone - 60) + "south")
                    else:
                        commands.append(str(utm_zone) + "north")
            elif projection < 5:
                sp_code = self.parameterAsInt(parameters, self.SP, context)
                if sp_code != 0:
                    commands.append("-" + self.PROJECTIONS[projection])
                    commands.append(self.STATE_PLANES[sp_code])
            else:
                commands.append("-" + self.PROJECTIONS[projection])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return Txt2LasPro()

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

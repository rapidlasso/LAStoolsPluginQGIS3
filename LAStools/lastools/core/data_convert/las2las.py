# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2las.py
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

from qgis.core import QgsProcessingParameterEnum, QgsProcessingParameterString, QgsProcessingParameterNumber

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class Las2LasFilter(LastoolsAlgorithm):
    TOOL_NAME = "Las2LasFilter"
    LASTOOL = "las2las"
    LICENSE = "o"
    LASGROUP = 2

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_filter2_return_class_flags_gui()
        self.add_parameters_filter1_coords_intensity_gui()
        self.add_parameters_filter2_coords_intensity_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_filter2_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_filter1_coords_intensity_commands(parameters, context, commands)
        self.add_parameters_filter2_coords_intensity_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2LasFilter()

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


class Las2LasProject(LastoolsAlgorithm):
    TOOL_NAME = "Las2LasProject"
    LASTOOL = "las2las"
    LICENSE = "o"
    LASGROUP = 2
    SOURCE_PROJECTION = "SOURCE_PROJECTION"
    SOURCE_EPSG_CODE = "SOURCE_EPSG_CODE"
    SOURCE_UTM = "SOURCE_UTM"
    SOURCE_SP = "SOURCE_SP"
    TARGET_PROJECTION = "TARGET_PROJECTION"
    TARGET_EPSG_CODE = "TARGET_EPSG_CODE"
    TARGET_UTM = "TARGET_UTM"
    TARGET_SP = "TARGET_SP"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterEnum(self.SOURCE_PROJECTION, "source projection", self.PROJECTIONS, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SOURCE_EPSG_CODE,
                "source EPSG code",
                QgsProcessingParameterNumber.Integer,
                25832,
                False,
                1,
                65535,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.SOURCE_UTM, "source utm zone", self.UTM_ZONES, False, 0))
        self.addParameter(
            QgsProcessingParameterEnum(self.SOURCE_SP, "source state plane code", self.STATE_PLANES, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterEnum(self.TARGET_PROJECTION, "target projection", self.PROJECTIONS, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TARGET_EPSG_CODE,
                "target EPSG code",
                QgsProcessingParameterNumber.Integer,
                25832,
                False,
                1,
                65535,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.TARGET_UTM, "target utm zone", self.UTM_ZONES, False, 0))
        self.addParameter(
            QgsProcessingParameterEnum(self.TARGET_SP, "target state plane code", self.STATE_PLANES, False, 0)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_commands(parameters, context, commands)
        source_projection = self.parameterAsInt(parameters, self.SOURCE_PROJECTION, context)
        if source_projection != 0:
            if source_projection == 1:
                epsg_code = self.parameterAsInt(parameters, self.SOURCE_EPSG_CODE, context)
                if epsg_code != 0:
                    commands.append("-" + self.PROJECTIONS[source_projection])
                    commands.append(str(epsg_code))
            elif source_projection == 2:
                source_utm_zone = self.parameterAsInt(parameters, self.SOURCE_UTM, context)
                if source_utm_zone != 0:
                    commands.append("-" + self.PROJECTIONS[source_projection])
                    if source_utm_zone > 60:
                        commands.append(str(source_utm_zone - 60) + "south")
                    else:
                        commands.append(str(source_utm_zone) + "north")
            elif source_projection < 5:
                source_sp_code = self.parameterAsInt(parameters, self.SOURCE_SP, context)
                if source_sp_code != 0:
                    commands.append("-" + self.PROJECTIONS[source_projection])
                    commands.append(STATE_PLANES[source_sp_code])
            else:
                commands.append("-" + self.PROJECTIONS[source_projection])
        target_projection = self.parameterAsInt(parameters, self.TARGET_PROJECTION, context)
        if target_projection != 0:
            if target_projection == 1:
                epsg_code = self.parameterAsInt(parameters, self.TARGET_EPSG_CODE, context)
                if epsg_code != 0:
                    commands.append("-target_" + self.PROJECTIONS[source_projection])
                    commands.append(str(epsg_code))
            elif target_projection == 2:
                target_utm_zone = self.parameterAsInt(parameters, self.TARGET_UTM, context)
                if target_utm_zone != 0:
                    commands.append("-target_" + self.PROJECTIONS[target_projection])
                    if target_utm_zone > 60:
                        commands.append(str(target_utm_zone - 60) + "south")
                    else:
                        commands.append(str(target_utm_zone) + "north")
            elif target_projection < 5:
                target_sp_code = self.parameterAsInt(parameters, self.TARGET_SP, context)
                if target_sp_code != 0:
                    commands.append("-target_" + self.PROJECTIONS[target_projection])
                    commands.append(STATE_PLANES[target_sp_code])
            else:
                commands.append("-target_" + self.PROJECTIONS[target_projection])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return Las2LasProject()

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


class Las2LasTransform(LastoolsAlgorithm):
    TOOL_NAME = "Las2LasTransform"
    LASTOOL = "las2las"
    LICENSE = "o"
    LASGROUP = 2
    OPERATION = "OPERATION"
    OPERATIONS = [
        "---",
        "set_point_type",
        "set_point_size",
        "set_version_minor",
        "set_version_major",
        "start_at_point",
        "stop_at_point",
        "remove_vlr",
        "week_to_adjusted",
        "adjusted_to_week",
        "auto_reoffset",
        "scale_rgb_up",
        "scale_rgb_down",
        "remove_all_vlrs",
        "remove_extra",
        "clip_to_bounding_box",
    ]
    OPERATIONARG = "OPERATIONARG"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_transform1_coordinate_gui()
        self.add_parameters_transform2_coordinate_gui()
        self.add_parameters_transform1_other_gui()
        self.add_parameters_transform2_other_gui()
        self.addParameter(
            QgsProcessingParameterEnum(
                self.OPERATION,
                "operations (first 8 need an argument)",
                self.OPERATIONS,
                False,
                0,
            )
        )
        self.addParameter(QgsProcessingParameterString(self.OPERATIONARG, "argument for operation"))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_transform1_coordinate_commands(parameters, context, commands)
        self.add_parameters_transform2_coordinate_commands(parameters, context, commands)
        self.add_parameters_transform1_other_commands(parameters, context, commands)
        self.add_parameters_transform2_other_commands(parameters, context, commands)
        operation = self.parameterAsInt(parameters, self.OPERATION, context)
        if operation != 0:
            commands.append("-" + self.OPERATIONS[operation])
            if operation > 8:
                commands.append(self.parameterAsString(parameters, self.OPERATIONARG, context))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2LasTransform()

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


class Las2LasProFilter(LastoolsAlgorithm):
    TOOL_NAME = "Las2LasProFilter"
    LASTOOL = "las2las"
    LICENSE = "o"
    LASGROUP = 2

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_filter2_return_class_flags_gui()
        self.add_parameters_filter1_coords_intensity_gui()
        self.add_parameters_filter2_coords_intensity_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_filter2_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_filter1_coords_intensity_commands(parameters, context, commands)
        self.add_parameters_filter2_coords_intensity_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return Las2LasProFilter()

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


class Las2LasProProject(LastoolsAlgorithm):
    TOOL_NAME = "Las2LasProProject"
    LASTOOL = "las2las"
    LICENSE = "o"
    LASGROUP = 2

    SOURCE_PROJECTION = "SOURCE_PROJECTION"
    SOURCE_EPSG_CODE = "SOURCE_EPSG_CODE"
    SOURCE_UTM = "SOURCE_UTM"
    SOURCE_SP = "SOURCE_SP"

    TARGET_PROJECTION = "TARGET_PROJECTION"
    TARGET_EPSG_CODE = "TARGET_EPSG_CODE"
    TARGET_UTM = "TARGET_UTM"
    TARGET_SP = "TARGET_SP"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterEnum(self.SOURCE_PROJECTION, "source projection", self.PROJECTIONS, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SOURCE_EPSG_CODE,
                "source EPSG code",
                QgsProcessingParameterNumber.Integer,
                25832,
                False,
                1,
                65535,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.SOURCE_UTM, "source utm zone", self.UTM_ZONES, False, 0))
        self.addParameter(
            QgsProcessingParameterEnum(self.SOURCE_SP, "source state plane code", self.STATE_PLANES, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterEnum(self.TARGET_PROJECTION, "target projection", self.PROJECTIONS, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TARGET_EPSG_CODE,
                "target EPSG code",
                QgsProcessingParameterNumber.Integer,
                25832,
                False,
                1,
                65535,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.TARGET_UTM, "target utm zone", self.UTM_ZONES, False, 0))
        self.addParameter(
            QgsProcessingParameterEnum(self.TARGET_SP, "target state plane code", self.STATE_PLANES, False, 0)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        source_projection = self.parameterAsInt(parameters, self.SOURCE_PROJECTION, context)
        if source_projection != 0:
            if source_projection == 1:
                epsg_code = self.parameterAsInt(parameters, self.SOURCE_EPSG_CODE, context)
                if epsg_code != 0:
                    commands.append("-" + self.PROJECTIONS[source_projection])
                    commands.append(str(epsg_code))
            elif source_projection == 2:
                source_utm_zone = self.parameterAsInt(parameters, self.SOURCE_UTM, context)
                if source_utm_zone != 0:
                    commands.append("-" + self.PROJECTIONS[source_projection])
                    if source_utm_zone > 60:
                        commands.append(str(source_utm_zone - 60) + "south")
                    else:
                        commands.append(str(source_utm_zone) + "north")
            elif source_projection < 5:
                source_sp_code = self.parameterAsInt(parameters, self.SOURCE_SP, context)
                if source_sp_code != 0:
                    commands.append("-" + self.PROJECTIONS[source_projection])
                    commands.append(STATE_PLANES[source_sp_code])
            else:
                commands.append("-" + self.PROJECTIONS[source_projection])
        target_projection = self.parameterAsInt(parameters, self.TARGET_PROJECTION, context)
        if target_projection != 0:
            if target_projection == 1:
                epsg_code = self.parameterAsInt(parameters, self.TARGET_EPSG_CODE, context)
                if epsg_code != 0:
                    commands.append("-target_" + self.PROJECTIONS[source_projection])
                    commands.append(str(epsg_code))
            elif target_projection == 2:
                target_utm_zone = self.parameterAsInt(parameters, self.TARGET_UTM, context)
                if target_utm_zone != 0:
                    commands.append("-target_" + self.PROJECTIONS[target_projection])
                    if target_utm_zone > 60:
                        commands.append(str(target_utm_zone - 60) + "south")
                    else:
                        commands.append(str(target_utm_zone) + "north")
            elif target_projection < 5:
                target_sp_code = self.parameterAsInt(parameters, self.TARGET_SP, context)
                if target_sp_code != 0:
                    commands.append("-target_" + self.PROJECTIONS[target_projection])
                    commands.append(STATE_PLANES[target_sp_code])
            else:
                commands.append("-target_" + self.PROJECTIONS[target_projection])
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2LasProProject()

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


class Las2LasProTransform(LastoolsAlgorithm):
    TOOL_NAME = "Las2LasProTransform"
    LASTOOL = "las2las"
    LICENSE = "o"
    LASGROUP = 2
    OPERATION = "OPERATION"
    OPERATIONS = [
        "---",
        "set_point_type",
        "set_point_size",
        "set_version_minor",
        "set_version_major",
        "start_at_point",
        "stop_at_point",
        "remove_vlr",
        "week_to_adjusted",
        "adjusted_to_week",
        "auto_reoffset",
        "scale_rgb_up",
        "scale_rgb_down",
        "remove_all_vlrs",
        "remove_extra",
        "clip_to_bounding_box",
    ]
    OPERATIONARG = "OPERATIONARG"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_transform1_coordinate_gui()
        self.add_parameters_transform2_coordinate_gui()
        self.add_parameters_transform1_other_gui()
        self.add_parameters_transform2_other_gui()
        self.addParameter(
            QgsProcessingParameterEnum(
                self.OPERATION,
                "operations (first 8 need an argument)",
                self.OPERATIONS,
                False,
                0,
            )
        )
        self.addParameter(QgsProcessingParameterString(self.OPERATIONARG, "argument for operation"))
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_transform1_coordinate_commands(parameters, context, commands)
        self.add_parameters_transform2_coordinate_commands(parameters, context, commands)
        self.add_parameters_transform1_other_commands(parameters, context, commands)
        self.add_parameters_transform2_other_commands(parameters, context, commands)
        operation = self.parameterAsInt(parameters, self.OPERATION, context)
        if operation != 0:
            commands.append("-" + self.OPERATIONS[operation])
            if operation > 8:
                commands.append(self.parameterAsString(parameters, self.OPERATIONARG, context))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2LasProTransform()

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

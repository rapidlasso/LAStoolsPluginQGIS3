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

__author__ = 'rapidlasso'
__date__ = 'September 2023'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os

from PyQt5.QtGui import QIcon

from qgis.core import QgsProcessingParameterEnum, QgsProcessingParameterString, QgsProcessingParameterNumber

from ..utils import LastoolsUtils, descript_data_convert as descript_info, paths
from ..algo import LastoolsAlgorithm


class Las2LasFilter(LastoolsAlgorithm):
    TOOL_INFO = ('las2las', 'Las2LasFilter')

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_filter2_return_class_flags_gui()
        self.add_parameters_filter1_coords_intensity_gui()
        self.add_parameters_filter2_coords_intensity_gui()
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_filter2_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_filter1_coords_intensity_commands(parameters, context, commands)
        self.add_parameters_filter2_coords_intensity_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2LasFilter()

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
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")


class Las2LasProject(LastoolsAlgorithm):
    TOOL_INFO = ('las2las', 'Las2LasProject')
    STATE_PLANES = ["---", "AK_10", "AK_2", "AK_3", "AK_4", "AK_5", "AK_6", "AK_7", "AK_8", "AK_9", "AL_E", "AL_W",
                    "AR_N", "AR_S", "AZ_C", "AZ_E", "AZ_W", "CA_I", "CA_II", "CA_III", "CA_IV", "CA_V", "CA_VI",
                    "CA_VII", "CO_C", "CO_N", "CO_S", "CT", "DE", "FL_E", "FL_N", "FL_W", "GA_E", "GA_W", "HI_1",
                    "HI_2", "HI_3", "HI_4", "HI_5", "IA_N", "IA_S", "ID_C", "ID_E", "ID_W", "IL_E", "IL_W", "IN_E",
                    "IN_W", "KS_N", "KS_S", "KY_N", "KY_S", "LA_N", "LA_S", "MA_I", "MA_M", "MD", "ME_E", "ME_W",
                    "MI_C", "MI_N", "MI_S", "MN_C", "MN_N", "MN_S", "MO_C", "MO_E", "MO_W", "MS_E", "MS_W", "MT_C",
                    "MT_N", "MT_S", "NC", "ND_N", "ND_S", "NE_N", "NE_S", "NH", "NJ", "NM_C", "NM_E", "NM_W", "NV_C",
                    "NV_E", "NV_W", "NY_C", "NY_E", "NY_LI", "NY_W", "OH_N", "OH_S", "OK_N", "OK_S", "OR_N", "OR_S",
                    "PA_N", "PA_S", "PR", "RI", "SC_N", "SC_S", "SD_N", "SD_S", "St.Croix", "TN", "TX_C", "TX_N",
                    "TX_NC", "TX_S", "TX_SC", "UT_C", "UT_N", "UT_S", "VA_N", "VA_S", "VT", "WA_N", "WA_S", "WI_C",
                    "WI_N", "WI_S", "WV_N", "WV_S", "WY_E", "WY_EC", "WY_W", "WY_WC"]

    UTM_ZONES = ["---", "1 (north)", "2 (north)", "3 (north)", "4 (north)", "5 (north)", "6 (north)", "7 (north)",
                 "8 (north)", "9 (north)", "10 (north)", "11 (north)", "12 (north)", "13 (north)", "14 (north)",
                 "15 (north)", "16 (north)", "17 (north)", "18 (north)", "19 (north)", "20 (north)", "21 (north)",
                 "22 (north)", "23 (north)", "24 (north)", "25 (north)", "26 (north)", "27 (north)", "28 (north)",
                 "29 (north)", "30 (north)", "31 (north)", "32 (north)", "33 (north)", "34 (north)", "35 (north)",
                 "36 (north)", "37 (north)", "38 (north)", "39 (north)", "40 (north)", "41 (north)", "42 (north)",
                 "43 (north)", "44 (north)", "45 (north)", "46 (north)", "47 (north)", "48 (north)", "49 (north)",
                 "50 (north)", "51 (north)", "52 (north)", "53 (north)", "54 (north)", "55 (north)", "56 (north)",
                 "57 (north)", "58 (north)", "59 (north)", "60 (north)", "1 (south)", "2 (south)", "3 (south)",
                 "4 (south)", "5 (south)", "6 (south)", "7 (south)", "8 (south)", "9 (south)", "10 (south)",
                 "11 (south)", "12 (south)", "13 (south)", "14 (south)", "15 (south)", "16 (south)", "17 (south)",
                 "18 (south)", "19 (south)", "20 (south)", "21 (south)", "22 (south)", "23 (south)", "24 (south)",
                 "25 (south)", "26 (south)", "27 (south)", "28 (south)", "29 (south)", "30 (south)", "31 (south)",
                 "32 (south)", "33 (south)", "34 (south)", "35 (south)", "36 (south)", "37 (south)", "38 (south)",
                 "39 (south)", "40 (south)", "41 (south)", "42 (south)", "43 (south)", "44 (south)", "45 (south)",
                 "46 (south)", "47 (south)", "48 (south)", "49 (south)", "50 (south)", "51 (south)", "52 (south)",
                 "53 (south)", "54 (south)", "55 (south)", "56 (south)", "57 (south)", "58 (south)", "59 (south)",
                 "60 (south)"]

    PROJECTIONS = ["---", "utm", "sp83", "sp27", "longlat", "latlong", "ecef"]
    SOURCE_PROJECTION = "SOURCE_PROJECTION"
    SOURCE_UTM = "SOURCE_UTM"
    SOURCE_SP = "SOURCE_SP"
    TARGET_PROJECTION = "TARGET_PROJECTION"
    TARGET_UTM = "TARGET_UTM"
    TARGET_SP = "TARGET_SP"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProject.SOURCE_PROJECTION, "source projection", Las2LasProject.PROJECTIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProject.SOURCE_UTM, "source utm zone", Las2LasProject.UTM_ZONES, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProject.SOURCE_SP, "source state plane code", Las2LasProject.STATE_PLANES, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProject.TARGET_PROJECTION, "target projection", Las2LasProject.PROJECTIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProject.TARGET_UTM, "target utm zone", Las2LasProject.UTM_ZONES, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProject.TARGET_SP, "target state plane code", Las2LasProject.STATE_PLANES, False, 0
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        source_projection = self.parameterAsInt(parameters, Las2LasProject.SOURCE_PROJECTION, context)
        if source_projection != 0:
            if source_projection == 1:
                source_utm_zone = self.parameterAsInt(parameters, Las2LasProject.SOURCE_UTM, context)
                if source_utm_zone != 0:
                    commands.append("-" + Las2LasProject.PROJECTIONS[source_projection])
                    if source_utm_zone > 60:
                        commands.append(str(source_utm_zone - 60) + "south")
                    else:
                        commands.append(str(source_utm_zone) + "north")
            elif source_projection < 4:
                source_sp_code = self.parameterAsInt(parameters, Las2LasProject.SOURCE_SP, context)
                if source_sp_code != 0:
                    commands.append("-" + Las2LasProject.PROJECTIONS[source_projection])
                    commands.append(Las2LasProject.STATE_PLANES[source_sp_code])
            else:
                commands.append("-" + Las2LasProject.PROJECTIONS[source_projection])
        target_projection = self.parameterAsInt(parameters, Las2LasProject.TARGET_PROJECTION, context)
        if target_projection != 0:
            if target_projection == 1:
                target_utm_zone = self.parameterAsInt(parameters, Las2LasProject.TARGET_UTM, context)
                if target_utm_zone != 0:
                    commands.append("-target_" + Las2LasProject.PROJECTIONS[target_projection])
                    if target_utm_zone > 60:
                        commands.append(str(target_utm_zone - 60) + "south")
                    else:
                        commands.append(str(target_utm_zone) + "north")
            elif target_projection < 4:
                target_sp_code = self.parameterAsInt(parameters, Las2LasProject.TARGET_SP, context)
                if target_sp_code != 0:
                    commands.append("-target_" + Las2LasProject.PROJECTIONS[target_projection])
                    commands.append(Las2LasProject.STATE_PLANES[target_sp_code])
            else:
                commands.append("-target_" + Las2LasProject.PROJECTIONS[target_projection])
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2LasProject()

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
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")


class Las2LasTransform(LastoolsAlgorithm):
    TOOL_INFO = ('las2las', 'Las2LasTransform')
    OPERATION = "OPERATION"
    OPERATIONS = ["---", "set_point_type", "set_point_size", "set_version_minor", "set_version_major", "start_at_point",
                  "stop_at_point", "remove_vlr", "week_to_adjusted", "adjusted_to_week", "auto_reoffset",
                  "scale_rgb_up", "scale_rgb_down", "remove_all_vlrs", "remove_extra", "clip_to_bounding_box"]
    OPERATIONARG = "OPERATIONARG"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_gui()
        self.add_parameters_transform1_coordinate_gui()
        self.add_parameters_transform2_coordinate_gui()
        self.add_parameters_transform1_other_gui()
        self.add_parameters_transform2_other_gui()
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasTransform.OPERATION, "operations (first 8 need an argument)", Las2LasTransform.OPERATIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterString(Las2LasTransform.OPERATIONARG, "argument for operation"))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_transform1_coordinate_commands(parameters, context, commands)
        self.add_parameters_transform2_coordinate_commands(parameters, context, commands)
        self.add_parameters_transform1_other_commands(parameters, context, commands)
        self.add_parameters_transform2_other_commands(parameters, context, commands)
        operation = self.parameterAsInt(parameters, Las2LasTransform.OPERATION, context)
        if operation != 0:
            commands.append("-" + Las2LasTransform.OPERATIONS[operation])
            if operation > 8:
                commands.append(self.parameterAsString(parameters, Las2LasTransform.OPERATIONARG, context))
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2LasTransform()

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
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")


class Las2LasProFilter(LastoolsAlgorithm):
    TOOL_INFO = ('las2las', 'Las2LasProFilter')

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_filter2_return_class_flags_gui()
        self.add_parameters_filter1_coords_intensity_gui()
        self.add_parameters_filter2_coords_intensity_gui()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_filter2_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_filter1_coords_intensity_commands(parameters, context, commands)
        self.add_parameters_filter2_coords_intensity_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2LasProFilter()

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
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")


class Las2LasProProject(LastoolsAlgorithm):
    TOOL_INFO = ('las2las', 'Las2LasProProject')
    STATE_PLANES = ["---", "AK_10", "AK_2", "AK_3", "AK_4", "AK_5", "AK_6", "AK_7", "AK_8", "AK_9", "AL_E", "AL_W",
                    "AR_N", "AR_S", "AZ_C", "AZ_E", "AZ_W", "CA_I", "CA_II", "CA_III", "CA_IV", "CA_V", "CA_VI",
                    "CA_VII", "CO_C", "CO_N", "CO_S", "CT", "DE", "FL_E", "FL_N", "FL_W", "GA_E", "GA_W", "HI_1",
                    "HI_2", "HI_3", "HI_4", "HI_5", "IA_N", "IA_S", "ID_C", "ID_E", "ID_W", "IL_E", "IL_W", "IN_E",
                    "IN_W", "KS_N", "KS_S", "KY_N", "KY_S", "LA_N", "LA_S", "MA_I", "MA_M", "MD", "ME_E", "ME_W",
                    "MI_C", "MI_N", "MI_S", "MN_C", "MN_N", "MN_S", "MO_C", "MO_E", "MO_W", "MS_E", "MS_W", "MT_C",
                    "MT_N", "MT_S", "NC", "ND_N", "ND_S", "NE_N", "NE_S", "NH", "NJ", "NM_C", "NM_E", "NM_W", "NV_C",
                    "NV_E", "NV_W", "NY_C", "NY_E", "NY_LI", "NY_W", "OH_N", "OH_S", "OK_N", "OK_S", "OR_N", "OR_S",
                    "PA_N", "PA_S", "PR", "RI", "SC_N", "SC_S", "SD_N", "SD_S", "St.Croix", "TN", "TX_C", "TX_N",
                    "TX_NC", "TX_S", "TX_SC", "UT_C", "UT_N", "UT_S", "VA_N", "VA_S", "VT", "WA_N", "WA_S", "WI_C",
                    "WI_N", "WI_S", "WV_N", "WV_S", "WY_E", "WY_EC", "WY_W", "WY_WC"]

    UTM_ZONES = ["---", "1 (north)", "2 (north)", "3 (north)", "4 (north)", "5 (north)", "6 (north)", "7 (north)",
                 "8 (north)", "9 (north)", "10 (north)", "11 (north)", "12 (north)", "13 (north)", "14 (north)",
                 "15 (north)", "16 (north)", "17 (north)", "18 (north)", "19 (north)", "20 (north)", "21 (north)",
                 "22 (north)", "23 (north)", "24 (north)", "25 (north)", "26 (north)", "27 (north)", "28 (north)",
                 "29 (north)", "30 (north)", "31 (north)", "32 (north)", "33 (north)", "34 (north)", "35 (north)",
                 "36 (north)", "37 (north)", "38 (north)", "39 (north)", "40 (north)", "41 (north)", "42 (north)",
                 "43 (north)", "44 (north)", "45 (north)", "46 (north)", "47 (north)", "48 (north)", "49 (north)",
                 "50 (north)", "51 (north)", "52 (north)", "53 (north)", "54 (north)", "55 (north)", "56 (north)",
                 "57 (north)", "58 (north)", "59 (north)", "60 (north)", "1 (south)", "2 (south)", "3 (south)",
                 "4 (south)", "5 (south)", "6 (south)", "7 (south)", "8 (south)", "9 (south)", "10 (south)",
                 "11 (south)", "12 (south)", "13 (south)", "14 (south)", "15 (south)", "16 (south)", "17 (south)",
                 "18 (south)", "19 (south)", "20 (south)", "21 (south)", "22 (south)", "23 (south)", "24 (south)",
                 "25 (south)", "26 (south)", "27 (south)", "28 (south)", "29 (south)", "30 (south)", "31 (south)",
                 "32 (south)", "33 (south)", "34 (south)", "35 (south)", "36 (south)", "37 (south)", "38 (south)",
                 "39 (south)", "40 (south)", "41 (south)", "42 (south)", "43 (south)", "44 (south)", "45 (south)",
                 "46 (south)", "47 (south)", "48 (south)", "49 (south)", "50 (south)", "51 (south)", "52 (south)",
                 "53 (south)", "54 (south)", "55 (south)", "56 (south)", "57 (south)", "58 (south)", "59 (south)",
                 "60 (south)"]

    PROJECTIONS = ["---", "epsg", "utm", "sp83", "sp27", "longlat", "latlong", "ecef"]

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
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProProject.SOURCE_PROJECTION, "source projection", Las2LasProProject.PROJECTIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Las2LasProProject.SOURCE_EPSG_CODE, "source EPSG code",
            QgsProcessingParameterNumber.Integer, 25832, False, 1, 65535
        ))
        self.addParameter(
            QgsProcessingParameterEnum(
                Las2LasProProject.SOURCE_UTM, "source utm zone", Las2LasProProject.UTM_ZONES, False, 0
            ))
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProProject.SOURCE_SP, "source state plane code", Las2LasProProject.STATE_PLANES, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProProject.TARGET_PROJECTION, "target projection", Las2LasProProject.PROJECTIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Las2LasProProject.TARGET_EPSG_CODE, "target EPSG code",
            QgsProcessingParameterNumber.Integer, 25832, False, 1, 65535
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProProject.TARGET_UTM, "target utm zone", Las2LasProProject.UTM_ZONES, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProProject.TARGET_SP, "target state plane code", Las2LasProProject.STATE_PLANES, False, 0
        ))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        source_projection = self.parameterAsInt(parameters, Las2LasProProject.SOURCE_PROJECTION, context)
        if source_projection != 0:
            if source_projection == 1:
                epsg_code = self.parameterAsInt(parameters, Las2LasProProject.SOURCE_EPSG_CODE, context)
                if epsg_code != 0:
                    commands.append("-" + Las2LasProProject.PROJECTIONS[source_projection])
                    commands.append(str(epsg_code))
            elif source_projection == 2:
                source_utm_zone = self.parameterAsInt(parameters, Las2LasProProject.SOURCE_UTM, context)
                if source_utm_zone != 0:
                    commands.append("-" + Las2LasProProject.PROJECTIONS[source_projection])
                    if source_utm_zone > 60:
                        commands.append(str(source_utm_zone - 60) + "south")
                    else:
                        commands.append(str(source_utm_zone) + "north")
            elif source_projection < 5:
                source_sp_code = self.parameterAsInt(parameters, Las2LasProProject.SOURCE_SP, context)
                if source_sp_code != 0:
                    commands.append("-" + Las2LasProProject.PROJECTIONS[source_projection])
                    commands.append(Las2LasProProject.STATE_PLANES[source_sp_code])
            else:
                commands.append("-" + Las2LasProProject.PROJECTIONS[source_projection])
        target_projection = self.parameterAsInt(parameters, Las2LasProProject.TARGET_PROJECTION, context)
        if target_projection != 0:
            if target_projection == 1:
                epsg_code = self.parameterAsInt(parameters, Las2LasProProject.TARGET_EPSG_CODE, context)
                if epsg_code != 0:
                    commands.append("-target_" + Las2LasProProject.PROJECTIONS[source_projection])
                    commands.append(str(epsg_code))
            elif target_projection == 2:
                target_utm_zone = self.parameterAsInt(parameters, Las2LasProProject.TARGET_UTM, context)
                if target_utm_zone != 0:
                    commands.append("-target_" + Las2LasProProject.PROJECTIONS[target_projection])
                    if target_utm_zone > 60:
                        commands.append(str(target_utm_zone - 60) + "south")
                    else:
                        commands.append(str(target_utm_zone) + "north")
            elif target_projection < 5:
                target_sp_code = self.parameterAsInt(parameters, Las2LasProProject.TARGET_SP, context)
                if target_sp_code != 0:
                    commands.append("-target_" + Las2LasProProject.PROJECTIONS[target_projection])
                    commands.append(Las2LasProProject.STATE_PLANES[target_sp_code])
            else:
                commands.append("-target_" + Las2LasProProject.PROJECTIONS[target_projection])
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2LasProProject()

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
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")


class Las2LasProTransform(LastoolsAlgorithm):
    TOOL_INFO = ('las2las', 'Las2LasProTransform')
    OPERATION = "OPERATION"
    OPERATIONS = ["---", "set_point_type", "set_point_size", "set_version_minor", "set_version_major", "start_at_point",
                  "stop_at_point", "remove_vlr", "week_to_adjusted", "adjusted_to_week", "auto_reoffset",
                  "scale_rgb_up", "scale_rgb_down", "remove_all_vlrs", "remove_extra", "clip_to_bounding_box"]
    OPERATIONARG = "OPERATIONARG"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_transform1_coordinate_gui()
        self.add_parameters_transform2_coordinate_gui()
        self.add_parameters_transform1_other_gui()
        self.add_parameters_transform2_other_gui()
        self.addParameter(QgsProcessingParameterEnum(
            Las2LasProTransform.OPERATION, "operations (first 8 need an argument)",
            Las2LasProTransform.OPERATIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterString(Las2LasProTransform.OPERATIONARG, "argument for operation"))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_transform1_coordinate_commands(parameters, context, commands)
        self.add_parameters_transform2_coordinate_commands(parameters, context, commands)
        self.add_parameters_transform1_other_commands(parameters, context, commands)
        self.add_parameters_transform2_other_commands(parameters, context, commands)
        operation = self.parameterAsInt(parameters, Las2LasProTransform.OPERATION, context)
        if operation != 0:
            commands.append("-" + Las2LasProTransform.OPERATIONS[operation])
            if operation > 8:
                commands.append(self.parameterAsString(parameters, Las2LasProTransform.OPERATIONARG, context))
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2LasProTransform()

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
        licence_icon_path = descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence_icon_path"]
        return QIcon(f"{paths['img']}{licence_icon_path}")

# -*- coding: utf-8 -*-

"""
***************************************************************************
    txt2las.py
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
from qgis.core import QgsProcessingParameterNumber, QgsProcessingParameterString, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_data_convert as descript_info, paths
from ..algo import LastoolsAlgorithm


class Txt2Las(LastoolsAlgorithm):
    TOOL_INFO = ('txt2las', 'Txt2Las')
    PARSE = "PARSE"
    SKIP = "SKIP"
    SCALE_FACTOR_XY = "SCALE_FACTOR_XY"
    SCALE_FACTOR_Z = "SCALE_FACTOR_Z"
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
    PROJECTION = "PROJECTION"
    EPSG_CODE = "EPSG_CODE"
    UTM = "UTM"
    SP = "SP"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui_64()
        self.add_parameters_generic_input_gui("Input ASCII file", "txt", False)
        self.addParameter(QgsProcessingParameterString(Txt2Las.PARSE, "parse lines as", "xyz"))
        self.addParameter(QgsProcessingParameterNumber(
            Txt2Las.SKIP, "skip the first n lines", QgsProcessingParameterNumber.Integer, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Txt2Las.SCALE_FACTOR_XY, "resolution of x and y coordinate",
            QgsProcessingParameterNumber.Double, 0.01, False, 0.00000001
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Txt2Las.SCALE_FACTOR_Z, "resolution of z coordinate",
            QgsProcessingParameterNumber.Double, 0.01, False, 0.00000001
        ))
        self.addParameter(QgsProcessingParameterEnum(Txt2Las.PROJECTION, "projection", Txt2Las.PROJECTIONS, False, 0))
        self.addParameter(QgsProcessingParameterNumber(
            Txt2Las.EPSG_CODE, "EPSG code", QgsProcessingParameterNumber.Integer, 25832
        ))
        self.addParameter(QgsProcessingParameterEnum(Txt2Las.UTM, "utm zone", Txt2Las.UTM_ZONES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(Txt2Las.SP, "state plane code", Txt2Las.STATE_PLANES, False, 0))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "txt2las.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "txt2las")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-i")
        parse_string = self.parameterAsString(parameters, Txt2Las.PARSE, context)
        if parse_string != "xyz":
            commands.append("-parse")
            commands.append(parse_string)
        skip = self.parameterAsInt(parameters, Txt2Las.SKIP, context)
        if skip != 0:
            commands.append("-skip")
            commands.append(str(skip))
        scale_factor_xy = self.parameterAsDouble(parameters, Txt2Las.SCALE_FACTOR_XY, context)
        scale_factor_z = self.parameterAsDouble(parameters, Txt2Las.SCALE_FACTOR_Z, context)
        if scale_factor_xy != 0.01 or scale_factor_z != 0.01:
            commands.append("-set_scale")
            commands.append(str(scale_factor_xy))
            commands.append(str(scale_factor_xy))
            commands.append(str(scale_factor_z))
        projection = self.parameterAsInt(parameters, Txt2Las.PROJECTION, context)
        if projection != 0:
            if projection == 1:
                epsg_code = self.parameterAsInt(parameters, Txt2Las.EPSG_CODE, context)
                if epsg_code != 0:
                    commands.append("-" + Txt2Las.PROJECTIONS[projection])
                    commands.append(str(epsg_code))
            elif projection == 2:
                utm_zone = self.parameterAsInt(parameters, Txt2Las.UTM, context)
                if utm_zone != 0:
                    commands.append("-" + Txt2Las.PROJECTIONS[projection])
                    if utm_zone > 60:
                        commands.append(str(utm_zone - 60) + "south")
                    else:
                        commands.append(str(utm_zone) + "north")
            elif projection < 5:
                sp_code = self.parameterAsInt(parameters, Txt2Las.SP, context)
                if sp_code != 0:
                    commands.append("-" + Txt2Las.PROJECTIONS[projection])
                    commands.append(Txt2Las.STATE_PLANES[sp_code])
            else:
                commands.append("-" + Txt2Las.PROJECTIONS[projection])
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Txt2Las()

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


class Txt2LasPro(LastoolsAlgorithm):
    TOOL_INFO = ('txt2las', 'Txt2LasPro')
    PARSE = "PARSE"
    SKIP = "SKIP"
    SCALE_FACTOR_XY = "SCALE_FACTOR_XY"
    SCALE_FACTOR_Z = "SCALE_FACTOR_Z"
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
    PROJECTION = "PROJECTION"
    EPSG_CODE = "EPSG_CODE"
    UTM = "UTM"
    SP = "SP"

    def initAlgorithm(self, config=None):
        self.add_parameters_generic_input_folder_gui("*.txt")
        self.addParameter(QgsProcessingParameterString(Txt2LasPro.PARSE, "parse lines as", "xyz"))
        self.addParameter(QgsProcessingParameterNumber(
            Txt2LasPro.SKIP, "skip the first n lines", QgsProcessingParameterNumber.Integer, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Txt2LasPro.SCALE_FACTOR_XY, "resolution of x and y coordinate",
            QgsProcessingParameterNumber.Double, 0.01, False, 0.00000001
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Txt2LasPro.SCALE_FACTOR_Z, "resolution of z coordinate",
            QgsProcessingParameterNumber.Double, 0.01, False, 0.00000001
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Txt2LasPro.PROJECTION, "projection", Txt2LasPro.PROJECTIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Txt2LasPro.EPSG_CODE, "EPSG code", QgsProcessingParameterNumber.Integer, 25832, False, 1, 65535
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Txt2LasPro.UTM, "utm zone", Txt2LasPro.UTM_ZONES, False, 0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            Txt2LasPro.SP, "state plane code", Txt2LasPro.STATE_PLANES, False, 0
        ))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        if LastoolsUtils.has_wine():
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "txt2las.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "txt2las")]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        # TODO: check the output and use f string
        self.add_parameters_generic_input_folder_commands(parameters, context, commands)
        parse_string = self.parameterAsString(parameters, Txt2LasPro.PARSE, context)
        if parse_string != "xyz":
            commands.append("-parse")
            commands.append(parse_string)
        skip = self.parameterAsInt(parameters, Txt2LasPro.SKIP, context)
        if skip != 0:
            commands.append("-skip")
            commands.append(str(skip))
        scale_factor_xy = self.parameterAsDouble(parameters, Txt2LasPro.SCALE_FACTOR_XY, context)
        scale_factor_z = self.parameterAsDouble(parameters, Txt2LasPro.SCALE_FACTOR_Z, context)
        if scale_factor_xy != 0.01 or scale_factor_z != 0.01:
            commands.append("-set_scale")
            commands.append(str(scale_factor_xy))
            commands.append(str(scale_factor_xy))
            commands.append(str(scale_factor_z))
        projection = self.parameterAsInt(parameters, Txt2LasPro.PROJECTION, context)
        if projection != 0:
            if projection == 1:
                epsg_code = self.parameterAsInt(parameters, Txt2LasPro.EPSG_CODE, context)
                if epsg_code != 0:
                    commands.append("-" + Txt2LasPro.PROJECTIONS[projection])
                    commands.append(str(epsg_code))
            elif projection == 2:
                utm_zone = self.parameterAsInt(parameters, Txt2LasPro.UTM, context)
                if utm_zone != 0:
                    commands.append("-" + Txt2LasPro.PROJECTIONS[projection])
                    if utm_zone > 60:
                        commands.append(str(utm_zone - 60) + "south")
                    else:
                        commands.append(str(utm_zone) + "north")
            elif projection < 5:
                sp_code = self.parameterAsInt(parameters, Txt2LasPro.SP, context)
                if sp_code != 0:
                    commands.append("-" + Txt2LasPro.PROJECTIONS[projection])
                    commands.append(Txt2LasPro.STATE_PLANES[sp_code])
            else:
                commands.append("-" + Txt2LasPro.PROJECTIONS[projection])
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Txt2LasPro()

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

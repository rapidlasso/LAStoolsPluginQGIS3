# -*- coding: utf-8 -*-

"""
***************************************************************************
    txt2lasPro.py
    ---------------------
    Date                 : October 2014, May 2016 and August 2018
    Copyright            : (C) 2014 by Martin Isenburg
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
__date__ = 'October 2014'
__copyright__ = '(C) 2014, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class txt2lasPro(LAStoolsAlgorithm):

    PARSE = "PARSE"
    SKIP = "SKIP"
    SCALE_FACTOR_XY = "SCALE_FACTOR_XY"
    SCALE_FACTOR_Z = "SCALE_FACTOR_Z"

    STATE_PLANES = ["---", "AK_10", "AK_2", "AK_3", "AK_4", "AK_5", "AK_6", "AK_7", "AK_8", "AK_9", "AL_E", "AL_W", "AR_N", "AR_S", "AZ_C", "AZ_E", "AZ_W", "CA_I", "CA_II", "CA_III", "CA_IV", "CA_V", "CA_VI", "CA_VII", "CO_C", "CO_N", "CO_S", "CT", "DE", "FL_E", "FL_N", "FL_W", "GA_E", "GA_W", "HI_1", "HI_2", "HI_3", "HI_4", "HI_5", "IA_N", "IA_S", "ID_C", "ID_E", "ID_W", "IL_E", "IL_W", "IN_E", "IN_W", "KS_N", "KS_S", "KY_N", "KY_S", "LA_N", "LA_S", "MA_I", "MA_M", "MD", "ME_E", "ME_W", "MI_C", "MI_N", "MI_S", "MN_C", "MN_N", "MN_S", "MO_C", "MO_E", "MO_W", "MS_E", "MS_W", "MT_C", "MT_N", "MT_S", "NC", "ND_N", "ND_S", "NE_N", "NE_S", "NH", "NJ", "NM_C", "NM_E", "NM_W", "NV_C", "NV_E", "NV_W", "NY_C", "NY_E", "NY_LI", "NY_W", "OH_N", "OH_S", "OK_N", "OK_S", "OR_N", "OR_S", "PA_N", "PA_S", "PR", "RI", "SC_N", "SC_S", "SD_N", "SD_S", "St.Croix", "TN", "TX_C", "TX_N", "TX_NC", "TX_S", "TX_SC", "UT_C", "UT_N", "UT_S", "VA_N", "VA_S", "VT", "WA_N", "WA_S", "WI_C", "WI_N", "WI_S", "WV_N", "WV_S", "WY_E", "WY_EC", "WY_W", "WY_WC"]

    UTM_ZONES = ["---", "1 (north)", "2 (north)", "3 (north)", "4 (north)", "5 (north)", "6 (north)", "7 (north)", "8 (north)", "9 (north)", "10 (north)", "11 (north)", "12 (north)", "13 (north)", "14 (north)", "15 (north)", "16 (north)", "17 (north)", "18 (north)", "19 (north)", "20 (north)", "21 (north)", "22 (north)", "23 (north)", "24 (north)", "25 (north)", "26 (north)", "27 (north)", "28 (north)", "29 (north)", "30 (north)", "31 (north)", "32 (north)", "33 (north)", "34 (north)", "35 (north)", "36 (north)", "37 (north)", "38 (north)", "39 (north)", "40 (north)", "41 (north)", "42 (north)", "43 (north)", "44 (north)", "45 (north)", "46 (north)", "47 (north)", "48 (north)", "49 (north)", "50 (north)", "51 (north)", "52 (north)", "53 (north)", "54 (north)", "55 (north)", "56 (north)", "57 (north)", "58 (north)", "59 (north)", "60 (north)", "1 (south)", "2 (south)", "3 (south)", "4 (south)", "5 (south)", "6 (south)", "7 (south)", "8 (south)", "9 (south)", "10 (south)", "11 (south)", "12 (south)", "13 (south)", "14 (south)", "15 (south)", "16 (south)", "17 (south)", "18 (south)", "19 (south)", "20 (south)", "21 (south)", "22 (south)", "23 (south)", "24 (south)", "25 (south)", "26 (south)", "27 (south)", "28 (south)", "29 (south)", "30 (south)", "31 (south)", "32 (south)", "33 (south)", "34 (south)", "35 (south)", "36 (south)", "37 (south)", "38 (south)", "39 (south)", "40 (south)", "41 (south)", "42 (south)", "43 (south)", "44 (south)", "45 (south)", "46 (south)", "47 (south)", "48 (south)", "49 (south)", "50 (south)", "51 (south)", "52 (south)", "53 (south)", "54 (south)", "55 (south)", "56 (south)", "57 (south)", "58 (south)", "59 (south)", "60 (south)"]

    PROJECTIONS = ["---", "epsg", "utm", "sp83", "sp27", "longlat", "latlong", "ecef"]

    PROJECTION = "PROJECTION"
    EPSG_CODE = "EPSG_CODE"
    UTM = "UTM"
    SP = "SP"

    def initAlgorithm(self, config):
        self.addParametersGenericInputFolderGUI("*.txt")
        self.addParameter(QgsProcessingParameterString(txt2lasPro.PARSE, "parse lines as", "xyz"))
        self.addParameter(QgsProcessingParameterNumber(txt2lasPro.SKIP, "skip the first n lines", QgsProcessingParameterNumber.Integer, 0))
        self.addParameter(QgsProcessingParameterNumber(txt2lasPro.SCALE_FACTOR_XY, "resolution of x and y coordinate", QgsProcessingParameterNumber.Double, 0.01, False, 0.00000001))
        self.addParameter(QgsProcessingParameterNumber(txt2lasPro.SCALE_FACTOR_Z, "resolution of z coordinate", QgsProcessingParameterNumber.Double, 0.01, False, 0.00000001))
        self.addParameter(QgsProcessingParameterEnum(txt2lasPro.PROJECTION, "projection", txt2lasPro.PROJECTIONS, False, 0))
        self.addParameter(QgsProcessingParameterNumber(txt2lasPro.EPSG_CODE, "EPSG code", QgsProcessingParameterNumber.Integer, 25832, False, 1, 65535))
        self.addParameter(QgsProcessingParameterEnum(txt2lasPro.UTM, "utm zone", txt2lasPro.UTM_ZONES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(txt2lasPro.SP, "state plane code", txt2lasPro.STATE_PLANES, False, 0))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI() 
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "txt2las.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "txt2las")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersGenericInputFolderCommands(parameters, context, commands)
        parse_string = self.parameterAsString(parameters, txt2lasPro.PARSE, context)
        if (parse_string != "xyz"):
            commands.append("-parse")
            commands.append(parse_string)
        skip = self.parameterAsInt(parameters, txt2lasPro.SKIP, context)
        if (skip != 0):
            commands.append("-skip")
            commands.append(unicode(skip))
        scale_factor_xy = self.parameterAsDouble(parameters, txt2lasPro.SCALE_FACTOR_XY, context)
        scale_factor_z = self.parameterAsDouble(parameters, txt2lasPro.SCALE_FACTOR_Z, context)
        if scale_factor_xy != 0.01 or scale_factor_z != 0.01:
            commands.append("-set_scale")
            commands.append(unicode(scale_factor_xy))
            commands.append(unicode(scale_factor_xy))
            commands.append(unicode(scale_factor_z))
        projection = self.parameterAsInt(parameters, txt2lasPro.PROJECTION, context)
        if (projection != 0):
            if (projection == 1):
                epsg_code = self.parameterAsInt(parameters, txt2lasPro.EPSG_CODE, context)
                if (epsg_code != 0):
                    commands.append("-" + txt2lasPro.PROJECTIONS[projection])
                    commands.append(unicode(epsg_code))
            elif (projection == 2):
                utm_zone = self.parameterAsInt(parameters, txt2lasPro.UTM, context)
                if (utm_zone != 0):
                    commands.append("-" + txt2lasPro.PROJECTIONS[projection])
                    if (utm_zone > 60):
                        commands.append(unicode(utm_zone - 60) + "south")
                    else:
                        commands.append(unicode(utm_zone) + "north")
            elif (projection < 5):
                sp_code = self.parameterAsInt(parameters, txt2lasPro.SP, context)
                if (sp_code != 0):
                    commands.append("-" + txt2lasPro.PROJECTIONS[projection])
                    commands.append(txt2lasPro.STATE_PLANES[sp_code])
            else:
                commands.append("-" + txt2lasPro.PROJECTIONS[projection])
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'txt2lasPro'

    def displayName(self):
        return 'txt2lasPro'

    def group(self):
        return 'folder - conversion'

    def groupId(self):
        return 'folder - conversion'

    def createInstance(self):
        return txt2lasPro()

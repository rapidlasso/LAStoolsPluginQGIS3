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

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterNumber, QgsProcessingParameterFileDestination, QgsProcessingParameterString

from ..utils import LastoolsUtils, descript_processing as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasIntensity(LastoolsAlgorithm):
    TOOL_INFO = ('lasintensity', 'LasIntensity')
    SCANNER_HEIGHT = "SCANNER_HEIGHT"
    ATMOSPHERIC_VISIBILITY_RANGE = "ATMOSPHERIC_VISIBILITY_RANGE"
    LASER_WAVELENGTH = "LASER_WAVELENGTH"
    ADDITIONAL_PARAM = 'ADDITIONAL_PARAM'
    OUTPUT_LAS_PATH = 'OUTPUT_LAS_PATH'

    def initAlgorithm(self, config=None):
        # input verbose and 64 bit exe
        self.add_parameters_verbose_64()
        # input las file
        self.add_parameters_point_input_gui()
        # Scanner Height
        self.addParameter(QgsProcessingParameterNumber(
            LasIntensity.SCANNER_HEIGHT, "Scanner Altitude in [km]",
            QgsProcessingParameterNumber.Double, 3.0, False, 0.0, 10000.0)
        )
        # atmospheric visibility range
        self.addParameter(QgsProcessingParameterNumber(
            LasIntensity.ATMOSPHERIC_VISIBILITY_RANGE, "Atmospheric Visibility Range in [km]",
            QgsProcessingParameterNumber.Double, 10.0, False, 0.0, 10000.0)
        )
        # Laser Wavelength
        self.addParameter(QgsProcessingParameterNumber(
            LasIntensity.LASER_WAVELENGTH, "Laser Wavelength in [µm]",
            QgsProcessingParameterNumber.Double, 0.905, False, 0.0, 10000.0)
        )
        # output las path
        self.addParameter(QgsProcessingParameterFileDestination(
            LasIntensity.OUTPUT_LAS_PATH, "Output LAS/LAZ file", "*.laz *.las", "", False, False)
        )
        # additional parameters
        self.addParameter(QgsProcessingParameterString(
            LasIntensity.ADDITIONAL_PARAM, "additional command line parameter(s)", ' ', False, False
        ))
        self.helpUrl()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasintensity64")]
        # append -v and -cpu64
        self.add_parameters_verbose_64_commands(parameters, context, commands)
        # append -i
        commands.append(f"-i {parameters['INPUT_LASLAZ']}")
        # append -scanner_height
        commands.append(f"-scanner_height {parameters['SCANNER_HEIGHT']}")
        # append -av
        commands.append(f"-av {parameters['ATMOSPHERIC_VISIBILITY_RANGE']} ")
        # append -w
        commands.append(f"-w {parameters['LASER_WAVELENGTH']} ")
        # append -o
        if parameters["OUTPUT_LAS_PATH"] != 'TEMPORARY_OUTPUT':
            commands.append(f"-o {parameters['OUTPUT_LAS_PATH']}")
        # append extra params
        commands.append(parameters['ADDITIONAL_PARAM'])
        LastoolsUtils.run_lastools(commands, feedback)
        return {"command": commands}

    def createInstance(self):
        return LasIntensity()

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


class LasIntensityAttenuationFactor(LastoolsAlgorithm):
    TOOL_INFO = ('lasintensity', 'LasIntensityAttenuationFactor')
    SCANNER_HEIGHT = "SCANNER_HEIGHT"
    ATTENUATION_COEFFICIENT = "ATTENUATION_COEFFICIENT"
    ADDITIONAL_PARAM = 'ADDITIONAL_PARAM'
    OUTPUT_LAS_PATH = 'OUTPUT_LAS_PATH'

    def initAlgorithm(self, config=None):
        # input verbose and 64 bit exe
        self.add_parameters_verbose_64()
        # input las file
        self.add_parameters_point_input_gui()
        # Scanner Height
        self.addParameter(QgsProcessingParameterNumber(
            LasIntensityAttenuationFactor.SCANNER_HEIGHT, "Scanner Altitude in [km]",
            QgsProcessingParameterNumber.Double, 3.0, False, 0.0, 10000.0)
        )
        # Attenuation Coefficient factor
        self.addParameter(QgsProcessingParameterNumber(
            LasIntensityAttenuationFactor.ATTENUATION_COEFFICIENT, "Attenuation Coefficient in [km^-1]",
            QgsProcessingParameterNumber.Double, 0.0, False, 0.0, 10000.0)
        )
        # output las path
        self.addParameter(QgsProcessingParameterFileDestination(
            LasIntensityAttenuationFactor.OUTPUT_LAS_PATH, "Output LAS/LAZ file", "*.laz *.las", "", False, False)
        )
        # additional parameters
        self.addParameter(QgsProcessingParameterString(
            LasIntensityAttenuationFactor.ADDITIONAL_PARAM, "additional command line parameter(s)", ' ', False, False
        ))
        self.helpUrl()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasintensity64")]
        # append -v and -cpu64
        self.add_parameters_verbose_64_commands(parameters, context, commands)
        # append -i
        self.add_parameters_point_input_commands(parameters, context, commands)
        # append -scanner_height
        commands.append(f"-scanner_height {parameters['SCANNER_HEIGHT']}")
        # append -a
        commands.append(f"-a {parameters['ATTENUATION_COEFFICIENT']}")
        # append -o
        if parameters["OUTPUT_LAS_PATH"] != 'TEMPORARY_OUTPUT':
            commands.append(f"-o {parameters['OUTPUT_LAS_PATH']}")
        # append extra params
        commands.append(parameters['ADDITIONAL_PARAM'])
        LastoolsUtils.run_lastools(commands, feedback)
        return {"command": commands}

    def createInstance(self):
        return LasIntensityAttenuationFactor()

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

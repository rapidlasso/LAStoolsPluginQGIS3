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

__author__ = "rapidlasso"
__date__ = "March 2024"
__copyright__ = "(C) 2024, rapidlasso GmbH"

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterNumber, QgsProcessingParameterFileDestination, QgsProcessingParameterString

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasIntensity(LastoolsAlgorithm):
    TOOL_NAME = "LasIntensity"
    LASTOOL = "lasintensity"
    LICENSE = "c"
    LASGROUP = 3
    SCANNER_HEIGHT = "SCANNER_HEIGHT"
    ATMOSPHERIC_VISIBILITY_RANGE = "ATMOSPHERIC_VISIBILITY_RANGE"
    LASER_WAVELENGTH = "LASER_WAVELENGTH"
    ADDITIONAL_PARAM = "ADDITIONAL_PARAM"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        # Scanner Height
        self.addParameter(
            QgsProcessingParameterNumber(
                LasIntensity.SCANNER_HEIGHT,
                "scanner altitude in [km]",
                QgsProcessingParameterNumber.Double,
                3.0,
                False,
                0.0,
                10000.0,
            )
        )
        # atmospheric visibility range
        self.addParameter(
            QgsProcessingParameterNumber(
                LasIntensity.ATMOSPHERIC_VISIBILITY_RANGE,
                "atmospheric visibility range in [km]",
                QgsProcessingParameterNumber.Double,
                10.0,
                False,
                0.0,
                10000.0,
            )
        )
        # Laser Wavelength
        self.addParameter(
            QgsProcessingParameterNumber(
                LasIntensity.LASER_WAVELENGTH,
                "laser wavelength in [µm]",
                QgsProcessingParameterNumber.Double,
                0.905,
                False,
                0.0,
                10000.0,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [
            os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + "64" + LastoolsUtils.command_ext())
        ]
        self.add_parameters_point_input_commands(parameters, context, commands)
        commands.append(f"-scanner_height {parameters['SCANNER_HEIGHT']}")
        commands.append(f"-av {parameters['ATMOSPHERIC_VISIBILITY_RANGE']} ")
        commands.append(f"-w {parameters['LASER_WAVELENGTH']} ")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"command": commands}

    def createInstance(self):
        return LasIntensity()

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


class LasIntensityAttenuationFactor(LastoolsAlgorithm):
    TOOL_NAME = "LasIntensityAttenuationFactor"
    LASTOOL = "lasintensity"
    LICENSE = "c"
    LASGROUP = 3
    SCANNER_HEIGHT = "SCANNER_HEIGHT"
    ATTENUATION_COEFFICIENT = "ATTENUATION_COEFFICIENT"
    ADDITIONAL_PARAM = "ADDITIONAL_PARAM"
    OUTPUT_LAS_PATH = "OUTPUT_LAS_PATH"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        # Scanner Height
        self.addParameter(
            QgsProcessingParameterNumber(
                LasIntensityAttenuationFactor.SCANNER_HEIGHT,
                "scanner altitude in [km]",
                QgsProcessingParameterNumber.Double,
                3.0,
                False,
                0.0,
                10000.0,
            )
        )
        # Attenuation Coefficient factor
        self.addParameter(
            QgsProcessingParameterNumber(
                LasIntensityAttenuationFactor.ATTENUATION_COEFFICIENT,
                "attenuation coefficient in [km^-1]",
                QgsProcessingParameterNumber.Double,
                0.0,
                False,
                0.0,
                10000.0,
            )
        )
        # output las path
        self.addParameter(
            QgsProcessingParameterFileDestination(
                LasIntensityAttenuationFactor.OUTPUT_LAS_PATH, "Output LAS/LAZ file", "*.laz *.las", "", False, False
            )
        )
        # additional parameters
        self.addParameter(
            QgsProcessingParameterString(
                LasIntensityAttenuationFactor.ADDITIONAL_PARAM,
                "additional command line arguments",
                " ",
                False,
                False,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [
            os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + "64" + LastoolsUtils.command_ext())
        ]
        self.add_parameters_point_input_commands(parameters, context, commands)
        # append -scanner_height
        commands.append(f"-scanner_height {parameters['SCANNER_HEIGHT']}")
        # append -a
        commands.append(f"-a {parameters['ATTENUATION_COEFFICIENT']}")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"command": commands}

    def createInstance(self):
        return LasIntensityAttenuationFactor()

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

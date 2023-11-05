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
__date__ = 'October 2023'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterNumber

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm


class LasIntensity(LAStoolsAlgorithm):
    SHORT_HELP_STRING = """
    ** Description
    This tool corrects the intensity attenuation due to atmospheric absorption. 
    Because the light has to travel longer distances for points with large scan angles, 
    these points may be detected with reduced intensities.
    
    In order to get a reliant attenuation estimate several parameters are essential:
    - Scanner height above ground level (AGL) [km]
    - Scanner wavelength [µm]
    - Atmospheric visibility range [km]
    """
    SHORT_DESCRIPTION = "corrects the intensity attenuation due to atmospheric absorption."
    URL_HELP_PATH = "https://downloads.rapidlasso.de/readme/lasintensity_README.md"
    SCANNER_HEIGHT = "SCANNER_HEIGHT"
    ATMOSPHERIC_VISIBILITY_RANGE = "ATMOSPHERIC_VISIBILITY_RANGE"
    LASER_WAVELENGTH = "LASER_WAVELENGTH"

    def initAlgorithm(self, config=None):
        # input verbose ans gui
        self.addParametersVerboseGUI()
        # input las file
        self.addParametersPointInputGUI()
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
        self.addParametersAdditionalGUI()
        self.helpUrl()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasintensity64")]
        # append -v and -gui
        self.addParametersVerboseCommands(parameters, context, commands)
        # append -i
        self.addParametersPointInputCommands(parameters, context, commands)
        # append -scanner_height
        scanner_height = self.parameterAsDouble(
            parameters, LasIntensity.SCANNER_HEIGHT, context
        )
        commands.append(f"-scanner_height {scanner_height} ")

        # append -av
        atmospheric_visibility_range = self.parameterAsDouble(
            parameters, LasIntensity.ATMOSPHERIC_VISIBILITY_RANGE, context
        )
        commands.append(f"-av {atmospheric_visibility_range} ")

        # append -w
        laser_wavelength = self.parameterAsDouble(
            parameters, LasIntensity.LASER_WAVELENGTH, context
        )
        commands.append(f"-w {laser_wavelength} ")

        self.addParametersAdditionalCommands(parameters, context, commands)
        LAStoolsUtils.runLAStools(commands, feedback)
        return {"command": commands}

    def name(self):
        return 'LasIntensity'

    def displayName(self):
        return 'lasintensity'

    def group(self):
        return 'Preprocessing'

    def groupId(self):
        return 'preprocessing'

    def createInstance(self):
        return LasIntensity()

    def helpUrl(self):
        return LasIntensity.URL_HELP_PATH

    def shortHelpString(self):
        return self.translatable_string(LasIntensity.SHORT_HELP_STRING)

    def shortDescription(self):
        return LasIntensity.SHORT_DESCRIPTION


class LasIntensityAttenuationFactor(LAStoolsAlgorithm):
    SHORT_HELP_STRING = """
    ** Description
    This tool corrects the intensity attenuation due to atmospheric absorption. 
    Because the light has to travel longer distances for points with large scan angles, 
    these points may be detected with reduced intensities.

    In order to get a reliant attenuation estimate several parameters are essential:
    - Scanner height above ground level (AGL) [km]
    - Absorption coefficient [km^-1]
    """
    SHORT_DESCRIPTION = "corrects the intensity attenuation due to atmospheric absorption."
    URL_HELP_PATH = "https://downloads.rapidlasso.de/readme/lasintensity_README.md"
    SCANNER_HEIGHT = "SCANNER_HEIGHT"
    ATTENUATION_COEFFICIENT = "ATTENUATION_COEFFICIENT"

    def initAlgorithm(self, config=None):
        # input verbose ans gui
        self.addParametersVerboseGUI()
        # input las file
        self.addParametersPointInputGUI()
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
        self.addParametersAdditionalGUI()
        self.helpUrl()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasintensity64")]
        # append -v and -gui
        self.addParametersVerboseCommands(parameters, context, commands)
        # append -i
        self.addParametersPointInputCommands(parameters, context, commands)
        # append -scanner_height
        scanner_height = self.parameterAsDouble(
            parameters, LasIntensityAttenuationFactor.SCANNER_HEIGHT, context
        )
        commands.append(f"-scanner_height {scanner_height} ")
        # append -a
        attenuation_coefficient = self.parameterAsDouble(
            parameters, LasIntensityAttenuationFactor.ATTENUATION_COEFFICIENT, context
        )
        commands.append(f"-a {attenuation_coefficient} ")
        self.addParametersAdditionalCommands(parameters, context, commands)
        LAStoolsUtils.runLAStools(commands, feedback)
        return {"command": commands}

    def name(self):
        return 'LasIntensityAttenuationFactor'

    def displayName(self):
        return 'lasintensity (Attenuation Factor)'

    def group(self):
        return 'Preprocessing'

    def groupId(self):
        return 'preprocessing'

    def createInstance(self):
        return LasIntensityAttenuationFactor()

    def helpUrl(self):
        return LasIntensityAttenuationFactor.URL_HELP_PATH

    def shortHelpString(self):
        return self.translatable_string(LasIntensityAttenuationFactor.SHORT_HELP_STRING)

    def shortDescription(self):
        return LasIntensityAttenuationFactor.SHORT_DESCRIPTION

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
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm


class LasIntensity(LAStoolsAlgorithm):
    SHORT_HELP_STRING = """
    ** Description
    This tool corrects the intensity attenuation due to atmospheric absorption. 
    Because the light has to travel longer distances for points with large scan angles, 
    these points may be detected with reduced intensities.
    
    In order to get a reliant attenuation estimate several parameters are essential:
    - Scanner height above ground level (AGL)
    - Scanner wavelength [µm]
    - Absorption coefficient [km^-1]
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
            LasIntensity.ATMOSPHERIC_VISIBILITY_RANGE, "Scanner Altitude in [km]",
            QgsProcessingParameterNumber.Type, 3, False, 0, 10000)
        )
        # atmospheric visibility range
        self.addParameter(QgsProcessingParameterNumber(
            LasIntensity.ATMOSPHERIC_VISIBILITY_RANGE, "Atmospheric Visibility Range in [km]",
            QgsProcessingParameterNumber.Integer, 10, False, 0, 10000)
        )
        # Laser Wavelength
        self.addParameter(QgsProcessingParameterNumber(
            LasIntensity.ATMOSPHERIC_VISIBILITY_RANGE, "Laser Wavelength in [µm]",
            QgsProcessingParameterNumber.Type, 0.905, False, 0, 10000)
        )
        self.addParametersAdditionalGUI()
        self.helpUrl()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasintensity")]
        # append -v and -gui
        self.addParametersVerboseCommands(parameters, context, commands)
        # append -i
        self.addParametersPointInputCommands(parameters, context, commands)
        # append -scanner_height
        scanner_height = self.parameterAsInt(
            parameters, LasIntensity.SCANNER_HEIGHT, context
        )
        commands.append(f"-scanner_height {scanner_height} ")

        # append -av
        scanner_height = self.parameterAsInt(
            parameters, LasIntensity.ATMOSPHERIC_VISIBILITY_RANGE, context
        )
        commands.append(f"-av {scanner_height} ")

        # append -w
        scanner_height = self.parameterAsInt(
            parameters, LasIntensity.LASER_WAVELENGTH, context
        )
        commands.append(f"-w {scanner_height} ")

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

# -*- coding: utf-8 -*-

"""
***************************************************************************
    las3poly.py
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
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm


class Las3PolyRadialDistance(LAStoolsAlgorithm):
    SHORT_HELP_STRING = """
    ** Description
    This tool modifies points within a certain distance of polylines. As an input take, for example, a LAS/LAZ/TXT file and a SHP/TXT file with one or many polylines (e.g. powerlines) by specify a radial distance to the 3D polygon
    
    Affected points can be classified, clipped, or flagged.
    
    The input SHP/TXT file must contain clean polygons or polylines that are free of self-intersections, duplicate points, and/or overlaps and they must all form closed loops (e.g. the last and first point should be identical).
    
    ** Note
       
    line.csv may look like
    
    -10,0,0
    10,0,0
    0,0,0
    0,-10,0
    0,10,0
    [...]
    """
    SHORT_DESCRIPTION = "Modifying points within a certain radial distance of polylines"
    URL_HELP_PATH = "https://downloads.rapidlasso.de/readme/las3dpoly_README.md"
    DISTANCE_RADIAL = "DISTANCE_RADIAL"
    CLASSIFY_AS = {
        "name": 'CLASSIFY_AS',
        "options": ["default", "never classified (0)", "unclassified (1)", "ground (2)", "veg low (3)", "veg mid (4)",
                    "veg high (5)", "buildings (6)", "noise (7)", "keypoint (8)", "water (9)", "rail (10)",
                    "road surface (11)", "overlap (12)"]
    }

    def initAlgorithm(self, config=None):
        # input verbose ans gui
        self.addParametersVerboseGUI()
        # input las file
        self.addParametersPointInputGUI()
        # input shp
        self.addParametersGenericInputGUI(
            "Input polyline(s)/polygons SHP/CSV file", "", False
        )
        # output las
        self.addParametersPointOutputGUI()
        # radial distance
        self.addParameter(QgsProcessingParameterNumber(
            Las3PolyRadialDistance.DISTANCE_RADIAL, "Radial Distance (m)",
            QgsProcessingParameterNumber.Integer, 10, False, 0, 10000)
        )
        # input classify_as
        self.addParameter(QgsProcessingParameterEnum(
            Las3PolyRadialDistance.CLASSIFY_AS['name'], "Classify as",
            Las3PolyRadialDistance.CLASSIFY_AS['options'], False, 0)
        )
        self.addParametersAdditionalGUI()
        self.helpUrl()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las3dpoly")]
        # append -v and -gui
        self.addParametersVerboseCommands(parameters, context, commands)
        # append -i
        self.addParametersPointInputCommands(parameters, context, commands)
        # append poly
        self.addParametersGenericInputCommands(parameters, context, commands, "-poly")
        # append -distance
        distance = self.parameterAsInt(parameters, Las3PolyRadialDistance.DISTANCE_RADIAL, context)
        commands.append(f"-distance {distance} ")
        # append -classify_as
        classify_as = self.parameterAsInt(parameters, Las3PolyRadialDistance.CLASSIFY_AS['name'], context)
        if classify_as != 0:
            commands.append(f"-classify_as {classify_as - 1}")
        # append extra tools
        self.addParametersAdditionalCommands(parameters, context, commands)
        LAStoolsUtils.runLAStools(commands, feedback)
        return {"command": commands}

    def name(self):
        return 'Las3PolyRadialDistance'

    def displayName(self):
        return 'las3poly (Radial Distance)'

    def group(self):
        return 'Preprocessing'

    def groupId(self):
        return 'preprocessing'

    def createInstance(self):
        return Las3PolyRadialDistance()

    def helpUrl(self):
        return Las3PolyRadialDistance.URL_HELP_PATH

    def shortHelpString(self):
        return self.translatable_string(Las3PolyRadialDistance.SHORT_HELP_STRING)

    def shortDescription(self):
        return Las3PolyRadialDistance.SHORT_DESCRIPTION


class Las3PolyHorizontalVerticalDistance(LAStoolsAlgorithm):
    SHORT_HELP_STRING = """
    ** Description
    This tool modifies points within a certain distance of polylines. As an input take, for example, a LAS/LAZ/TXT file and a SHP/TXT file with one or many polylines (e.g. powerlines) by specify a horizontal and vertical distance to the 3D polygon

    Affected points can be classified, clipped, or flagged.

    The input SHP/TXT file must contain clean polygons or polylines that are free of self-intersections, duplicate points, and/or overlaps and they must all form closed loops (e.g. the last and first point should be identical).

    ** Note

    line.csv may look like

    -10,0,0
    10,0,0
    0,0,0
    0,-10,0
    0,10,0
    [...]
    """
    SHORT_DESCRIPTION = "Modifying points within a certain horizontal and vertical distance of polylines"
    URL_HELP_PATH = "https://downloads.rapidlasso.de/readme/las3dpoly_README.md"
    DISTANCE_HORIZONTAL = "DISTANCE_HORIZONTAL"
    DISTANCE_VERTICAL = "DISTANCE_VERTICAL"
    CLASSIFY_AS = {
        "name": 'CLASSIFY_AS',
        "options": ["default", "never classified (0)", "unclassified (1)", "ground (2)", "veg low (3)", "veg mid (4)",
                    "veg high (5)", "buildings (6)", "noise (7)", "keypoint (8)", "water (9)", "rail (10)",
                    "road surface (11)", "overlap (12)"]
    }

    def initAlgorithm(self, config=None):
        # input verbose ans gui
        self.addParametersVerboseGUI()
        # input las file
        self.addParametersPointInputGUI()
        # input shp
        self.addParametersGenericInputGUI(
            "Input polyline(s)/polygons SHP/CSV file", "", False
        )
        # output las
        self.addParametersPointOutputGUI()
        # horizontal and vertical distance
        self.addParameter(QgsProcessingParameterNumber(
            Las3PolyHorizontalVerticalDistance.DISTANCE_VERTICAL, "Vertical Distance (m)",
            QgsProcessingParameterNumber.Integer, 10, False, 0, 10000)
        )
        self.addParameter(QgsProcessingParameterNumber(
            Las3PolyHorizontalVerticalDistance.DISTANCE_HORIZONTAL, "Horizontal Distance (m)",
            QgsProcessingParameterNumber.Integer, 10, False, 0, 10000)
        )
        # input classify_as
        self.addParameter(QgsProcessingParameterEnum(
            Las3PolyHorizontalVerticalDistance.CLASSIFY_AS['name'], "Classify as",
            Las3PolyHorizontalVerticalDistance.CLASSIFY_AS['options'], False, 0)
        )
        self.addParametersAdditionalGUI()
        self.helpUrl()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las3dpoly")]
        # append -v and -gui
        self.addParametersVerboseCommands(parameters, context, commands)
        # append -i
        self.addParametersPointInputCommands(parameters, context, commands)
        # append poly
        self.addParametersGenericInputCommands(parameters, context, commands, "-poly")
        # append -distance
        distance_vertical = self.parameterAsInt(parameters, Las3PolyHorizontalVerticalDistance.DISTANCE_VERTICAL, context)
        distance_horizontal = self.parameterAsInt(parameters, Las3PolyHorizontalVerticalDistance.DISTANCE_VERTICAL, context)
        commands.append(f"-distance {distance_vertical} {distance_horizontal} ")
        # append -classify_as
        classify_as = self.parameterAsInt(parameters, Las3PolyHorizontalVerticalDistance.CLASSIFY_AS['name'], context)
        if classify_as != 0:
            commands.append(f"-classify_as {classify_as - 1}")
        # append extra tools
        self.addParametersAdditionalCommands(parameters, context, commands)
        LAStoolsUtils.runLAStools(commands, feedback)
        return {"command": commands}

    def name(self):
        return 'Las3PolyHorizontalVerticalDistance'

    def displayName(self):
        return 'las3poly (Horizontal and Vertical Distance)'

    def group(self):
        return 'Preprocessing'

    def groupId(self):
        return 'preprocessing'

    def createInstance(self):
        return Las3PolyHorizontalVerticalDistance()

    def helpUrl(self):
        return Las3PolyHorizontalVerticalDistance.URL_HELP_PATH

    def shortHelpString(self):
        return self.translatable_string(Las3PolyHorizontalVerticalDistance.SHORT_HELP_STRING)

    def shortDescription(self):
        return Las3PolyHorizontalVerticalDistance.SHORT_DESCRIPTION

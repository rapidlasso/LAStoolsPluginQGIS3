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

from qgis._core import QgsProcessingParameterField, QgsProcessingParameterDefinition
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm


class Las3dPolyRadialDistance(LAStoolsAlgorithm):
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
    SHORT_DESCRIPTION = "Modifies points within a certain radial distance of 3D polylines"
    URL_HELP_PATH = "https://downloads.rapidlasso.de/readme/las3dpoly_README.md"
    DISTANCE_RADIAL = "DISTANCE_RADIAL"
    WEIGHT_FIELD = 'WEIGHT_FIELD'
    INPUT = 'INPUT'
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
            Las3dPolyRadialDistance.DISTANCE_RADIAL, "Radial Distance (m)",
            QgsProcessingParameterNumber.Integer, 10, False, 0, 10000)
        )
        # input classify_as
        self.addParameter(QgsProcessingParameterEnum(
            Las3dPolyRadialDistance.CLASSIFY_AS['name'], "Classify as",
            Las3dPolyRadialDistance.CLASSIFY_AS['options'], False, 0)
        )
        weight_field_param = QgsProcessingParameterField(self.WEIGHT_FIELD,
                                                         self.translatable_string('Weight from field'),
                                                         None,
                                                         self.INPUT,
                                                         QgsProcessingParameterField.Numeric,
                                                         optional=True
                                                         )
        weight_field_param.setFlags(weight_field_param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(weight_field_param)
        self.addParametersAdditionalGUI()
        self.helpUrl()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las3dpoly64")]
        # append -v and -gui
        self.addParametersVerboseCommands(parameters, context, commands)
        # append -i
        self.addParametersPointInputCommands(parameters, context, commands)
        # append poly
        self.addParametersGenericInputCommands(parameters, context, commands, "-poly")
        # append -distance
        distance = self.parameterAsInt(parameters, Las3dPolyRadialDistance.DISTANCE_RADIAL, context)
        commands.append(f"-distance {distance} ")
        # append -classify_as
        classify_as = self.parameterAsInt(parameters, Las3dPolyRadialDistance.CLASSIFY_AS['name'], context)
        if classify_as != 0:
            commands.append(f"-classify_as {classify_as - 1}")
        # append extra tools
        self.addParametersAdditionalCommands(parameters, context, commands)
        LAStoolsUtils.runLAStools(commands, feedback)
        return {"command": commands}

    def name(self):
        return 'Las3dPolyRadialDistance'

    def displayName(self):
        return 'las3dpoly (Radial Distance)'

    def group(self):
        return 'Preprocessing'

    def groupId(self):
        return 'preprocessing'

    def createInstance(self):
        return Las3dPolyRadialDistance()

    def helpUrl(self):
        return Las3dPolyRadialDistance.URL_HELP_PATH

    def shortHelpString(self):
        return self.translatable_string(Las3dPolyRadialDistance.SHORT_HELP_STRING)

    def shortDescription(self):
        return Las3dPolyRadialDistance.SHORT_DESCRIPTION


class Las3dPolyHorizontalVerticalDistance(LAStoolsAlgorithm):
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
    SHORT_DESCRIPTION = "Modifies points within a certain horizontal and vertical distance of 3D polylines"
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
            Las3dPolyHorizontalVerticalDistance.DISTANCE_VERTICAL, "Vertical Distance (m)",
            QgsProcessingParameterNumber.Integer, 10, False, 0, 10000)
        )
        self.addParameter(QgsProcessingParameterNumber(
            Las3dPolyHorizontalVerticalDistance.DISTANCE_HORIZONTAL, "Horizontal Distance (m)",
            QgsProcessingParameterNumber.Integer, 10, False, 0, 10000)
        )
        # input classify_as
        self.addParameter(QgsProcessingParameterEnum(
            Las3dPolyHorizontalVerticalDistance.CLASSIFY_AS['name'], "Classify as",
            Las3dPolyHorizontalVerticalDistance.CLASSIFY_AS['options'], False, 0)
        )
        self.addParametersAdditionalGUI()
        self.helpUrl()

    def processAlgorithm(self, parameters, context, feedback):
        # calling the specific .exe files from source of software
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las3dpoly64")]
        # append -v and -gui
        self.addParametersVerboseCommands(parameters, context, commands)
        # append -i
        self.addParametersPointInputCommands(parameters, context, commands)
        # append poly
        self.addParametersGenericInputCommands(parameters, context, commands, "-poly")
        # append -distance
        distance_vertical = self.parameterAsInt(
            parameters, Las3dPolyHorizontalVerticalDistance.DISTANCE_VERTICAL, context
        )
        distance_horizontal = self.parameterAsInt(
            parameters, Las3dPolyHorizontalVerticalDistance.DISTANCE_VERTICAL, context
        )
        commands.append(f"-distance {distance_vertical} {distance_horizontal} ")
        # append -classify_as
        classify_as = self.parameterAsInt(parameters, Las3dPolyHorizontalVerticalDistance.CLASSIFY_AS['name'], context)
        if classify_as != 0:
            commands.append(f"-classify_as {classify_as - 1}")
        # append extra tools
        self.addParametersAdditionalCommands(parameters, context, commands)
        LAStoolsUtils.runLAStools(commands, feedback)
        return {"command": commands}

    def name(self):
        return 'Las3PolyHorizontalVerticalDistance'

    def displayName(self):
        return 'las3dpoly (Horizontal and Vertical Distance)'

    def group(self):
        return 'Preprocessing'

    def groupId(self):
        return 'preprocessing'

    def createInstance(self):
        return Las3dPolyHorizontalVerticalDistance()

    def helpUrl(self):
        return Las3dPolyHorizontalVerticalDistance.URL_HELP_PATH

    def shortHelpString(self):
        return self.translatable_string(Las3dPolyHorizontalVerticalDistance.SHORT_HELP_STRING)

    def shortDescription(self):
        return Las3dPolyHorizontalVerticalDistance.SHORT_DESCRIPTION

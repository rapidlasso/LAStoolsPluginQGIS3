# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasboundaryPro.py
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
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasboundaryPro(LAStoolsAlgorithm):

    MODE = "MODE"
    MODES = ["points", "spatial index (the *.lax file)", "bounding box", "tile bounding box"]
    CONCAVITY = "CONCAVITY"
    HOLES = "HOLES"
    DISJOINT = "DISJOINT"
    LABELS = "LABELS"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParametersFilter1ReturnClassFlagsGUI()
        self.addParameter(QgsProcessingParameterEnum(lasboundaryPro.MODE, "compute boundary based on", lasboundaryPro.MODES, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasboundaryPro.CONCAVITY, "concavity", QgsProcessingParameterNumber.Double, 50.0, False, 0.0001))
        self.addParameter(QgsProcessingParameterBoolean(lasboundaryPro.HOLES, "interior holes", False))
        self.addParameter(QgsProcessingParameterBoolean(lasboundaryPro.DISJOINT, "disjoint polygon", False))
        self.addParameter(QgsProcessingParameterBoolean(lasboundaryPro.LABELS, "produce labels", False))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersVectorOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasboundary")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersFilter1ReturnClassFlagsCommands(parameters, context, commands)
        mode = self.parameterAsInt(parameters, lasboundaryPro.MODE, context)
        if (mode != 0):
            if (mode == 1):
                commands.append("-use_lax")
            elif (mode == 2):
                commands.append("-use_bb")
            else:
                commands.append("-use_tile_bb")
        else:
            concavity = self.parameterAsDouble(parameters, lasboundaryPro.CONCAVITY, context)
            commands.append("-concavity")
            commands.append(unicode(concavity))
            if (self.parameterAsBool(parameters, lasboundaryPro.HOLES, context)):
                commands.append("-holes")
            if (self.parameterAsBool(parameters, lasboundaryPro.DISJOINT, context)):
                commands.append("-disjoint")
            if (self.parameterAsBool(parameters, lasboundaryPro.LABELS, context)):
                commands.append("-labels")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersVectorOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasboundaryPro'

    def displayName(self):
        return 'lasboundaryPro'

    def group(self):
        return 'folder - vector derivatives'

    def groupId(self):
        return 'folder - vector derivatives'

    def createInstance(self):
        return lasboundaryPro()

# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasthinPro.py
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
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasthinPro(LAStoolsAlgorithm):

    THIN_STEP = "THIN_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["lowest", "random", "highest", "central", "adaptive", "contours", "percentile"]
    THRESHOLD_OR_INTERVAL_OR_PERCENTILE = "THRESHOLD_OR_INTERVAL_OR_PERCENTILE"
    WITHHELD = "WITHHELD"
    CLASSIFY_AS = "CLASSIFY_AS"
    CLASSIFY_AS_CLASS = "CLASSIFY_AS_CLASS"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParametersIgnoreClass1GUI()
        self.addParametersIgnoreClass2GUI()
        self.addParameter(QgsProcessingParameterNumber(lasthinPro.THIN_STEP, "size of grid used for thinning", QgsProcessingParameterNumber.Double, 1.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(lasthinPro.OPERATION, "keep particular point per cell", lasthinPro.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasthinPro.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, "adaptive threshold, contour intervals, or percentile", QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 100.0))
        self.addParameter(QgsProcessingParameterBoolean(lasthinPro.WITHHELD, "mark thinned-away points as withheld", False))
        self.addParameter(QgsProcessingParameterBoolean(lasthinPro.CLASSIFY_AS, "classify surviving points as", False))
        self.addParameter(QgsProcessingParameterNumber(lasthinPro.CLASSIFY_AS_CLASS, "classification code", QgsProcessingParameterNumber.Integer, 8, False, 0, 255))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasthin")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersIgnoreClass1Commands(parameters, context, commands)
        self.addParametersIgnoreClass2Commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, lasthinPro.THIN_STEP, context)
        if (step != 1.0):
            commands.append("-step")
            commands.append(unicode(step))
        operation = self.parameterAsInt(parameters, lasthinPro.OPERATION, context)
        if (operation != 0):
            commands.append("-" + self.OPERATIONS[operation])
        if (operation >= 4):
            commands.append(unicode(self.parameterAsDouble(parameters, lasthinPro.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, context)))
        if (self.parameterAsBool(parameters, lasthinPro.WITHHELD, context)):
            commands.append("-withheld")
        if (self.parameterAsBool(parameters, lasthinPro.CLASSIFY_AS, context)):
            commands.append("-classify_as")
            commands.append(unicode(self.parameterAsInt(parameters, lasthinPro.CLASSIFY_AS_CLASS, context)))
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasthinPro'

    def displayName(self):
        return 'lasthinPro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasthinPro()

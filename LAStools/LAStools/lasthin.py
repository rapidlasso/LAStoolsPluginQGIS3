# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasthin.py
    ---------------------
    Date                 : September 2013, May 2016 and August 2018
    Copyright            : (C) 2013 by Martin Isenburg
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
__date__ = 'September 2013'
__copyright__ = '(C) 2013, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasthin(LAStoolsAlgorithm):

    THIN_STEP = "THIN_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["lowest", "random", "highest", "central", "adaptive", "contours", "percentile"]
    THRESHOLD_OR_INTERVAL_OR_PERCENTILE = "THRESHOLD_OR_INTERVAL_OR_PERCENTILE"
    WITHHELD = "WITHHELD"
    CLASSIFY_AS = "CLASSIFY_AS"
    CLASSIFY_AS_CLASS = "CLASSIFY_AS_CLASS"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParametersIgnoreClass1GUI()
        self.addParametersIgnoreClass2GUI()
        self.addParameter(QgsProcessingParameterNumber(lasthin.THIN_STEP, "size of grid used for thinning", QgsProcessingParameterNumber.Double, 1.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(lasthin.OPERATION, "keep particular point per cell", lasthin.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasthin.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, "adaptive threshold, contour intervals, or percentile", QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 100.0))
        self.addParameter(QgsProcessingParameterBoolean(lasthin.WITHHELD, "mark thinned-away points as withheld", False))
        self.addParameter(QgsProcessingParameterBoolean(lasthin.CLASSIFY_AS, "classify surviving points as", False))
        self.addParameter(QgsProcessingParameterNumber(lasthin.CLASSIFY_AS_CLASS, "classification code", QgsProcessingParameterNumber.Integer, 8, False, 0, 255))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasthin")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersIgnoreClass1Commands(parameters, context, commands)
        self.addParametersIgnoreClass2Commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, lasthin.THIN_STEP, context)
        if (step != 1.0):
            commands.append("-step")
            commands.append(unicode(step))
        operation = self.parameterAsInt(parameters, lasthin.OPERATION, context)
        if (operation != 0):
            commands.append("-" + self.OPERATIONS[operation])
        if (operation >= 4):
            commands.append(unicode(self.parameterAsDouble(parameters, lasthin.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, context)))
        if (self.parameterAsBool(parameters, lasthin.WITHHELD, context)):
            commands.append("-withheld")
        if (self.parameterAsBool(parameters, lasthin.CLASSIFY_AS, context)):
            commands.append("-classify_as")
            commands.append(unicode(self.parameterAsInt(parameters, lasthin.CLASSIFY_AS_CLASS, context)))
        self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasthin'

    def displayName(self):
        return 'lasthin'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lasthin()

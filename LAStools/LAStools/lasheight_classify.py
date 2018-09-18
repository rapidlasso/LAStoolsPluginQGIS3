# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasheight_classify.py
    ---------------------
    Date                 : May 2016 and August 2018
    Copyright            : (C) 2016 by Martin Isenburg
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
__date__ = 'May 2016'
__copyright__ = '(C) 2016, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasheight_classify(LAStoolsAlgorithm):

    REPLACE_Z = "REPLACE_Z"
    CLASSIFY_BELOW = "CLASSIFY_BELOW"
    CLASSIFY_BELOW_HEIGHT = "CLASSIFY_BELOW_HEIGHT"
    CLASSIFY_BETWEEN1 = "CLASSIFY_BETWEEN1"
    CLASSIFY_BETWEEN1_HEIGHT_FROM = "CLASSIFY_BETWEEN1_HEIGHT_FROM"
    CLASSIFY_BETWEEN1_HEIGHT_TO = "CLASSIFY_BETWEEN1_HEIGHT_TO"
    CLASSIFY_BETWEEN2 = "CLASSIFY_BETWEEN2"
    CLASSIFY_BETWEEN2_HEIGHT_FROM = "CLASSIFY_BETWEEN2_HEIGHT_FROM"
    CLASSIFY_BETWEEN2_HEIGHT_TO = "CLASSIFY_BETWEEN2_HEIGHT_TO"
    CLASSIFY_ABOVE = "CLASSIFY_ABOVE"
    CLASSIFY_ABOVE_HEIGHT = "CLASSIFY_ABOVE_HEIGHT"

    CLASSIFY_CLASSES = ["---", "never classified (0)", "unclassified (1)", "ground (2)", "veg low (3)", "veg mid (4)", "veg high (5)", "buildings (6)", "noise (7)", "keypoint (8)", "water (9)", "water (9)", "rail (10)", "road surface (11)", "overlap (12)"]

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParametersIgnoreClass1GUI()
        self.addParametersIgnoreClass2GUI()
        self.addParameter(QgsProcessingParameterBoolean(lasheight_classify.REPLACE_Z, "replace z", False))
        self.addParameter(QgsProcessingParameterEnum(lasheight_classify.CLASSIFY_BELOW, "classify below height as", lasheight_classify.CLASSIFY_CLASSES, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasheight_classify.CLASSIFY_BELOW_HEIGHT, "below height", QgsProcessingParameterNumber.Double, -2.0, False))
        self.addParameter(QgsProcessingParameterEnum(lasheight_classify.CLASSIFY_BETWEEN1,  "classify between height as", lasheight_classify.CLASSIFY_CLASSES, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasheight_classify.CLASSIFY_BETWEEN1_HEIGHT_FROM, "between height ... ", QgsProcessingParameterNumber.Double, 0.5))
        self.addParameter(QgsProcessingParameterNumber(lasheight_classify.CLASSIFY_BETWEEN1_HEIGHT_TO, "... and height", QgsProcessingParameterNumber.Double, 2.0))
        self.addParameter(QgsProcessingParameterEnum(lasheight_classify.CLASSIFY_BETWEEN2, "classify between height as", lasheight_classify.CLASSIFY_CLASSES, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasheight_classify.CLASSIFY_BETWEEN2_HEIGHT_FROM, "between height ...", QgsProcessingParameterNumber.Double, 2.0))
        self.addParameter(QgsProcessingParameterNumber(lasheight_classify.CLASSIFY_BETWEEN2_HEIGHT_TO, "... and height", QgsProcessingParameterNumber.Double, 5.0))
        self.addParameter(QgsProcessingParameterEnum(lasheight_classify.CLASSIFY_ABOVE, "classify above", lasheight_classify.CLASSIFY_CLASSES, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasheight_classify.CLASSIFY_ABOVE_HEIGHT, "classify above height", QgsProcessingParameterNumber.Double, 100.0))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasheight")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersIgnoreClass1Commands(parameters, context, commands)
        self.addParametersIgnoreClass2Commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasheight_classify.REPLACE_Z, context)):
            commands.append("-replace_z")
        classify = self.parameterAsInt(parameters, lasheight_classify.CLASSIFY_BELOW, context)
        if (classify != 0):
            commands.append("-classify_below")
            commands.append(unicode(self.parameterAsDouble(parameters, lasheight_classify.CLASSIFY_BELOW_HEIGHT, context)))
            commands.append(unicode(classify-1))
        classify = self.parameterAsInt(parameters, lasheight_classify.CLASSIFY_BETWEEN1, context)
        if (classify != 0):
            commands.append("-classify_between")
            commands.append(unicode(self.parameterAsDouble(parameters, lasheight_classify.CLASSIFY_BETWEEN1_HEIGHT_FROM, context)))
            commands.append(unicode(self.parameterAsDouble(parameters, lasheight_classify.CLASSIFY_BETWEEN1_HEIGHT_TO, context)))
            commands.append(unicode(classify-1))
        classify = self.parameterAsInt(parameters, lasheight_classify.CLASSIFY_BETWEEN2, context)
        if (classify != 0):
            commands.append("-classify_between")
            commands.append(unicode(self.parameterAsDouble(parameters, lasheight_classify.CLASSIFY_BETWEEN2_HEIGHT_FROM, context)))
            commands.append(unicode(self.parameterAsDouble(parameters, lasheight_classify.CLASSIFY_BETWEEN2_HEIGHT_TO, context)))
            commands.append(unicode(classify-1))
        classify = self.parameterAsInt(parameters, lasheight_classify.CLASSIFY_ABOVE, context)
        if (classify != 0):
            commands.append("-classify_above")
            commands.append(unicode(self.parameterAsDouble(parameters, lasheight_classify.CLASSIFY_ABOVE_HEIGHT, context)))
            commands.append(unicode(classify-1))
        self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasheight_classify'

    def displayName(self):
        return 'lasheight_classify'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lasheight_classify()

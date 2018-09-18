# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2iso.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : September 2013 and August 2018
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from qgis.core import QgsProcessingParameterNumber

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class las2iso(LAStoolsAlgorithm):

    SMOOTH = "SMOOTH"
    ISO_EVERY = "ISO_EVERY"
    SIMPLIFY_LENGTH = "SIMPLIFY_LENGTH"
    SIMPLIFY_AREA = "SIMPLIFY_AREA"
    CLEAN = "CLEAN"

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterNumber(las2iso.SMOOTH, "smooth underlying TIN", QgsProcessingParameterNumber.Integer, 0, False, 0, 10))
        self.addParameter(QgsProcessingParameterNumber(las2iso.ISO_EVERY, "extract isoline with a spacing of", QgsProcessingParameterNumber.Double, 10.0, False, 0.05, 1000.0))
        self.addParameter(QgsProcessingParameterNumber(las2iso.CLEAN, "clean isolines shorter than (0 = do not clean)", QgsProcessingParameterNumber.Double, 0.0, False, 0.0, 100.0))
        self.addParameter(QgsProcessingParameterNumber(las2iso.SIMPLIFY_LENGTH, "simplify segments shorter than (0 = do not simplify)", QgsProcessingParameterNumber.Double, 0.0, False, 0.0, 100.0))
        self.addParameter(QgsProcessingParameterNumber(las2iso.SIMPLIFY_AREA, "simplify segments pairs with area less than (0 = do not simplify)", QgsProcessingParameterNumber.Double, 0.0, False, 0.0, 100.0))
        self.addParametersVectorOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2iso")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        smooth = self.parameterAsInt(parameters, las2iso.SMOOTH, context)
        if (smooth != 0):
            commands.append("-smooth")
            commands.append(unicode(smooth))
        commands.append("-iso_every")
        commands.append(unicode(self.parameterAsDouble(parameters, las2iso.ISO_EVERY, context)))
        clean = self.parameterAsDouble(parameters, las2iso.CLEAN, context)
        if (clean != 0):
            commands.append("-clean")
            commands.append(unicode(clean))
        simplify_length = self.parameterAsDouble(parameters, las2iso.SIMPLIFY_LENGTH, context)
        if (simplify_length != 0):
            commands.append("-simplify_length")
            commands.append(unicode(simplify_length))
        simplify_area = self.parameterAsDouble(parameters, las2iso.SIMPLIFY_AREA, context)
        if (simplify_area != 0):
            commands.append("-simplify_area")
            commands.append(unicode(simplify_area))
        self.addParametersVectorOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'las2iso'

    def displayName(self):
        return 'las2iso'

    def group(self):
        return 'file - vector derivatives'

    def groupId(self):
        return 'file - vector derivatives'

    def createInstance(self):
        return las2iso()

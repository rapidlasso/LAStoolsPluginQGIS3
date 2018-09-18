
# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasheightPro.py
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

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasheightPro(LAStoolsAlgorithm):

    REPLACE_Z = "REPLACE_Z"
    DROP_ABOVE = "DROP_ABOVE"
    DROP_ABOVE_HEIGHT = "DROP_ABOVE_HEIGHT"
    DROP_BELOW = "DROP_BELOW"
    DROP_BELOW_HEIGHT = "DROP_BELOW_HEIGHT"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParametersIgnoreClass1GUI()
        self.addParametersIgnoreClass2GUI()
        self.addParameter(QgsProcessingParameterBoolean(lasheightPro.REPLACE_Z, "replace z", False))
        self.addParameter(QgsProcessingParameterBoolean(lasheightPro.DROP_ABOVE, "drop above", False))
        self.addParameter(QgsProcessingParameterNumber(lasheightPro.DROP_ABOVE_HEIGHT, "drop above height", QgsProcessingParameterNumber.Double, 100.0))
        self.addParameter(QgsProcessingParameterBoolean(lasheightPro.DROP_BELOW, "drop below", False))
        self.addParameter(QgsProcessingParameterNumber(lasheightPro.DROP_BELOW_HEIGHT, "drop below height", QgsProcessingParameterNumber.Double, -2.0))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasheight")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersIgnoreClass1Commands(parameters, context, commands)
        self.addParametersIgnoreClass2Commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasheightPro.REPLACE_Z, context)):
            commands.append("-replace_z")
        if (self.parameterAsBool(parameters, lasheightPro.DROP_ABOVE, context)):
            commands.append("-drop_above")
            commands.append(unicode(self.parameterAsDouble(parameters, lasheightPro.DROP_ABOVE_HEIGHT, context)))
        if (self.parameterAsBool(parameters, lasheightPro.DROP_BELOW, context)):
            commands.append("-drop_below")
            commands.append(unicode(self.parameterAsDouble(parameters, lasheightPro.DROP_BELOW_HEIGHT, context)))
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasheightPro'

    def displayName(self):
        return 'lasheightPro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasheightPro()

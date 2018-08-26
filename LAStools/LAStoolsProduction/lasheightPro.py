
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
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber


class lasheightPro(LAStoolsAlgorithm):

    REPLACE_Z = "REPLACE_Z"
    DROP_ABOVE = "DROP_ABOVE"
    DROP_ABOVE_HEIGHT = "DROP_ABOVE_HEIGHT"
    DROP_BELOW = "DROP_BELOW"
    DROP_BELOW_HEIGHT = "DROP_BELOW_HEIGHT"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasheightPro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParametersIgnoreClass1GUI()
        self.addParametersIgnoreClass2GUI()
        self.addParameter(ParameterBoolean(lasheightPro.REPLACE_Z,
                                           self.tr("replace z"), False))
        self.addParameter(ParameterBoolean(lasheightPro.DROP_ABOVE,
                                           self.tr("drop above"), False))
        self.addParameter(ParameterNumber(lasheightPro.DROP_ABOVE_HEIGHT,
                                          self.tr("drop above height"), None, None, 100.0))
        self.addParameter(ParameterBoolean(lasheightPro.DROP_BELOW,
                                           self.tr("drop below"), False))
        self.addParameter(ParameterNumber(lasheightPro.DROP_BELOW_HEIGHT,
                                          self.tr("drop below height"), None, None, -2.0))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasheight")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersIgnoreClass1Commands(parameters, context, commands)
        self.addParametersIgnoreClass2Commands(parameters, context, commands)
        if self.getParameterValue(lasheightPro.REPLACE_Z):
            commands.append("-replace_z")
        if self.getParameterValue(lasheightPro.DROP_ABOVE):
            commands.append("-drop_above")
            commands.append(unicode(self.getParameterValue(lasheightPro.DROP_ABOVE_HEIGHT)))
        if self.getParameterValue(lasheightPro.DROP_BELOW):
            commands.append("-drop_below")
            commands.append(unicode(self.getParameterValue(lasheightPro.DROP_BELOW_HEIGHT)))
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersPointOutputFormatCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszipPro'

    def displayName(self):
        return 'laszipPro'

    def group(self):
        return 'folder - conversion'

    def groupId(self):
        return 'folder - conversion'

    def createInstance(self):
        return laszipPro()
	

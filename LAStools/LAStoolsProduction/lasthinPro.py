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
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum


class lasthinPro(LAStoolsAlgorithm):

    THIN_STEP = "THIN_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["lowest", "random", "highest", "central", "adaptive", "contours"]
    THRESHOLD_OR_INTERVAL = "THRESHOLD_OR_INTERVAL"
    WITHHELD = "WITHHELD"
    CLASSIFY_AS = "CLASSIFY_AS"
    CLASSIFY_AS_CLASS = "CLASSIFY_AS_CLASS"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasthinPro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParametersIgnoreClass1GUI()
        self.addParametersIgnoreClass2GUI()
        self.addParameter(ParameterNumber(lasthinPro.THIN_STEP,
                                          self.tr("size of grid used for thinning"), 0, None, 1.0))
        self.addParameter(ParameterSelection(lasthinPro.OPERATION,
                                             self.tr("keep particular point per cell"), lasthinPro.OPERATIONS, 0))
        self.addParameter(ParameterNumber(lasthinPro.THRESHOLD_OR_INTERVAL,
                                          self.tr("vertical threshold or contour intervals (only for 'adaptive' or 'contours' thinning)"), 0, None, 0.1))
        self.addParameter(ParameterBoolean(lasthinPro.WITHHELD,
                                           self.tr("mark thinned-away points as withheld"), False))
        self.addParameter(ParameterBoolean(lasthinPro.CLASSIFY_AS,
                                           self.tr("classify surviving points as class"), False))
        self.addParameter(ParameterNumber(lasthinPro.CLASSIFY_AS_CLASS,
                                          self.tr("class"), 0, None, 8))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersPointOutputFormatGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasthin")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersIgnoreClass1Commands(parameters, context, commands)
        self.addParametersIgnoreClass2Commands(parameters, context, commands)
        step = self.getParameterValue(lasthinPro.THIN_STEP)
        if step != 0.0:
            commands.append("-step")
            commands.append(unicode(step))
        operation = self.getParameterValue(lasthinPro.OPERATION)
        if (operation != 0):
            commands.append("-" + self.OPERATIONS[operation])
        if (operation >= 4):
            commands.append(unicode(self.getParameterValue(lasthinPro.THRESHOLD_OR_INTERVAL)))
        if self.getParameterValue(lasthinPro.WITHHELD):
            commands.append("-withheld")
        if self.getParameterValue(lasthinPro.CLASSIFY_AS):
            commands.append("-classify_as")
            commands.append(unicode(self.getParameterValue(lasthinPro.CLASSIFY_AS_CLASS)))
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
	

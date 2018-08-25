# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasboundary.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'


import os
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber


class lasboundary(LAStoolsAlgorithm):

    MODE = "MODE"
    MODES = ["points", "spatial index (the *.lax file)", "bounding box", "tile bounding box"]
    CONCAVITY = "CONCAVITY"
    DISJOINT = "DISJOINT"
    HOLES = "HOLES"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasboundary')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParametersFilter1ReturnClassFlagsGUI()
        self.addParameter(QgsProcessingParameterEnum(lasboundary.MODE,
                                             self.tr("compute boundary based on"), lasboundary.MODES, 0))
        self.addParameter(QgsProcessingParameterNumber(lasboundary.CONCAVITY,
                                          self.tr("concavity"), 0, None, 50.0))
        self.addParameter(QgsProcessingParameterBoolean(lasboundary.HOLES,
                                           self.tr("interior holes"), False))
        self.addParameter(QgsProcessingParameterBoolean(lasboundary.DISJOINT,
                                           self.tr("disjoint polygon"), False))
        self.addParametersVectorOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasboundary")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        self.addParametersFilter1ReturnClassFlagsCommands(parameters, context, commands)
        mode = self.parameterAsInt(parameters, lasboundary.MODE)
        if (mode != 0):
            if (mode == 1):
                commands.append("-use_lax")
            elif (mode == 2):
                commands.append("-use_bb")
            else:
                commands.append("-use_tile_bb")
        else:
            concavity = self.parameterAsInt(parameters, lasboundary.CONCAVITY)
            commands.append("-concavity")
            commands.append(unicode(concavity))
            if self.parameterAsInt(parameters, lasboundary.HOLES):
                commands.append("-holes")
            if self.parameterAsInt(parameters, lasboundary.DISJOINT):
                commands.append("-disjoint")
        self.addParametersVectorOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszip'

    def displayName(self):
        return 'laszip'

    def group(self):
        return 'LAStools'

    def groupId(self):
        return 'LAStools'

    def createInstance(self):
        return laszip()
	
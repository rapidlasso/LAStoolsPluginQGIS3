# -*- coding: utf-8 -*-

"""
***************************************************************************
    lastile.py
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
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber


class lastile(LAStoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    REVERSIBLE = "REVERSIBLE"
    FLAG_AS_WITHHELD = "FLAG_AS_WITHHELD"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lastile')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterNumber(lastile.TILE_SIZE,
                                          self.tr("tile size (side length of square tile)"),
                                          0.0, None, 1000.0))
        self.addParameter(QgsProcessingParameterNumber(lastile.BUFFER,
                                          self.tr("buffer around each tile"),
                                          0.0, None, 25.0))
        self.addParameter(QgsProcessingParameterBoolean(lastile.FLAG_AS_WITHHELD,
                                           self.tr("flag buffer points as 'withheld' for easier removal later"), True))
        self.addParameter(QgsProcessingParameterBoolean(lastile.REVERSIBLE,
                                           self.tr("make tiling reversible (advanced, usually not needed)"), False))
        self.addParametersPointOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lastile")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        tile_size = self.parameterAsInt(parameters, lastile.TILE_SIZE)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsInt(parameters, lastile.BUFFER)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(unicode(buffer))
        if self.parameterAsInt(parameters, lastile.FLAG_AS_WITHHELD):
            commands.append("-flag_as_withheld")
        if self.parameterAsInt(parameters, lastile.REVERSIBLE):
            commands.append("-reversible")
        self.addParametersPointOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszip'

    def displayName(self):
        return 'laszip'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return laszip()
	
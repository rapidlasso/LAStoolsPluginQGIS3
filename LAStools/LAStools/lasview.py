# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasview.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : September 2013
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
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lasview(LAStoolsAlgorithm):

    POINTS = "POINTS"

    SIZE = "SIZE"
    SIZES = ["1024 768", "800 600", "1200 900", "1200 400", "1550 900", "1550 1150"]

    COLORING = "COLORING"
    COLORINGS = ["default", "classification", "elevation1", "elevation2", "intensity", "return", "flightline", "rgb"]

    def initAlgorithm(self, config):
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterNumber(lasview.POINTS, "max number of points sampled", QgsProcessingParameterNumber.Integer, 5000000, False, 100000, 20000000))
        self.addParameter(QgsProcessingParameterEnum(lasview.COLORING, "color by", lasview.COLORINGS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lasview.SIZE,"window size (x y) in pixels", lasview.SIZES, False, 0))
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasview")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        points = self.parameterAsInt(parameters, lasview.POINTS, context)
        commands.append("-points " + unicode(points))
        coloring = self.parameterAsInt(parameters, lasview.COLORING, context)
        if (coloring != 0):
            commands.append("-color_by_" + lasview.COLORINGS[coloring])
        size = self.parameterAsInt(parameters, lasview.SIZE, context)
        if (size != 0):
            commands.append("-win " + lasview.SIZES[size])
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasview'

    def displayName(self):
        return 'lasview'

    def group(self):
        return 'file - checking quality'

    def groupId(self):
        return 'file - checking quality'

    def createInstance(self):
        return lasview()

# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasviewPro.py
    ---------------------
    Date                 : October 2014 and August 2018
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

from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterNumber


class lasviewPro(LAStoolsAlgorithm):

    POINTS = "POINTS"

    SIZE = "SIZE"
    SIZES = ["1024 768", "800 600", "1200 900", "1200 400", "1550 900", "1550 1150"]

    COLORING = "COLORING"
    COLORINGS = ["default", "classification", "elevation1", "elevation2", "intensity", "return", "flightline", "rgb"]

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasviewPro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParametersFilesAreFlightlinesGUI()
        self.addParameter(ParameterNumber(lasviewPro.POINTS,
                                          self.tr("max number of points sampled"), 100000, 20000000, 5000000))
        self.addParameter(ParameterSelection(lasviewPro.COLORING,
                                             self.tr("color by"), lasviewPro.COLORINGS, 0))
        self.addParameter(ParameterSelection(lasviewPro.SIZE,
                                             self.tr("window size (x y) in pixels"), lasviewPro.SIZES, 0))
        self.addParametersAdditionalGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasview")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersFilesAreFlightlinesCommands(parameters, context, commands)
        points = self.getParameterValue(lasviewPro.POINTS)
        commands.append("-points " + unicode(points))
        self.addParametersAdditionalCommands(parameters, context, commands)
        coloring = self.getParameterValue(lasviewPro.COLORING)
        if coloring != 0:
            commands.append("-color_by_" + lasviewPro.COLORINGS[coloring])
        size = self.getParameterValue(lasviewPro.SIZE)
        if size != 0:
            commands.append("-win " + lasviewPro.SIZES[size])

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
	

# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasindex.py
    ---------------------
    Date                 : September 2013, May 2016 and August 2018
    Copyright            : (C) 2013 by rapidlasso GmbH
    Email                : info near rapidlasso point de
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
__copyright__ = '(C) 2013, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterBoolean

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasindex(LastoolsAlgorithm):

    MOBILE_OR_TERRESTRIAL = "MOBILE_OR_TERRESTRIAL"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasindex.APPEND_LAX, "append *.lax file to *.laz file", False))
        self.addParameter(QgsProcessingParameterBoolean(lasindex.MOBILE_OR_TERRESTRIAL, "is mobile or terrestrial LiDAR (not airborne)", False))
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if (LastoolsUtils.has_wine()):
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasindex.APPEND_LAX, context)):
            commands.append("-append")
        if (self.parameterAsBool(parameters, lasindex.MOBILE_OR_TERRESTRIAL, context)):
            commands.append("-tile_size")
            commands.append("10")
            commands.append("-maximum")
            commands.append("-100")
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasindex'

    def displayName(self):
        return 'lasindex'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lasindex()

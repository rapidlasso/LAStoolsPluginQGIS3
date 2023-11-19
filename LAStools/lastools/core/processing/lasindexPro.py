# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasindexPro.py
    ---------------------
    Date                 : October 2014, May 2016 and August 2018
    Copyright            : (C) 2023 by rapidlasso GmbH
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
__date__ = 'October 2014'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterBoolean

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasindexPro(LastoolsAlgorithm):

    MOBILE_OR_TERRESTRIAL = "MOBILE_OR_TERRESTRIAL"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasindexPro.APPEND_LAX, "append *.lax file to *.laz file", False))
        self.addParameter(QgsProcessingParameterBoolean(lasindexPro.MOBILE_OR_TERRESTRIAL, "is mobile or terrestrial LiDAR (not airborne)", False))
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        if (LastoolsUtils.has_wine()):
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasindex")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasindexPro.APPEND_LAX, context)):
            commands.append("-append")
        if (self.parameterAsBool(parameters, lasindexPro.MOBILE_OR_TERRESTRIAL, context)):
            commands.append("-tile_size")
            commands.append("10")
            commands.append("-maximum")
            commands.append("-100")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasindexPro'

    def displayName(self):
        return 'lasindexPro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasindexPro()


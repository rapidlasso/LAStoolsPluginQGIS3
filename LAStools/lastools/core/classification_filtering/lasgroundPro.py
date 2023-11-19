# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasgroundPro.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : April 2014 and August 2018
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasgroundPro(LastoolsAlgorithm):

    NO_BULGE = "NO_BULGE"
    BY_FLIGHTLINE = "BY_FLIGHTLINE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasgroundPro.NO_BULGE, "no triangle bulging during TIN refinement", False))
        self.addParameter(QgsProcessingParameterBoolean(lasgroundPro.BY_FLIGHTLINE, "classify flightlines separately (needs point source IDs populated)", False))
        self.addParameter(QgsProcessingParameterEnum(lasgroundPro.TERRAIN, "terrain type", lasgroundPro.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterEnum(lasgroundPro.GRANULARITY, "preprocessing", lasgroundPro.GRANULARITIES, False, 1))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasgroundPro.NO_BULGE, context)):
            commands.append("-no_bulge")
        if (self.parameterAsBool(parameters, lasgroundPro.BY_FLIGHTLINE, context)):
            commands.append("-by_flightline")
        method = self.parameterAsInt(parameters, lasgroundPro.TERRAIN, context)
        if (method != 2):
            commands.append("-" + lasgroundPro.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, lasgroundPro.GRANULARITY, context)
        if (granularity != 1):
            commands.append("-" + lasgroundPro.GRANULARITIES[granularity])
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasgroundPro'

    def displayName(self):
        return 'lasgroundPro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasgroundPro()

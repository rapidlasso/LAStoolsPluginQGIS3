# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasgroundPro_new.py
    Date                 : May 2016 and August 2018
    Copyright            : (C) 2016 by rapidlasso GmbH
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
__date__ = 'May 2016'
__copyright__ = '(C) 2016 by rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasgroundPro_new(LastoolsAlgorithm):
    TERRAIN = "TERRAIN"
    TERRAINS = ["wilderness", "nature", "town", "city", "metro", "custom"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine", "hyper_fine"]
    STEP = "STEP"
    BULGE = "BULGE"
    SPIKE = "SPIKE"
    DOWN_SPIKE = "DOWN_SPIKE"
    OFFSET = "OFFSET"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(QgsProcessingParameterEnum(lasgroundPro_new.TERRAIN, "terrain type", lasgroundPro_new.TERRAINS, False, 3))
        self.addParameter(QgsProcessingParameterEnum(lasgroundPro_new.GRANULARITY, "preprocessing", lasgroundPro_new.GRANULARITIES, False, 2))
        self.addParameter(QgsProcessingParameterNumber(lasgroundPro_new.STEP, "step (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0, 500.0))
        self.addParameter(QgsProcessingParameterNumber(lasgroundPro_new.BULGE, "bulge (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 2.0, False, 0.0, 25.0))
        self.addParameter(QgsProcessingParameterNumber(lasgroundPro_new.SPIKE, "spike (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 25.0))
        self.addParameter(QgsProcessingParameterNumber(lasgroundPro_new.DOWN_SPIKE, "down spike (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 25.0))
        self.addParameter(QgsProcessingParameterNumber(lasgroundPro_new.OFFSET, "offset (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 0.05, False, 0.0, 1.0))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground_new")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        method = self.parameterAsInt(parameters, lasgroundPro_new.TERRAIN, context)
        if (method == 5):
            commands.append("-step")
            commands.append(unicode(self.parameterAsDouble(parameters, lasgroundPro_new.STEP, context)))
            commands.append("-bulge")
            commands.append(unicode(self.parameterAsDouble(parameters, lasgroundPro_new.BULGE, context)))
            commands.append("-spike")
            commands.append(unicode(self.parameterAsDouble(parameters, lasgroundPro_new.SPIKE, context)))
            commands.append("-spike_down")
            commands.append(unicode(self.parameterAsDouble(parameters, lasgroundPro_new.DOWN_SPIKE, context)))
            commands.append("-offset")
            commands.append(unicode(self.parameterAsDouble(parameters, lasgroundPro_new.OFFSET, context)))
        else:
            commands.append("-" + lasgroundPro_new.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, lasgroundPro_new.GRANULARITY, context)
        if (granularity != 1):
            commands.append("-" + lasgroundPro_new.GRANULARITIES[granularity])
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasgroundPro_new'

    def displayName(self):
        return 'lasgroundPro_new'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasgroundPro_new()

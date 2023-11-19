# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasground_new.py
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

class lasground_new(LastoolsAlgorithm):
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
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(QgsProcessingParameterEnum(lasground_new.TERRAIN, "terrain type", lasground_new.TERRAINS, False, 3))
        self.addParameter(QgsProcessingParameterEnum(lasground_new.GRANULARITY, "preprocessing", lasground_new.GRANULARITIES, False, 2))
        self.addParameter(QgsProcessingParameterNumber(lasground_new.STEP, "step (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 25.0, False, 0.0, 500.0))
        self.addParameter(QgsProcessingParameterNumber(lasground_new.BULGE, "bulge (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 2.0, False, 0.0, 25.0))
        self.addParameter(QgsProcessingParameterNumber(lasground_new.SPIKE, "spike (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 25.0))
        self.addParameter(QgsProcessingParameterNumber(lasground_new.DOWN_SPIKE, "down spike (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 25.0))
        self.addParameter(QgsProcessingParameterNumber(lasground_new.OFFSET, "offset (for 'custom' terrain only)", QgsProcessingParameterNumber.Double, 0.05, False, 0.0, 1.0))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasground_new")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        method = self.parameterAsInt(parameters, lasground_new.TERRAIN, context)
        if (method == 5):
            commands.append("-step")
            commands.append(unicode(self.parameterAsDouble(parameters, lasground_new.STEP, context)))
            commands.append("-bulge")
            commands.append(unicode(self.parameterAsDouble(parameters, lasground_new.BULGE, context)))
            commands.append("-spike")
            commands.append(unicode(self.parameterAsDouble(parameters, lasground_new.SPIKE, context)))
            commands.append("-spike_down")
            commands.append(unicode(self.parameterAsDouble(parameters, lasground_new.DOWN_SPIKE, context)))
            commands.append("-offset")
            commands.append(unicode(self.parameterAsDouble(parameters, lasground_new.OFFSET, context)))
        else:
            commands.append("-" + lasground_new.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, lasground_new.GRANULARITY, context)
        if (granularity != 1):
            commands.append("-" + lasground_new.GRANULARITIES[granularity])
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasground_new'

    def displayName(self):
        return 'lasground_new'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lasground_new()

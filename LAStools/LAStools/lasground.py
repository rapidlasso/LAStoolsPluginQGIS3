# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasground.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class lasground(LAStoolsAlgorithm):

    NO_BULGE = "NO_BULGE"
    BY_FLIGHTLINE = "BY_FLIGHTLINE"
    TERRAIN = "TERRAIN"
    TERRAINS = ["archaeology", "wilderness", "nature", "town", "city", "metro"]
    GRANULARITY = "GRANULARITY"
    GRANULARITIES = ["coarse", "default", "fine", "extra_fine", "ultra_fine"]

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_horizontal_and_vertical_feet_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasground.NO_BULGE, "no triangle bulging during TIN refinement", False))
        self.addParameter(QgsProcessingParameterBoolean(lasground.BY_FLIGHTLINE, "classify flightlines separately (needs point source IDs populated)", False))
        self.addParameter(QgsProcessingParameterEnum(lasground.TERRAIN, "terrain type", lasground.TERRAINS, False, 2))
        self.addParameter(QgsProcessingParameterEnum(lasground.GRANULARITY, "preprocessing", lasground.GRANULARITIES, False, 1))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasground")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_horizontal_and_vertical_feet_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasground.NO_BULGE, context)):
            commands.append("-no_bulge")
        if (self.parameterAsBool(parameters, lasground.BY_FLIGHTLINE, context)):
            commands.append("-by_flightline")
        method = self.parameterAsInt(parameters, lasground.TERRAIN, context)
        if (method != 2):
            commands.append("-" + lasground.TERRAINS[method])
        granularity = self.parameterAsInt(parameters, lasground.GRANULARITY, context)
        if (granularity != 1):
            commands.append("-" + lasground.GRANULARITIES[granularity])
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasground'

    def displayName(self):
        return 'lasground'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lasground()

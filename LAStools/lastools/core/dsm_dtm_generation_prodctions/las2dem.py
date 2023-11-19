# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2dem.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : September 2013 and August 2018
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
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class las2dem(LastoolsAlgorithm):

    ATTRIBUTE = "ATTRIBUTE"
    PRODUCT = "PRODUCT"
    ATTRIBUTES = ["elevation", "slope", "intensity", "rgb", "edge_longest", "edge_shortest"]
    PRODUCTS = ["actual values", "hillshade", "gray", "false"]
    USE_TILE_BB = "USE_TILE_BB"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_step_gui()
        self.addParameter(QgsProcessingParameterEnum(las2dem.ATTRIBUTE, "Attribute", las2dem.ATTRIBUTES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(las2dem.PRODUCT, "Product", las2dem.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterBoolean(las2dem.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False))
        self.add_parameters_raster_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2dem")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_step_commands(parameters, context, commands)
        attribute = self.parameterAsInt(parameters, las2dem.ATTRIBUTE, context)
        if (attribute != 0):
            commands.append("-" + las2dem.ATTRIBUTES[attribute])
        product = self.parameterAsInt(parameters, las2dem.PRODUCT, context)
        if (product != 0):
            commands.append("-" + las2dem.PRODUCTS[product])
        if (self.parameterAsBool(parameters, las2dem.USE_TILE_BB, context)):
            commands.append("-use_tile_bb")
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'las2dem'

    def displayName(self):
        return 'las2dem'

    def group(self):
        return 'file - raster derivatives'

    def groupId(self):
        return 'file - raster derivatives'

    def createInstance(self):
        return las2dem()

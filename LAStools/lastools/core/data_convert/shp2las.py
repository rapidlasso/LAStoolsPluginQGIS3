# -*- coding: utf-8 -*-

"""
***************************************************************************
    shp2las.py
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

__author__ = 'Martin Isenburg'
__date__ = 'September 2013'
__copyright__ = '(C) 2013, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterNumber

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class shp2las(LastoolsAlgorithm):

    SCALE_FACTOR_XY = "SCALE_FACTOR_XY"
    SCALE_FACTOR_Z = "SCALE_FACTOR_Z"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui()
        self.add_parameters_generic_input_gui("Input SHP file", "shp", False)
        self.addParameter(QgsProcessingParameterNumber(shp2las.SCALE_FACTOR_XY, "resolution of x and y coordinate", QgsProcessingParameterNumber.Double, 0.01, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(shp2las.SCALE_FACTOR_Z, "resolution of z coordinate", QgsProcessingParameterNumber.Double, 0.01, False, 0.0))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "shp2las")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-i")
        scale_factor_xy = self.parameterAsDouble(parameters, shp2las.SCALE_FACTOR_XY, context)
        scale_factor_z = self.parameterAsInt(parameters, shp2las.SCALE_FACTOR_Z, context)
        if scale_factor_xy != 0.01 or scale_factor_z != 0.01:
            commands.append("-set_scale_factor")
            commands.append(unicode(scale_factor_xy) + " " + unicode(scale_factor_xy) + " " + unicode(scale_factor_z))
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'shp2las'

    def displayName(self):
        return 'shp2las'

    def group(self):
        return 'file - conversion'

    def groupId(self):
        return 'file - conversion'

    def createInstance(self):
        return shp2las()
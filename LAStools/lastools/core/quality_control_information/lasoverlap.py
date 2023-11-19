# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasoverlap.py
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
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasoverlap(LastoolsAlgorithm):

    CHECK_STEP = "CHECK_STEP"
    ATTRIBUTE = "ATTRIBUTE"
    OPERATION = "OPERATION"
    ATTRIBUTES = ["elevation", "intensity", "number_of_returns", "scan_angle_abs", "density"]
    OPERATIONS = ["lowest", "highest", "average"]
    CREATE_OVERLAP_RASTER = "CREATE_OVERLAP_RASTER"
    CREATE_DIFFERENCE_RASTER = "CREATE_DIFFERENCE_RASTER"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.addParameter(QgsProcessingParameterNumber(lasoverlap.CHECK_STEP, "size of grid used for overlap check", QgsProcessingParameterNumber.Double, 2.0, False, 0.001, 50.0))
        self.addParameter(QgsProcessingParameterEnum(lasoverlap.ATTRIBUTE, "attribute to check", lasoverlap.ATTRIBUTES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lasoverlap.OPERATION, "operation on attribute per cell", lasoverlap.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterBoolean(lasoverlap.CREATE_OVERLAP_RASTER, "create overlap raster", True))
        self.addParameter(QgsProcessingParameterBoolean(lasoverlap.CREATE_DIFFERENCE_RASTER, "create difference raster", True))
        self.add_parameters_raster_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasoverlap")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, lasoverlap.CHECK_STEP, context)
        if (step != 2.0):
            commands.append("-step")
            commands.append(unicode(step))
        commands.append("-values")
        attribute = self.parameterAsInt(parameters, lasoverlap.ATTRIBUTE, context)
        if (attribute != 0):
            commands.append("-" + lasoverlap.ATTRIBUTES[attribute])
        operation = self.parameterAsInt(parameters, lasoverlap.OPERATION, context)
        if (operation != 0):
            commands.append("-" + lasoverlap.OPERATIONS[operation])
        if (not self.parameterAsBool(parameters, lasoverlap.CREATE_OVERLAP_RASTER, context)):
            commands.append("-no_over")
        if (not self.parameterAsBool(parameters, lasoverlap.CREATE_DIFFERENCE_RASTER, context)):
            commands.append("-no_diff")
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasoverlap'

    def displayName(self):
        return 'lasoverlap'

    def group(self):
        return 'file - checking quality'

    def groupId(self):
        return 'file - checking quality'

    def createInstance(self):
        return lasoverlap()

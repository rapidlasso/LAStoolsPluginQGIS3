# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasoverlapPro.py
    ---------------------
    Date                 : October 2014 and August 2018
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
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasoverlapPro(LastoolsAlgorithm):

    CHECK_STEP = "CHECK_STEP"
    ATTRIBUTE = "ATTRIBUTE"
    OPERATION = "OPERATION"
    ATTRIBUTES = ["elevation", "intensity", "number_of_returns", "scan_angle_abs", "density"]
    OPERATIONS = ["lowest", "highest", "average"]
    CREATE_OVERLAP_RASTER = "CREATE_OVERLAP_RASTER"
    CREATE_DIFFERENCE_RASTER = "CREATE_DIFFERENCE_RASTER"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.addParameter(QgsProcessingParameterNumber(lasoverlapPro.CHECK_STEP, "size of grid used for overlap check", QgsProcessingParameterNumber.Double, 2.0, False, 0.001, 50.0))
        self.addParameter(QgsProcessingParameterEnum(lasoverlapPro.ATTRIBUTE, "attribute to check", lasoverlapPro.ATTRIBUTES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lasoverlapPro.OPERATION, "operation on attribute per cell", lasoverlapPro.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterBoolean(lasoverlapPro.CREATE_OVERLAP_RASTER, "create overlap raster", True))
        self.addParameter(QgsProcessingParameterBoolean(lasoverlapPro.CREATE_DIFFERENCE_RASTER, "create difference raster", True))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_raster_output_format_gui()
        self.add_parameters_raster_output_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasoverlap")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, lasoverlapPro.CHECK_STEP, context)
        if (step != 2.0):
            commands.append("-step")
            commands.append(unicode(step))
        commands.append("-values")
        attribute = self.parameterAsInt(parameters, lasoverlapPro.ATTRIBUTE, context)
        if (attribute != 0):
            commands.append("-" + lasoverlapPro.ATTRIBUTES[attribute])
        operation = self.parameterAsInt(parameters, lasoverlapPro.OPERATION, context)
        if (operation != 0):
            commands.append("-" + lasoverlapPro.OPERATIONS[operation])
        if (not self.parameterAsBool(parameters, lasoverlapPro.CREATE_OVERLAP_RASTER, context)):
            commands.append("-no_over")
        if (not self.parameterAsBool(parameters, lasoverlapPro.CREATE_DIFFERENCE_RASTER, context)):
            commands.append("-no_diff")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_raster_output_format_commands(parameters, context, commands)
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasoverlapPro'

    def displayName(self):
        return 'lasoverlapPro'

    def group(self):
        return 'folder - checking quality'

    def groupId(self):
        return 'folder - checking quality'

    def createInstance(self):
        return lasoverlapPro()

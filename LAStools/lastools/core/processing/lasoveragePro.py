# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasoveragePro.py
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
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasoveragePro(LastoolsAlgorithm):

    CHECK_STEP = "CHECK_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify as overlap", "flag as withheld", "remove from output"]

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_horizontal_feet_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.addParameter(QgsProcessingParameterNumber(lasoveragePro.CHECK_STEP, "size of grid used for scan angle check", QgsProcessingParameterNumber.Double, 1.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(lasoveragePro.OPERATION, "mode of operation", lasoveragePro.OPERATIONS, False, 0))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasoverage")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_horizontal_feet_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, lasoveragePro.CHECK_STEP, context)
        if (step != 1.0):
            commands.append("-step")
            commands.append(unicode(step))
        operation = self.parameterAsInt(parameters, lasoveragePro.OPERATION, context)
        if (operation == 1):
            commands.append("-flag_as_withheld")
        elif (operation == 2):
            commands.append("-remove_overage")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasoveragePro'

    def displayName(self):
        return 'lasoveragePro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasoveragePro()

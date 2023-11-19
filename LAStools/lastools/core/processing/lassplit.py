# -*- coding: utf-8 -*-

"""
***************************************************************************
    lassplit.py
    ---------------------
    Date                 : March 2014 and August 2018
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
__date__ = 'March 2014'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lassplit(LastoolsAlgorithm):

    DIGITS = "DIGITS"
    OPERATION = "OPERATION"
    OPERATIONS = ["by_flightline", "by_classification", "by_gps_time_interval", "by_intensity_interval", "by_x_interval", "by_y_interval", "by_z_interval", "by_scan_angle_interval", "by_user_data_interval", "every_x_points", "recover_flightlines"]
    INTERVAL = "INTERVAL"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterNumber(lassplit.DIGITS, "number of digits for file names", QgsProcessingParameterNumber.Integer, 5, False, 2, 10))
        self.addParameter(QgsProcessingParameterEnum(lassplit.OPERATION, "how to split", lassplit.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lassplit.INTERVAL, "interval or number", QgsProcessingParameterNumber.Double, 5.0, False, 0.00001, 100000.0))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lassplit")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        digits = self.parameterAsInt(parameters, lassplit.DIGITS, context)
        if (digits != 5):
            commands.append("-digits")
            commands.append(unicode(digits))
        operation = self.parameterAsInt(parameters, lassplit.OPERATION, context)
        if (operation != 0):
            if operation == 9:
                commands.append("-split")
            else:
                commands.append("-" + lassplit.OPERATIONS[operation])
        if operation > 1 and operation < 10:
            interval = self.parameterAsDouble(parameters, lassplit.INTERVAL, context)
            commands.append(unicode(interval))
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lassplit'

    def displayName(self):
        return 'lassplit'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lassplit()

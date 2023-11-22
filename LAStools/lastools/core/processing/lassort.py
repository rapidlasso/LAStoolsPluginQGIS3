# -*- coding: utf-8 -*-

"""
***************************************************************************
    lassort.py
    ---------------------
    Date                 : November 2023
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

__author__ = 'rapidlasso'
__date__ = 'September 2023'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterBoolean

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm


class lassort(LastoolsAlgorithm):
    BY_GPS_TIME = "BY_GPS_TIME"
    BY_RETURN_NUMBER = "BY_RETURN_NUMBER"
    BY_POINT_SOURCE_ID = "BY_POINT_SOURCE_ID"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(lassort.BY_GPS_TIME, "sort by GPS time", False))
        self.addParameter(QgsProcessingParameterBoolean(lassort.BY_RETURN_NUMBER, "sort by return number", False))
        self.addParameter(QgsProcessingParameterBoolean(lassort.BY_POINT_SOURCE_ID, "sort by point source ID", False))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lassort")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lassort.BY_GPS_TIME, context)):
            commands.append("-gps_time")
        if (self.parameterAsBool(parameters, lassort.BY_RETURN_NUMBER, context)):
            commands.append("-return_number")
        if (self.parameterAsBool(parameters, lassort.BY_POINT_SOURCE_ID, context)):
            commands.append("-point_source")
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lassort'

    def displayName(self):
        return 'lassort'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lassort()

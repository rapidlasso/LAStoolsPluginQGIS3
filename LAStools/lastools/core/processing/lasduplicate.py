# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasduplicate.py
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

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasduplicate(LastoolsAlgorithm):

    LOWEST_Z = "LOWEST_Z"
    HIGHEST_Z = "HIGHEST_Z"
    UNIQUE_XYZ = "UNIQUE_XYZ"
    SINGLE_RETURNS = "SINGLE_RETURNS"
    NEARBY = "NEARBY"
    NEARBY_TOLERANCE = "NEARBY_TOLERANCE"
    RECORD_REMOVED = "RECORD_REMOVED"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasduplicate.LOWEST_Z, "keep duplicate with lowest z coordinate", False))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicate.HIGHEST_Z, "keep duplicate with highest z coordinate", False))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicate.UNIQUE_XYZ, "only remove duplicates in x y and z", False))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicate.SINGLE_RETURNS, "mark surviving duplicate as single return", False))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicate.NEARBY, "keep only one point within specified tolerance ", False))
        self.addParameter(QgsProcessingParameterNumber(lasduplicate.NEARBY_TOLERANCE, "tolerance value", QgsProcessingParameterNumber.Double, 0.02, False, 0.001))
        self.addParameter(QgsProcessingParameterBoolean(lasduplicate.RECORD_REMOVED, "record removed duplicates to LAS/LAZ file", False))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasduplicate")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasduplicate.LOWEST_Z, context)):
            commands.append("-lowest_z")
        if (self.parameterAsBool(parameters, lasduplicate.HIGHEST_Z, context)):
            commands.append("-highest_z")
        if (self.parameterAsBool(parameters, lasduplicate.UNIQUE_XYZ, context)):
            commands.append("-unique_xyz")
        if (self.parameterAsBool(parameters, lasduplicate.SINGLE_RETURNS, context)):
            commands.append("-single_returns")
        if (self.parameterAsBool(parameters, lasduplicate.NEARBY, context)):
            commands.append("-nearby")
            commands.append(unicode(self.parameterAsDouble(parameters, lasduplicate.NEARBY_TOLERANCE, context)))
        if (self.parameterAsBool(parameters, lasduplicate.RECORD_REMOVED, context)):
            commands.append("-record_removed")
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasduplicate'

    def displayName(self):
        return 'lasduplicate'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lasduplicate()

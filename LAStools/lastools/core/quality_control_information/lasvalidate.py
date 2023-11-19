# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasvalidate.py
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

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasvalidate(LastoolsAlgorithm):

    ONE_REPORT_PER_FILE = "ONE_REPORT_PER_FILE"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasvalidate.ONE_REPORT_PER_FILE, "save report to '*_LVS.xml'", False))
        self.add_parameters_generic_output_gui("Output XML file", "xml", True)
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasvalidate")]
        self.add_parameters_point_input_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasvalidate.ONE_REPORT_PER_FILE, context)):
            commands.append("-oxml")
        self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasvalidate'

    def displayName(self):
        return 'lasvalidate'

    def group(self):
        return 'file - checking quality'

    def groupId(self):
        return 'file - checking quality'

    def createInstance(self):
        return lasvalidate()

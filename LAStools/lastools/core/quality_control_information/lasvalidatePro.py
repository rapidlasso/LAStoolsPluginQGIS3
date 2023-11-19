# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasvalidatePro.py
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

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasvalidatePro(LastoolsAlgorithm):

    ONE_REPORT_PER_FILE = "ONE_REPORT_PER_FILE"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasvalidatePro.ONE_REPORT_PER_FILE, "save report to '*_LVS.xml'", False))
        self.add_parameters_generic_output_gui("Output XML file", "xml", True)
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasvalidate")]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasvalidatePro.ONE_REPORT_PER_FILE, context)):
            commands.append("-oxml")
        self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasvalidatePro'

    def displayName(self):
        return 'lasvalidatePro'

    def group(self):
        return 'folder - checking quality'

    def groupId(self):
        return 'folder - checking quality'

    def createInstance(self):
        return lasvalidatePro()

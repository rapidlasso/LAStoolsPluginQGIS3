# -*- coding: utf-8 -*-

"""
***************************************************************************
    laszip.py
    ---------------------
    Date                 : September 2013 and August 2018, August 2018
    Copyright            : (C) 2013 - 2018 by rapidlasso GmbH
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
	
class laszip(LastoolsAlgorithm):

    REPORT_SIZE = "REPORT_SIZE"
    CREATE_LAX = "CREATE_LAX"
    APPEND_LAX = "APPEND_LAX"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(laszip.REPORT_SIZE, "only report size", False))
        self.addParameter(QgsProcessingParameterBoolean(laszip.CREATE_LAX, "create spatial indexing file (*.lax)", False))
        self.addParameter(QgsProcessingParameterBoolean(laszip.APPEND_LAX, "append *.lax into *.laz file", False))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if (LastoolsUtils.has_wine()):
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "laszip.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "laszip")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, laszip.REPORT_SIZE, context):
            commands.append("-size")
        if self.parameterAsBool(parameters, laszip.CREATE_LAX, context):
            commands.append("-lax")
        if self.parameterAsBool(parameters, laszip.APPEND_LAX, context):
            commands.append("-append")
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
		
        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszip'

    def displayName(self):
        return 'laszip'

    def group(self):
        return 'file - conversion'

    def groupId(self):
        return 'file - conversion'

    def createInstance(self):
        return laszip()
	
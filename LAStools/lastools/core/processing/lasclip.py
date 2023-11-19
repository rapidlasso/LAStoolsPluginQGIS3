# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasclip.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasclip(LastoolsAlgorithm):

    INTERIOR = "INTERIOR"
    OPERATION = "OPERATION"
    OPERATIONS = ["clip", "classify"]
    CLASSIFY_AS = "CLASSIFY_AS"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.add_parameters_generic_input_gui("Input polygon(s)", "shp", False)
        self.addParameter(QgsProcessingParameterBoolean(lasclip.INTERIOR, "interior", False))
        self.addParameter(QgsProcessingParameterEnum(lasclip.OPERATION, "what to do with points", lasclip.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasclip.CLASSIFY_AS, "classify as", QgsProcessingParameterNumber.Integer, 12, False, 0, 255))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasclip")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-poly")
        if (self.parameterAsBool(parameters, lasclip.INTERIOR, context)):
            commands.append("-interior")
        operation = self.parameterAsInt(parameters, lasclip.OPERATION, context)
        if operation != 0:
            commands.append("-classify")
            classify_as = self.parameterAsInt(parameters, lasclip.CLASSIFY_AS, context)
            commands.append(unicode(classify_as))
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasclip'

    def displayName(self):
        return 'lasclip'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lasclip()
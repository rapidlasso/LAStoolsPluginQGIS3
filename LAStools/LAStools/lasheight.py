# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasheight.py
    ---------------------
    Date                 : September 2013, May 2016 and August 2018
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

from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class lasheight(LAStoolsAlgorithm):

    REPLACE_Z = "REPLACE_Z"
    DROP_ABOVE = "DROP_ABOVE"
    DROP_ABOVE_HEIGHT = "DROP_ABOVE_HEIGHT"
    DROP_BELOW = "DROP_BELOW"
    DROP_BELOW_HEIGHT = "DROP_BELOW_HEIGHT"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasheight.REPLACE_Z, "replace z", False))
        self.addParameter(QgsProcessingParameterBoolean(lasheight.DROP_ABOVE, "drop above", False))
        self.addParameter(QgsProcessingParameterNumber(lasheight.DROP_ABOVE_HEIGHT, "drop above height", QgsProcessingParameterNumber.Double, 100.0))
        self.addParameter(QgsProcessingParameterBoolean(lasheight.DROP_BELOW, "drop below", False))
        self.addParameter(QgsProcessingParameterNumber(lasheight.DROP_BELOW_HEIGHT, "drop below height", QgsProcessingParameterNumber.Double, -2.0))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasheight")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasheight.REPLACE_Z, context)):
            commands.append("-replace_z")
        if (self.parameterAsBool(parameters, lasheight.DROP_ABOVE, context)):
            commands.append("-drop_above")
            commands.append(unicode(self.parameterAsDouble(parameters, lasheight.DROP_ABOVE_HEIGHT, context)))
        if (self.parameterAsBool(parameters, lasheight.DROP_BELOW, context)):
            commands.append("-drop_below")
            commands.append(unicode(self.parameterAsDouble(parameters, lasheight.DROP_BELOW_HEIGHT, context)))
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasheight'

    def displayName(self):
        return 'lasheight'

    def group(self):
        return 'file - processing points'

    def groupId(self):
        return 'file - processing points'

    def createInstance(self):
        return lasheight()

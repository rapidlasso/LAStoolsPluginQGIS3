
# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasheightPro.py
    ---------------------
    Date                 : October 2014, May 2016 and August 2018
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

from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class lasheightPro(LAStoolsAlgorithm):

    REPLACE_Z = "REPLACE_Z"
    DROP_ABOVE = "DROP_ABOVE"
    DROP_ABOVE_HEIGHT = "DROP_ABOVE_HEIGHT"
    DROP_BELOW = "DROP_BELOW"
    DROP_BELOW_HEIGHT = "DROP_BELOW_HEIGHT"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasheightPro.REPLACE_Z, "replace z", False))
        self.addParameter(QgsProcessingParameterBoolean(lasheightPro.DROP_ABOVE, "drop above", False))
        self.addParameter(QgsProcessingParameterNumber(lasheightPro.DROP_ABOVE_HEIGHT, "drop above height", QgsProcessingParameterNumber.Double, 100.0))
        self.addParameter(QgsProcessingParameterBoolean(lasheightPro.DROP_BELOW, "drop below", False))
        self.addParameter(QgsProcessingParameterNumber(lasheightPro.DROP_BELOW_HEIGHT, "drop below height", QgsProcessingParameterNumber.Double, -2.0))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasheight")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lasheightPro.REPLACE_Z, context)):
            commands.append("-replace_z")
        if (self.parameterAsBool(parameters, lasheightPro.DROP_ABOVE, context)):
            commands.append("-drop_above")
            commands.append(unicode(self.parameterAsDouble(parameters, lasheightPro.DROP_ABOVE_HEIGHT, context)))
        if (self.parameterAsBool(parameters, lasheightPro.DROP_BELOW, context)):
            commands.append("-drop_below")
            commands.append(unicode(self.parameterAsDouble(parameters, lasheightPro.DROP_BELOW_HEIGHT, context)))
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasheightPro'

    def displayName(self):
        return 'lasheightPro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasheightPro()

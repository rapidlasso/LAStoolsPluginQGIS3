# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasnoisePro.py
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
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasnoisePro(LastoolsAlgorithm):

    ISOLATED = "ISOLATED"
    STEP_XY = "STEP_XY"
    STEP_Z = "STEP_Z"
    OPERATION = "OPERATION"
    OPERATIONS = ["classify", "remove"]
    CLASSIFY_AS = "CLASSIFY_AS"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterNumber(lasnoisePro.ISOLATED, "isolated if surrounding cells have only", QgsProcessingParameterNumber.Integer, 5, False, 1))
        self.addParameter(QgsProcessingParameterNumber(lasnoisePro.STEP_XY, "resolution of isolation grid in xy", QgsProcessingParameterNumber.Double, 4.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(lasnoisePro.STEP_Z, "resolution of isolation grid in z", QgsProcessingParameterNumber.Double, 4.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(lasnoisePro.OPERATION, "what to do with isolated points", lasnoisePro.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasnoisePro.CLASSIFY_AS, "classify as", QgsProcessingParameterNumber.Integer, 7, False, 0, 255))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasnoise")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        isolated = self.parameterAsInt(parameters, lasnoisePro.ISOLATED, context)
        commands.append("-isolated")
        commands.append(unicode(isolated))
        step_xy = self.parameterAsDouble(parameters, lasnoisePro.STEP_XY, context)
        commands.append("-step_xy")
        commands.append(unicode(step_xy))
        step_z = self.parameterAsDouble(parameters, lasnoisePro.STEP_Z, context)
        commands.append("-step_z")
        commands.append(unicode(step_z))
        operation = self.parameterAsInt(parameters, lasnoisePro.OPERATION, context)
        if (operation != 0):
            commands.append("-remove_noise")
        else:
            commands.append("-classify_as")
            classify_as = self.parameterAsInt(parameters, lasnoisePro.CLASSIFY_AS, context)
            commands.append(unicode(classify_as))
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasnoisePro'

    def displayName(self):
        return 'lasnoisePro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasnoisePro()

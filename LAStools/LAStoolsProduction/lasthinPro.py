# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasthinPro.py
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
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class lasthinPro(LAStoolsAlgorithm):

    THIN_STEP = "THIN_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["lowest", "random", "highest", "central", "adaptive", "contours", "percentile"]
    THRESHOLD_OR_INTERVAL_OR_PERCENTILE = "THRESHOLD_OR_INTERVAL_OR_PERCENTILE"
    WITHHELD = "WITHHELD"
    CLASSIFY_AS = "CLASSIFY_AS"
    CLASSIFY_AS_CLASS = "CLASSIFY_AS_CLASS"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterNumber(lasthinPro.THIN_STEP, "size of grid used for thinning", QgsProcessingParameterNumber.Double, 1.0, False, 0.0))
        self.addParameter(QgsProcessingParameterEnum(lasthinPro.OPERATION, "keep particular point per cell", lasthinPro.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasthinPro.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, "adaptive threshold, contour intervals, or percentile", QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 100.0))
        self.addParameter(QgsProcessingParameterBoolean(lasthinPro.WITHHELD, "mark thinned-away points as withheld", False))
        self.addParameter(QgsProcessingParameterBoolean(lasthinPro.CLASSIFY_AS, "classify surviving points as", False))
        self.addParameter(QgsProcessingParameterNumber(lasthinPro.CLASSIFY_AS_CLASS, "classification code", QgsProcessingParameterNumber.Integer, 8, False, 0, 255))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasthin")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, lasthinPro.THIN_STEP, context)
        if (step != 1.0):
            commands.append("-step")
            commands.append(unicode(step))
        operation = self.parameterAsInt(parameters, lasthinPro.OPERATION, context)
        if (operation != 0):
            commands.append("-" + self.OPERATIONS[operation])
        if (operation >= 4):
            commands.append(unicode(self.parameterAsDouble(parameters, lasthinPro.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, context)))
        if (self.parameterAsBool(parameters, lasthinPro.WITHHELD, context)):
            commands.append("-withheld")
        if (self.parameterAsBool(parameters, lasthinPro.CLASSIFY_AS, context)):
            commands.append("-classify_as")
            commands.append(unicode(self.parameterAsInt(parameters, lasthinPro.CLASSIFY_AS_CLASS, context)))
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasthinPro'

    def displayName(self):
        return 'lasthinPro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lasthinPro()

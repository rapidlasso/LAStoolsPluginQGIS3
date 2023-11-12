# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasinfoPro.py
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
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber

from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class lasinfoPro(LAStoolsAlgorithm):

    COMPUTE_DENSITY = "COMPUTE_DENSITY"
    REPAIR_BB = "REPAIR_BB"
    REPAIR_COUNTERS = "REPAIR_COUNTERS"
    HISTO1 = "HISTO1"
    HISTO2 = "HISTO2"
    HISTO3 = "HISTO3"
    HISTOGRAM = ["---", "x", "y", "z", "intensity", "classification", "scan_angle", "user_data", "point_source", "gps_time", "X", "Y", "Z", "attribute0", "attribute1", "attribute2"]
    HISTO1_BIN = "HISTO1_BIN"
    HISTO2_BIN = "HISTO2_BIN"
    HISTO3_BIN = "HISTO3_BIN"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasinfoPro.COMPUTE_DENSITY, "compute density", False))
        self.addParameter(QgsProcessingParameterBoolean(lasinfoPro.REPAIR_BB, "repair bounding box", False))
        self.addParameter(QgsProcessingParameterBoolean(lasinfoPro.REPAIR_COUNTERS, "repair counters", False))
        self.addParameter(QgsProcessingParameterEnum(lasinfoPro.HISTO1, "histogram", lasinfoPro.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasinfoPro.HISTO1_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lasinfoPro.HISTO2, "histogram", lasinfoPro.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasinfoPro.HISTO2_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lasinfoPro.HISTO3, "histogram", lasinfoPro.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasinfoPro.HISTO3_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasinfo.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasinfo")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, lasinfoPro.COMPUTE_DENSITY, context):
            commands.append("-cd")
        if self.parameterAsBool(parameters, lasinfoPro.REPAIR_BB, context):
            commands.append("-repair_bb")
        if self.parameterAsBool(parameters, lasinfoPro.REPAIR_COUNTERS, context):
            commands.append("-repair_counters")
        histo = self.parameterAsInt(parameters, lasinfoPro.HISTO1, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(lasinfoPro.HISTOGRAM[histo])
            commands.append(unicode(self.parameterAsDouble(parameters, lasinfoPro.HISTO1_BIN, context)))
        histo = self.parameterAsInt(parameters, lasinfoPro.HISTO2, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(lasinfoPro.HISTOGRAM[histo])
            commands.append(unicode(self.parameterAsDouble(parameters, lasinfoPro.HISTO2_BIN, context)))
        histo = self.parameterAsInt(parameters, lasinfoPro.HISTO3, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(lasinfoPro.HISTOGRAM[histo])
            commands.append(unicode(self.parameterAsDouble(parameters, lasinfoPro.HISTO3_BIN, context)))
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        commands.append("-otxt")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasinfoPro'

    def displayName(self):
        return 'lasinfoPro'

    def group(self):
        return 'folder - checking quality'

    def groupId(self):
        return 'folder - checking quality'

    def createInstance(self):
        return lasinfoPro()

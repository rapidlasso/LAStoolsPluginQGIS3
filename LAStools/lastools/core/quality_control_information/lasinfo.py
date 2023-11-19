# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasinfo.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : September 2013, May 2016, and August 2018
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

class lasinfo(LastoolsAlgorithm):

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
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(lasinfo.COMPUTE_DENSITY, "compute density", False))
        self.addParameter(QgsProcessingParameterBoolean(lasinfo.REPAIR_BB, "repair bounding box", False))
        self.addParameter(QgsProcessingParameterBoolean(lasinfo.REPAIR_COUNTERS, "repair counters", False))
        self.addParameter(QgsProcessingParameterEnum(lasinfo.HISTO1, "histogram", lasinfo.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasinfo.HISTO1_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lasinfo.HISTO2, "histogram", lasinfo.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasinfo.HISTO2_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lasinfo.HISTO3, "histogram", lasinfo.HISTOGRAM, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasinfo.HISTO3_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0))
        self.add_parameters_generic_output_gui("Output ASCII file", "txt", True)
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if (LastoolsUtils.has_wine()):
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasinfo.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasinfo")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, lasinfo.COMPUTE_DENSITY, context):
            commands.append("-cd")
        if self.parameterAsBool(parameters, lasinfo.REPAIR_BB, context):
            commands.append("-repair_bb")
        if self.parameterAsBool(parameters, lasinfo.REPAIR_COUNTERS, context):
            commands.append("-repair_counters")
        histo = self.parameterAsInt(parameters, lasinfo.HISTO1, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(lasinfo.HISTOGRAM[histo])
            commands.append(unicode(self.parameterAsDouble(parameters, lasinfo.HISTO1_BIN, context)))
        histo = self.parameterAsInt(parameters, lasinfo.HISTO2, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(lasinfo.HISTOGRAM[histo])
            commands.append(unicode(self.parameterAsDouble(parameters, lasinfo.HISTO2_BIN, context)))
        histo = self.parameterAsInt(parameters, lasinfo.HISTO3, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(lasinfo.HISTOGRAM[histo])
            commands.append(unicode(self.parameterAsDouble(parameters, lasinfo.HISTO3_BIN, context)))
        self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasinfo'

    def displayName(self):
        return 'lasinfo'

    def group(self):
        return 'file - checking quality'

    def groupId(self):
        return 'file - checking quality'

    def createInstance(self):
        return lasinfo()

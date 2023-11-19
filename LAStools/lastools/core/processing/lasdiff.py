# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasdiff.py
    ---------------------
    Date                 : May 2016 and August 2018
    Copyright            : (C) 2016 by rapidlasso GmbH
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
__date__ = 'May 2016'
__copyright__ = '(C) 2016, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasdiff(LastoolsAlgorithm):

    CREATE_DIFFERENCE_FILE = "CREATE_DIFFERENCE_FILE"
    SHUTUP = "SHUTUP"
    SHUTUP_AFTER = ["5", "10", "50", "100", "1000", "10000", "50000"]

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.add_parameters_generic_input_gui("other input LAS/LAZ file", "laz", False)
        self.addParameter(QgsProcessingParameterEnum(lasdiff.SHUTUP, "stop reporting difference after this many points", lasdiff.SHUTUP_AFTER, False, 0))
        self.addParameter(QgsProcessingParameterBoolean(lasdiff.CREATE_DIFFERENCE_FILE, "create elevation difference file (if points are in the same order)", False))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if (LastoolsUtils.has_wine()):
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasdiff.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasdiff")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_generic_input_commands(parameters, context, commands, "-i")
        shutup = self.parameterAsInt(parameters, lasdiff.SHUTUP, context)
        if (shutup != 0):
            commands.append("-shutup")
            commands.append(lasdiff.SHUTUP_AFTER[shutup])
        if (self.parameterAsBool(parameters, lasdiff.CREATE_DIFFERENCE_FILE, context)):
            self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasdiff'

    def displayName(self):
        return 'lasdiff'

    def group(self):
        return 'file - checking quality'

    def groupId(self):
        return 'file - checking quality'

    def createInstance(self):
        return lasdiff()

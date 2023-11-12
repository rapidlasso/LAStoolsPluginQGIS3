# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasboundary.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber

from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class lasboundary(LAStoolsAlgorithm):

    MODE = "MODE"
    MODES = ["points", "spatial index (the *.lax file)", "bounding box", "tile bounding box"]
    CONCAVITY = "CONCAVITY"
    HOLES = "HOLES"
    DISJOINT = "DISJOINT"
    LABELS = "LABELS"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.addParameter(QgsProcessingParameterEnum(lasboundary.MODE, "compute boundary based on", lasboundary.MODES, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasboundary.CONCAVITY, "concavity", QgsProcessingParameterNumber.Double, 50.0, False, 0.0001))
        self.addParameter(QgsProcessingParameterBoolean(lasboundary.HOLES, "interior holes", False))
        self.addParameter(QgsProcessingParameterBoolean(lasboundary.DISJOINT, "disjoint polygon", False))
        self.addParameter(QgsProcessingParameterBoolean(lasboundary.LABELS, "produce labels", False))
        self.add_parameters_vector_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasboundary")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        mode = self.parameterAsInt(parameters, lasboundary.MODE, context)
        if (mode != 0):
            if (mode == 1):
                commands.append("-use_lax")
            elif (mode == 2):
                commands.append("-use_bb")
            else:
                commands.append("-use_tile_bb")
        else:
            concavity = self.parameterAsDouble(parameters, lasboundary.CONCAVITY, context)
            commands.append("-concavity")
            commands.append(unicode(concavity))
            if (self.parameterAsBool(parameters, lasboundary.HOLES, context)):
                commands.append("-holes")
            if (self.parameterAsBool(parameters, lasboundary.DISJOINT, context)):
                commands.append("-disjoint")
            if (self.parameterAsBool(parameters, lasboundary.LABELS, context)):
                commands.append("-labels")
        self.add_parameters_vector_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasboundary'

    def displayName(self):
        return 'lasboundary'

    def group(self):
        return 'file - vector derivatives'

    def groupId(self):
        return 'file - vector derivatives'

    def createInstance(self):
        return lasboundary()

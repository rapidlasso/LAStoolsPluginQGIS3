# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasboundaryPro.py
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

class lasboundaryPro(LAStoolsAlgorithm):

    MODE = "MODE"
    MODES = ["points", "spatial index (the *.lax file)", "bounding box", "tile bounding box"]
    CONCAVITY = "CONCAVITY"
    HOLES = "HOLES"
    DISJOINT = "DISJOINT"
    LABELS = "LABELS"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.addParameter(QgsProcessingParameterEnum(lasboundaryPro.MODE, "compute boundary based on", lasboundaryPro.MODES, False, 0))
        self.addParameter(QgsProcessingParameterNumber(lasboundaryPro.CONCAVITY, "concavity", QgsProcessingParameterNumber.Double, 50.0, False, 0.0001))
        self.addParameter(QgsProcessingParameterBoolean(lasboundaryPro.HOLES, "interior holes", False))
        self.addParameter(QgsProcessingParameterBoolean(lasboundaryPro.DISJOINT, "disjoint polygon", False))
        self.addParameter(QgsProcessingParameterBoolean(lasboundaryPro.LABELS, "produce labels", False))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_vector_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasboundary")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        mode = self.parameterAsInt(parameters, lasboundaryPro.MODE, context)
        if (mode != 0):
            if (mode == 1):
                commands.append("-use_lax")
            elif (mode == 2):
                commands.append("-use_bb")
            else:
                commands.append("-use_tile_bb")
        else:
            concavity = self.parameterAsDouble(parameters, lasboundaryPro.CONCAVITY, context)
            commands.append("-concavity")
            commands.append(unicode(concavity))
            if (self.parameterAsBool(parameters, lasboundaryPro.HOLES, context)):
                commands.append("-holes")
            if (self.parameterAsBool(parameters, lasboundaryPro.DISJOINT, context)):
                commands.append("-disjoint")
            if (self.parameterAsBool(parameters, lasboundaryPro.LABELS, context)):
                commands.append("-labels")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_vector_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasboundaryPro'

    def displayName(self):
        return 'lasboundaryPro'

    def group(self):
        return 'folder - vector derivatives'

    def groupId(self):
        return 'folder - vector derivatives'

    def createInstance(self):
        return lasboundaryPro()

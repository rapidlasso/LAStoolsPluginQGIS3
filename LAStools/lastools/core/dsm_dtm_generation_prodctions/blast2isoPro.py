# -*- coding: utf-8 -*-

"""
***************************************************************************
    blast2isoPro.py
    ---------------------
    Date                 : October 2014 and August 2018
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
from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

from qgis.core import QgsProcessingParameterNumber


class blast2isoPro(LastoolsAlgorithm):

    SMOOTH = "SMOOTH"
    ISO_EVERY = "ISO_EVERY"
    SIMPLIFY_LENGTH = "SIMPLIFY_LENGTH"
    SIMPLIFY_AREA = "SIMPLIFY_AREA"
    CLEAN = "CLEAN"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_point_input_merged_gui()
        self.addParameter(QgsProcessingParameterNumber(blast2isoPro.SMOOTH, "smooth underlying TIN", QgsProcessingParameterNumber.Integer, 0, False, 0, 10))
        self.addParameter(QgsProcessingParameterNumber(blast2isoPro.ISO_EVERY, "extract isoline with a spacing of", QgsProcessingParameterNumber.Double, 10.0, False, 0.05, 1000.0))
        self.addParameter(QgsProcessingParameterNumber(blast2isoPro.CLEAN, "clean isolines shorter than (0 = do not clean)", QgsProcessingParameterNumber.Double, 0.0, False, 0.0, 100.0))
        self.addParameter(QgsProcessingParameterNumber(blast2isoPro.SIMPLIFY_LENGTH, "simplify segments shorter than (0 = do not simplify)", QgsProcessingParameterNumber.Double, 0.0, False, 0.0, 100.0))
        self.addParameter(QgsProcessingParameterNumber(blast2isoPro.SIMPLIFY_AREA, "simplify segments pairs with area less than (0 = do not simplify)", QgsProcessingParameterNumber.Double, 0.0, False, 0.0, 100.0))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_vector_output_format_gui()
        self.add_parameters_vector_output_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "blast2iso")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_point_input_merged_commands(parameters, context, commands)
        smooth = self.parameterAsInt(parameters, blast2isoPro.SMOOTH, context)
        if (smooth != 0):
            commands.append("-smooth")
            commands.append(unicode(smooth))
        commands.append("-iso_every")
        commands.append(unicode(self.parameterAsDouble(parameters, blast2isoPro.ISO_EVERY, context)))
        clean = self.parameterAsDouble(parameters, blast2isoPro.CLEAN, context)
        if (clean != 0.0):
            commands.append("-clean")
            commands.append(unicode(clean))
        simplify_length = self.parameterAsDouble(parameters, blast2isoPro.SIMPLIFY_LENGTH, context)
        if (simplify_length != 0.0):
            commands.append("-simplify_length")
            commands.append(unicode(simplify_length))
        simplify_area = self.parameterAsDouble(parameters, blast2isoPro.SIMPLIFY_AREA, context)
        if (simplify_area != 0.0):
            commands.append("-simplify_area")
            commands.append(unicode(simplify_area))
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_vector_output_format_commands(parameters, context, commands)
        self.add_parameters_vector_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'blast2isoPro'

    def displayName(self):
        return 'blast2isoPro'

    def group(self):
        return 'folder - vector derivatives'

    def groupId(self):
        return 'folder - vector derivatives'

    def createInstance(self):
        return blast2isoPro()

# -*- coding: utf-8 -*-

"""
***************************************************************************
    lastilePro.py
    ---------------------
    Date                 : April 2014 and May 2016
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
__date__ = 'April 2014'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterString

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lastilePro(LastoolsAlgorithm):

    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    FLAG_AS_WITHHELD = "FLAG_AS_WITHHELD"
    EXTRA_PASS = "EXTRA_PASS"
    BASE_NAME = "BASE_NAME"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.add_parameters_apply_file_source_id_gui()
        self.addParameter(QgsProcessingParameterNumber(lastilePro.TILE_SIZE, "tile size (side length of square tile)", QgsProcessingParameterNumber.Double, 1000.0, False, 4.0, 10000.0))
        self.addParameter(QgsProcessingParameterNumber(lastilePro.BUFFER, "buffer around each tile", QgsProcessingParameterNumber.Double, 30.0, False, 0.0, 100.0))
        self.addParameter(QgsProcessingParameterBoolean(lastilePro.FLAG_AS_WITHHELD, "flag buffer points as 'withheld' for easier removal later", True))
        self.addParameter(QgsProcessingParameterBoolean(lastilePro.EXTRA_PASS, "more than 2000 output tiles", False))
        self.add_parameters_output_directory_gui()
        self.addParameter(QgsProcessingParameterString(lastilePro.BASE_NAME, "tile base name (using sydney.laz creates sydney_274000_4714000.laz)",""))
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lastile")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        self.add_parameters_apply_file_source_id_commands(parameters, context, commands)
        tile_size = self.parameterAsInt(parameters, lastilePro.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(unicode(tile_size))
        buffer = self.parameterAsDouble(parameters, lastilePro.BUFFER, context)
        if (buffer != 0.0):
            commands.append("-buffer")
            commands.append(unicode(buffer))
        if (self.parameterAsBool(parameters, lastilePro.FLAG_AS_WITHHELD, context)):
            commands.append("-flag_as_withheld")
        if (self.parameterAsBool(parameters, lastilePro.EXTRA_PASS, context)):
            commands.append("-extra_pass")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        base_name = self.parameterAsString(parameters, lastilePro.BASE_NAME, context)
        if (base_name != ""):
            commands.append("-o")
            commands.append('"' + base_name + '"')
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lastilePro'

    def displayName(self):
        return 'lastilePro'

    def group(self):
        return 'folder - conversion'

    def groupId(self):
        return 'folder - conversion'

    def createInstance(self):
        return lastilePro()

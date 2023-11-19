# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2lasPro_transform.py
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

from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterEnum

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class las2lasPro_transform(LastoolsAlgorithm):

    OPERATION = "OPERATION"
    OPERATIONS = ["---", "set_point_type", "set_point_size", "set_version_minor", "set_version_major", "start_at_point", "stop_at_point", "remove_vlr", "week_to_adjusted", "adjusted_to_week", "auto_reoffset", "scale_rgb_up", "scale_rgb_down", "remove_all_vlrs", "remove_extra", "clip_to_bounding_box"]
    OPERATIONARG = "OPERATIONARG"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_transform1_coordinate_gui()
        self.add_parameters_transform2_coordinate_gui()
        self.add_parameters_transform1_other_gui()
        self.add_parameters_transform2_other_gui()
        self.addParameter(QgsProcessingParameterEnum(las2lasPro_transform.OPERATION, "operations (first 8 need an argument)", las2lasPro_transform.OPERATIONS, False, 0))
        self.addParameter(QgsProcessingParameterString(las2lasPro_transform.OPERATIONARG, "argument for operation"))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        if (LastoolsUtils.has_wine()):
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_transform1_coordinate_commands(parameters, context, commands)
        self.add_parameters_transform2_coordinate_commands(parameters, context, commands)
        self.add_parameters_transform1_other_commands(parameters, context, commands)
        self.add_parameters_transform2_other_commands(parameters, context, commands)
        operation = self.parameterAsInt(parameters, las2lasPro_transform.OPERATION, context)
        if (operation != 0):
            commands.append("-" + las2lasPro_transform.OPERATIONS[operation])
            if (operation > 8):
                commands.append(self.parameterAsString(parameters, las2lasPro_transform.OPERATIONARG, context))
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'las2lasPro_transform'

    def displayName(self):
        return 'las2lasPro_transform'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return las2lasPro_transform()
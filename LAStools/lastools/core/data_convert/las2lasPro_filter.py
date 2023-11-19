# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2lasPro_filter.py
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

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class las2lasPro_filter(LastoolsAlgorithm):

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_filter2_return_class_flags_gui()
        self.add_parameters_filter1_coords_intensity_gui()
        self.add_parameters_filter2_coords_intensity_gui()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if (LastoolsUtils.has_wine()):
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2las")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_filter2_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_filter1_coords_intensity_commands(parameters, context, commands)
        self.add_parameters_filter2_coords_intensity_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'las2lasPro_filter'

    def displayName(self):
        return 'las2lasPro_filter'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return las2lasPro_filter()

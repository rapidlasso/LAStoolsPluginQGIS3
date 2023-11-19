# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasmergePro.py
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

class lasmergePro(LastoolsAlgorithm):

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.add_parameters_apply_file_source_id_gui()
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        if (LastoolsUtils.has_wine()):
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasmerge.exe")]
        else:
            commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasmerge")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        self.add_parameters_apply_file_source_id_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasmergePro'

    def displayName(self):
        return 'lasmergePro'

    def group(self):
        return 'folder - conversion'

    def groupId(self):
        return 'folder - conversion'

    def createInstance(self):
        return lasmergePro()

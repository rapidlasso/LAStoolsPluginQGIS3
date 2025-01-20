# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2tin.py
    ---------------------
    Date                 : January 2025
    Copyright            : (c) 2025 by rapidlasso GmbH
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

__author__ = "rapidlasso"
__date__ = "January 2025"
__copyright__ = "(c) 2025, rapidlasso GmbH"

import os
from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm


class las2tin(LastoolsAlgorithm):
    LASTOOL = "las2tin"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_vector_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_vector_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return self.LASTOOL

    def displayName(self):
        return self.LASTOOL

    def group(self):
        return "file - vector derivatives"

    def groupId(self):
        return "file - vector derivatives"

    def createInstance(self):
        return las2tin()

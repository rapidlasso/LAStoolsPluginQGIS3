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


from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm
from lastools.core.utils.utils import LastoolsUtils


class las2tin(LastoolsAlgorithm):
    LASTOOL = "las2tin"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_verbose_64_gui()
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_vector_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_vector_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

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

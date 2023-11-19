# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasprecision.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : September 2013 and August 2018
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

from lastools.core.utils.utils import LastoolsUtils
from lastools.core.algo.lastools_algorithm import LastoolsAlgorithm

class lasprecision(LastoolsAlgorithm):

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui()
        self.add_parameters_point_input_gui()
        self.add_parameters_generic_output_gui("Output ASCII file", "txt", True)
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasprecision")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasprecision'

    def displayName(self):
        return 'lasprecision'

    def group(self):
        return 'file - checking quality'

    def groupId(self):
        return 'file - checking quality'

    def createInstance(self):
        return lasprecision()

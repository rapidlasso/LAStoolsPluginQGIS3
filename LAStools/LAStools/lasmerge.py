# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasmerge.py
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

__author__ = 'Martin Isenburg'
__date__ = 'September 2013'
__copyright__ = '(C) 2013, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterFile

from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class lasmerge(LAStoolsAlgorithm):

    FILE2 = "FILE2"
    FILE3 = "FILE3"
    FILE4 = "FILE4"
    FILE5 = "FILE5"
    FILE6 = "FILE6"
    FILE7 = "FILE7"

    def initAlgorithm(self, config):
        self.add_parameters_verbose_gui64()
        self.add_parameters_files_are_flightlines_gui()
        self.add_parameters_apply_file_source_id_gui()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE2, "2nd file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE3, "3rd file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE4, "4th file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE5, "5th file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE6, "6th file", QgsProcessingParameterFile.File, "laz", None, True))
        self.addParameter(QgsProcessingParameterFile(lasmerge.FILE7, "7th file", QgsProcessingParameterFile.File, "laz", None, True))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasmerge.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasmerge")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        file2 = self.parameterAsString(parameters, lasmerge.FILE2, context)
        if file2 != '':
            commands.append("-i")
            commands.append(file2)
        file3 = self.parameterAsString(parameters, lasmerge.FILE3, context)
        if file3 != '':
            commands.append("-i")
            commands.append(file3)
        file4 = self.parameterAsString(parameters, lasmerge.FILE4, context)
        if file4 != '':
            commands.append("-i")
            commands.append(file4)
        file5 = self.parameterAsString(parameters, lasmerge.FILE5, context)
        if file5 != '':
            commands.append("-i")
            commands.append(file5)
        file6 = self.parameterAsString(parameters, lasmerge.FILE6, context)
        if file6 != '':
            commands.append("-i")
            commands.append(file6)
        file7 = self.parameterAsString(parameters, lasmerge.FILE7, context)
        if file7 != '':
            commands.append("-i")
            commands.append(file7)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        self.add_parameters_apply_file_source_id_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasmerge'

    def displayName(self):
        return 'lasmerge'

    def group(self):
        return 'file - conversion'

    def groupId(self):
        return 'file - conversion'

    def createInstance(self):
        return lasmerge()

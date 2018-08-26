# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasinfoPro.py
    ---------------------
    Date                 : October 2014, May 2016 and August 2018
    Copyright            : (C) 2014 by Martin Isenburg
    Email                : martin near rapidlasso point com
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
__copyright__ = '(C) 2014, Martin Isenburg'

import os
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber


class lasinfoPro(LAStoolsAlgorithm):

    COMPUTE_DENSITY = "COMPUTE_DENSITY"
    REPAIR_BB = "REPAIR_BB"
    REPAIR_COUNTERS = "REPAIR_COUNTERS"
    HISTO1 = "HISTO1"
    HISTO2 = "HISTO2"
    HISTO3 = "HISTO3"
    HISTOGRAM = ["---", "x", "y", "z", "intensity", "classification", "scan_angle", "user_data", "point_source", "gps_time", "X", "Y", "Z"]
    HISTO1_BIN = "HISTO1_BIN"
    HISTO2_BIN = "HISTO2_BIN"
    HISTO3_BIN = "HISTO3_BIN"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('lasinfoPro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParameter(ParameterBoolean(lasinfoPro.COMPUTE_DENSITY,
                                           self.tr("compute density"), False))
        self.addParameter(ParameterBoolean(lasinfoPro.REPAIR_BB,
                                           self.tr("repair bounding box"), False))
        self.addParameter(ParameterBoolean(lasinfoPro.REPAIR_COUNTERS,
                                           self.tr("repair counters"), False))
        self.addParameter(ParameterSelection(lasinfoPro.HISTO1,
                                             self.tr("histogram"), lasinfoPro.HISTOGRAM, 0))
        self.addParameter(ParameterNumber(lasinfoPro.HISTO1_BIN,
                                          self.tr("bin size"), 0, None, 1.0))
        self.addParameter(ParameterSelection(lasinfoPro.HISTO2,
                                             self.tr("histogram"), lasinfoPro.HISTOGRAM, 0))
        self.addParameter(ParameterNumber(lasinfoPro.HISTO2_BIN,
                                          self.tr("bin size"), 0, None, 1.0))
        self.addParameter(ParameterSelection(lasinfoPro.HISTO3,
                                             self.tr("histogram"), lasinfoPro.HISTOGRAM, 0))
        self.addParameter(ParameterNumber(lasinfoPro.HISTO3_BIN,
                                          self.tr("bin size"), 0, None, 1.0))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        if (LAStoolsUtils.hasWine()):
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasinfo.exe")]
        else:
            commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasinfo")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        if self.getParameterValue(lasinfoPro.COMPUTE_DENSITY):
            commands.append("-cd")
        if self.getParameterValue(lasinfoPro.REPAIR_BB):
            commands.append("-repair_bb")
        if self.getParameterValue(lasinfoPro.REPAIR_COUNTERS):
            commands.append("-repair_counters")
        histo = self.getParameterValue(lasinfoPro.HISTO1)
        if histo != 0:
            commands.append("-histo")
            commands.append(lasinfoPro.HISTOGRAM[histo])
            commands.append(unicode(self.getParameterValue(lasinfoPro.HISTO1_BIN)))
        histo = self.getParameterValue(lasinfoPro.HISTO2)
        if histo != 0:
            commands.append("-histo")
            commands.append(lasinfoPro.HISTOGRAM[histo])
            commands.append(unicode(self.getParameterValue(lasinfoPro.HISTO2_BIN)))
        histo = self.getParameterValue(lasinfoPro.HISTO3)
        if histo != 0:
            commands.append("-histo")
            commands.append(lasinfoPro.HISTOGRAM[histo])
            commands.append(unicode(self.getParameterValue(lasinfoPro.HISTO3_BIN)))
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        commands.append("-otxt")
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszipPro'

    def displayName(self):
        return 'laszipPro'

    def group(self):
        return 'folder - conversion'

    def groupId(self):
        return 'folder - conversion'

    def createInstance(self):
        return laszipPro()
	

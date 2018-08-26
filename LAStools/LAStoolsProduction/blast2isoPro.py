# -*- coding: utf-8 -*-

"""
***************************************************************************
    blast2isoPro.py
    ---------------------
    Date                 : October 2014 and August 2018
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

from qgis.core import QgsProcessingParameterNumber


class blast2isoPro(LAStoolsAlgorithm):

    SMOOTH = "SMOOTH"
    ISO_EVERY = "ISO_EVERY"
    SIMPLIFY_LENGTH = "SIMPLIFY_LENGTH"
    SIMPLIFY_AREA = "SIMPLIFY_AREA"
    CLEAN = "CLEAN"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('blast2isoPro')
        self.group, self.i18n_group = self.trAlgorithm('LAStools Production')
        self.addParametersPointInputFolderGUI()
        self.addParametersPointInputMergedGUI()
        self.addParameter(ParameterNumber(blast2isoPro.SMOOTH,
                                          self.tr("smooth underlying TIN"), 0, None, 0))
        self.addParameter(ParameterNumber(blast2isoPro.ISO_EVERY,
                                          self.tr("extract isoline with a spacing of"), 0, None, 10.0))
        self.addParameter(ParameterNumber(blast2isoPro.CLEAN,
                                          self.tr("clean isolines shorter than (0 = do not clean)"),
                                          None, None, 0.0))
        self.addParameter(ParameterNumber(blast2isoPro.SIMPLIFY_LENGTH,
                                          self.tr("simplify segments shorter than (0 = do not simplify)"),
                                          None, None, 0.0))
        self.addParameter(ParameterNumber(blast2isoPro.SIMPLIFY_AREA,
                                          self.tr("simplify segments pairs with area less than (0 = do not simplify)"),
                                          None, None, 0.0))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersVectorOutputFormatGUI()
        self.addParametersVectorOutputGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "blast2iso")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersPointInputMergedCommands(parameters, context, commands)
        smooth = self.getParameterValue(blast2isoPro.SMOOTH)
        if smooth != 0:
            commands.append("-smooth")
            commands.append(unicode(smooth))
        commands.append("-iso_every")
        commands.append(unicode(self.getParameterValue(blast2isoPro.ISO_EVERY)))
        simplify_length = self.getParameterValue(blast2isoPro.SIMPLIFY_LENGTH)
        if simplify_length != 0:
            commands.append("-simplify_length")
            commands.append(unicode(simplify_length))
        simplify_area = self.getParameterValue(blast2isoPro.SIMPLIFY_AREA)
        if simplify_area != 0:
            commands.append("-simplify_area")
            commands.append(unicode(simplify_area))
        clean = self.getParameterValue(blast2isoPro.CLEAN)
        if clean != 0:
            commands.append("-clean")
            commands.append(unicode(clean))
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersVectorOutputFormatCommands(parameters, context, commands)
        self.addParametersVectorOutputCommands(parameters, context, commands)
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
	

# -*- coding: utf-8 -*-

"""
***************************************************************************
    las2iso.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : September 2013 and August 2018
    Copyright            : (C) 2013 by Martin Isenburg
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

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'


import os
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterNumber


class las2iso(LAStoolsAlgorithm):

    SMOOTH = "SMOOTH"
    ISO_EVERY = "ISO_EVERY"
    SIMPLIFY_LENGTH = "SIMPLIFY_LENGTH"
    SIMPLIFY_AREA = "SIMPLIFY_AREA"
    CLEAN = "CLEAN"

    def initAlgorithm(self, config):
        self.name, self.i18n_name = self.trAlgorithm('las2iso')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterNumber(las2iso.SMOOTH,
                                          self.tr("smooth underlying TIN"), 0, None, 0))
        self.addParameter(QgsProcessingParameterNumber(las2iso.ISO_EVERY,
                                          self.tr("extract isoline with a spacing of"), 0, None, 10.0))
        self.addParameter(QgsProcessingParameterNumber(las2iso.CLEAN,
                                          self.tr("clean isolines shorter than (0 = do not clean)"),
                                          None, None, 0.0))
        self.addParameter(QgsProcessingParameterNumber(las2iso.SIMPLIFY_LENGTH,
                                          self.tr("simplify segments shorter than (0 = do not simplify)"),
                                          None, None, 0.0))
        self.addParameter(QgsProcessingParameterNumber(las2iso.SIMPLIFY_AREA,
                                          self.tr("simplify segments pairs with area less than (0 = do not simplify)"),
                                          None, None, 0.0))
        self.addParametersVectorOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "las2iso")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        smooth = self.parameterAsInt(parameters, las2iso.SMOOTH)
        if smooth != 0:
            commands.append("-smooth")
            commands.append(unicode(smooth))
        commands.append("-iso_every")
        commands.append(unicode(self.parameterAsInt(parameters, las2iso.ISO_EVERY)))
        simplify_length = self.parameterAsInt(parameters, las2iso.SIMPLIFY_LENGTH)
        if simplify_length != 0:
            commands.append("-simplify_length")
            commands.append(unicode(simplify_length))
        simplify_area = self.parameterAsInt(parameters, las2iso.SIMPLIFY_AREA)
        if simplify_area != 0:
            commands.append("-simplify_area")
            commands.append(unicode(simplify_area))
        clean = self.parameterAsInt(parameters, las2iso.CLEAN)
        if clean != 0:
            commands.append("-clean")
            commands.append(unicode(clean))
        self.addParametersVectorOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszip'

    def displayName(self):
        return 'laszip'

    def group(self):
        return 'LAStools'

    def groupId(self):
        return 'LAStools'

    def createInstance(self):
        return laszip()
	
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

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterNumber

from ..utils import LastoolsUtils, descript_dsm_dtm_generation_production as descript_info, paths
from ..algo import LastoolsAlgorithm


class Las2Iso(LastoolsAlgorithm):
    TOOL_INFO = ('las2iso', 'Las2Iso')
    SMOOTH = "SMOOTH"
    ISO_EVERY = "ISO_EVERY"
    SIMPLIFY_LENGTH = "SIMPLIFY_LENGTH"
    SIMPLIFY_AREA = "SIMPLIFY_AREA"
    CLEAN = "CLEAN"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterNumber(
            Las2Iso.SMOOTH, "smooth underlying TIN", QgsProcessingParameterNumber.Integer, 0, False, 0, 10
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Las2Iso.ISO_EVERY, "extract isoline with a spacing of",
            QgsProcessingParameterNumber.Double, 10.0, False, 0.05, 1000.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Las2Iso.CLEAN, "clean isolines shorter than (0 = do not clean)",
            QgsProcessingParameterNumber.Double, 0.0, False, 0.0, 100.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Las2Iso.SIMPLIFY_LENGTH, "simplify segments shorter than (0 = do not simplify)",
            QgsProcessingParameterNumber.Double, 0.0, False, 0.0, 100.0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            Las2Iso.SIMPLIFY_AREA, "simplify segments pairs with area less than (0 = do not simplify)",
            QgsProcessingParameterNumber.Double, 0.0, False, 0.0, 100.0
        ))
        self.add_parameters_vector_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "las2iso")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        smooth = self.parameterAsInt(parameters, Las2Iso.SMOOTH, context)
        if smooth != 0:
            commands.append("-smooth")
            commands.append(str(smooth))
        commands.append("-iso_every")
        commands.append(str(self.parameterAsDouble(parameters, Las2Iso.ISO_EVERY, context)))
        clean = self.parameterAsDouble(parameters, Las2Iso.CLEAN, context)
        if clean != 0:
            commands.append("-clean")
            commands.append(str(clean))
        simplify_length = self.parameterAsDouble(parameters, Las2Iso.SIMPLIFY_LENGTH, context)
        if simplify_length != 0:
            commands.append("-simplify_length")
            commands.append(str(simplify_length))
        simplify_area = self.parameterAsDouble(parameters, Las2Iso.SIMPLIFY_AREA, context)
        if simplify_area != 0:
            commands.append("-simplify_area")
            commands.append(str(simplify_area))
        self.add_parameters_vector_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return Las2Iso()

    def name(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["name"]

    def displayName(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["display_name"]

    def group(self):
        return descript_info["info"]["group"]

    def groupId(self):
        return descript_info["info"]["group_id"]

    def helpUrl(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["url_path"]

    def shortHelpString(self):
        return self.tr(descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_help_string"])

    def shortDescription(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_description"]

    def icon(self):
        img_path = 'licenced.png' \
            if descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence"] else 'open_source.png'
        return QIcon(f"{paths['img']}{img_path}")

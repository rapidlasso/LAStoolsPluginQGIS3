# -*- coding: utf-8 -*-
"""
***************************************************************************
    blast2iso.py
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


from qgis.core import QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class Blast2Iso(LastoolsAlgorithm):
    TOOL_NAME = "Blast2Iso"
    LASTOOL = "blast2iso"
    LICENSE = "c"
    LASGROUP = 5
    SMOOTH = "SMOOTH"
    ISO_EVERY = "ISO_EVERY"
    SIMPLIFY_LENGTH = "SIMPLIFY_LENGTH"
    SIMPLIFY_AREA = "SIMPLIFY_AREA"
    CLEAN = "CLEAN"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SMOOTH, "smooth underlying TIN", QgsProcessingParameterNumber.Integer, 0, False, 0, 10
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ISO_EVERY,
                "extract isoline with a spacing of",
                QgsProcessingParameterNumber.Double,
                10.0,
                False,
                0.05,
                1000.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CLEAN,
                "clean isolines shorter than (0 = do not clean)",
                QgsProcessingParameterNumber.Double,
                0.0,
                False,
                0.0,
                100.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SIMPLIFY_LENGTH,
                "simplify segments shorter than (0 = do not simplify)",
                QgsProcessingParameterNumber.Double,
                0.0,
                False,
                0.0,
                100.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SIMPLIFY_AREA,
                "simplify segments pairs with area less than (0 = do not simplify)",
                QgsProcessingParameterNumber.Double,
                0.0,
                False,
                0.0,
                100.0,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_vector_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        smooth = self.parameterAsInt(parameters, self.SMOOTH, context)
        if smooth != 0:
            commands.append("-smooth")
            commands.append(str(smooth))
        commands.append("-iso_every")
        commands.append(str(self.parameterAsDouble(parameters, self.ISO_EVERY, context)))
        clean = self.parameterAsDouble(parameters, self.CLEAN, context)
        if clean != 0.0:
            commands.append("-clean")
            commands.append(str(clean))
        simplify_length = self.parameterAsDouble(parameters, self.SIMPLIFY_LENGTH, context)
        if simplify_length != 0.0:
            commands.append("-simplify_length")
            commands.append(str(simplify_length))
        simplify_area = self.parameterAsDouble(parameters, self.SIMPLIFY_AREA, context)
        if simplify_area != 0.0:
            commands.append("-simplify_area")
            commands.append(str(simplify_area))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_vector_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": None}

    def createInstance(self):
        return Blast2Iso()

    def name(self):
        return self.TOOL_NAME

    def displayName(self):
        return lastool_info[self.TOOL_NAME]["disp"]

    def group(self):
        return lasgroup_info[self.LASGROUP]["group"]

    def groupId(self):
        return lasgroup_info[self.LASGROUP]["group_id"]

    def helpUrl(self):
        return readme_url(self.LASTOOL)

    def shortHelpString(self):
        return lastool_info[self.TOOL_NAME]["help"] + help_string_help(self.LASTOOL, self.LICENSE)

    def shortDescription(self):
        return lastool_info[self.TOOL_NAME]["desc"]

    def icon(self):
        icon_file = licence[self.LICENSE]["path"]
        return QIcon(f"{paths['img']}{icon_file}")


class Blast2IsoPro(LastoolsAlgorithm):
    TOOL_NAME = "Blast2IsoPro"
    LASTOOL = "blast2iso"
    LICENSE = "c"
    LASGROUP = 5
    SMOOTH = "SMOOTH"
    ISO_EVERY = "ISO_EVERY"
    SIMPLIFY_LENGTH = "SIMPLIFY_LENGTH"
    SIMPLIFY_AREA = "SIMPLIFY_AREA"
    CLEAN = "CLEAN"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_point_input_merged_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SMOOTH, "smooth underlying TIN", QgsProcessingParameterNumber.Integer, 0, False, 0, 10
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ISO_EVERY,
                "extract isoline with a spacing of",
                QgsProcessingParameterNumber.Double,
                10.0,
                False,
                0.05,
                1000.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CLEAN,
                "clean isolines shorter than (0 = do not clean)",
                QgsProcessingParameterNumber.Double,
                0.0,
                False,
                0.0,
                100.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SIMPLIFY_LENGTH,
                "simplify segments shorter than (0 = do not simplify)",
                QgsProcessingParameterNumber.Double,
                0.0,
                False,
                0.0,
                100.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SIMPLIFY_AREA,
                "simplify segments pairs with area less than (0 = do not simplify)",
                QgsProcessingParameterNumber.Double,
                0.0,
                False,
                0.0,
                100.0,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_vector_output_format_gui()
        self.add_parameters_vector_output_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_point_input_merged_commands(parameters, context, commands)
        smooth = self.parameterAsInt(parameters, self.SMOOTH, context)
        if smooth != 0:
            commands.append("-smooth")
            commands.append(str(smooth))
        commands.append("-iso_every")
        commands.append(str(self.parameterAsDouble(parameters, self.ISO_EVERY, context)))
        clean = self.parameterAsDouble(parameters, self.CLEAN, context)
        if clean != 0.0:
            commands.append("-clean")
            commands.append(str(clean))
        simplify_length = self.parameterAsDouble(parameters, self.SIMPLIFY_LENGTH, context)
        if simplify_length != 0.0:
            commands.append("-simplify_length")
            commands.append(str(simplify_length))
        simplify_area = self.parameterAsDouble(parameters, self.SIMPLIFY_AREA, context)
        if simplify_area != 0.0:
            commands.append("-simplify_area")
            commands.append(str(simplify_area))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_vector_output_format_commands(parameters, context, commands)
        self.add_parameters_vector_output_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return Blast2IsoPro()

    def name(self):
        return self.TOOL_NAME

    def displayName(self):
        return lastool_info[self.TOOL_NAME]["disp"]

    def group(self):
        return lasgroup_info[self.LASGROUP]["group"]

    def groupId(self):
        return lasgroup_info[self.LASGROUP]["group_id"]

    def helpUrl(self):
        return readme_url(self.LASTOOL)

    def shortHelpString(self):
        return lastool_info[self.TOOL_NAME]["help"] + help_string_help(self.LASTOOL, self.LICENSE)

    def shortDescription(self):
        return lastool_info[self.TOOL_NAME]["desc"]

    def icon(self):
        icon_file = licence[self.LICENSE]["path"]
        return QIcon(f"{paths['img']}{icon_file}")

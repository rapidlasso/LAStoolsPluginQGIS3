"""
***************************************************************************
    lastile.py
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


from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber, QgsProcessingParameterString
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasTile(LastoolsAlgorithm):
    TOOL_NAME = "LasTile"
    LASTOOL = "lastile"
    LICENSE = "c"
    LASGROUP = 3
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    REVERSIBLE = "REVERSIBLE"
    FLAG_AS_WITHHELD = "FLAG_AS_WITHHELD"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                4.0,
                10000.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.BUFFER, "buffer around each tile", QgsProcessingParameterNumber.Double, 30.0, False, 0.0, 100.0
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.FLAG_AS_WITHHELD, "flag buffer points as 'withheld' for easier removal later", True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.REVERSIBLE, "make tiling reversible (advanced, usually not needed)", False
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        tile_size = self.parameterAsInt(parameters, self.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, self.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        if self.parameterAsBool(parameters, self.FLAG_AS_WITHHELD, context):
            commands.append("-flag_as_withheld")
        if self.parameterAsBool(parameters, self.REVERSIBLE, context):
            commands.append("-reversible")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasTile()

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


class LasTilePro(LastoolsAlgorithm):
    TOOL_NAME = "LasTilePro"
    LASTOOL = "lastile"
    LICENSE = "c"
    LASGROUP = 3
    TILE_SIZE = "TILE_SIZE"
    BUFFER = "BUFFER"
    FLAG_AS_WITHHELD = "FLAG_AS_WITHHELD"
    EXTRA_PASS = "EXTRA_PASS"
    BASE_NAME = "BASE_NAME"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.add_parameters_apply_file_source_id_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TILE_SIZE,
                "tile size (side length of square tile)",
                QgsProcessingParameterNumber.Double,
                1000.0,
                False,
                4.0,
                10000.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.BUFFER,
                "buffer around each tile",
                QgsProcessingParameterNumber.Double,
                30.0,
                False,
                0.0,
                100.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.FLAG_AS_WITHHELD, "flag buffer points as 'withheld' for easier removal later", True
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(self.EXTRA_PASS, "more than 2000 output tiles", False))
        self.addParameter(
            QgsProcessingParameterString(
                self.BASE_NAME, "tile base name (using sydney.laz creates sydney_274000_4714000.laz)", ""
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context)]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        self.add_parameters_apply_file_source_id_commands(parameters, context, commands)
        tile_size = self.parameterAsInt(parameters, self.TILE_SIZE, context)
        commands.append("-tile_size")
        commands.append(str(tile_size))
        buffer = self.parameterAsDouble(parameters, self.BUFFER, context)
        if buffer != 0.0:
            commands.append("-buffer")
            commands.append(str(buffer))
        if self.parameterAsBool(parameters, self.FLAG_AS_WITHHELD, context):
            commands.append("-flag_as_withheld")
        if self.parameterAsBool(parameters, self.EXTRA_PASS, context):
            commands.append("-extra_pass")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        base_name = self.parameterAsString(parameters, self.BASE_NAME, context)
        if base_name != "":
            commands.append("-o")
            commands.append('"' + base_name + '"')
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasTilePro()

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

# -*- coding: utf-8 -*-
"""
***************************************************************************
    blast2dem.py
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


from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class Blast2Dem(LastoolsAlgorithm):
    TOOL_NAME = "Blast2Dem"
    LASTOOL = "blast2dem"
    LICENSE = "c"
    LASGROUP = 5
    ATTRIBUTE = "ATTRIBUTE"
    PRODUCT = "PRODUCT"
    ATTRIBUTES = ["elevation", "slope", "intensity", "rgb"]
    PRODUCTS = ["actual values", "hillshade", "gray", "false"]
    USE_TILE_BB = "USE_TILE_BB"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_step_gui()
        self.addParameter(QgsProcessingParameterEnum(self.ATTRIBUTE, "attribute", self.ATTRIBUTES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT, "method", self.PRODUCTS, False, 0))
        self.addParameter(
            QgsProcessingParameterBoolean(self.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_raster_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_step_commands(parameters, context, commands)
        attribute = self.parameterAsInt(parameters, self.ATTRIBUTE, context)
        if attribute != 0:
            commands.append("-" + self.ATTRIBUTES[attribute])
        product = self.parameterAsInt(parameters, self.PRODUCT, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        if self.parameterAsBool(parameters, self.USE_TILE_BB, context):
            commands.append("-use_tile_bb")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return Blast2Dem()

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


class Blast2DemPro(LastoolsAlgorithm):
    TOOL_NAME = "Blast2DemPro"
    LASTOOL = "blast2dem"
    LICENSE = "c"
    LASGROUP = 5
    ATTRIBUTE = "ATTRIBUTE"
    PRODUCT = "PRODUCT"
    ATTRIBUTES = ["elevation", "slope", "intensity", "rgb"]
    PRODUCTS = ["actual values", "hillshade", "gray", "false"]
    USE_TILE_BB = "USE_TILE_BB"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_point_input_merged_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.add_parameters_step_gui()
        self.addParameter(QgsProcessingParameterEnum(self.ATTRIBUTE, "Attribute", self.ATTRIBUTES, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT, "Product", self.PRODUCTS, False, 0))
        self.addParameter(
            QgsProcessingParameterBoolean(self.USE_TILE_BB, "Use tile bounding box (after tiling with buffer)", False)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_raster_output_format_gui()
        self.add_parameters_raster_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_point_input_merged_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        self.add_parameters_step_commands(parameters, context, commands)
        attribute = self.parameterAsInt(parameters, self.ATTRIBUTE, context)
        if attribute != 0:
            commands.append("-" + self.ATTRIBUTES[attribute])
        product = self.parameterAsInt(parameters, self.PRODUCT, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        if self.parameterAsBool(parameters, self.USE_TILE_BB, context):
            commands.append("-use_tile_bb")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_raster_output_format_commands(parameters, context, commands)
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return Blast2DemPro()

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

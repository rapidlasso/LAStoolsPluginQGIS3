"""
***************************************************************************
    lascanopy.py
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

import os

from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
)
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasCanopy(LastoolsAlgorithm):
    TOOL_NAME = "LasCanopy"
    LASTOOL = "lascanopy"
    LICENSE = "c"
    LASGROUP = 5
    PLOT_SIZE = "PLOT_SIZE"
    HEIGHT_CUTOFF = "HEIGHT_CUTOFF"
    PRODUCT1 = "PRODUCT1"
    PRODUCT2 = "PRODUCT2"
    PRODUCT3 = "PRODUCT3"
    PRODUCT4 = "PRODUCT4"
    PRODUCT5 = "PRODUCT5"
    PRODUCT6 = "PRODUCT6"
    PRODUCT7 = "PRODUCT7"
    PRODUCT8 = "PRODUCT8"
    PRODUCT9 = "PRODUCT9"
    PRODUCTS = [
        "---",
        "min",
        "max",
        "avg",
        "std",
        "ske",
        "kur",
        "qav",
        "cov",
        "dns",
        "all",
        "p 1",
        "p 5",
        "p 10",
        "p 25",
        "p 50",
        "p 75",
        "p 90",
        "p 99",
        "int_min",
        "int_max",
        "int_avg",
        "int_std",
        "int_ske",
        "int_kur",
        "int_p 1",
        "int_p 5",
        "int_p 10",
        "int_p 25",
        "int_p 50",
        "int_p 75",
        "int_p 90",
        "int_p 99",
    ]
    COUNTS = "COUNTS"
    DENSITIES = "DENSITIES"
    USE_TILE_BB = "USE_TILE_BB"
    FILES_ARE_PLOTS = "FILES_ARE_PLOTS"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PLOT_SIZE, "square plot size", QgsProcessingParameterNumber.Double, 20.0, False, 0.0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.HEIGHT_CUTOFF,
                "height cutoff / breast height",
                QgsProcessingParameterNumber.Double,
                1.37,
                False,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT1, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT2, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT3, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT4, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT5, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT6, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT7, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT8, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT9, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterString(self.COUNTS, "count rasters (e.g. 2.0 5.0 10.0 20.0)", ""))
        self.addParameter(QgsProcessingParameterString(self.DENSITIES, "density rasters (e.g. 2.0 5.0 10.0 20.0)", ""))
        self.addParameter(
            QgsProcessingParameterBoolean(self.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False)
        )
        self.addParameter(QgsProcessingParameterBoolean(self.FILES_ARE_PLOTS, "input file is single plot", False))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_raster_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_point_input_commands(parameters, context, commands)
        plot_size = self.parameterAsDouble(parameters, self.PLOT_SIZE, context)
        if plot_size != 20.0:
            commands.append("-step")
            commands.append(str(plot_size))
        height_cutoff = self.parameterAsDouble(parameters, self.HEIGHT_CUTOFF, context)
        if height_cutoff != 1.37:
            commands.append("-height_cutoff")
            commands.append(str(height_cutoff))
        product = self.parameterAsInt(parameters, self.PRODUCT1, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT2, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT3, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT4, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT5, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT6, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT7, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT8, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT9, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        array = self.parameterAsString(parameters, self.COUNTS, context).split()
        if len(array) > 1:
            commands.append("-c")
            for a in array:
                commands.append(a)
        array = self.parameterAsString(parameters, self.DENSITIES, context).split()
        if len(array) > 1:
            commands.append("-d")
            for a in array:
                commands.append(a)
        if self.parameterAsBool(parameters, self.USE_TILE_BB, context):
            commands.append("-use_tile_bb")
        if self.parameterAsBool(parameters, self.FILES_ARE_PLOTS, context):
            commands.append("-files_are_plots")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_raster_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasCanopy()

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


class LasCanopyPro(LastoolsAlgorithm):
    TOOL_NAME = "LasCanopyPro"
    LASTOOL = "lascanopy"
    LICENSE = "c"
    LASGROUP = 5
    PLOT_SIZE = "PLOT_SIZE"
    HEIGHT_CUTOFF = "HEIGHT_CUTOFF"
    PRODUCT1 = "PRODUCT1"
    PRODUCT2 = "PRODUCT2"
    PRODUCT3 = "PRODUCT3"
    PRODUCT4 = "PRODUCT4"
    PRODUCT5 = "PRODUCT5"
    PRODUCT6 = "PRODUCT6"
    PRODUCT7 = "PRODUCT7"
    PRODUCT8 = "PRODUCT8"
    PRODUCT9 = "PRODUCT9"
    PRODUCTS = [
        "---",
        "min",
        "max",
        "avg",
        "std",
        "ske",
        "kur",
        "qav",
        "cov",
        "dns",
        "all",
        "p 1",
        "p 5",
        "p 10",
        "p 25",
        "p 50",
        "p 75",
        "p 90",
        "p 99",
        "int_min",
        "int_max",
        "int_avg",
        "int_std",
        "int_ske",
        "int_kur",
        "int_p 1",
        "int_p 5",
        "int_p 10",
        "int_p 25",
        "int_p 50",
        "int_p 75",
        "int_p 90",
        "int_p 99",
    ]
    COUNTS = "COUNTS"
    DENSITIES = "DENSITIES"
    USE_TILE_BB = "USE_TILE_BB"
    FILES_ARE_PLOTS = "FILES_ARE_PLOTS"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_point_input_merged_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PLOT_SIZE, "square plot size", QgsProcessingParameterNumber.Double, 20.0, False, 0.0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.HEIGHT_CUTOFF,
                "height cutoff / breast height",
                QgsProcessingParameterNumber.Double,
                1.37,
                False,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT1, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT2, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT3, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT4, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT5, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT6, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT7, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT8, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(self.PRODUCT9, "create", self.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterString(self.COUNTS, "count rasters (e.g. 2.0 5.0 10.0 20.0)", ""))
        self.addParameter(QgsProcessingParameterString(self.DENSITIES, "density rasters (e.g. 2.0 5.0 10.0 20.0)", ""))
        self.addParameter(
            QgsProcessingParameterBoolean(self.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False)
        )
        self.addParameter(QgsProcessingParameterBoolean(self.FILES_ARE_PLOTS, "input files are single plots", False))
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_raster_output_format_gui()
        self.add_parameters_raster_output_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_point_input_merged_commands(parameters, context, commands)
        plot_size = self.parameterAsDouble(parameters, self.PLOT_SIZE, context)
        if plot_size != 20.0:
            commands.append("-step")
            commands.append(str(plot_size))
        height_cutoff = self.parameterAsDouble(parameters, self.HEIGHT_CUTOFF, context)
        if height_cutoff != 1.37:
            commands.append("-height_cutoff")
            commands.append(str(height_cutoff))
        product = self.parameterAsInt(parameters, self.PRODUCT1, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT2, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT3, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT4, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT5, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT6, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT7, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT8, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        product = self.parameterAsInt(parameters, self.PRODUCT9, context)
        if product != 0:
            commands.append("-" + self.PRODUCTS[product])
        array = self.parameterAsString(parameters, self.COUNTS, context).split()
        if len(array) > 1:
            commands.append("-c")
            for a in array:
                commands.append(a)
        array = self.parameterAsString(parameters, self.DENSITIES, context).split()
        if len(array) > 1:
            commands.append("-d")
            for a in array:
                commands.append(a)
        if self.parameterAsBool(parameters, self.USE_TILE_BB, context):
            commands.append("-use_tile_bb")
        if self.parameterAsBool(parameters, self.FILES_ARE_PLOTS, context):
            commands.append("-files_are_plots")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_raster_output_format_commands(parameters, context, commands)
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"": None}

    def createInstance(self):
        return LasCanopyPro()

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

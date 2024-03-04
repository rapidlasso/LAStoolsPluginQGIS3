# -*- coding: utf-8 -*-

"""
***************************************************************************
    lascanopy.py
    ---------------------
    Date                 : November 2023
    Copyright            : (C) 2023 by rapidlasso GmbH
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
__date__ = "March 2024"
__copyright__ = "(C) 2024, rapidlasso GmbH"

import os

from PyQt5.QtGui import QIcon
from qgis.core import (
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
)

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


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
                LasCanopy.PLOT_SIZE, "square plot size", QgsProcessingParameterNumber.Double, 20.0, False, 0.0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasCanopy.HEIGHT_CUTOFF,
                "height cutoff / breast height",
                QgsProcessingParameterNumber.Double,
                1.37,
                False,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(LasCanopy.PRODUCT1, "create", LasCanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopy.PRODUCT2, "create", LasCanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopy.PRODUCT3, "create", LasCanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopy.PRODUCT4, "create", LasCanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopy.PRODUCT5, "create", LasCanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopy.PRODUCT6, "create", LasCanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopy.PRODUCT7, "create", LasCanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopy.PRODUCT8, "create", LasCanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopy.PRODUCT9, "create", LasCanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterString(LasCanopy.COUNTS, "count rasters (e.g. 2.0 5.0 10.0 20.0)", ""))
        self.addParameter(
            QgsProcessingParameterString(LasCanopy.DENSITIES, "density rasters (e.g. 2.0 5.0 10.0 20.0)", "")
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                LasCanopy.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(LasCanopy.FILES_ARE_PLOTS, "input file is single plot", False))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_raster_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lascanopy")]
        self.add_parameters_point_input_commands(parameters, context, commands)
        plot_size = self.parameterAsDouble(parameters, LasCanopy.PLOT_SIZE, context)
        if plot_size != 20.0:
            commands.append("-step")
            commands.append(str(plot_size))
        height_cutoff = self.parameterAsDouble(parameters, LasCanopy.HEIGHT_CUTOFF, context)
        if height_cutoff != 1.37:
            commands.append("-height_cutoff")
            commands.append(str(height_cutoff))
        product = self.parameterAsInt(parameters, LasCanopy.PRODUCT1, context)
        if product != 0:
            commands.append("-" + LasCanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopy.PRODUCT2, context)
        if product != 0:
            commands.append("-" + LasCanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopy.PRODUCT3, context)
        if product != 0:
            commands.append("-" + LasCanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopy.PRODUCT4, context)
        if product != 0:
            commands.append("-" + LasCanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopy.PRODUCT5, context)
        if product != 0:
            commands.append("-" + LasCanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopy.PRODUCT6, context)
        if product != 0:
            commands.append("-" + LasCanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopy.PRODUCT7, context)
        if product != 0:
            commands.append("-" + LasCanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopy.PRODUCT8, context)
        if product != 0:
            commands.append("-" + LasCanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopy.PRODUCT9, context)
        if product != 0:
            commands.append("-" + LasCanopy.PRODUCTS[product])
        array = self.parameterAsString(parameters, LasCanopy.COUNTS, context).split()
        if len(array) > 1:
            commands.append("-c")
            for a in array:
                commands.append(a)
        array = self.parameterAsString(parameters, LasCanopy.DENSITIES, context).split()
        if len(array) > 1:
            commands.append("-d")
            for a in array:
                commands.append(a)
        if self.parameterAsBool(parameters, LasCanopy.USE_TILE_BB, context):
            commands.append("-use_tile_bb")
        if self.parameterAsBool(parameters, LasCanopy.FILES_ARE_PLOTS, context):
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
                LasCanopyPro.PLOT_SIZE, "square plot size", QgsProcessingParameterNumber.Double, 20.0, False, 0.0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasCanopyPro.HEIGHT_CUTOFF,
                "height cutoff / breast height",
                QgsProcessingParameterNumber.Double,
                1.37,
                False,
            )
        )
        self.addParameter(QgsProcessingParameterEnum(LasCanopyPro.PRODUCT1, "create", LasCanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopyPro.PRODUCT2, "create", LasCanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopyPro.PRODUCT3, "create", LasCanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopyPro.PRODUCT4, "create", LasCanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopyPro.PRODUCT5, "create", LasCanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopyPro.PRODUCT6, "create", LasCanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopyPro.PRODUCT7, "create", LasCanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopyPro.PRODUCT8, "create", LasCanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(LasCanopyPro.PRODUCT9, "create", LasCanopyPro.PRODUCTS, False, 0))
        self.addParameter(
            QgsProcessingParameterString(LasCanopyPro.COUNTS, "count rasters (e.g. 2.0 5.0 10.0 20.0)", "")
        )
        self.addParameter(
            QgsProcessingParameterString(LasCanopyPro.DENSITIES, "density rasters (e.g. 2.0 5.0 10.0 20.0)", "")
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                LasCanopyPro.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(LasCanopyPro.FILES_ARE_PLOTS, "input files are single plots", False)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_raster_output_format_gui()
        self.add_parameters_raster_output_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lascanopy")]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_point_input_merged_commands(parameters, context, commands)
        plot_size = self.parameterAsDouble(parameters, LasCanopyPro.PLOT_SIZE, context)
        if plot_size != 20.0:
            commands.append("-step")
            commands.append(str(plot_size))
        height_cutoff = self.parameterAsDouble(parameters, LasCanopyPro.HEIGHT_CUTOFF, context)
        if height_cutoff != 1.37:
            commands.append("-height_cutoff")
            commands.append(str(height_cutoff))
        product = self.parameterAsInt(parameters, LasCanopyPro.PRODUCT1, context)
        if product != 0:
            commands.append("-" + LasCanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopyPro.PRODUCT2, context)
        if product != 0:
            commands.append("-" + LasCanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopyPro.PRODUCT3, context)
        if product != 0:
            commands.append("-" + LasCanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopyPro.PRODUCT4, context)
        if product != 0:
            commands.append("-" + LasCanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopyPro.PRODUCT5, context)
        if product != 0:
            commands.append("-" + LasCanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopyPro.PRODUCT6, context)
        if product != 0:
            commands.append("-" + LasCanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopyPro.PRODUCT7, context)
        if product != 0:
            commands.append("-" + LasCanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopyPro.PRODUCT8, context)
        if product != 0:
            commands.append("-" + LasCanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, LasCanopyPro.PRODUCT9, context)
        if product != 0:
            commands.append("-" + LasCanopyPro.PRODUCTS[product])
        array = self.parameterAsString(parameters, LasCanopyPro.COUNTS, context).split()
        if len(array) > 1:
            commands.append("-c")
            for a in array:
                commands.append(a)
        array = self.parameterAsString(parameters, LasCanopyPro.DENSITIES, context).split()
        if len(array) > 1:
            commands.append("-d")
            for a in array:
                commands.append(a)
        if self.parameterAsBool(parameters, LasCanopyPro.USE_TILE_BB, context):
            commands.append("-use_tile_bb")
        if self.parameterAsBool(parameters, LasCanopyPro.FILES_ARE_PLOTS, context):
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

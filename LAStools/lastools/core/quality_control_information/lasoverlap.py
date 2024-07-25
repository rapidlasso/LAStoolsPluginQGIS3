# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasoverlap.py
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
from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, lastool_info, lasgroup_info, paths, licence, help_string_help, readme_url
from ..algo import LastoolsAlgorithm


class LasOverlap(LastoolsAlgorithm):
    TOOL_NAME = "LasOverlap"
    LASTOOL = "lasoverlap"
    LICENSE = "c"
    LASGROUP = 6
    CHECK_STEP = "CHECK_STEP"
    ATTRIBUTE = "ATTRIBUTE"
    OPERATION = "OPERATION"
    ATTRIBUTES = ["elevation", "intensity", "number_of_returns", "scan_angle_abs", "density"]
    OPERATIONS = ["lowest", "highest", "average"]
    CREATE_OVERLAP_RASTER = "CREATE_OVERLAP_RASTER"
    CREATE_DIFFERENCE_RASTER = "CREATE_DIFFERENCE_RASTER"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                LasOverlap.CHECK_STEP,
                "size of grid used for overlap check",
                QgsProcessingParameterNumber.Double,
                2.0,
                False,
                0.001,
                50.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(LasOverlap.ATTRIBUTE, "attribute to check", LasOverlap.ATTRIBUTES, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                LasOverlap.OPERATION, "operation on attribute per cell", LasOverlap.OPERATIONS, False, 0
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(LasOverlap.CREATE_OVERLAP_RASTER, "create overlap raster", True)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(LasOverlap.CREATE_DIFFERENCE_RASTER, "create difference raster", True)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_raster_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, LasOverlap.CHECK_STEP, context)
        if step != 2.0:
            commands.append("-step")
            commands.append(str(step))
        commands.append("-values")
        attribute = self.parameterAsInt(parameters, LasOverlap.ATTRIBUTE, context)
        if attribute != 0:
            commands.append("-" + LasOverlap.ATTRIBUTES[attribute])
        operation = self.parameterAsInt(parameters, LasOverlap.OPERATION, context)
        if operation != 0:
            commands.append("-" + LasOverlap.OPERATIONS[operation])
        if not self.parameterAsBool(parameters, LasOverlap.CREATE_OVERLAP_RASTER, context):
            commands.append("-no_over")
        if not self.parameterAsBool(parameters, LasOverlap.CREATE_DIFFERENCE_RASTER, context):
            commands.append("-no_diff")
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasOverlap()

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


class LasOverlapPro(LastoolsAlgorithm):
    TOOL_NAME = "LasOverlapPro"
    LASTOOL = "lasoverlap"
    LICENSE = "c"
    LASGROUP = 6
    CHECK_STEP = "CHECK_STEP"
    ATTRIBUTE = "ATTRIBUTE"
    OPERATION = "OPERATION"
    ATTRIBUTES = ["elevation", "intensity", "number_of_returns", "scan_angle_abs", "density"]
    OPERATIONS = ["lowest", "highest", "average"]
    CREATE_OVERLAP_RASTER = "CREATE_OVERLAP_RASTER"
    CREATE_DIFFERENCE_RASTER = "CREATE_DIFFERENCE_RASTER"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                LasOverlapPro.CHECK_STEP,
                "size of grid used for overlap check",
                QgsProcessingParameterNumber.Double,
                2.0,
                False,
                0.001,
                50.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                LasOverlapPro.ATTRIBUTE, "attribute to check", LasOverlapPro.ATTRIBUTES, False, 0
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                LasOverlapPro.OPERATION, "operation on attribute per cell", LasOverlapPro.OPERATIONS, False, 0
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(LasOverlapPro.CREATE_OVERLAP_RASTER, "create overlap raster", True)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(LasOverlapPro.CREATE_DIFFERENCE_RASTER, "create difference raster", True)
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_raster_output_gui()
        self.add_parameters_raster_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", self.LASTOOL + LastoolsUtils.command_ext())]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, LasOverlapPro.CHECK_STEP, context)
        if step != 2.0:
            commands.append("-step")
            commands.append(str(step))
        commands.append("-values")
        attribute = self.parameterAsInt(parameters, LasOverlapPro.ATTRIBUTE, context)
        if attribute != 0:
            commands.append("-" + LasOverlapPro.ATTRIBUTES[attribute])
        operation = self.parameterAsInt(parameters, LasOverlapPro.OPERATION, context)
        if operation != 0:
            commands.append("-" + LasOverlapPro.OPERATIONS[operation])
        if not self.parameterAsBool(parameters, LasOverlapPro.CREATE_OVERLAP_RASTER, context):
            commands.append("-no_over")
        if not self.parameterAsBool(parameters, LasOverlapPro.CREATE_DIFFERENCE_RASTER, context):
            commands.append("-no_diff")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_raster_output_format_commands(parameters, context, commands)
        self.add_parameters_raster_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasOverlapPro()

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

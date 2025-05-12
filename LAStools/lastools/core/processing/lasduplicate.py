# -*- coding: utf-8 -*-
"""
***************************************************************************
    lasduplicate.py
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

__author__ = "rapidlasso"
__date__ = "January 2025"
__copyright__ = "(c) 2025, rapidlasso GmbH"


from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasDuplicate(LastoolsAlgorithm):
    TOOL_NAME = "LasDuplicate"
    LASTOOL = "lasduplicate"
    LICENSE = "c"
    LASGROUP = 3
    LOWEST_Z = "LOWEST_Z"
    HIGHEST_Z = "HIGHEST_Z"
    UNIQUE_XYZ = "UNIQUE_XYZ"
    SINGLE_RETURNS = "SINGLE_RETURNS"
    NEARBY = "NEARBY"
    NEARBY_TOLERANCE = "NEARBY_TOLERANCE"
    RECORD_REMOVED = "RECORD_REMOVED"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterBoolean(self.LOWEST_Z, "keep duplicate with lowest z coordinate", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.HIGHEST_Z, "keep duplicate with highest z coordinate", False)
        )
        self.addParameter(QgsProcessingParameterBoolean(self.UNIQUE_XYZ, "only remove duplicates in x y and z", False))
        self.addParameter(
            QgsProcessingParameterBoolean(self.SINGLE_RETURNS, "mark surviving duplicate as single return", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.NEARBY, "keep only one point within specified tolerance ", False)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.NEARBY_TOLERANCE,
                "tolerance value",
                QgsProcessingParameterNumber.Double,
                0.02,
                False,
                0.001,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.RECORD_REMOVED, "record removed duplicates to LAS/LAZ file", False)
        )
        self.add_parameters_verbose_64_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.LOWEST_Z, context):
            commands.append("-lowest_z")
        if self.parameterAsBool(parameters, self.HIGHEST_Z, context):
            commands.append("-highest_z")
        if self.parameterAsBool(parameters, self.UNIQUE_XYZ, context):
            commands.append("-unique_xyz")
        if self.parameterAsBool(parameters, self.SINGLE_RETURNS, context):
            commands.append("-single_returns")
        if self.parameterAsBool(parameters, self.NEARBY, context):
            commands.append("-nearby")
            commands.append(str(self.parameterAsDouble(parameters, self.NEARBY_TOLERANCE, context)))
        if self.parameterAsBool(parameters, self.RECORD_REMOVED, context):
            commands.append("-record_removed")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"": None}

    def createInstance(self):
        return LasDuplicate()

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


class LasDuplicatePro(LastoolsAlgorithm):
    TOOL_NAME = "LasDuplicatePro"
    LASTOOL = "lasduplicate"
    LICENSE = "c"
    LASGROUP = 3
    LOWEST_Z = "LOWEST_Z"
    HIGHEST_Z = "HIGHEST_Z"
    UNIQUE_XYZ = "UNIQUE_XYZ"
    SINGLE_RETURNS = "SINGLE_RETURNS"
    NEARBY = "NEARBY"
    NEARBY_TOLERANCE = "NEARBY_TOLERANCE"
    RECORD_REMOVED = "RECORD_REMOVED"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.addParameter(
            QgsProcessingParameterBoolean(self.LOWEST_Z, "keep duplicate with lowest z coordinate", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.HIGHEST_Z, "keep duplicate with highest z coordinate", False)
        )
        self.addParameter(QgsProcessingParameterBoolean(self.UNIQUE_XYZ, "only remove duplicates in x y and z", False))
        self.addParameter(
            QgsProcessingParameterBoolean(self.SINGLE_RETURNS, "mark surviving duplicate as single return", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.NEARBY, "keep only one point within specified tolerance ", False)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.NEARBY_TOLERANCE,
                "tolerance value",
                QgsProcessingParameterNumber.Double,
                0.02,
                False,
                0.001,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.RECORD_REMOVED, "record removed duplicates to LAS/LAZ file", False)
        )
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.LOWEST_Z, context):
            commands.append("-lowest_z")
        if self.parameterAsBool(parameters, self.HIGHEST_Z, context):
            commands.append("-highest_z")
        if self.parameterAsBool(parameters, self.UNIQUE_XYZ, context):
            commands.append("-unique_xyz")
        if self.parameterAsBool(parameters, self.SINGLE_RETURNS, context):
            commands.append("-single_returns")
        if self.parameterAsBool(parameters, self.NEARBY, context):
            commands.append("-nearby")
            commands.append(str(self.parameterAsDouble(parameters, self.NEARBY_TOLERANCE, context)))
        if self.parameterAsBool(parameters, self.RECORD_REMOVED, context):
            commands.append("-record_removed")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        self.run_lastools(commands, feedback)

        return {"": None}

    def createInstance(self):
        return LasDuplicatePro()

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

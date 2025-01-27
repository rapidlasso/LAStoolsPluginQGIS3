"""
***************************************************************************
    lasvoxel.py
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


from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasVoxel(LastoolsAlgorithm):
    TOOL_NAME = "LasVoxel"
    LASTOOL = "lasvoxel"
    LICENSE = "c"
    LASGROUP = 5

    ARG_COMPUTE_MEAN_XYZ = "ARG_COMPUTE_MEAN_XYZ"
    ARG_EMPTY_VOXELS = "ARG_EMPTY_VOXELS"
    ARG_MAX_COUNT = "ARG_MAX_COUNT"
    ARG_STEP = "ARG_STEP"
    ARG_STORE_IDS_IN_INTENSITY = "ARG_STORE_IDS_IN_INTENSITY"
    ARG_STORE_IDS_IN_POINT_SOURCE = "ARG_STORE_IDS_IN_POINT_SOURCE"

    ARG_COMPUTE_MEAN_XYZ = "ARG_COMPUTE_MEAN_XYZ"
    ARG_EMPTY_VOXELS = "ARG_EMPTY_VOXELS"
    ARG_STORE_IDS_IN_INTENSITY = "ARG_STORE_IDS_IN_INTENSITY"
    ARG_STORE_IDS_IN_POINT_SOURCE = "ARG_STORE_IDS_IN_POINT_SOURCE"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ARG_STEP,
                "grid size",
                QgsProcessingParameterNumber.Double,
                1,
                True,
                0.001,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ARG_MAX_COUNT,
                "maximum point count per voxel",
                QgsProcessingParameterNumber.Integer,
                0,
                False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(self.ARG_COMPUTE_MEAN_XYZ, "compute averaged coordinate each voxel", False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ARG_EMPTY_VOXELS, "output voxels without returns as intensity zero", False
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ARG_STORE_IDS_IN_INTENSITY, "store voxel IDs into " "intensity" "", False
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ARG_STORE_IDS_IN_POINT_SOURCE, "store voxel IDs into " "point source" "", False
            )
        )
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, self.ARG_STEP, context)
        commands.append("-step")
        commands.append(str(step))
        count = self.parameterAsInt(parameters, self.ARG_MAX_COUNT, context)
        commands.append("-max_count")
        commands.append(str(count))
        if self.parameterAsBool(parameters, self.ARG_COMPUTE_MEAN_XYZ, context):
            commands.append("-compute_mean_xyz")
        if self.parameterAsBool(parameters, self.ARG_EMPTY_VOXELS, context):
            commands.append("-empty_voxels")
        if self.parameterAsBool(parameters, self.ARG_STORE_IDS_IN_INTENSITY, context):
            commands.append("-store_IDs_in_intensity")
        if self.parameterAsBool(parameters, self.ARG_STORE_IDS_IN_POINT_SOURCE, context):
            commands.append("-store_IDs_in_point_source")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasVoxel()

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

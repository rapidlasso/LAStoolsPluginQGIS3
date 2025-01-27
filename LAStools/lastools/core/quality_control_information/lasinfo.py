"""
***************************************************************************
    lasinfo.py
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

from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasInfo(LastoolsAlgorithm):
    TOOL_NAME = "LasInfo"
    LASTOOL = "lasinfo"
    LICENSE = "o"
    LASGROUP = 6
    COMPUTE_DENSITY = "COMPUTE_DENSITY"
    REPAIR_BB = "REPAIR_BB"
    REPAIR_COUNTERS = "REPAIR_COUNTERS"
    HISTO1 = "HISTO1"
    HISTO2 = "HISTO2"
    HISTO3 = "HISTO3"
    HISTOGRAM = [
        "---",
        "x",
        "y",
        "z",
        "intensity",
        "classification",
        "scan_angle",
        "user_data",
        "point_source",
        "gps_time",
        "X",
        "Y",
        "Z",
        "attribute0",
        "attribute1",
        "attribute2",
    ]
    HISTO1_BIN = "HISTO1_BIN"
    HISTO2_BIN = "HISTO2_BIN"
    HISTO3_BIN = "HISTO3_BIN"
    JSON = "JSON"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.addParameter(QgsProcessingParameterBoolean(self.COMPUTE_DENSITY, "compute density", False))
        self.addParameter(QgsProcessingParameterBoolean(self.REPAIR_BB, "repair bounding box", False))
        self.addParameter(QgsProcessingParameterBoolean(self.REPAIR_COUNTERS, "repair counters", False))
        self.addParameter(QgsProcessingParameterEnum(self.HISTO1, "histogram", self.HISTOGRAM, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.HISTO1_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.HISTO2, "histogram", self.HISTOGRAM, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.HISTO2_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.HISTO3, "histogram", self.HISTOGRAM, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.HISTO3_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(self.JSON, "JSON output", False))
        self.add_parameters_generic_output_gui("Output ASCII file", "txt", True)
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.COMPUTE_DENSITY, context):
            commands.append("-cd")
        if self.parameterAsBool(parameters, self.REPAIR_BB, context):
            commands.append("-repair_bb")
        if self.parameterAsBool(parameters, self.REPAIR_COUNTERS, context):
            commands.append("-repair_counters")
        histo = self.parameterAsInt(parameters, self.HISTO1, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(self.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, self.HISTO1_BIN, context)))
        histo = self.parameterAsInt(parameters, self.HISTO2, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(self.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, self.HISTO2_BIN, context)))
        histo = self.parameterAsInt(parameters, self.HISTO3, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(self.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, self.HISTO3_BIN, context)))
        if self.parameterAsBool(parameters, self.JSON, context):
            commands.append("-js")
        self.add_parameters_generic_output_commands(parameters, context, commands, "-o")
        self.add_parameters_additional_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasInfo()

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


class LasInfoPro(LastoolsAlgorithm):
    TOOL_NAME = "LasInfoPro"
    LASTOOL = "lasinfo"
    LICENSE = "o"
    LASGROUP = 6
    COMPUTE_DENSITY = "COMPUTE_DENSITY"
    REPAIR_BB = "REPAIR_BB"
    REPAIR_COUNTERS = "REPAIR_COUNTERS"
    HISTO1 = "HISTO1"
    HISTO2 = "HISTO2"
    HISTO3 = "HISTO3"
    HISTOGRAM = [
        "---",
        "x",
        "y",
        "z",
        "intensity",
        "classification",
        "scan_angle",
        "user_data",
        "point_source",
        "gps_time",
        "X",
        "Y",
        "Z",
        "attribute0",
        "attribute1",
        "attribute2",
    ]
    HISTO1_BIN = "HISTO1_BIN"
    HISTO2_BIN = "HISTO2_BIN"
    HISTO3_BIN = "HISTO3_BIN"
    JSON = "JSON"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterBoolean(self.COMPUTE_DENSITY, "compute density", False))
        self.addParameter(QgsProcessingParameterBoolean(self.REPAIR_BB, "repair bounding box", False))
        self.addParameter(QgsProcessingParameterBoolean(self.REPAIR_COUNTERS, "repair counters", False))
        self.addParameter(QgsProcessingParameterEnum(self.HISTO1, "histogram", self.HISTOGRAM, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.HISTO1_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.HISTO2, "histogram", self.HISTOGRAM, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.HISTO2_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
            )
        )
        self.addParameter(QgsProcessingParameterEnum(self.HISTO3, "histogram", self.HISTOGRAM, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.HISTO3_BIN, "bin size", QgsProcessingParameterNumber.Double, 1.0, False, 0
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(self.JSON, "JSON output", False))
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, self.COMPUTE_DENSITY, context):
            commands.append("-cd")
        if self.parameterAsBool(parameters, self.REPAIR_BB, context):
            commands.append("-repair_bb")
        if self.parameterAsBool(parameters, self.REPAIR_COUNTERS, context):
            commands.append("-repair_counters")
        histo = self.parameterAsInt(parameters, self.HISTO1, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(self.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, self.HISTO1_BIN, context)))
        histo = self.parameterAsInt(parameters, self.HISTO2, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(self.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, self.HISTO2_BIN, context)))
        histo = self.parameterAsInt(parameters, self.HISTO3, context)
        if histo != 0:
            commands.append("-histo")
            commands.append(self.HISTOGRAM[histo])
            commands.append(str(self.parameterAsDouble(parameters, self.HISTO3_BIN, context)))
        if self.parameterAsBool(parameters, self.JSON, context):
            commands.append("-js")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        commands.append("-otxt")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasInfoPro()

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

"""
***************************************************************************
    lasthin.py
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


class LasThin(LastoolsAlgorithm):
    TOOL_NAME = "LasThin"
    LASTOOL = "lasthin"
    LICENSE = "c"
    LASGROUP = 4
    THIN_STEP = "THIN_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["lowest", "random", "highest", "central", "adaptive", "contours", "percentile"]
    THRESHOLD_OR_INTERVAL_OR_PERCENTILE = "THRESHOLD_OR_INTERVAL_OR_PERCENTILE"
    WITHHELD = "WITHHELD"
    CLASSIFY_AS = "CLASSIFY_AS"
    CLASSIFY_AS_CLASS = "CLASSIFY_AS_CLASS"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.THIN_STEP,
                "size of grid used for thinning",
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(self.OPERATION, "keep particular point per cell", self.OPERATIONS, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.THRESHOLD_OR_INTERVAL_OR_PERCENTILE,
                "adaptive threshold, contour intervals, or percentile",
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.0,
                100.0,
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(self.WITHHELD, "mark thinned-away points as withheld", False))
        self.addParameter(QgsProcessingParameterBoolean(self.CLASSIFY_AS, "classify surviving points as", False))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CLASSIFY_AS_CLASS, "classification code", QgsProcessingParameterNumber.Integer, 8, False, 0, 255
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [
            os.path.join(
                LastoolsUtils.lastools_path(),
                "bin",
                self.LASTOOL + self.cpu64(parameters, context) + LastoolsUtils.command_ext(),
            )
        ]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, self.THIN_STEP, context)
        if step != 1.0:
            commands.append("-step")
            commands.append(str(step))
        operation = self.parameterAsInt(parameters, self.OPERATION, context)
        if operation != 0:
            commands.append("-" + self.OPERATIONS[operation])
        if operation >= 4:
            commands.append(str(self.parameterAsDouble(parameters, self.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, context)))
        if self.parameterAsBool(parameters, self.WITHHELD, context):
            commands.append("-withheld")
        if self.parameterAsBool(parameters, self.CLASSIFY_AS, context):
            commands.append("-classify_as")
            commands.append(str(self.parameterAsInt(parameters, self.CLASSIFY_AS_CLASS, context)))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasThin()

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


class LasThinPro(LastoolsAlgorithm):
    TOOL_NAME = "LasThinPro"
    LASTOOL = "lasthin"
    LICENSE = "c"
    LASGROUP = 4
    THIN_STEP = "THIN_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["lowest", "random", "highest", "central", "adaptive", "contours", "percentile"]
    THRESHOLD_OR_INTERVAL_OR_PERCENTILE = "THRESHOLD_OR_INTERVAL_OR_PERCENTILE"
    WITHHELD = "WITHHELD"
    CLASSIFY_AS = "CLASSIFY_AS"
    CLASSIFY_AS_CLASS = "CLASSIFY_AS_CLASS"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                self.THIN_STEP,
                "size of grid used for thinning",
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(self.OPERATION, "keep particular point per cell", self.OPERATIONS, False, 0)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.THRESHOLD_OR_INTERVAL_OR_PERCENTILE,
                "adaptive threshold, contour intervals, or percentile",
                QgsProcessingParameterNumber.Double,
                1.0,
                False,
                0.0,
                100.0,
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(self.WITHHELD, "mark thinned-away points as withheld", False))
        self.addParameter(QgsProcessingParameterBoolean(self.CLASSIFY_AS, "classify surviving points as", False))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CLASSIFY_AS_CLASS,
                "classification code",
                QgsProcessingParameterNumber.Integer,
                8,
                False,
                0,
                255,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
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
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, self.THIN_STEP, context)
        if step != 1.0:
            commands.append("-step")
            commands.append(str(step))
        operation = self.parameterAsInt(parameters, self.OPERATION, context)
        if operation != 0:
            commands.append("-" + self.OPERATIONS[operation])
        if operation >= 4:
            commands.append(str(self.parameterAsDouble(parameters, self.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, context)))
        if self.parameterAsBool(parameters, self.WITHHELD, context):
            commands.append("-withheld")
        if self.parameterAsBool(parameters, self.CLASSIFY_AS, context):
            commands.append("-classify_as")
            commands.append(str(self.parameterAsInt(parameters, self.CLASSIFY_AS_CLASS, context)))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasThinPro()

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

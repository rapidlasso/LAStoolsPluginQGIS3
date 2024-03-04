# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasheight.py
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


class LasHeight(LastoolsAlgorithm):
    TOOL_NAME = "LasHeight"
    LASTOOL = "lasheight"
    LICENSE = "c"
    LASGROUP = 5
    REPLACE_Z = "REPLACE_Z"
    DROP_ABOVE = "DROP_ABOVE"
    DROP_ABOVE_HEIGHT = "DROP_ABOVE_HEIGHT"
    DROP_BELOW = "DROP_BELOW"
    DROP_BELOW_HEIGHT = "DROP_BELOW_HEIGHT"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterBoolean(LasHeight.REPLACE_Z, "replace z", False))
        self.addParameter(QgsProcessingParameterBoolean(LasHeight.DROP_ABOVE, "drop above", False))
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeight.DROP_ABOVE_HEIGHT, "drop above height", QgsProcessingParameterNumber.Double, 100.0
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(LasHeight.DROP_BELOW, "drop below", False))
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeight.DROP_BELOW_HEIGHT, "drop below height", QgsProcessingParameterNumber.Double, -2.0
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasHeight.REPLACE_Z, context):
            commands.append("-replace_z")
        if self.parameterAsBool(parameters, LasHeight.DROP_ABOVE, context):
            commands.append("-drop_above")
            commands.append(str(self.parameterAsDouble(parameters, LasHeight.DROP_ABOVE_HEIGHT, context)))
        if self.parameterAsBool(parameters, LasHeight.DROP_BELOW, context):
            commands.append("-drop_below")
            commands.append(str(self.parameterAsDouble(parameters, LasHeight.DROP_BELOW_HEIGHT, context)))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasHeight()

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


class LasHeightClassify(LastoolsAlgorithm):
    TOOL_NAME = "LasHeightClassify"
    LASTOOL = "lasheight"
    LICENSE = "c"
    LASGROUP = 5
    REPLACE_Z = "REPLACE_Z"
    CLASSIFY_BELOW = "CLASSIFY_BELOW"
    CLASSIFY_BELOW_HEIGHT = "CLASSIFY_BELOW_HEIGHT"
    CLASSIFY_BETWEEN1 = "CLASSIFY_BETWEEN1"
    CLASSIFY_BETWEEN1_HEIGHT_FROM = "CLASSIFY_BETWEEN1_HEIGHT_FROM"
    CLASSIFY_BETWEEN1_HEIGHT_TO = "CLASSIFY_BETWEEN1_HEIGHT_TO"
    CLASSIFY_BETWEEN2 = "CLASSIFY_BETWEEN2"
    CLASSIFY_BETWEEN2_HEIGHT_FROM = "CLASSIFY_BETWEEN2_HEIGHT_FROM"
    CLASSIFY_BETWEEN2_HEIGHT_TO = "CLASSIFY_BETWEEN2_HEIGHT_TO"
    CLASSIFY_ABOVE = "CLASSIFY_ABOVE"
    CLASSIFY_ABOVE_HEIGHT = "CLASSIFY_ABOVE_HEIGHT"

    CLASSIFY_CLASSES = [
        "---",
        "never classified (0)",
        "unclassified (1)",
        "ground (2)",
        "veg low (3)",
        "veg mid (4)",
        "veg high (5)",
        "buildings (6)",
        "noise (7)",
        "keypoint (8)",
        "water (9)",
        "water (9)",
        "rail (10)",
        "road surface (11)",
        "overlap (12)",
    ]

    def initAlgorithm(self, config):
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterBoolean(LasHeightClassify.REPLACE_Z, "replace z", False))
        self.addParameter(
            QgsProcessingParameterEnum(
                LasHeightClassify.CLASSIFY_BELOW,
                "classify below height as",
                LasHeightClassify.CLASSIFY_CLASSES,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightClassify.CLASSIFY_BELOW_HEIGHT,
                "below height",
                QgsProcessingParameterNumber.Double,
                -2.0,
                False,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                LasHeightClassify.CLASSIFY_BETWEEN1,
                "classify between height as",
                LasHeightClassify.CLASSIFY_CLASSES,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightClassify.CLASSIFY_BETWEEN1_HEIGHT_FROM,
                "between height ... ",
                QgsProcessingParameterNumber.Double,
                0.5,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightClassify.CLASSIFY_BETWEEN1_HEIGHT_TO,
                "... and height",
                QgsProcessingParameterNumber.Double,
                2.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                LasHeightClassify.CLASSIFY_BETWEEN2,
                "classify between height as",
                LasHeightClassify.CLASSIFY_CLASSES,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightClassify.CLASSIFY_BETWEEN2_HEIGHT_FROM,
                "between height ...",
                QgsProcessingParameterNumber.Double,
                2.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightClassify.CLASSIFY_BETWEEN2_HEIGHT_TO,
                "... and height",
                QgsProcessingParameterNumber.Double,
                5.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                LasHeightClassify.CLASSIFY_ABOVE, "classify above", LasHeightClassify.CLASSIFY_CLASSES, False, 0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightClassify.CLASSIFY_ABOVE_HEIGHT,
                "classify above height",
                QgsProcessingParameterNumber.Double,
                100.0,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasHeightClassify.REPLACE_Z, context):
            commands.append("-replace_z")
        classify = self.parameterAsInt(parameters, LasHeightClassify.CLASSIFY_BELOW, context)
        if classify != 0:
            commands.append("-classify_below")
            commands.append(str(self.parameterAsDouble(parameters, LasHeightClassify.CLASSIFY_BELOW_HEIGHT, context)))
            commands.append(str(classify - 1))
        classify = self.parameterAsInt(parameters, LasHeightClassify.CLASSIFY_BETWEEN1, context)
        if classify != 0:
            commands.append("-classify_between")
            commands.append(
                str(self.parameterAsDouble(parameters, LasHeightClassify.CLASSIFY_BETWEEN1_HEIGHT_FROM, context))
            )
            commands.append(
                str(self.parameterAsDouble(parameters, LasHeightClassify.CLASSIFY_BETWEEN1_HEIGHT_TO, context))
            )
            commands.append(str(classify - 1))
        classify = self.parameterAsInt(parameters, LasHeightClassify.CLASSIFY_BETWEEN2, context)
        if classify != 0:
            commands.append("-classify_between")
            commands.append(
                str(self.parameterAsDouble(parameters, LasHeightClassify.CLASSIFY_BETWEEN2_HEIGHT_FROM, context))
            )
            commands.append(
                str(self.parameterAsDouble(parameters, LasHeightClassify.CLASSIFY_BETWEEN2_HEIGHT_TO, context))
            )
            commands.append(str(classify - 1))
        classify = self.parameterAsInt(parameters, LasHeightClassify.CLASSIFY_ABOVE, context)
        if classify != 0:
            commands.append("-classify_above")
            commands.append(str(self.parameterAsDouble(parameters, LasHeightClassify.CLASSIFY_ABOVE_HEIGHT, context)))
            commands.append(str(classify - 1))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasHeightClassify()

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


class LasHeightPro(LastoolsAlgorithm):
    TOOL_NAME = "LasHeightPro"
    LASTOOL = "lasheight"
    LICENSE = "c"
    LASGROUP = 5
    REPLACE_Z = "REPLACE_Z"
    DROP_ABOVE = "DROP_ABOVE"
    DROP_ABOVE_HEIGHT = "DROP_ABOVE_HEIGHT"
    DROP_BELOW = "DROP_BELOW"
    DROP_BELOW_HEIGHT = "DROP_BELOW_HEIGHT"

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterBoolean(LasHeightPro.REPLACE_Z, "replace z", False))
        self.addParameter(QgsProcessingParameterBoolean(LasHeightPro.DROP_ABOVE, "drop above", False))
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightPro.DROP_ABOVE_HEIGHT, "drop above height", QgsProcessingParameterNumber.Double, 100.0
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(LasHeightPro.DROP_BELOW, "drop below", False))
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightPro.DROP_BELOW_HEIGHT, "drop below height", QgsProcessingParameterNumber.Double, -2.0
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasHeightPro.REPLACE_Z, context):
            commands.append("-replace_z")
        if self.parameterAsBool(parameters, LasHeightPro.DROP_ABOVE, context):
            commands.append("-drop_above")
            commands.append(str(self.parameterAsDouble(parameters, LasHeightPro.DROP_ABOVE_HEIGHT, context)))
        if self.parameterAsBool(parameters, LasHeightPro.DROP_BELOW, context):
            commands.append("-drop_below")
            commands.append(str(self.parameterAsDouble(parameters, LasHeightPro.DROP_BELOW_HEIGHT, context)))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasHeightPro()

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


class LasHeightProClassify(LastoolsAlgorithm):
    TOOL_NAME = "LasHeightProClassify"
    LASTOOL = "lasheight"
    LICENSE = "c"
    LASGROUP = 5
    REPLACE_Z = "REPLACE_Z"
    CLASSIFY_BELOW = "CLASSIFY_BELOW"
    CLASSIFY_BELOW_HEIGHT = "CLASSIFY_BELOW_HEIGHT"
    CLASSIFY_BETWEEN1 = "CLASSIFY_BETWEEN1"
    CLASSIFY_BETWEEN1_HEIGHT_FROM = "CLASSIFY_BETWEEN1_HEIGHT_FROM"
    CLASSIFY_BETWEEN1_HEIGHT_TO = "CLASSIFY_BETWEEN1_HEIGHT_TO"
    CLASSIFY_BETWEEN2 = "CLASSIFY_BETWEEN2"
    CLASSIFY_BETWEEN2_HEIGHT_FROM = "CLASSIFY_BETWEEN2_HEIGHT_FROM"
    CLASSIFY_BETWEEN2_HEIGHT_TO = "CLASSIFY_BETWEEN2_HEIGHT_TO"
    CLASSIFY_ABOVE = "CLASSIFY_ABOVE"
    CLASSIFY_ABOVE_HEIGHT = "CLASSIFY_ABOVE_HEIGHT"

    CLASSIFY_CLASSES = [
        "---",
        "never classified (0)",
        "unclassified (1)",
        "ground (2)",
        "veg low (3)",
        "veg mid (4)",
        "veg high (5)",
        "buildings (6)",
        "noise (7)",
        "keypoint (8)",
        "water (9)",
        "water (9)",
        "rail (10)",
        "road surface (11)",
        "overlap (12)",
    ]

    def initAlgorithm(self, config=None):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterBoolean(LasHeightProClassify.REPLACE_Z, "replace z", False))
        self.addParameter(
            QgsProcessingParameterEnum(
                LasHeightProClassify.CLASSIFY_BELOW,
                "classify below height as",
                LasHeightProClassify.CLASSIFY_CLASSES,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightProClassify.CLASSIFY_BELOW_HEIGHT,
                "below height",
                QgsProcessingParameterNumber.Double,
                -2.0,
                False,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                LasHeightProClassify.CLASSIFY_BETWEEN1,
                "classify between height as",
                LasHeightProClassify.CLASSIFY_CLASSES,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightProClassify.CLASSIFY_BETWEEN1_HEIGHT_FROM,
                "between height ... ",
                QgsProcessingParameterNumber.Double,
                0.5,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightProClassify.CLASSIFY_BETWEEN1_HEIGHT_TO,
                "... and height",
                QgsProcessingParameterNumber.Double,
                2.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                LasHeightProClassify.CLASSIFY_BETWEEN2,
                "classify between height as",
                LasHeightProClassify.CLASSIFY_CLASSES,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightProClassify.CLASSIFY_BETWEEN2_HEIGHT_FROM,
                "between height ...",
                QgsProcessingParameterNumber.Double,
                2.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightProClassify.CLASSIFY_BETWEEN2_HEIGHT_TO,
                "... and height",
                QgsProcessingParameterNumber.Double,
                5.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                LasHeightProClassify.CLASSIFY_ABOVE, "classify above", LasHeightProClassify.CLASSIFY_CLASSES, False, 0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                LasHeightProClassify.CLASSIFY_ABOVE_HEIGHT,
                "classify above height",
                QgsProcessingParameterNumber.Double,
                100.0,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui_64()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasheight")]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        if self.parameterAsBool(parameters, LasHeightProClassify.REPLACE_Z, context):
            commands.append("-replace_z")
        classify = self.parameterAsInt(parameters, LasHeightProClassify.CLASSIFY_BELOW, context)
        if classify != 0:
            commands.append("-classify_below")
            commands.append(
                str(self.parameterAsDouble(parameters, LasHeightProClassify.CLASSIFY_BELOW_HEIGHT, context))
            )
            commands.append(str(classify - 1))
        classify = self.parameterAsInt(parameters, LasHeightProClassify.CLASSIFY_BETWEEN1, context)
        if classify != 0:
            commands.append("-classify_between")
            commands.append(
                str(self.parameterAsDouble(parameters, LasHeightProClassify.CLASSIFY_BETWEEN1_HEIGHT_FROM, context))
            )
            commands.append(
                str(self.parameterAsDouble(parameters, LasHeightProClassify.CLASSIFY_BETWEEN1_HEIGHT_TO, context))
            )
            commands.append(str(classify - 1))
        classify = self.parameterAsInt(parameters, LasHeightProClassify.CLASSIFY_BETWEEN2, context)
        if classify != 0:
            commands.append("-classify_between")
            commands.append(
                str(self.parameterAsDouble(parameters, LasHeightProClassify.CLASSIFY_BETWEEN2_HEIGHT_FROM, context))
            )
            commands.append(
                str(self.parameterAsDouble(parameters, LasHeightProClassify.CLASSIFY_BETWEEN2_HEIGHT_TO, context))
            )
            commands.append(str(classify - 1))
        classify = self.parameterAsInt(parameters, LasHeightProClassify.CLASSIFY_ABOVE, context)
        if classify != 0:
            commands.append("-classify_above")
            commands.append(
                str(self.parameterAsDouble(parameters, LasHeightProClassify.CLASSIFY_ABOVE_HEIGHT, context))
            )
            commands.append(str(classify - 1))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_gui_64_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        LastoolsUtils.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasHeightProClassify()

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

# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasthin.py
    ---------------------
    Date                 : September 2013, May 2016 and August 2018
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

__author__ = 'Martin Isenburg'
__date__ = 'September 2013'
__copyright__ = '(C) 2013, rapidlasso GmbH'

import os

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterNumber, QgsProcessingParameterEnum

from ..utils import LastoolsUtils, descript_classification_filtering as descript_info, paths
from ..algo import LastoolsAlgorithm


class LasThin(LastoolsAlgorithm):
    TOOL_INFO = ('lasthin', 'LasThin')
    THIN_STEP = "THIN_STEP"
    OPERATION = "OPERATION"
    OPERATIONS = ["lowest", "random", "highest", "central", "adaptive", "contours", "percentile"]
    THRESHOLD_OR_INTERVAL_OR_PERCENTILE = "THRESHOLD_OR_INTERVAL_OR_PERCENTILE"
    WITHHELD = "WITHHELD"
    CLASSIFY_AS = "CLASSIFY_AS"
    CLASSIFY_AS_CLASS = "CLASSIFY_AS_CLASS"

    def initAlgorithm(self, config=None):
        self.add_parameters_verbose_gui64()
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(QgsProcessingParameterNumber(
            LasThin.THIN_STEP, "size of grid used for thinning", QgsProcessingParameterNumber.Double, 1.0, False, 0.0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasThin.OPERATION, "keep particular point per cell", LasThin.OPERATIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasThin.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, "adaptive threshold, contour intervals, or percentile",
            QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 100.0
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasThin.WITHHELD, "mark thinned-away points as withheld", False
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasThin.CLASSIFY_AS, "classify surviving points as", False
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasThin.CLASSIFY_AS_CLASS, "classification code", QgsProcessingParameterNumber.Integer, 8, False, 0, 255
        ))
        self.add_parameters_point_output_gui()
        self.add_parameters_additional_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasthin")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, LasThin.THIN_STEP, context)
        if step != 1.0:
            commands.append("-step")
            commands.append(str(step))
        operation = self.parameterAsInt(parameters, LasThin.OPERATION, context)
        if operation != 0:
            commands.append("-" + self.OPERATIONS[operation])
        if operation >= 4:
            commands.append(
                str(self.parameterAsDouble(parameters, LasThin.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, context))
            )
        if self.parameterAsBool(parameters, LasThin.WITHHELD, context):
            commands.append("-withheld")
        if self.parameterAsBool(parameters, LasThin.CLASSIFY_AS, context):
            commands.append("-classify_as")
            commands.append(str(self.parameterAsInt(parameters, LasThin.CLASSIFY_AS_CLASS, context)))
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasThin()

    def name(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["name"]

    def displayName(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["display_name"]

    def group(self):
        return descript_info["info"]["group"]

    def groupId(self):
        return descript_info["info"]["group_id"]

    def helpUrl(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["url_path"]

    def shortHelpString(self):
        return self.tr(descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_help_string"])

    def shortDescription(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_description"]

    def icon(self):
        img_path = 'licenced.png' \
            if descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence"] else 'open_source.png'
        return QIcon(f"{paths['img']}{img_path}")


class LasThinPro(LastoolsAlgorithm):
    TOOL_INFO = ('lasthin', 'LasThinPro')
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
        self.addParameter(QgsProcessingParameterNumber(
            LasThinPro.THIN_STEP, "size of grid used for thinning",
            QgsProcessingParameterNumber.Double, 1.0, False, 0.0
        ))
        self.addParameter(QgsProcessingParameterEnum(
            LasThinPro.OPERATION, "keep particular point per cell", LasThinPro.OPERATIONS, False, 0
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasThinPro.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, "adaptive threshold, contour intervals, or percentile",
            QgsProcessingParameterNumber.Double, 1.0, False, 0.0, 100.0
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasThinPro.WITHHELD, "mark thinned-away points as withheld", False
        ))
        self.addParameter(QgsProcessingParameterBoolean(
            LasThinPro.CLASSIFY_AS, "classify surviving points as", False
        ))
        self.addParameter(QgsProcessingParameterNumber(
            LasThinPro.CLASSIFY_AS_CLASS, "classification code", QgsProcessingParameterNumber.Integer, 8, False, 0, 255
        ))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LastoolsUtils.lastools_path(), "bin", "lasthin")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, LasThinPro.THIN_STEP, context)
        if step != 1.0:
            commands.append("-step")
            commands.append(str(step))
        operation = self.parameterAsInt(parameters, LasThinPro.OPERATION, context)
        if operation != 0:
            commands.append("-" + self.OPERATIONS[operation])
        if operation >= 4:
            commands.append(str(
                self.parameterAsDouble(parameters, LasThinPro.THRESHOLD_OR_INTERVAL_OR_PERCENTILE, context))
            )
        if self.parameterAsBool(parameters, LasThinPro.WITHHELD, context):
            commands.append("-withheld")
        if self.parameterAsBool(parameters, LasThinPro.CLASSIFY_AS, context):
            commands.append("-classify_as")
            commands.append(str(self.parameterAsInt(parameters, LasThinPro.CLASSIFY_AS_CLASS, context)))
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LastoolsUtils.run_lastools(commands, feedback)

        return {"commands": commands}

    def createInstance(self):
        return LasThinPro()

    def name(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["name"]

    def displayName(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["display_name"]

    def group(self):
        return descript_info["info"]["group"]

    def groupId(self):
        return descript_info["info"]["group_id"]

    def helpUrl(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["url_path"]

    def shortHelpString(self):
        return self.tr(descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_help_string"])

    def shortDescription(self):
        return descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["short_description"]

    def icon(self):
        img_path = 'licenced.png' \
            if descript_info["items"][self.TOOL_INFO[0]][self.TOOL_INFO[1]]["licence"] else 'open_source.png'
        return QIcon(f"{paths['img']}{img_path}")

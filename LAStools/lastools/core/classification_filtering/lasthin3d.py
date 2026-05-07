# -*- coding: utf-8 -*-
"""
***************************************************************************
    lasthin3d.py
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


from qgis.core import (
  QgsProcessingParameterBoolean,
  QgsProcessingParameterEnum,
  QgsProcessingParameterNumber,
  QgsProcessingParameterDefinition,
)
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url

# gl
OPERATION = "OPERATION"
OPERATION_DESC = "keep this point per cell"
OPERATIONS = [ # names must match the lasthin3d-argument name!
    "closest", #0
    "highest", 
    "lowest", 
    "use_cell_center",
    "random_cell_occurrence", 
    "every_nth", #5 [n] 
    "random_nth", #6 [n] 
    "intensity_min", 
    "intensity_max", 
    "return_min", 
    "return_max", 
    "attribute_min", #11 [n] 
    "attribute_max", #12 [n] 
    ]
OPERATIONS_WITH_PARAM = {5,6,11,12}
TARGET_POINT_PARAM = "TARGET_POINT_PARAM"
TARGET_POINT_PARAM_DESC = "additional parameter (for every_nth, random_nth and attribute)"
THIN_STEP = "THIN_STEP"
THIN_STEP_DESC = "size of grid used for thinning"
WITHHELD = "WITHHELD"
WITHHELD_DESC = "mark thinned-away points as withheld"
CLASSIFY_AS = "CLASSIFY_AS"
CLASSIFY_AS_DESC = "classify surviving points as"
CLASSIFY_AS_CLASS = "CLASSIFY_AS_CLASS"
CLASSIFY_AS_CLASS_DESC = "classification code"
COUNT_USER_BYTE = "COUNT_USER_BYTE"
COUNT_USER_BYTE_DESC = "counts number of points per cell to 'user byte'"

class LasThin3d(LastoolsAlgorithm):
    # local vars, needed by base class
    TOOL_NAME = "LasThin3d"
    LASTOOL = "lasthin3d"
    LICENSE = "c"
    LASGROUP = 4

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                THIN_STEP,
                THIN_STEP_DESC,
                QgsProcessingParameterNumber.Double,
                1.0,False,0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
              OPERATION,
              OPERATION_DESC,
              OPERATIONS, 
              False, 
              0
            )
        )
        self.addParameter(
             QgsProcessingParameterNumber(
                TARGET_POINT_PARAM,
                TARGET_POINT_PARAM_DESC,
                QgsProcessingParameterNumber.Integer,
                5.0, False, 1.0, 10000.0)
        )
        self.addParameter(QgsProcessingParameterBoolean(COUNT_USER_BYTE, COUNT_USER_BYTE_DESC, False))
        self.addParameter(QgsProcessingParameterBoolean(WITHHELD, WITHHELD_DESC, False))
        self.addParameter(QgsProcessingParameterBoolean(CLASSIFY_AS, CLASSIFY_AS_DESC, False))
        self.addParameter(
            QgsProcessingParameterNumber(
                CLASSIFY_AS_CLASS, CLASSIFY_AS_CLASS_DESC, QgsProcessingParameterNumber.Integer, 8, False, 0, 255
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_point_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, THIN_STEP, context)
        if step != 1.0:
            commands.append("-step")
            commands.append(str(step))
        operation = self.parameterAsInt(parameters, OPERATION, context)
        if operation != 0:
            commands.append("-" + OPERATIONS[operation])
        if operation in OPERATIONS_WITH_PARAM:
            commands.append(str(self.parameterAsDouble(parameters, TARGET_POINT_PARAM, context)))
        if self.parameterAsBool(parameters, COUNT_USER_BYTE, context):
            commands.append("-count_to_user_byte")
        if self.parameterAsBool(parameters, WITHHELD, context):
            commands.append("-withheld")
        if self.parameterAsBool(parameters, CLASSIFY_AS, context):
            commands.append("-classify_as")
            commands.append(str(self.parameterAsInt(parameters, CLASSIFY_AS_CLASS, context)))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_point_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasThin3d()

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


class LasThin3dPro(LastoolsAlgorithm):
    # local vars, needed by base class
    TOOL_NAME = "LasThin3dPro"
    LASTOOL = "lasthin3d"
    LICENSE = "c"
    LASGROUP = 4

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_ignore_class1_gui()
        self.add_parameters_ignore_class2_gui()
        self.addParameter(
            QgsProcessingParameterNumber(
                THIN_STEP,
                THIN_STEP_DESC,
                QgsProcessingParameterNumber.Double,
                1.0,False,0.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
              OPERATION,
              OPERATION_DESC,
              OPERATIONS, False, 0)
        )
        self.addParameter(
             QgsProcessingParameterNumber(
                TARGET_POINT_PARAM,
                TARGET_POINT_PARAM_DESC,
                QgsProcessingParameterNumber.Integer,
                5.0, False, 1.0, 10000.0)
        )
        self.addParameter(QgsProcessingParameterBoolean(COUNT_USER_BYTE, COUNT_USER_BYTE_DESC, False))
        self.addParameter(QgsProcessingParameterBoolean(WITHHELD, WITHHELD_DESC, False))
        self.addParameter(QgsProcessingParameterBoolean(CLASSIFY_AS, CLASSIFY_AS_DESC, False))
        self.addParameter(
            QgsProcessingParameterNumber(
                CLASSIFY_AS_CLASS,
                CLASSIFY_AS_CLASS_DESC,
                QgsProcessingParameterNumber.Integer,
                8,
                False,
                0,
                255,
            )
        )
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_ignore_class1_commands(parameters, context, commands)
        self.add_parameters_ignore_class2_commands(parameters, context, commands)
        step = self.parameterAsDouble(parameters, THIN_STEP, context)
        if step != 1.0:
            commands.append("-step")
            commands.append(str(step))
        operation = self.parameterAsInt(parameters, OPERATION, context)
        if operation != 0:
            commands.append("-" + OPERATIONS[operation])
        if operation in OPERATIONS_WITH_PARAM:
            commands.append(str(self.parameterAsDouble(parameters, TARGET_POINT_PARAM, context)))
        if self.parameterAsBool(parameters, COUNT_USER_BYTE, context):
            commands.append("-count_to_user_byte")
        if self.parameterAsBool(parameters, WITHHELD, context):
            commands.append("-withheld")
        if self.parameterAsBool(parameters, CLASSIFY_AS, context):
            commands.append("-classify_as")
            commands.append(str(self.parameterAsInt(parameters, CLASSIFY_AS_CLASS, context)))
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"commands": commands}

    def createInstance(self):
        return LasThin3dPro()

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

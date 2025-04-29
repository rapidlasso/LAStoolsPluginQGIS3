# -*- coding: utf-8 -*-
"""
***************************************************************************
    lasboundary.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
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

__author__ = "Victor Olaya"
__date__ = "August 2012"
__copyright__ = "(C) 2012, Victor Olaya"


from qgis.core import QgsProcessingParameterBoolean, QgsProcessingParameterEnum, QgsProcessingParameterNumber
from qgis.PyQt.QtGui import QIcon

from ..algo import LastoolsAlgorithm
from ..utils import LastoolsUtils, help_string_help, lasgroup_info, lastool_info, licence, paths, readme_url


class LasBoundary(LastoolsAlgorithm):
    TOOL_NAME = "LasBoundary"
    LASTOOL = "lasboundary"
    LICENSE = "c"
    LASGROUP = 3
    MODE = "MODE"
    MODES = ["points", "spatial index (the *.lax file)", "bounding box", "tile bounding box"]
    CONCAVITY = "CONCAVITY"
    HOLES = "HOLES"
    DISJOINT = "DISJOINT"
    LABELS = "LABELS"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.addParameter(QgsProcessingParameterEnum(self.MODE, "compute boundary based on", self.MODES, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CONCAVITY, "concavity", QgsProcessingParameterNumber.Double, 50.0, False, 0.0001
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(self.HOLES, "interior holes", False))
        self.addParameter(QgsProcessingParameterBoolean(self.DISJOINT, "disjoint polygon", False))
        self.addParameter(QgsProcessingParameterBoolean(self.LABELS, "produce labels", False))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_vector_output_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        mode = self.parameterAsInt(parameters, self.MODE, context)
        if mode != 0:
            if mode == 1:
                commands.append("-use_lax")
            elif mode == 2:
                commands.append("-use_bb")
            else:
                commands.append("-use_tile_bb")
        else:
            concavity = self.parameterAsDouble(parameters, self.CONCAVITY, context)
            commands.append("-concavity")
            commands.append(str(concavity))
            if self.parameterAsBool(parameters, self.HOLES, context):
                commands.append("-holes")
            if self.parameterAsBool(parameters, self.DISJOINT, context):
                commands.append("-disjoint")
            if self.parameterAsBool(parameters, self.LABELS, context):
                commands.append("-labels")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_vector_output_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"command": commands}

    def createInstance(self):
        return LasBoundary()

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


class LasBoundaryPro(LastoolsAlgorithm):
    TOOL_NAME = "LasBoundaryPro"
    LASTOOL = "lasboundary"
    LICENSE = "c"
    LASGROUP = 3
    MODE = "MODE"
    MODES = ["points", "spatial index (the *.lax file)", "bounding box", "tile bounding box"]
    CONCAVITY = "CONCAVITY"
    HOLES = "HOLES"
    DISJOINT = "DISJOINT"
    LABELS = "LABELS"

    def initAlgorithm(self, config=None):
        super().initAlgorithm(config)
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_filter1_return_class_flags_gui()
        self.addParameter(QgsProcessingParameterEnum(self.MODE, "compute boundary based on", self.MODES, False, 0))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CONCAVITY, "concavity", QgsProcessingParameterNumber.Double, 50.0, False, 0.0001
            )
        )
        self.addParameter(QgsProcessingParameterBoolean(self.HOLES, "interior holes", False))
        self.addParameter(QgsProcessingParameterBoolean(self.DISJOINT, "disjoint polygon", False))
        self.addParameter(QgsProcessingParameterBoolean(self.LABELS, "produce labels", False))
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_64_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_vector_output_format_gui()
        self.add_parameters_output_directory_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [self.get_command(parameters, context, feedback)]
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_filter1_return_class_flags_commands(parameters, context, commands)
        mode = self.parameterAsInt(parameters, self.MODE, context)
        if mode != 0:
            if mode == 1:
                commands.append("-use_lax")
            elif mode == 2:
                commands.append("-use_bb")
            else:
                commands.append("-use_tile_bb")
        else:
            concavity = self.parameterAsDouble(parameters, self.CONCAVITY, context)
            commands.append("-concavity")
            commands.append(str(concavity))
            if self.parameterAsBool(parameters, self.HOLES, context):
                commands.append("-holes")
            if self.parameterAsBool(parameters, self.DISJOINT, context):
                commands.append("-disjoint")
            if self.parameterAsBool(parameters, self.LABELS, context):
                commands.append("-labels")
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)
        self.add_parameters_verbose_64_gui_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_vector_output_format_commands(parameters, context, commands)
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.run_lastools(commands, feedback)
        return {"command": commands}

    def createInstance(self):
        return LasBoundaryPro()

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

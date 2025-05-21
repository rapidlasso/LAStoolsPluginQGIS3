# -*- coding: utf-8 -*-
"""
***************************************************************************
    lastools_algorithm.py
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

import re
import os
from qgis.core import (
    Qgis,
    QgsProcessingAlgorithm,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsMessageLog,
    QgsProcessingException,
)
from qgis.PyQt.QtCore import QCoreApplication
from processing.tools.system import isWindows

from ..utils import LastoolsUtils

class LastoolsAlgorithm(QgsProcessingAlgorithm):
        
    VERBOSE = "VERBOSE"
    CPU64 = "CPU64"
    GUI = "GUI"
    CORES = "CORES"
    INPUT_GENERIC = "INPUT_GENERIC"
    INPUT_GENERIC_DIRECTORY = "INPUT_GENERIC_DIRECTORY"
    INPUT_GENERIC_WILDCARDS = "INPUT_GENERIC_WILDCARDS"
    INPUT_LASLAZ = "INPUT_LASLAZ"
    INPUT_DIRECTORY = "INPUT_DIRECTORY"
    INPUT_WILDCARDS = "INPUT_WILDCARDS"
    MERGED = "MERGED"
    OUTPUT_GENERIC = "OUTPUT_GENERIC"
    OUTPUT_LASLAZ = "OUTPUT_LASLAZ"
    OUTPUT_DIRECTORY = "OUTPUT_DIRECTORY"
    OUTPUT_APPENDIX = "OUTPUT_APPENDIX"
    OUTPUT_POINT_FORMAT = "OUTPUT_POINT_FORMAT"
    OUTPUT_POINT_FORMATS = ["laz", "las"]
    OUTPUT_RASTER = "OUTPUT_RASTER"
    OUTPUT_RASTER_FORMAT = "OUTPUT_RASTER_FORMAT"
    OUTPUT_RASTER_FORMATS = ["tif", "bil", "img", "dtm", "asc", "xyz", "png", "jpg", "laz"]
    OUTPUT_VECTOR = "OUTPUT_VECTOR"
    OUTPUT_VECTOR_FORMAT = "OUTPUT_VECTOR_FORMAT"
    OUTPUT_VECTOR_FORMATS = ["shp", "wkt", "kml", "txt"]
    ADDITIONAL_OPTIONS = "ADDITIONAL_OPTIONS"
    TEMPORARY_DIRECTORY = "TEMPORARY_DIRECTORY"
    HORIZONTAL_FEET = "HORIZONTAL_FEET"
    VERTICAL_FEET = "VERTICAL_FEET"
    FILES_ARE_FLIGHTLINES = "FILES_ARE_FLIGHTLINES"
    APPLY_FILE_SOURCE_ID = "APPLY_FILE_SOURCE_ID"
    STEP = "STEP"
    FILE_FILTER_LASLAZ = "LAZ/LAS files (*.las *.laz);;TXT-files (*.txt);;All files (*.*))"

    # Generic options that should be reimplemented in child classes
    TOOL_NAME = "Generic"
    LASTOOL = "generic"
    LICENSE = "o"
    LASGROUP = 1

    def __init__(self):
        super().__init__()
        self.canGui = True
        self.canCpu64 = True
        self.has32 = False
        self.has64 = False
        self.isCpu64 = False

    @staticmethod
    def tr(string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate("Processing", string)

    @staticmethod
    def command_ext():
        if LastoolsUtils.has_wine() or isWindows():
            return ".exe"
        else:
            return ""

    @staticmethod
    def pathwrap(inpath):
        # warp path containing spaces with "..."
        if inpath.find(" ")>=0:
            return '"' + inpath + '"'
        else:
            return inpath

    def cpu64ext(self):
        return "64" if self.isCpu64 else ""

    # called already at plugin load and on each tool load
    def initAlgorithm(self, config=None):
        LastoolsUtils.lastools_check_path()
        # check for avaliable 32/64 bit versions
        file32 = ""
        file64 = ""
        if LastoolsUtils.has_wine() or isWindows():
            file32 = os.path.join(LastoolsUtils.lastools_path(),self.LASTOOL+".exe")
            file64 = os.path.join(LastoolsUtils.lastools_path(),self.LASTOOL+"64.exe")
            self.has32 = os.path.isfile(file32)
            self.has64 = os.path.isfile(file64)
            LastoolsUtils.debug(f"[{self.LASTOOL}] versions = {'32' if self.has32 else ''} {'64' if self.has64 else ''}")
        else:
            self.has32 = False
            file64 = os.path.join(LastoolsUtils.lastools_path(),self.LASTOOL+"64")
            self.has64 = os.path.isfile(file64)
        if not self.has32 and not self.has64:
            LastoolsUtils.log(f"[{self.LASTOOL}] No exe found at [{LastoolsUtils.lastools_path()}]")
        self.canCpu64 = self.has32 and self.has64
        self.canGui = self.has32
        self.isCpu64 = self.has64

    def get_command(self, parameters, context, feedback):
        # check if 64 bit was changed by user
        if self.canCpu64:
            self.isCpu64 = self.parameterAsBool(parameters, self.CPU64, context)
        # we only get the COMMAND, path settings set on execution
        las_command = self.LASTOOL + self.cpu64ext() + self.command_ext()
        # report missing executeable
        if not self.has32 and not self.has64:
            feedback.reportError(f"Executeable {las_command} not found. Check configuration.")
        # check for license file - if no license at all: run in demo mode. otherwise fail if license is overdue
        isDemo = not os.path.isfile(os.path.join(LastoolsUtils.lastools_path(),"lastoolslicense.txt"))
        if isDemo and (self.LICENSE == "c") and self.isCpu64:
            feedback.pushWarning("No license file found. Run in demo mode.")
            las_command = f"{las_command} -demo"
        return las_command

    def run_lastools(self, commands, feedback):
        # add path to command
        commands[0] = self.pathwrap(os.path.join(LastoolsUtils.lastools_path(),commands[0]))
        # add optional wine
        if not isWindows() and LastoolsUtils.has_wine():
            command_prefix = self.pathwrap(LastoolsUtils.wine_folder())
            commands.insert(0,command_prefix)
        #
        if ("-gui" in commands) and (self.isCpu64):
            feedback.reportError("GUI not available at 64 bit")
        commandline = " ".join(commands)
        feedback.pushConsoleInfo("LAStools command line")
        feedback.pushConsoleInfo(commandline)
        feedback.pushConsoleInfo("LAStools console output")
        ret, output = LastoolsUtils.execute_command(commandline)
        # wrap ret on win32: unreliable
        if not self.isCpu64 or ("-cores" in commands):
            if "ERROR:" in output:
                ret = 3
            elif "WARNING:" in output:
                ret = 1
            else:
                ret = 0
        if ret >= 3:
            feedback.reportError(output)
        elif ret >= 1:
            feedback.pushWarning(output)
        else:
            feedback.pushConsoleInfo(output)

    def add_parameters_verbose_64_gui(self):
        self.addParameter(QgsProcessingParameterBoolean(self.VERBOSE, "verbose", True))
        if self.canCpu64:
            self.addParameter(QgsProcessingParameterBoolean(self.CPU64, "64 bit", True))
        if self.canGui:
            self.addParameter(QgsProcessingParameterBoolean(self.GUI, "open LAStools GUI", False))

    def add_parameters_verbose_64_gui_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, self.VERBOSE, context):
            commands.append("-v")
        if self.canGui and self.parameterAsBool(parameters, self.GUI, context):
            commands.append("-gui")

    def add_parameters_cores_gui(self):
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CORES, "number of cores", QgsProcessingParameterNumber.Integer, 4, False, 1, 32
            )
        )

    def add_parameters_cores_commands(self, parameters, context, commands):
        cores = self.parameterAsInt(parameters, self.CORES, context)
        if cores != 1:
            commands.append("-cores")
            commands.append(str(cores))

    def add_parameters_generic_input_gui(self, description, extension, optional):
        param = QgsProcessingParameterFile(self.INPUT_GENERIC, description, QgsProcessingParameterFile.File, extension, None, optional)
        if LastoolsUtils.isDebug():
            if extension == "laz":
                param.setDefaultValue('/lastools/data/in.laz') 
                param.setFileFilter(self.FILE_FILTER_LASLAZ)
            elif extension == "txt":
                param.setDefaultValue('/lastools/data/in.txt') 
            elif extension == "e57":
                param.setDefaultValue('/lastools/data/in.e57') 
            elif extension == "shp":
                param.setDefaultValue('/lastools/data/in.shp')
                param.setFileFilter("Shapefiles (*.shp);;CSV-files (*.csv);;All files (*.*))")                
            elif extension == "tif":
                param.setDefaultValue('/lastools/data/in.tif') 
                param.setFileFilter("Image files (*.tif *.tiff *.png *.jpg);;All files (*.*))")                
            elif extension == "csv":
                param.setDefaultValue('/lastools/data/in.csv')
        # optional external support for multipls file extensions (given filter string as extension input)
        if extension.find(';')>=0:
            param.setFileFilter(extension)
        self.addParameter(param)

    def add_parameters_generic_input_commands(self, parameters, context, commands, switch):
        input_generic = self.parameterAsString(parameters, self.INPUT_GENERIC, context)
        if input_generic != "":
            commands.append(switch)
            commands.append(self.pathwrap(input_generic))

    def add_parameters_generic_input_folder_gui(self, wildcard):
        param = QgsProcessingParameterFile(self.INPUT_GENERIC_DIRECTORY, "input directory", QgsProcessingParameterFile.Folder)
        if LastoolsUtils.isDebug():
            param.setDefaultValue('/lastools/data') 
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterString(self.INPUT_GENERIC_WILDCARDS, "input wildcard(s)", wildcard))

    def add_parameters_generic_input_folder_commands(self, parameters, context, commands):
        input_generic_directory = self.parameterAsString(parameters, self.INPUT_GENERIC_DIRECTORY, context)
        wildcards = self.parameterAsString(parameters, self.INPUT_GENERIC_WILDCARDS, context).split()
        for wildcard in wildcards:
            commands.append("-i")
            if input_generic_directory is not None:
                commands.append(os.path.join(self.pathwrap(input_generic_directory), wildcard))
            else:
                commands.append(self.pathwrap(wildcard))

    def add_parameters_point_input_gui(self):
        param = QgsProcessingParameterFile(self.INPUT_LASLAZ, "input LAS/LAZ file", QgsProcessingParameterFile.File)
        if LastoolsUtils.isDebug():
            param.setDefaultValue('/lastools/data/lake.laz') 
        param.setFileFilter("LAZ/LAS files (*.las *.laz);;TXT-files (*.txt);;All files (*.*))")
        self.addParameter(param)

    def add_parameters_point_input_commands(self, parameters, context, commands):
        input_las_laz = self.parameterAsString(parameters, self.INPUT_LASLAZ, context)
        if input_las_laz is not None:
            commands.append("-i")
            commands.append(self.pathwrap(input_las_laz))

    def add_parameters_point_input_folder_gui(self, uselas=False):
        param = QgsProcessingParameterFile(self.INPUT_DIRECTORY, "input directory", QgsProcessingParameterFile.Folder)
        if LastoolsUtils.isDebug():
            param.setDefaultValue('/lastools/data/tiles') 
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterString(self.INPUT_WILDCARDS, "input wildcard(s)", "*.laz" if uselas == False else "*.las"))

    def add_parameters_point_input_folder_commands(self, parameters, context, commands):
        input_directory = self.parameterAsString(parameters, self.INPUT_DIRECTORY, context)
        wildcards = self.parameterAsString(parameters, self.INPUT_WILDCARDS, context).split()
        for wildcard in wildcards:
            commands.append("-i")
            if input_directory is not None:
                commands.append(os.path.join(self.pathwrap(input_directory), wildcard))
            else:
                commands.append(self.pathwrap(wildcard))

    def add_parameters_point_input_merged_gui(self):
        self.addParameter(
            QgsProcessingParameterBoolean(self.MERGED, "merge all input files on-the-fly into one", False)
        )

    def add_parameters_point_input_merged_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, self.MERGED, context):
            commands.append("-merged")

    def add_parameters_horizontal_feet_gui(self):
        self.addParameter(QgsProcessingParameterBoolean(self.HORIZONTAL_FEET, "horizontal feet", False))

    def add_parameters_horizontal_feet_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, self.HORIZONTAL_FEET, context):
            commands.append("-feet")

    def add_parameters_vertical_feet_gui(self):
        self.addParameter(QgsProcessingParameterBoolean(self.VERTICAL_FEET, "vertical feet", False))

    def add_parameters_vertical_feet_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, self.VERTICAL_FEET, context):
            commands.append("-elevation_feet")

    def add_parameters_horizontal_and_vertical_feet_gui(self):
        self.add_parameters_horizontal_feet_gui()
        self.add_parameters_vertical_feet_gui()

    def add_parameters_horizontal_and_vertical_feet_commands(self, parameters, context, commands):
        self.add_parameters_horizontal_feet_commands(parameters, context, commands)
        self.add_parameters_vertical_feet_commands(parameters, context, commands)

    def add_parameters_files_are_flightlines_gui(self):
        self.addParameter(QgsProcessingParameterBoolean(self.FILES_ARE_FLIGHTLINES, "files are flightlines", False))

    def add_parameters_files_are_flightlines_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, self.FILES_ARE_FLIGHTLINES, context):
            commands.append("-files_are_flightlines")

    def add_parameters_apply_file_source_id_gui(self):
        self.addParameter(QgsProcessingParameterBoolean(self.APPLY_FILE_SOURCE_ID, "apply file source ID", False))

    def add_parameters_apply_file_source_id_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, self.APPLY_FILE_SOURCE_ID, context):
            commands.append("-apply_file_source_ID")

    def add_parameters_step_gui(self):
        self.addParameter(
            QgsProcessingParameterNumber(
                self.STEP, "step size / pixel size", QgsProcessingParameterNumber.Double, 1.0, False, 0
            )
        )

    def add_parameters_step_commands(self, parameters, context, commands):
        step = self.parameterAsDouble(parameters, self.STEP, context)
        if step != 0.0:
            commands.append("-step")
            commands.append(str(step))

    def get_parameters_step_value(self, parameters, context):
        step = self.parameterAsDouble(parameters, self.STEP, context)
        return step

    def add_parameters_generic_output_gui(self, description, extension, optional):
        param = QgsProcessingParameterFileDestination(self.OUTPUT_GENERIC, description, extension, "", optional, False)
        if LastoolsUtils.isDebug():
            param.setDefaultValue('/lastools/data/out') 
        self.addParameter(param)

    def add_parameters_generic_output_commands(self, parameters, context, commands, switch):
        output = self.parameterAsString(parameters, self.OUTPUT_GENERIC, context)
        if output != "":
            commands.append(switch)
            commands.append(self.pathwrap(output))

    def add_parameters_point_output_gui(self):
        param = QgsProcessingParameterFileDestination(self.OUTPUT_LASLAZ, "output LAS/LAZ file", "laz", "", True, False)
        if LastoolsUtils.isDebug():
            param.setDefaultValue('/lastools/data/out.laz') 
        self.addParameter(param)

    def add_parameters_point_output_commands(self, parameters, context, commands):
        output = self.parameterAsString(parameters, self.OUTPUT_LASLAZ, context)
        if output != "":
            commands.append("-o")
            commands.append(self.pathwrap(output))

    def add_parameters_point_output_format_gui(self, default=0):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.OUTPUT_POINT_FORMAT,
                "output format",
                self.OUTPUT_POINT_FORMATS,
                False,
                default,
            )
        )

    def add_parameters_point_output_format_commands(self, parameters, context, commands):
        format_output_point = self.parameterAsInt(parameters, self.OUTPUT_POINT_FORMAT, context)
        commands.append("-o" + self.OUTPUT_POINT_FORMATS[format_output_point])

    def add_parameters_raster_output_gui(self):
        param = QgsProcessingParameterFileDestination(self.OUTPUT_RASTER, "output raster file", "tif", "", True, False)
        if LastoolsUtils.isDebug():
            param.setDefaultValue('/lastools/data/out.tif') 
        self.addParameter(param)

    def add_parameters_raster_output_commands(self, parameters, context, commands):
        output = self.parameterAsString(parameters, self.OUTPUT_RASTER, context)
        if output != "":
            commands.append("-o")
            commands.append(self.pathwrap(output))

    def add_parameters_raster_output_format_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.OUTPUT_RASTER_FORMAT,
                "output format",
                self.OUTPUT_RASTER_FORMATS,
                False,
                0,
            )
        )

    def add_parameters_raster_output_format_commands(self, parameters, context, commands):
        format_output_raster = self.parameterAsInt(parameters, self.OUTPUT_RASTER_FORMAT, context)
        commands.append("-o" + self.OUTPUT_RASTER_FORMATS[format_output_raster])

    def add_parameters_vector_output_gui(self):
        param = QgsProcessingParameterFileDestination(self.OUTPUT_VECTOR, "output vector file", "shp", "", True, False)
        if LastoolsUtils.isDebug():
            param.setDefaultValue('/lastools/data/out.shp') 
        self.addParameter(param)

    def add_parameters_vector_output_commands(self, parameters, context, commands):
        output = self.parameterAsString(parameters, self.OUTPUT_VECTOR, context)
        if output != "":
            commands.append("-o")
            commands.append(self.pathwrap(output))

    def add_parameters_vector_output_format_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.OUTPUT_VECTOR_FORMAT,
                "output format",
                self.OUTPUT_VECTOR_FORMATS,
                False,
                0,
            )
        )

    def add_parameters_vector_output_format_commands(self, parameters, context, commands):
        format_output_vector = self.parameterAsInt(parameters, self.OUTPUT_VECTOR_FORMAT, context)
        commands.append("-o" + self.OUTPUT_VECTOR_FORMATS[format_output_vector])

    def add_parameters_output_directory_gui(self, optional_value=True):
        param = QgsProcessingParameterFolderDestination(self.OUTPUT_DIRECTORY, "output directory", None, optional_value)
        if LastoolsUtils.isDebug():
            param.setDefaultValue('/lastools/data/out') 
        self.addParameter(param)

    def add_parameters_output_directory_commands(self, parameters, context, commands):
        output_dir = self.parameterAsString(parameters, self.OUTPUT_DIRECTORY, context)
        if output_dir != "":
            commands.append("-odir")
            output_dir = output_dir.removesuffix(self.OUTPUT_DIRECTORY) # may added on temp dir, remove now!
            commands.append(self.pathwrap(output_dir))

    def add_parameters_output_appendix_gui(self):
        self.addParameter(QgsProcessingParameterString(self.OUTPUT_APPENDIX, "output appendix", None, False, True))

    def add_parameters_output_appendix_commands(self, parameters, context, commands):
        output_appendix = self.parameterAsString(parameters, self.OUTPUT_APPENDIX, context)
        if output_appendix != "":
            commands.append("-odix")
            commands.append(self.pathwrap(output_appendix))

    def add_parameters_temporary_directory_gui(self):
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.TEMPORARY_DIRECTORY, "temporary directory (must be empty!!!)", None, False
            )
        )

    def add_parameters_temporary_directory_as_output_directory_commands(self, parameters, context, commands):
        output_dir = self.parameterAsString(parameters, self.TEMPORARY_DIRECTORY, context)
        if output_dir != "":
            commands.append("-odir")
            output_dir = output_dir.removesuffix(self.OUTPUT_DIRECTORY) # may added on temp dir, remove now!
            commands.append(self.pathwrap(output_dir))

    def add_parameters_temporary_directory_as_input_files_commands(self, parameters, context, commands, files):
        temp_output = self.parameterAsString(parameters, self.TEMPORARY_DIRECTORY, context)
        if temp_output != "":
            commands.append("-i")
            commands.append(os.path.join(self.pathwrap(temp_output), files))

    def add_parameters_additional_gui(self):
        self.addParameter(
            QgsProcessingParameterString(
                self.ADDITIONAL_OPTIONS, "additional command line arguments", None, False, True
            )
        )

    def add_parameters_additional_commands(self, parameters, context, commands):
        additional_options = self.parameterAsString(parameters, self.ADDITIONAL_OPTIONS, context).split()
        for option in additional_options:
            commands.append(option)

    def add_parameters_filter1_return_class_flags_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.FILTER_RETURN_CLASS_FLAGS1,
                "filter (by return, classification, flags)",
                self.FILTERS_RETURN_CLASS_FLAGS,
                False,
                0,
            )
        )

    def add_parameters_filter1_return_class_flags_commands(self, parameters, context, commands):
        filter1 = self.parameterAsInt(parameters, self.FILTER_RETURN_CLASS_FLAGS1, context)
        if filter1 != 0:
            commands.append("-" + self.FILTERS_RETURN_CLASS_FLAGS[filter1])

    def add_parameters_filter2_return_class_flags_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.FILTER_RETURN_CLASS_FLAGS2,
                "second filter (by return, classification, flags)",
                self.FILTERS_RETURN_CLASS_FLAGS,
                False,
                0,
            )
        )

    def add_parameters_filter2_return_class_flags_commands(self, parameters, context, commands):
        filter_return_class_flags2 = self.parameterAsInt(parameters, self.FILTER_RETURN_CLASS_FLAGS2, context)
        if filter_return_class_flags2 != 0:
            commands.append("-" + self.FILTERS_RETURN_CLASS_FLAGS[filter_return_class_flags2])

    def add_parameters_filter3_return_class_flags_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.FILTER_RETURN_CLASS_FLAGS3,
                "third filter (by return, classification, flags)",
                self.FILTERS_RETURN_CLASS_FLAGS,
                False,
                0,
            )
        )

    def add_parameters_filter3_return_class_flags_commands(self, parameters, context, commands):
        filter_return_class_flags3 = self.parameterAsInt(parameters, self.FILTER_RETURN_CLASS_FLAGS3, context)
        if filter_return_class_flags3 != 0:
            commands.append("-" + self.FILTERS_RETURN_CLASS_FLAGS[filter_return_class_flags3])

    def add_parameters_filter1_coords_intensity_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.FILTER_COORDS_INTENSITY1,
                "filter (by coordinate, intensity, GPS time, ...)",
                self.FILTERS_COORDS_INTENSITY,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.FILTER_COORDS_INTENSITY1_ARG,
                "value for filter (by coordinate, intensity, GPS time, ...)",
                optional=True,
            )
        )

    def add_parameters_filter1_coords_intensity_commands(self, parameters, context, commands):
        filter_coords_intensity1 = self.parameterAsInt(parameters, self.FILTER_COORDS_INTENSITY1, context)
        filter_coords_intensity1_arg = self.parameterAsDouble(parameters, self.FILTER_COORDS_INTENSITY1_ARG, context)
        if filter_coords_intensity1 != 0 and filter_coords_intensity1_arg is not None:
            commands.append("-" + self.FILTERS_COORDS_INTENSITY[filter_coords_intensity1])
            commands.append(str(filter_coords_intensity1_arg))

    def add_parameters_filter2_coords_intensity_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.FILTER_COORDS_INTENSITY2,
                "second filter (by coordinate, intensity, GPS time, ...)",
                self.FILTERS_COORDS_INTENSITY,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.FILTER_COORDS_INTENSITY2_ARG,
                "value for second filter (by coordinate, intensity, GPS time, ...)",
                optional=True,
            )
        )

    def add_parameters_filter2_coords_intensity_commands(self, parameters, context, commands):
        filter_coords_intensity2 = self.parameterAsInt(parameters, self.FILTER_COORDS_INTENSITY2, context)
        filter_coords_intensity2_arg = self.parameterAsDouble(parameters, self.FILTER_COORDS_INTENSITY2_ARG, context)
        if filter_coords_intensity2 != 0 and filter_coords_intensity2_arg is not None:
            commands.append("-" + self.FILTERS_COORDS_INTENSITY[filter_coords_intensity2])
            commands.append(str(filter_coords_intensity2_arg))

    def add_parameters_transform1_coordinate_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.TRANSFORM_COORDINATE1,
                "transform (coordinates)",
                self.TRANSFORM_COORDINATES,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.TRANSFORM_COORDINATE1_ARG, "value for transform (coordinates)", optional=True
            )
        )

    def add_parameters_transform1_coordinate_commands(self, parameters, context, commands):
        transform_coordinate1 = self.parameterAsInt(parameters, self.TRANSFORM_COORDINATE1, context)
        transform_coordinate_1_arg = self.parameterAsDouble(parameters, self.TRANSFORM_COORDINATE1_ARG, context)
        if transform_coordinate1 != 0 and transform_coordinate_1_arg is not None:
            commands.append("-" + self.TRANSFORM_COORDINATES[transform_coordinate1])
            commands.append(str(transform_coordinate_1_arg))

    def add_parameters_transform2_coordinate_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.TRANSFORM_COORDINATE2,
                "second transform (coordinates)",
                self.TRANSFORM_COORDINATES,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.TRANSFORM_COORDINATE2_ARG, "value for second transform (coordinates)", optional=True
            )
        )

    def add_parameters_transform2_coordinate_commands(self, parameters, context, commands):
        transform_coordinate2 = self.parameterAsInt(parameters, self.TRANSFORM_COORDINATE2, context)
        transform_coordinate2_arg = self.parameterAsDouble(parameters, self.TRANSFORM_COORDINATE2_ARG, context)
        if transform_coordinate2 != 0 and transform_coordinate2_arg is not None:
            commands.append("-" + self.TRANSFORM_COORDINATES[transform_coordinate2])
            commands.append(str(transform_coordinate2_arg))

    def add_parameters_transform1_other_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.TRANSFORM_OTHER1,
                "transform (intensities, scan angles, GPS times, ...)",
                self.TRANSFORM_OTHERS,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.TRANSFORM_OTHER1_ARG,
                "value for transform (intensities, scan angles, GPS times, ...)",
                optional=True,
            )
        )

    def add_parameters_transform1_other_commands(self, parameters, context, commands):
        transform_other1 = self.parameterAsInt(parameters, self.TRANSFORM_OTHER1, context)
        transform_other1_arg = self.parameterAsDouble(parameters, self.TRANSFORM_OTHER1_ARG, context)
        if transform_other1 != 0:
            commands.append("-" + self.TRANSFORM_OTHERS[transform_other1])
            if transform_other1 < 11 and transform_other1_arg is not None:
                commands.append(str(transform_other1_arg))

    def add_parameters_transform2_other_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.TRANSFORM_OTHER2,
                "second transform (intensities, scan angles, GPS times, ...)",
                self.TRANSFORM_OTHERS,
                False,
                0,
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.TRANSFORM_OTHER2_ARG,
                "value for second transform (intensities, scan angles, GPS times, ...)",
                optional=True,
            )
        )

    def add_parameters_transform2_other_commands(self, parameters, context, commands):
        transform_other2 = self.parameterAsInt(parameters, self.TRANSFORM_OTHER2, context)
        transform_other2_arg = self.parameterAsDouble(parameters, self.TRANSFORM_OTHER2_ARG, context)
        if transform_other2 != 0:
            commands.append("-" + self.TRANSFORM_OTHERS[transform_other2])
            if transform_other2 < 11 and transform_other2_arg is not None:
                commands.append(str(transform_other2_arg))

    def add_parameters_ignore_class1_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.IGNORE_CLASS1,
                "ignore points with this classification",
                self.IGNORE_CLASSES,
                False,
                0,
            )
        )

    def add_parameters_ignore_class1_commands(self, parameters, context, commands):
        ignore_class1 = self.parameterAsInt(parameters, self.IGNORE_CLASS1, context)
        if ignore_class1 != 0:
            commands.append("-ignore_class")
            commands.append(str(ignore_class1 - 1))

    def add_parameters_ignore_class2_gui(self):
        self.addParameter(
            QgsProcessingParameterEnum(
                self.IGNORE_CLASS2,
                "also ignore points with this classification",
                self.IGNORE_CLASSES,
                False,
                0,
            )
        )

    def add_parameters_ignore_class2_commands(self, parameters, context, commands):
        ignore_class2 = self.parameterAsInt(parameters, self.IGNORE_CLASS2, context)
        if ignore_class2 != 0:
            commands.append("-ignore_class")
            commands.append(str(ignore_class2 - 1))

    FILTER_RETURN_CLASS_FLAGS1 = "FILTER_RETURN_CLASS_FLAGS1"
    FILTER_RETURN_CLASS_FLAGS2 = "FILTER_RETURN_CLASS_FLAGS2"
    FILTER_RETURN_CLASS_FLAGS3 = "FILTER_RETURN_CLASS_FLAGS3"
    FILTERS_RETURN_CLASS_FLAGS = [
        "---",
        "keep_last",
        "keep_first",
        "keep_middle",
        "keep_single",
        "drop_single",
        "keep_double",
        "keep_class 2",
        "keep_class 2 8",
        "keep_class 8",
        "keep_class 6",
        "keep_class 9",
        "keep_class 3 4 5",
        "keep_class 3",
        "keep_class 4",
        "keep_class 5",
        "keep_class 2 6",
        "drop_class 7",
        "drop_withheld",
        "drop_synthetic",
        "drop_overlap",
        "keep_withheld",
        "keep_synthetic",
        "keep_keypoint",
        "keep_overlap",
    ]
    FILTER_COORDS_INTENSITY1 = "FILTER_COORDS_INTENSITY1"
    FILTER_COORDS_INTENSITY2 = "FILTER_COORDS_INTENSITY2"
    FILTER_COORDS_INTENSITY3 = "FILTER_COORDS_INTENSITY3"
    FILTER_COORDS_INTENSITY1_ARG = "FILTER_COORDS_INTENSITY1_ARG"
    FILTER_COORDS_INTENSITY2_ARG = "FILTER_COORDS_INTENSITY2_ARG"
    FILTER_COORDS_INTENSITY3_ARG = "FILTER_COORDS_INTENSITY3_ARG"
    FILTERS_COORDS_INTENSITY = [
        "---",
        "drop_x_above",
        "drop_x_below",
        "drop_y_above",
        "drop_y_below",
        "drop_z_above",
        "drop_z_below",
        "drop_intensity_above",
        "drop_intensity_below",
        "drop_gps_time_above",
        "drop_gps_time_below",
        "drop_scan_angle_above",
        "drop_scan_angle_below",
        "keep_point_source",
        "drop_point_source",
        "drop_point_source_above",
        "drop_point_source_below",
        "keep_user_data",
        "drop_user_data",
        "drop_user_data_above",
        "drop_user_data_below",
        "keep_every_nth",
        "keep_random_fraction",
        "thin_with_grid",
    ]

    TRANSFORM_COORDINATE1 = "TRANSFORM_COORDINATE1"
    TRANSFORM_COORDINATE2 = "TRANSFORM_COORDINATE2"
    TRANSFORM_COORDINATE1_ARG = "TRANSFORM_COORDINATE1_ARG"
    TRANSFORM_COORDINATE2_ARG = "TRANSFORM_COORDINATE2_ARG"
    TRANSFORM_COORDINATES = [
        "---",
        "translate_x",
        "translate_y",
        "translate_z",
        "scale_x",
        "scale_y",
        "scale_z",
        "clamp_z_above",
        "clamp_z_below",
    ]

    TRANSFORM_OTHER1 = "TRANSFORM_OTHER1"
    TRANSFORM_OTHER2 = "TRANSFORM_OTHER2"
    TRANSFORM_OTHER1_ARG = "TRANSFORM_OTHER1_ARG"
    TRANSFORM_OTHER2_ARG = "TRANSFORM_OTHER2_ARG"
    TRANSFORM_OTHERS = [
        "---",
        "scale_intensity",
        "translate_intensity",
        "clamp_intensity_above",
        "clamp_intensity_below",
        "scale_scan_angle",
        "translate_scan_angle",
        "translate_gps_time",
        "set_classification",
        "set_user_data",
        "set_point_source",
        "scale_rgb_up",
        "scale_rgb_down",
        "repair_zero_returns",
    ]

    IGNORE_CLASS1 = "IGNORE_CLASS1"
    IGNORE_CLASS2 = "IGNORE_CLASS2"
    IGNORE_CLASSES = [
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
        "rail (10)",
        "road surface (11)",
        "overlap (12)",
    ]

    PROJECTIONS = ["---", "epsg", "utm", "sp83", "sp27", "longlat", "latlong", "ecef"]

    STATE_PLANES = [
        "---",
        "AK_10",
        "AK_2",
        "AK_3",
        "AK_4",
        "AK_5",
        "AK_6",
        "AK_7",
        "AK_8",
        "AK_9",
        "AL_E",
        "AL_W",
        "AR_N",
        "AR_S",
        "AZ_C",
        "AZ_E",
        "AZ_W",
        "CA_I",
        "CA_II",
        "CA_III",
        "CA_IV",
        "CA_V",
        "CA_VI",
        "CA_VII",
        "CO_C",
        "CO_N",
        "CO_S",
        "CT",
        "DE",
        "FL_E",
        "FL_N",
        "FL_W",
        "GA_E",
        "GA_W",
        "HI_1",
        "HI_2",
        "HI_3",
        "HI_4",
        "HI_5",
        "IA_N",
        "IA_S",
        "ID_C",
        "ID_E",
        "ID_W",
        "IL_E",
        "IL_W",
        "IN_E",
        "IN_W",
        "KS_N",
        "KS_S",
        "KY_N",
        "KY_S",
        "LA_N",
        "LA_S",
        "MA_I",
        "MA_M",
        "MD",
        "ME_E",
        "ME_W",
        "MI_C",
        "MI_N",
        "MI_S",
        "MN_C",
        "MN_N",
        "MN_S",
        "MO_C",
        "MO_E",
        "MO_W",
        "MS_E",
        "MS_W",
        "MT_C",
        "MT_N",
        "MT_S",
        "NC",
        "ND_N",
        "ND_S",
        "NE_N",
        "NE_S",
        "NH",
        "NJ",
        "NM_C",
        "NM_E",
        "NM_W",
        "NV_C",
        "NV_E",
        "NV_W",
        "NY_C",
        "NY_E",
        "NY_LI",
        "NY_W",
        "OH_N",
        "OH_S",
        "OK_N",
        "OK_S",
        "OR_N",
        "OR_S",
        "PA_N",
        "PA_S",
        "PR",
        "RI",
        "SC_N",
        "SC_S",
        "SD_N",
        "SD_S",
        "St.Croix",
        "TN",
        "TX_C",
        "TX_N",
        "TX_NC",
        "TX_S",
        "TX_SC",
        "UT_C",
        "UT_N",
        "UT_S",
        "VA_N",
        "VA_S",
        "VT",
        "WA_N",
        "WA_S",
        "WI_C",
        "WI_N",
        "WI_S",
        "WV_N",
        "WV_S",
        "WY_E",
        "WY_EC",
        "WY_W",
        "WY_WC",
    ]

    UTM_ZONES = [
        "---",
        "1 (north)",
        "2 (north)",
        "3 (north)",
        "4 (north)",
        "5 (north)",
        "6 (north)",
        "7 (north)",
        "8 (north)",
        "9 (north)",
        "10 (north)",
        "11 (north)",
        "12 (north)",
        "13 (north)",
        "14 (north)",
        "15 (north)",
        "16 (north)",
        "17 (north)",
        "18 (north)",
        "19 (north)",
        "20 (north)",
        "21 (north)",
        "22 (north)",
        "23 (north)",
        "24 (north)",
        "25 (north)",
        "26 (north)",
        "27 (north)",
        "28 (north)",
        "29 (north)",
        "30 (north)",
        "31 (north)",
        "32 (north)",
        "33 (north)",
        "34 (north)",
        "35 (north)",
        "36 (north)",
        "37 (north)",
        "38 (north)",
        "39 (north)",
        "40 (north)",
        "41 (north)",
        "42 (north)",
        "43 (north)",
        "44 (north)",
        "45 (north)",
        "46 (north)",
        "47 (north)",
        "48 (north)",
        "49 (north)",
        "50 (north)",
        "51 (north)",
        "52 (north)",
        "53 (north)",
        "54 (north)",
        "55 (north)",
        "56 (north)",
        "57 (north)",
        "58 (north)",
        "59 (north)",
        "60 (north)",
        "1 (south)",
        "2 (south)",
        "3 (south)",
        "4 (south)",
        "5 (south)",
        "6 (south)",
        "7 (south)",
        "8 (south)",
        "9 (south)",
        "10 (south)",
        "11 (south)",
        "12 (south)",
        "13 (south)",
        "14 (south)",
        "15 (south)",
        "16 (south)",
        "17 (south)",
        "18 (south)",
        "19 (south)",
        "20 (south)",
        "21 (south)",
        "22 (south)",
        "23 (south)",
        "24 (south)",
        "25 (south)",
        "26 (south)",
        "27 (south)",
        "28 (south)",
        "29 (south)",
        "30 (south)",
        "31 (south)",
        "32 (south)",
        "33 (south)",
        "34 (south)",
        "35 (south)",
        "36 (south)",
        "37 (south)",
        "38 (south)",
        "39 (south)",
        "40 (south)",
        "41 (south)",
        "42 (south)",
        "43 (south)",
        "44 (south)",
        "45 (south)",
        "46 (south)",
        "47 (south)",
        "48 (south)",
        "49 (south)",
        "50 (south)",
        "51 (south)",
        "52 (south)",
        "53 (south)",
        "54 (south)",
        "55 (south)",
        "56 (south)",
        "57 (south)",
        "58 (south)",
        "59 (south)",
        "60 (south)",
    ]

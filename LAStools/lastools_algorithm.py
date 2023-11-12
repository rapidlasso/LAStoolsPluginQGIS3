# -*- coding: utf-8 -*-

"""
***************************************************************************
    lastools_algorithm.py
    ---------------------
    Date                 : August 2012, September 2023
    Copyright            : (C) 2012 by Victor Olaya, (C) 2014 - 2023, rapidlasso GmbH
    Email                : volayaf at gmail dot com, info near rapidlasso point de
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = ('Victor Olaya', 'rapidlasso')
__date__ = ('August 2012', 'September 2023')
__copyright__ = ('(C) 2012, Victor Olaya', '(C) 2023, rapidlasso GmbH')

from PyQt5.QtGui import QIcon
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterString,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterFolderDestination)
from qgis.PyQt.QtCore import QCoreApplication
from .LAStoolsUtils import LAStoolsUtils


class LAStoolsAlgorithm(QgsProcessingAlgorithm):
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

    FILTER_RETURN_CLASS_FLAGS1 = "FILTER_RETURN_CLASS_FLAGS1"
    FILTER_RETURN_CLASS_FLAGS2 = "FILTER_RETURN_CLASS_FLAGS2"
    FILTER_RETURN_CLASS_FLAGS3 = "FILTER_RETURN_CLASS_FLAGS3"
    FILTERS_RETURN_CLASS_FLAGS = ["---", "keep_last", "keep_first", "keep_middle", "keep_single", "drop_single",
                                  "keep_double", "keep_class 2", "keep_class 2 8", "keep_class 8", "keep_class 6",
                                  "keep_class 9", "keep_class 3 4 5", "keep_class 3", "keep_class 4", "keep_class 5",
                                  "keep_class 2 6", "drop_class 7", "drop_withheld", "drop_synthetic", "drop_overlap",
                                  "keep_withheld", "keep_synthetic", "keep_keypoint", "keep_overlap"]
    FILTER_COORDS_INTENSITY1 = "FILTER_COORDS_INTENSITY1"
    FILTER_COORDS_INTENSITY2 = "FILTER_COORDS_INTENSITY2"
    FILTER_COORDS_INTENSITY3 = "FILTER_COORDS_INTENSITY3"
    FILTER_COORDS_INTENSITY1_ARG = "FILTER_COORDS_INTENSITY1_ARG"
    FILTER_COORDS_INTENSITY2_ARG = "FILTER_COORDS_INTENSITY2_ARG"
    FILTER_COORDS_INTENSITY3_ARG = "FILTER_COORDS_INTENSITY3_ARG"
    FILTERS_COORDS_INTENSITY = ["---", "drop_x_above", "drop_x_below", "drop_y_above", "drop_y_below", "drop_z_above",
                                "drop_z_below", "drop_intensity_above", "drop_intensity_below", "drop_gps_time_above",
                                "drop_gps_time_below", "drop_scan_angle_above", "drop_scan_angle_below",
                                "keep_point_source",
                                "drop_point_source", "drop_point_source_above", "drop_point_source_below",
                                "keep_user_data",
                                "drop_user_data", "drop_user_data_above", "drop_user_data_below", "keep_every_nth",
                                "keep_random_fraction", "thin_with_grid"]

    TRANSFORM_COORDINATE1 = "TRANSFORM_COORDINATE1"
    TRANSFORM_COORDINATE2 = "TRANSFORM_COORDINATE2"
    TRANSFORM_COORDINATE1_ARG = "TRANSFORM_COORDINATE1_ARG"
    TRANSFORM_COORDINATE2_ARG = "TRANSFORM_COORDINATE2_ARG"
    TRANSFORM_COORDINATES = ["---", "translate_x", "translate_y", "translate_z", "scale_x", "scale_y", "scale_z",
                             "clamp_z_above", "clamp_z_below"]

    TRANSFORM_OTHER1 = "TRANSFORM_OTHER1"
    TRANSFORM_OTHER2 = "TRANSFORM_OTHER2"
    TRANSFORM_OTHER1_ARG = "TRANSFORM_OTHER1_ARG"
    TRANSFORM_OTHER2_ARG = "TRANSFORM_OTHER2_ARG"
    TRANSFORM_OTHERS = ["---", "scale_intensity", "translate_intensity", "clamp_intensity_above",
                        "clamp_intensity_below",
                        "scale_scan_angle", "translate_scan_angle", "translate_gps_time", "set_classification",
                        "set_user_data",
                        "set_point_source", "scale_rgb_up", "scale_rgb_down", "repair_zero_returns"]

    IGNORE_CLASS1 = "IGNORE_CLASS1"
    IGNORE_CLASS2 = "IGNORE_CLASS2"
    IGNORE_CLASSES = ["---", "never classified (0)", "unclassified (1)", "ground (2)", "veg low (3)", "veg mid (4)",
                      "veg high (5)", "buildings (6)", "noise (7)", "keypoint (8)", "water (9)", "rail (10)",
                      "road surface (11)", "overlap (12)"]

    @staticmethod
    def tr(string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def icon(self):
        return QIcon(":/plugins/LAStools/LAStools.png")

    @staticmethod
    def check_before_opening_parameters_dialog():
        path = LAStoolsUtils.LAStoolsPath()
        if path == "":
            return "LAStools folder is not configured. Please configure it before running LAStools algorithms."

    def add_parameters_verbose_gui(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.VERBOSE, "verbose", False))
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.GUI, "open LAStools GUI", False))

    def add_parameters_verbose_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.VERBOSE, context):
            commands.append("-v")
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.GUI, context):
            commands.append("-gui")

    def add_parameters_verbose_gui64(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.VERBOSE, "verbose", False))
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.CPU64, "run new 64 bit executable", False))
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.GUI, "open LAStools GUI", False))

    def add_parameters_verbose_commands64(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.VERBOSE, context):
            commands.append("-v")
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.CPU64, context):
            commands.append("-cpu64")
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.GUI, context):
            commands.append("-gui")

    def add_parameters_cores_gui(self):
        self.addParameter(QgsProcessingParameterNumber(LAStoolsAlgorithm.CORES, "number of cores",
                                                       QgsProcessingParameterNumber.Integer, 4, False, 1, 32))

    def add_parameters_cores_commands(self, parameters, context, commands):
        cores = self.parameterAsInt(parameters, LAStoolsAlgorithm.CORES, context)
        if cores != 1:
            commands.append("-cores")
            commands.append(str(cores))

    def add_parameters_generic_input_gui(self, description, extension, optional):
        self.addParameter(
            QgsProcessingParameterFile(LAStoolsAlgorithm.INPUT_GENERIC, description,
                                       QgsProcessingParameterFile.File,
                                       extension, None, optional)
        )

    def add_parameters_generic_input_commands(self, parameters, context, commands, switch):
        input_generic = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_GENERIC, context)
        if input_generic != "":
            commands.append(switch)
            commands.append('"' + input_generic + '"')

    def add_parameters_generic_input_folder_gui(self, wildcard):
        self.addParameter(QgsProcessingParameterFile(
            LAStoolsAlgorithm.INPUT_GENERIC_DIRECTORY, "input directory", QgsProcessingParameterFile.Folder)
        )
        self.addParameter(
            QgsProcessingParameterString(LAStoolsAlgorithm.INPUT_GENERIC_WILDCARDS, "input wildcard(s)", wildcard))

    def add_parameters_generic_input_folder_commands(self, parameters, context, commands):
        input_generic_directory = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_GENERIC_DIRECTORY, context)
        wildcards = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_GENERIC_WILDCARDS, context).split()
        for wildcard in wildcards:
            commands.append("-i")
            if input_generic_directory is not None:
                commands.append('"' + input_generic_directory + "\\" + wildcard + '"')
            else:
                commands.append('"' + wildcard + '"')

    def add_parameters_point_input_gui(self):
        self.addParameter(QgsProcessingParameterFile(
            LAStoolsAlgorithm.INPUT_LASLAZ, "input LAS/LAZ file", QgsProcessingParameterFile.File)
        )

    def add_parameters_point_input_commands(self, parameters, context, commands):
        input_las_laz = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_LASLAZ, context)
        if input_las_laz is not None:
            commands.append("-i")
            commands.append('"' + input_las_laz + '"')

    def add_parameters_point_input_folder_gui(self):
        self.addParameter(QgsProcessingParameterFile(LAStoolsAlgorithm.INPUT_DIRECTORY, "input directory",
                                                     QgsProcessingParameterFile.Folder))
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.INPUT_WILDCARDS, "input wildcard(s)", "*.laz"))

    def add_parameters_point_input_folder_commands(self, parameters, context, commands):
        input_directory = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_DIRECTORY, context)
        wildcards = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_WILDCARDS, context).split()
        for wildcard in wildcards:
            commands.append("-i")
            if input_directory is not None:
                commands.append('"' + input_directory + "\\" + wildcard + '"')
            else:
                commands.append('"' + wildcard + '"')

    def add_parameters_point_input_merged_gui(self):
        self.addParameter(
            QgsProcessingParameterBoolean(LAStoolsAlgorithm.MERGED, "merge all input files on-the-fly into one", False))

    def add_parameters_point_input_merged_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.MERGED, context):
            commands.append("-merged")

    def add_parameters_horizontal_feet_gui(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.HORIZONTAL_FEET, "horizontal feet", False))

    def add_parameters_horizontal_feet_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.HORIZONTAL_FEET, context):
            commands.append("-feet")

    def add_parameters_vertical_feet_gui(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.VERTICAL_FEET, "vertical feet", False))

    def add_parameters_vertical_feet_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.VERTICAL_FEET, context):
            commands.append("-elevation_feet")

    def add_parameters_horizontal_and_vertical_feet_gui(self):
        self.add_parameters_horizontal_feet_gui()
        self.add_parameters_vertical_feet_gui()

    def add_parameters_horizontal_and_vertical_feet_commands(self, parameters, context, commands):
        self.add_parameters_horizontal_feet_commands(parameters, context, commands)
        self.add_parameters_vertical_feet_commands(parameters, context, commands)

    def add_parameters_files_are_flightlines_gui(self):
        self.addParameter(
            QgsProcessingParameterBoolean(LAStoolsAlgorithm.FILES_ARE_FLIGHTLINES, "files are flightlines", False))

    def add_parameters_files_are_flightlines_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.FILES_ARE_FLIGHTLINES, context):
            commands.append("-files_are_flightlines")

    def add_parameters_apply_file_source_id_gui(self):
        self.addParameter(
            QgsProcessingParameterBoolean(LAStoolsAlgorithm.APPLY_FILE_SOURCE_ID, "apply file source ID", False))

    def add_parameters_apply_file_source_id_commands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.APPLY_FILE_SOURCE_ID, context):
            commands.append("-apply_file_source_ID")

    def add_parameters_step_gui(self):
        self.addParameter(QgsProcessingParameterNumber(
            LAStoolsAlgorithm.STEP, "step size / pixel size", QgsProcessingParameterNumber.Double, 1.0, False, 0)
        )

    def add_parameters_step_commands(self, parameters, context, commands):
        step = self.parameterAsDouble(parameters, LAStoolsAlgorithm.STEP, context)
        if step != 0.0:
            commands.append("-step")
            commands.append(str(step))

    def get_parameters_step_value(self, parameters, context):
        step = self.parameterAsDouble(parameters, LAStoolsAlgorithm.STEP, context)
        return step

    def add_parameters_generic_output_gui(self, description, extension, optional):
        self.addParameter(
            QgsProcessingParameterFileDestination(LAStoolsAlgorithm.OUTPUT_GENERIC, description, extension, "",
                                                  optional, False))

    def add_parameters_generic_output_commands(self, parameters, context, commands, switch):
        output = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_GENERIC, context)
        if output != "":
            commands.append(switch)
            commands.append('"' + output + '"')

    def add_parameters_point_output_gui(self):
        self.addParameter(
            QgsProcessingParameterFileDestination(LAStoolsAlgorithm.OUTPUT_LASLAZ, "Output LAS/LAZ file", "laz", "",
                                                  True, False))

    def add_parameters_point_output_commands(self, parameters, context, commands):
        output = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_LASLAZ, context)
        if output != "":
            commands.append("-o")
            commands.append('"' + output + '"')

    def add_parameters_point_output_format_gui(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.OUTPUT_POINT_FORMAT, "output format",
                                                     LAStoolsAlgorithm.OUTPUT_POINT_FORMATS, False, 0))

    def add_parameters_point_output_format_commands(self, parameters, context, commands):
        format_output_point = self.parameterAsInt(parameters, LAStoolsAlgorithm.OUTPUT_POINT_FORMAT, context)
        commands.append("-o" + LAStoolsAlgorithm.OUTPUT_POINT_FORMATS[format_output_point])

    def add_parameters_raster_output_gui(self):
        self.addParameter(
            QgsProcessingParameterFileDestination(
                LAStoolsAlgorithm.OUTPUT_RASTER, "Output raster file", "tif", "", True, False)
        )

    def add_parameters_raster_output_commands(self, parameters, context, commands):
        output = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_RASTER, context)
        if output != "":
            commands.append("-o")
            commands.append('"' + output + '"')

    def add_parameters_raster_output_format_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.OUTPUT_RASTER_FORMAT, "output format", LAStoolsAlgorithm.OUTPUT_RASTER_FORMATS, False, 0)
        )

    def add_parameters_raster_output_format_commands(self, parameters, context, commands):
        format_output_raster = self.parameterAsInt(parameters, LAStoolsAlgorithm.OUTPUT_RASTER_FORMAT, context)
        commands.append("-o" + LAStoolsAlgorithm.OUTPUT_RASTER_FORMATS[format_output_raster])

    def add_parameters_vector_output_gui(self):
        self.addParameter(
            QgsProcessingParameterFileDestination(LAStoolsAlgorithm.OUTPUT_VECTOR, "Output vector file", "shp", "",
                                                  True, False))

    def add_parameters_vector_output_commands(self, parameters, context, commands):
        output = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_VECTOR, context)
        if output != "":
            commands.append("-o")
            commands.append('"' + output + '"')

    def add_parameters_vector_output_format_gui(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.OUTPUT_VECTOR_FORMAT, "output format",
                                                     LAStoolsAlgorithm.OUTPUT_VECTOR_FORMATS, False, 0))

    def add_parameters_vector_output_format_commands(self, parameters, context, commands):
        format_output_vector = self.parameterAsInt(parameters, LAStoolsAlgorithm.OUTPUT_VECTOR_FORMAT, context)
        commands.append("-o" + LAStoolsAlgorithm.OUTPUT_VECTOR_FORMATS[format_output_vector])

    def add_parameters_output_directory_gui(self):
        self.addParameter(QgsProcessingParameterFolderDestination(
            LAStoolsAlgorithm.OUTPUT_DIRECTORY, "output directory", None, True)
        )

    def add_parameters_output_directory_commands(self, parameters, context, commands):
        output_dir = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_DIRECTORY, context)
        if output_dir != "":
            commands.append("-odir")
            commands.append('"' + output_dir + '"')

    def add_parameters_output_appendix_gui(self):
        self.addParameter(QgsProcessingParameterString(
            LAStoolsAlgorithm.OUTPUT_APPENDIX, "output appendix", None, False, True)
        )

    def add_parameters_output_appendix_commands(self, parameters, context, commands):
        output_appendix = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_APPENDIX, context)
        if output_appendix != "":
            commands.append("-odix")
            commands.append('"' + output_appendix + '"')

    def add_parameters_temporary_directory_gui(self):
        self.addParameter(QgsProcessingParameterFolderDestination(
            LAStoolsAlgorithm.TEMPORARY_DIRECTORY, "temporary directory (must be empty!!!)", None, False
        ))

    def add_parameters_temporary_directory_as_output_directory_commands(self, parameters, context, commands):
        output_dir = self.parameterAsString(parameters, LAStoolsAlgorithm.TEMPORARY_DIRECTORY, context)
        if output_dir != "":
            commands.append("-odir")
            commands.append('"' + output_dir + '"')

    def add_parameters_temporary_directory_as_input_files_commands(self, parameters, context, commands, files):
        temp_output = self.parameterAsString(parameters, LAStoolsAlgorithm.TEMPORARY_DIRECTORY, context)
        if temp_output != "":
            commands.append("-i")
            commands.append(temp_output + '\\' + files)

    def add_parameters_additional_gui(self):
        self.addParameter(QgsProcessingParameterString(
            LAStoolsAlgorithm.ADDITIONAL_OPTIONS, "additional command line parameter(s)", None, False, True)
        )

    def add_parameters_additional_commands(self, parameters, context, commands):
        additional_options = self.parameterAsString(parameters, LAStoolsAlgorithm.ADDITIONAL_OPTIONS, context).split()
        for option in additional_options:
            commands.append(option)

    def add_parameters_filter1_return_class_flags_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS1, "filter (by return, classification, flags)",
            LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS, False, 0
        ))

    def add_parameters_filter1_return_class_flags_commands(self, parameters, context, commands):
        filter1 = self.parameterAsInt(parameters, LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS1, context)
        if filter1 != 0:
            commands.append("-" + LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS[filter1])

    def add_parameters_filter2_return_class_flags_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS2, "second filter (by return, classification, flags)",
            LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS, False, 0
        ))

    def add_parameters_filter2_return_class_flags_commands(self, parameters, context, commands):
        filter_return_class_flags2 = self.parameterAsInt(
            parameters, LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS2, context
        )
        if filter_return_class_flags2 != 0:
            commands.append("-" + LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS[filter_return_class_flags2])

    def add_parameters_filter3_return_class_flags_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS3, "third filter (by return, classification, flags)",
            LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS, False, 0
        ))

    def add_parameters_filter3_return_class_flags_commands(self, parameters, context, commands):
        filter_return_class_flags3 = self.parameterAsInt(
            parameters, LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS3, context
        )
        if filter_return_class_flags3 != 0:
            commands.append("-" + LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS[filter_return_class_flags3])

    def add_parameters_filter1_coords_intensity_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.FILTER_COORDS_INTENSITY1, "filter (by coordinate, intensity, GPS time, ...)",
            LAStoolsAlgorithm.FILTERS_COORDS_INTENSITY, False, 0
        ))
        self.addParameter(QgsProcessingParameterString(
            LAStoolsAlgorithm.FILTER_COORDS_INTENSITY1_ARG, "value for filter (by coordinate, intensity, GPS time, ...)"
        ))

    def add_parameters_filter1_coords_intensity_commands(self, parameters, context, commands):
        filter_coords_intensity1 = self.parameterAsInt(parameters, LAStoolsAlgorithm.FILTER_COORDS_INTENSITY1, context)
        filter_coords_intensity1_arg = self.parameterAsDouble(
            parameters, LAStoolsAlgorithm.FILTER_COORDS_INTENSITY1_ARG, context
        )
        if filter_coords_intensity1 != 0 and filter_coords_intensity1_arg is not None:
            commands.append("-" + LAStoolsAlgorithm.FILTERS_COORDS_INTENSITY[filter_coords_intensity1])
            commands.append(str(filter_coords_intensity1_arg))

    def add_parameters_filter2_coords_intensity_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.FILTER_COORDS_INTENSITY2, "second filter (by coordinate, intensity, GPS time, ...)",
            LAStoolsAlgorithm.FILTERS_COORDS_INTENSITY, False, 0
        ))
        self.addParameter(QgsProcessingParameterString(
            LAStoolsAlgorithm.FILTER_COORDS_INTENSITY2_ARG,
            "value for second filter (by coordinate, intensity, GPS time, ...)"
        ))

    def add_parameters_filter2_coords_intensity_commands(self, parameters, context, commands):
        filter_coords_intensity2 = self.parameterAsInt(parameters, LAStoolsAlgorithm.FILTER_COORDS_INTENSITY2, context)
        filter_coords_intensity2_arg = self.parameterAsDouble(
            parameters, LAStoolsAlgorithm.FILTER_COORDS_INTENSITY2_ARG, context
        )
        if filter_coords_intensity2 != 0 and filter_coords_intensity2_arg is not None:
            commands.append("-" + LAStoolsAlgorithm.FILTERS_COORDS_INTENSITY[filter_coords_intensity2])
            commands.append(str(filter_coords_intensity2_arg))

    def add_parameters_transform1_coordinate_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.TRANSFORM_COORDINATE1, "transform (coordinates)",
            LAStoolsAlgorithm.TRANSFORM_COORDINATES, False, 0
        ))
        self.addParameter(QgsProcessingParameterString(
            LAStoolsAlgorithm.TRANSFORM_COORDINATE1_ARG, "value for transform (coordinates)"
        ))

    def add_parameters_transform1_coordinate_commands(self, parameters, context, commands):
        transform_coordinate1 = self.parameterAsInt(parameters, LAStoolsAlgorithm.TRANSFORM_COORDINATE1, context)
        transform_coordinate_1_arg = self.parameterAsDouble(
            parameters, LAStoolsAlgorithm.TRANSFORM_COORDINATE1_ARG, context
        )
        if transform_coordinate1 != 0 and transform_coordinate_1_arg is not None:
            commands.append("-" + LAStoolsAlgorithm.TRANSFORM_COORDINATES[transform_coordinate1])
            commands.append(str(transform_coordinate_1_arg))

    def add_parameters_transform2_coordinate_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.TRANSFORM_COORDINATE2, "second transform (coordinates)",
            LAStoolsAlgorithm.TRANSFORM_COORDINATES, False, 0
        ))
        self.addParameter(QgsProcessingParameterString(
            LAStoolsAlgorithm.TRANSFORM_COORDINATE2_ARG, "value for second transform (coordinates)"
        ))

    def add_parameters_transform2_coordinate_commands(self, parameters, context, commands):
        transform_coordinate2 = self.parameterAsInt(parameters, LAStoolsAlgorithm.TRANSFORM_COORDINATE2, context)
        transform_coordinate2_arg = self.parameterAsDouble(
            parameters, LAStoolsAlgorithm.TRANSFORM_COORDINATE2_ARG, context
        )
        if transform_coordinate2 != 0 and transform_coordinate2_arg is not None:
            commands.append("-" + LAStoolsAlgorithm.TRANSFORM_COORDINATES[transform_coordinate2])
            commands.append(str(transform_coordinate2_arg))

    def add_parameters_transform1_other_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.TRANSFORM_OTHER1, "transform (intensities, scan angles, GPS times, ...)",
            LAStoolsAlgorithm.TRANSFORM_OTHERS, False, 0
        ))
        self.addParameter(QgsProcessingParameterString(
            LAStoolsAlgorithm.TRANSFORM_OTHER1_ARG, "value for transform (intensities, scan angles, GPS times, ...)"
        ))

    def add_parameters_transform1_other_commands(self, parameters, context, commands):
        transform_other1 = self.parameterAsInt(parameters, LAStoolsAlgorithm.TRANSFORM_OTHER1, context)
        transform_other1_arg = self.parameterAsDouble(parameters, LAStoolsAlgorithm.TRANSFORM_OTHER1_ARG, context)
        if transform_other1 != 0:
            commands.append("-" + LAStoolsAlgorithm.TRANSFORM_OTHERS[transform_other1])
            if transform_other1 < 11 and transform_other1_arg is not None:
                commands.append(str(transform_other1_arg))

    def add_parameters_transform2_other_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.TRANSFORM_OTHER2, "second transform (intensities, scan angles, GPS times, ...)",
            LAStoolsAlgorithm.TRANSFORM_OTHERS, False, 0
        ))
        self.addParameter(QgsProcessingParameterString(
            LAStoolsAlgorithm.TRANSFORM_OTHER2_ARG,
            "value for second transform (intensities, scan angles, GPS times, ...)"
        ))

    def add_parameters_transform2_other_commands(self, parameters, context, commands):
        transform_other2 = self.parameterAsInt(parameters, LAStoolsAlgorithm.TRANSFORM_OTHER2, context)
        transform_other2_arg = self.parameterAsDouble(parameters, LAStoolsAlgorithm.TRANSFORM_OTHER2_ARG, context)
        if transform_other2 != 0:
            commands.append("-" + LAStoolsAlgorithm.TRANSFORM_OTHERS[transform_other2])
            if transform_other2 < 11 and transform_other2_arg is not None:
                commands.append(str(transform_other2_arg))

    def add_parameters_ignore_class1_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.IGNORE_CLASS1, "ignore points with this classification",
            LAStoolsAlgorithm.IGNORE_CLASSES, False, 0
        ))

    def add_parameters_ignore_class1_commands(self, parameters, context, commands):
        ignore_class1 = self.parameterAsInt(parameters, LAStoolsAlgorithm.IGNORE_CLASS1, context)
        if ignore_class1 != 0:
            commands.append("-ignore_class")
            commands.append(str(ignore_class1 - 1))

    def add_parameters_ignore_class2_gui(self):
        self.addParameter(QgsProcessingParameterEnum(
            LAStoolsAlgorithm.IGNORE_CLASS2, "also ignore points with this classification",
            LAStoolsAlgorithm.IGNORE_CLASSES, False, 0
        ))

    def add_parameters_ignore_class2_commands(self, parameters, context, commands):
        ignore_class2 = self.parameterAsInt(parameters, LAStoolsAlgorithm.IGNORE_CLASS2, context)
        if ignore_class2 != 0:
            commands.append("-ignore_class")
            commands.append(str(ignore_class2 - 1))

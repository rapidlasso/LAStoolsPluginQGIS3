# -*- coding: utf-8 -*-

"""
***************************************************************************
    LAStoolsAlgorithm.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
    ---------------------
    Date                 : April 2014, May 2016, and August 2018
    Copyright            : (C) 2014 - 2018 by Martin Isenburg
    Email                : martin near rapidlasso point com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

import os
from qgis.PyQt import QtGui
from PyQt5.QtGui import QIcon
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterString,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterFolderDestination)

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
                                "drop_gps_time_below", "drop_scan_angle_above", "drop_scan_angle_below", "keep_point_source",
                                "drop_point_source", "drop_point_source_above", "drop_point_source_below", "keep_user_data",
                                "drop_user_data", "drop_user_data_above", "drop_user_data_below", "keep_every_nth",
                                "keep_random_fraction", "thin_with_grid"]

    TRANSFORM_COORDINATE1 = "TRANSFORM_COORDINATE1"
    TRANSFORM_COORDINATE2 = "TRANSFORM_COORDINATE2"
    TRANSFORM_COORDINATE1_ARG = "TRANSFORM_COORDINATE1_ARG"
    TRANSFORM_COORDINATE2_ARG = "TRANSFORM_COORDINATE2_ARG"
    TRANSFORM_COORDINATES = ["---", "translate_x", "translate_y", "translate_z", "scale_x", "scale_y", "scale_z", "clamp_z_above", "clamp_z_below"]

    TRANSFORM_OTHER1 = "TRANSFORM_OTHER1"
    TRANSFORM_OTHER2 = "TRANSFORM_OTHER2"
    TRANSFORM_OTHER1_ARG = "TRANSFORM_OTHER1_ARG"
    TRANSFORM_OTHER2_ARG = "TRANSFORM_OTHER2_ARG"
    TRANSFORM_OTHERS = ["---", "scale_intensity", "translate_intensity", "clamp_intensity_above", "clamp_intensity_below",
                        "scale_scan_angle", "translate_scan_angle", "translate_gps_time", "set_classification", "set_user_data",
                        "set_point_source", "scale_rgb_up", "scale_rgb_down", "repair_zero_returns"]

    IGNORE_CLASS1 = "IGNORE_CLASS1"
    IGNORE_CLASS2 = "IGNORE_CLASS2"
    IGNORE_CLASSES = ["---", "never classified (0)", "unclassified (1)", "ground (2)", "veg low (3)", "veg mid (4)", "veg high (5)", "buildings (6)", "noise (7)", "keypoint (8)", "water (9)", "rail (10)", "road surface (11)", "overlap (12)"]

    def icon(self):
        return QIcon(":/plugins/LAStools/LAStools.png")

    def checkBeforeOpeningParametersDialog(self):
        path = LAStoolsUtils.LAStoolsPath()
        if (path == ""):
            return "LAStools folder is not configured. Please configure it before running LAStools algorithms."

    def addParametersVerboseGUI(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.VERBOSE, "verbose", False))
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.GUI, "open LAStools GUI", False))

    def addParametersVerboseCommands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.VERBOSE, context):
            commands.append("-v")
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.GUI, context):
            commands.append("-gui")

    def addParametersVerboseGUI64(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.VERBOSE, "verbose", False))
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.CPU64, "run new 64 bit executable", False))
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.GUI, "open LAStools GUI", False))

    def addParametersVerboseCommands64(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.VERBOSE, context):
            commands.append("-v")
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.CPU64, context):
            commands.append("-cpu64")
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.GUI, context):
            commands.append("-gui")

    def addParametersCoresGUI(self):
        self.addParameter(QgsProcessingParameterNumber(LAStoolsAlgorithm.CORES, "number of cores", QgsProcessingParameterNumber.Integer, 4, False, 1, 32))

    def addParametersCoresCommands(self, parameters, context, commands):
        cores = self.parameterAsInt(parameters, LAStoolsAlgorithm.CORES, context)
        if (cores != 1):
            commands.append("-cores")
            commands.append(unicode(cores))

    def addParametersGenericInputGUI(self, description, extension, optional):
        self.addParameter(QgsProcessingParameterFile(LAStoolsAlgorithm.INPUT_GENERIC, description, QgsProcessingParameterFile.File, extension, None, optional))

    def addParametersGenericInputCommands(self, parameters, context, commands, switch):
        input = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_GENERIC, context)
        if (input != ""):
            commands.append(switch)
            commands.append('"' + input + '"')

    def addParametersGenericInputFolderGUI(self, wildcard):
        self.addParameter(QgsProcessingParameterFile(LAStoolsAlgorithm.INPUT_GENERIC_DIRECTORY, "input directory", QgsProcessingParameterFile.Folder))
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.INPUT_GENERIC_WILDCARDS, "input wildcard(s)", wildcard))

    def addParametersGenericInputFolderCommands(self, parameters, context, commands):
        input = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_GENERIC_DIRECTORY, context)
        wildcards = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_GENERIC_WILDCARDS, context).split()
        for wildcard in wildcards:
            commands.append("-i")
            if input is not None:
                commands.append('"' + input + "\\" + wildcard + '"')
            else:
                commands.append('"' + wildcard + '"')

    def addParametersPointInputGUI(self):
        self.addParameter(QgsProcessingParameterFile(LAStoolsAlgorithm.INPUT_LASLAZ, "input LAS/LAZ file", QgsProcessingParameterFile.File))

    def addParametersPointInputCommands(self, parameters, context, commands):
        input = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_LASLAZ, context)
        if (input is not None):
            commands.append("-i")
            commands.append('"' + input + '"')

    def addParametersPointInputFolderGUI(self):
        self.addParameter(QgsProcessingParameterFile(LAStoolsAlgorithm.INPUT_DIRECTORY, "input directory", QgsProcessingParameterFile.Folder))
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.INPUT_WILDCARDS, "input wildcard(s)", "*.laz"))

    def addParametersPointInputFolderCommands(self, parameters, context, commands):
        input = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_DIRECTORY, context)
        wildcards = self.parameterAsString(parameters, LAStoolsAlgorithm.INPUT_WILDCARDS, context).split()
        for wildcard in wildcards:
            commands.append("-i")
            if (input is not None):
                commands.append('"' + input + "\\" + wildcard + '"')
            else:
                commands.append('"' + wildcard + '"')

    def addParametersPointInputMergedGUI(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.MERGED, "merge all input files on-the-fly into one", False))

    def addParametersPointInputMergedCommands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.MERGED, context):
            commands.append("-merged")

    def addParametersHorizontalFeetGUI(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.HORIZONTAL_FEET, "horizontal feet", False))

    def addParametersHorizontalFeetCommands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.HORIZONTAL_FEET, context):
            commands.append("-feet")

    def addParametersVerticalFeetGUI(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.VERTICAL_FEET, "vertical feet", False))

    def addParametersVerticalFeetCommands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.VERTICAL_FEET, context):
            commands.append("-elevation_feet")

    def addParametersHorizontalAndVerticalFeetGUI(self):
        self.addParametersHorizontalFeetGUI()
        self.addParametersVerticalFeetGUI()

    def addParametersHorizontalAndVerticalFeetCommands(self, parameters, context, commands):
        self.addParametersHorizontalFeetCommands(parameters, context, commands)
        self.addParametersVerticalFeetCommands(parameters, context, commands)

    def addParametersFilesAreFlightlinesGUI(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.FILES_ARE_FLIGHTLINES, "files are flightlines", False))

    def addParametersFilesAreFlightlinesCommands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.FILES_ARE_FLIGHTLINES, context):
            commands.append("-files_are_flightlines")

    def addParametersApplyFileSourceIdGUI(self):
        self.addParameter(QgsProcessingParameterBoolean(LAStoolsAlgorithm.APPLY_FILE_SOURCE_ID, "apply file source ID", False))

    def addParametersApplyFileSourceIdCommands(self, parameters, context, commands):
        if self.parameterAsBool(parameters, LAStoolsAlgorithm.APPLY_FILE_SOURCE_ID, context):
            commands.append("-apply_file_source_ID")

    def addParametersStepGUI(self):
        self.addParameter(QgsProcessingParameterNumber(LAStoolsAlgorithm.STEP, "step size / pixel size", QgsProcessingParameterNumber.Double, 1.0, False, 0))

    def addParametersStepCommands(self, parameters, context, commands):
        step = self.parameterAsDouble(parameters,LAStoolsAlgorithm.STEP, context)
        if (step != 0.0):
            commands.append("-step")
            commands.append(unicode(step))

    def getParametersStepValue(self, parameters, context):
        step = self.parameterAsDouble(parameters,LAStoolsAlgorithm.STEP, context)
        return step

    def addParametersGenericOutputGUI(self, description, extension, optional):
        self.addParameter(QgsProcessingParameterFileDestination(LAStoolsAlgorithm.OUTPUT_GENERIC, description, extension, "", optional, False))

    def addParametersGenericOutputCommands(self, parameters, context, commands, switch):
        output = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_GENERIC, context)
        if (output != ""):
            commands.append(switch)
            commands.append('"' + output + '"')

    def addParametersPointOutputGUI(self):
        self.addParameter(QgsProcessingParameterFileDestination(LAStoolsAlgorithm.OUTPUT_LASLAZ, "Output LAS/LAZ file", "laz", "", True, False))

    def addParametersPointOutputCommands(self, parameters, context, commands):
        output = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_LASLAZ, context)
        if (output != ""):
            commands.append("-o")
            commands.append('"' + output + '"')

    def addParametersPointOutputFormatGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.OUTPUT_POINT_FORMAT, "output format", LAStoolsAlgorithm.OUTPUT_POINT_FORMATS, False, 0))

    def addParametersPointOutputFormatCommands(self, parameters, context, commands):
        format = self.parameterAsInt(parameters, LAStoolsAlgorithm.OUTPUT_POINT_FORMAT, context)
        commands.append("-o" + LAStoolsAlgorithm.OUTPUT_POINT_FORMATS[format])

    def addParametersRasterOutputGUI(self):
        self.addParameter(QgsProcessingParameterFileDestination(LAStoolsAlgorithm.OUTPUT_RASTER, "Output raster file", "tif", "", True, False))

    def addParametersRasterOutputCommands(self, parameters, context, commands):
        output = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_RASTER, context)
        if (output != ""):
            commands.append("-o")
            commands.append('"' + output + '"')

    def addParametersRasterOutputFormatGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.OUTPUT_RASTER_FORMAT, "output format", LAStoolsAlgorithm.OUTPUT_RASTER_FORMATS, False, 0))

    def addParametersRasterOutputFormatCommands(self, parameters, context, commands):
        format = self.parameterAsInt(parameters, LAStoolsAlgorithm.OUTPUT_RASTER_FORMAT, context)
        commands.append("-o" + LAStoolsAlgorithm.OUTPUT_RASTER_FORMATS[format])

    def addParametersVectorOutputGUI(self):
        self.addParameter(QgsProcessingParameterFileDestination(LAStoolsAlgorithm.OUTPUT_VECTOR, "Output vector file", "shp", "", True, False))

    def addParametersVectorOutputCommands(self, parameters, context, commands):
        output = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_VECTOR, context)
        if (output != ""):
            commands.append("-o")
            commands.append('"' + output + '"')

    def addParametersVectorOutputFormatGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.OUTPUT_VECTOR_FORMAT, "output format", LAStoolsAlgorithm.OUTPUT_VECTOR_FORMATS, False, 0))

    def addParametersVectorOutputFormatCommands(self, parameters, context, commands):
        format = self.parameterAsInt(parameters, LAStoolsAlgorithm.OUTPUT_VECTOR_FORMAT, context)
        commands.append("-o" + LAStoolsAlgorithm.OUTPUT_VECTOR_FORMATS[format])

    def addParametersOutputDirectoryGUI(self):
        self.addParameter(QgsProcessingParameterFolderDestination(LAStoolsAlgorithm.OUTPUT_DIRECTORY, "output directory", None, True))

    def addParametersOutputDirectoryCommands(self, parameters, context, commands):
        odir = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_DIRECTORY, context)
        if odir != "":
            commands.append("-odir")
            commands.append('"' + odir + '"')

    def addParametersOutputAppendixGUI(self):
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.OUTPUT_APPENDIX, "output appendix", None, False, True))

    def addParametersOutputAppendixCommands(self, parameters, context, commands):
        odix = self.parameterAsString(parameters, LAStoolsAlgorithm.OUTPUT_APPENDIX, context)
        if odix != "":
            commands.append("-odix")
            commands.append('"' + odix + '"')

    def addParametersTemporaryDirectoryGUI(self):
        self.addParameter(QgsProcessingParameterFolderDestination(LAStoolsAlgorithm.TEMPORARY_DIRECTORY, "temporary directory (must be empty!!!)", None, False))

    def addParametersTemporaryDirectoryAsOutputDirectoryCommands(self, parameters, context, commands):
        odir = self.parameterAsString(parameters, LAStoolsAlgorithm.TEMPORARY_DIRECTORY, context)
        if odir != "":
            commands.append("-odir")
            commands.append('"' + odir + '"')

    def addParametersTemporaryDirectoryAsInputFilesCommands(self, parameters, context, commands, files):
        idir = self.parameterAsString(parameters, LAStoolsAlgorithm.TEMPORARY_DIRECTORY, context)
        if idir != "":
            commands.append("-i")
            commands.append(idir + '\\' + files)    

    def addParametersAdditionalGUI(self):
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.ADDITIONAL_OPTIONS, "additional command line parameter(s)", None, False, True))

    def addParametersAdditionalCommands(self, parameters, context, commands):
        additional_options = self.parameterAsString(parameters, LAStoolsAlgorithm.ADDITIONAL_OPTIONS, context).split()
        for option in additional_options:
            commands.append(option)

    def addParametersFilter1ReturnClassFlagsGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS1, "filter (by return, classification, flags)", LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS, False, 0))

    def addParametersFilter1ReturnClassFlagsCommands(self, parameters, context, commands):
        filter1 = self.parameterAsInt(parameters, LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS1, context)
        if filter1 != 0:
            commands.append("-" + LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS[filter1])

    def addParametersFilter2ReturnClassFlagsGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS2, "second filter (by return, classification, flags)", LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS, False, 0))

    def addParametersFilter2ReturnClassFlagsCommands(self, parameters, context, commands):
        filter2 = self.parameterAsInt(parameters, LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS2, context)
        if filter2 != 0:
            commands.append("-" + LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS[filter2])

    def addParametersFilter3ReturnClassFlagsGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS3, "third filter (by return, classification, flags)", LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS, False, 0))

    def addParametersFilter3ReturnClassFlagsCommands(self, parameters, context, commands):
        filter3 = self.parameterAsInt(parameters, LAStoolsAlgorithm.FILTER_RETURN_CLASS_FLAGS3, context)
        if filter3 != 0:
            commands.append("-" + LAStoolsAlgorithm.FILTERS_RETURN_CLASS_FLAGS[filter3])

    def addParametersFilter1CoordsIntensityGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.FILTER_COORDS_INTENSITY1, "filter (by coordinate, intensity, GPS time, ...)", LAStoolsAlgorithm.FILTERS_COORDS_INTENSITY, False, 0))
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.FILTER_COORDS_INTENSITY1_ARG, "value for filter (by coordinate, intensity, GPS time, ...)"))

    def addParametersFilter1CoordsIntensityCommands(self, parameters, context, commands):
        filter1 = self.parameterAsInt(parameters, LAStoolsAlgorithm.FILTER_COORDS_INTENSITY1, context)
        filter1_arg = self.parameterAsDouble(parameters, LAStoolsAlgorithm.FILTER_COORDS_INTENSITY1_ARG, context)
        if filter1 != 0 and filter1_arg is not None:
            commands.append("-" + LAStoolsAlgorithm.FILTERS_COORDS_INTENSITY[filter1])
            commands.append(unicode(filter1_arg))

    def addParametersFilter2CoordsIntensityGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.FILTER_COORDS_INTENSITY2, "second filter (by coordinate, intensity, GPS time, ...)", LAStoolsAlgorithm.FILTERS_COORDS_INTENSITY, False, 0))
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.FILTER_COORDS_INTENSITY2_ARG, "value for second filter (by coordinate, intensity, GPS time, ...)"))

    def addParametersFilter2CoordsIntensityCommands(self, parameters, context, commands):
        filter2 = self.parameterAsInt(parameters, LAStoolsAlgorithm.FILTER_COORDS_INTENSITY2, context)
        filter2_arg = self.parameterAsDouble(parameters, LAStoolsAlgorithm.FILTER_COORDS_INTENSITY2_ARG, context)
        if filter2 != 0 and filter2_arg is not None:
            commands.append("-" + LAStoolsAlgorithm.FILTERS_COORDS_INTENSITY[filter2])
            commands.append(unicode(filter2_arg))

    def addParametersTransform1CoordinateGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.TRANSFORM_COORDINATE1, "transform (coordinates)", LAStoolsAlgorithm.TRANSFORM_COORDINATES, False, 0))
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.TRANSFORM_COORDINATE1_ARG, "value for transform (coordinates)"))

    def addParametersTransform1CoordinateCommands(self, parameters, context, commands):
        transform1 = self.parameterAsInt(parameters, LAStoolsAlgorithm.TRANSFORM_COORDINATE1, context)
        transform1_arg = self.parameterAsDouble(parameters, LAStoolsAlgorithm.TRANSFORM_COORDINATE1_ARG, context)
        if transform1 != 0 and transform1_arg is not None:
            commands.append("-" + LAStoolsAlgorithm.TRANSFORM_COORDINATES[transform1])
            commands.append(unicode(transform1_arg))

    def addParametersTransform2CoordinateGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.TRANSFORM_COORDINATE2, "second transform (coordinates)", LAStoolsAlgorithm.TRANSFORM_COORDINATES, False, 0))
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.TRANSFORM_COORDINATE2_ARG, "value for second transform (coordinates)"))

    def addParametersTransform2CoordinateCommands(self, parameters, context, commands):
        transform2 = self.parameterAsInt(parameters, LAStoolsAlgorithm.TRANSFORM_COORDINATE2, context)
        transform2_arg = self.parameterAsDouble(parameters, LAStoolsAlgorithm.TRANSFORM_COORDINATE2_ARG, context)
        if transform2 != 0 and transform2_arg is not None:
            commands.append("-" + LAStoolsAlgorithm.TRANSFORM_COORDINATES[transform2])
            commands.append(unicode(transform2_arg))

    def addParametersTransform1OtherGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.TRANSFORM_OTHER1, "transform (intensities, scan angles, GPS times, ...)", LAStoolsAlgorithm.TRANSFORM_OTHERS, False, 0))
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.TRANSFORM_OTHER1_ARG, "value for transform (intensities, scan angles, GPS times, ...)"))

    def addParametersTransform1OtherCommands(self, parameters, context, commands):
        transform1 = self.parameterAsInt(parameters, LAStoolsAlgorithm.TRANSFORM_OTHER1, context)
        transform1_arg = self.parameterAsDouble(parameters, LAStoolsAlgorithm.TRANSFORM_OTHER1_ARG, context)
        if transform1 != 0:
            commands.append("-" + LAStoolsAlgorithm.TRANSFORM_OTHERS[transform1])
            if transform1 < 11 and transform1_arg is not None:
                commands.append(unicode(transform1_arg))

    def addParametersTransform2OtherGUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.TRANSFORM_OTHER2, "second transform (intensities, scan angles, GPS times, ...)", LAStoolsAlgorithm.TRANSFORM_OTHERS, False, 0))
        self.addParameter(QgsProcessingParameterString(LAStoolsAlgorithm.TRANSFORM_OTHER2_ARG, "value for second transform (intensities, scan angles, GPS times, ...)"))

    def addParametersTransform2OtherCommands(self, parameters, context, commands):
        transform2 = self.parameterAsInt(parameters, LAStoolsAlgorithm.TRANSFORM_OTHER2, context)
        transform2_arg = self.parameterAsDouble(parameters, LAStoolsAlgorithm.TRANSFORM_OTHER2_ARG, context)
        if transform2 != 0:
            commands.append("-" + LAStoolsAlgorithm.TRANSFORM_OTHERS[transform2])
            if transform2 < 11 and transform2_arg is not None:
                commands.append(unicode(transform2_arg))

    def addParametersIgnoreClass1GUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.IGNORE_CLASS1, "ignore points with this classification", LAStoolsAlgorithm.IGNORE_CLASSES, False, 0))

    def addParametersIgnoreClass1Commands(self, parameters, context, commands):
        ignore1 = self.parameterAsInt(parameters, LAStoolsAlgorithm.IGNORE_CLASS1, context)
        if ignore1 != 0:
            commands.append("-ignore_class")
            commands.append(unicode(ignore1-1))

    def addParametersIgnoreClass2GUI(self):
        self.addParameter(QgsProcessingParameterEnum(LAStoolsAlgorithm.IGNORE_CLASS2, "also ignore points with this classification", LAStoolsAlgorithm.IGNORE_CLASSES, False, 0))

    def addParametersIgnoreClass2Commands(self, parameters, context, commands):
        ignore2 = self.parameterAsInt(parameters, LAStoolsAlgorithm.IGNORE_CLASS2, context)
        if ignore2 != 0:
            commands.append("-ignore_class")
            commands.append(unicode(ignore2-1))

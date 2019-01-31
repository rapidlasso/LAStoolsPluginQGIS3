# -*- coding: utf-8 -*-

"""
***************************************************************************
    lascanopyPro.py
    ---------------------
    Date                 : October 2014 and August 2018
    Copyright            : (C) 2014 by Martin Isenburg
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

__author__ = 'Martin Isenburg'
__date__ = 'October 2014'
__copyright__ = '(C) 2014, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lascanopyPro(LAStoolsAlgorithm):

    PLOT_SIZE = "PLOT_SIZE"
    HEIGHT_CUTOFF = "HEIGHT_CUTOFF"
    PRODUCT1 = "PRODUCT1"
    PRODUCT2 = "PRODUCT2"
    PRODUCT3 = "PRODUCT3"
    PRODUCT4 = "PRODUCT4"
    PRODUCT5 = "PRODUCT5"
    PRODUCT6 = "PRODUCT6"
    PRODUCT7 = "PRODUCT7"
    PRODUCT8 = "PRODUCT8"
    PRODUCT9 = "PRODUCT9"
    PRODUCTS = ["---", "min", "max", "avg", "std", "ske", "kur", "qav", "cov", "dns", "all",
                "p 1", "p 5", "p 10", "p 25", "p 50", "p 75", "p 90", "p 99",
                "int_min", "int_max", "int_avg", "int_std", "int_ske", "int_kur",
                "int_p 1", "int_p 5", "int_p 10", "int_p 25", "int_p 50", "int_p 75", "int_p 90", "int_p 99"]
    COUNTS = "COUNTS"
    DENSITIES = "DENSITIES"
    USE_TILE_BB = "USE_TILE_BB"
    FILES_ARE_PLOTS = "FILES_ARE_PLOTS"

    def initAlgorithm(self, config):
        self.addParametersPointInputFolderGUI()
        self.addParametersPointInputMergedGUI()
        self.addParameter(QgsProcessingParameterNumber(lascanopyPro.PLOT_SIZE, "square plot size", QgsProcessingParameterNumber.Double, 20.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(lascanopyPro.HEIGHT_CUTOFF, "height cutoff / breast height", QgsProcessingParameterNumber.Double, 1.37, False))
        self.addParameter(QgsProcessingParameterEnum(lascanopyPro.PRODUCT1, "create", lascanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopyPro.PRODUCT2, "create", lascanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopyPro.PRODUCT3, "create", lascanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopyPro.PRODUCT4, "create", lascanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopyPro.PRODUCT5, "create", lascanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopyPro.PRODUCT6, "create", lascanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopyPro.PRODUCT7, "create", lascanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopyPro.PRODUCT8, "create", lascanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopyPro.PRODUCT9, "create", lascanopyPro.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterString(lascanopyPro.COUNTS, "count rasters (e.g. 2.0 5.0 10.0 20.0)", ""))
        self.addParameter(QgsProcessingParameterString(lascanopyPro.DENSITIES, "density rasters (e.g. 2.0 5.0 10.0 20.0)", ""))
        self.addParameter(QgsProcessingParameterBoolean(lascanopyPro.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False))
        self.addParameter(QgsProcessingParameterBoolean(lascanopyPro.FILES_ARE_PLOTS, "input files are single plots", False))
        self.addParametersOutputDirectoryGUI()
        self.addParametersOutputAppendixGUI()
        self.addParametersRasterOutputFormatGUI()
        self.addParametersRasterOutputGUI()
        self.addParametersAdditionalGUI()
        self.addParametersCoresGUI()
        self.addParametersVerboseGUI64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lascanopy")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputFolderCommands(parameters, context, commands)
        self.addParametersPointInputMergedCommands(parameters, context, commands)
        plot_size = self.getParameterValue(lascanopyPro.PLOT_SIZE)
        plot_size = self.parameterAsDouble(parameters, lascanopyPro.PLOT_SIZE, context)
        if (plot_size != 20.0):
            commands.append("-step")
            commands.append(unicode(plot_size))
        height_cutoff = self.parameterAsDouble(parameters, lascanopyPro.HEIGHT_CUTOFF, context)
        if (height_cutoff != 1.37):
            commands.append("-height_cutoff")
            commands.append(unicode(height_cutoff))
        product = self.parameterAsInt(parameters, lascanopyPro.PRODUCT1, context)
        if (product != 0):
            commands.append("-" + lascanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopyPro.PRODUCT2, context)
        if (product != 0):
            commands.append("-" + lascanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopyPro.PRODUCT3, context)
        if (product != 0):
            commands.append("-" + lascanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopyPro.PRODUCT4, context)
        if (product != 0):
            commands.append("-" + lascanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopyPro.PRODUCT5, context)
        if (product != 0):
            commands.append("-" + lascanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopyPro.PRODUCT6, context)
        if (product != 0):
            commands.append("-" + lascanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopyPro.PRODUCT7, context)
        if (product != 0):
            commands.append("-" + lascanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopyPro.PRODUCT8, context)
        if (product != 0):
            commands.append("-" + lascanopyPro.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopyPro.PRODUCT9, context)
        if (product != 0):
            commands.append("-" + lascanopyPro.PRODUCTS[product])
        array = self.parameterAsString(parameters, lascanopyPro.COUNTS, context).split()
        if (len(array) > 1):
            commands.append("-c")
            for a in array:
                commands.append(a)
        array = self.parameterAsString(parameters, lascanopyPro.DENSITIES, context).split()
        if (len(array) > 1):
            commands.append("-d")
            for a in array:
                commands.append(a)
        if (self.parameterAsBool(parameters, lascanopyPro.USE_TILE_BB, context)):
            commands.append("-use_tile_bb")
        if (self.parameterAsBool(parameters, lascanopyPro.FILES_ARE_PLOTS, context)):
            commands.append("-files_are_plots")
        self.addParametersOutputDirectoryCommands(parameters, context, commands)
        self.addParametersOutputAppendixCommands(parameters, context, commands)
        self.addParametersRasterOutputFormatCommands(parameters, context, commands)
        self.addParametersRasterOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)
        self.addParametersCoresCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lascanopyPro'

    def displayName(self):
        return 'lascanopyPro'

    def group(self):
        return 'folder - raster derivatives'

    def groupId(self):
        return 'folder - raster derivatives'

    def createInstance(self):
        return lascanopyPro()

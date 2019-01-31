# -*- coding: utf-8 -*-

"""
***************************************************************************
    lascanopy.py
    ---------------------
    Date                 : September 2013 and August 2018
    Copyright            : (C) 2013 by Martin Isenburg
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
__date__ = 'September 2013'
__copyright__ = '(C) 2013, Martin Isenburg'

import os
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterEnum

from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

class lascanopy(LAStoolsAlgorithm):

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
        self.addParametersVerboseGUI64()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterNumber(lascanopy.PLOT_SIZE, "square plot size", QgsProcessingParameterNumber.Double, 20.0, False, 0.0))
        self.addParameter(QgsProcessingParameterNumber(lascanopy.HEIGHT_CUTOFF, "height cutoff / breast height", QgsProcessingParameterNumber.Double, 1.37, False))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT1, "create", lascanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT2, "create", lascanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT3, "create", lascanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT4, "create", lascanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT5, "create", lascanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT6, "create", lascanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT7, "create", lascanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT8, "create", lascanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT9, "create", lascanopy.PRODUCTS, False, 0))
        self.addParameter(QgsProcessingParameterString(lascanopy.COUNTS, "count rasters (e.g. 2.0 5.0 10.0 20.0)", ""))
        self.addParameter(QgsProcessingParameterString(lascanopy.DENSITIES, "density rasters (e.g. 2.0 5.0 10.0 20.0)", ""))
        self.addParameter(QgsProcessingParameterBoolean(lascanopy.USE_TILE_BB, "use tile bounding box (after tiling with buffer)", False))
        self.addParameter(QgsProcessingParameterBoolean(lascanopy.FILES_ARE_PLOTS, "input file is single plot", False))
        self.addParametersRasterOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lascanopy")]
        self.addParametersVerboseCommands64(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        plot_size = self.parameterAsDouble(parameters, lascanopy.PLOT_SIZE, context)
        if (plot_size != 20.0):
            commands.append("-step")
            commands.append(unicode(plot_size))
        height_cutoff = self.parameterAsDouble(parameters, lascanopy.HEIGHT_CUTOFF, context)
        if (height_cutoff != 1.37):
            commands.append("-height_cutoff")
            commands.append(unicode(height_cutoff))
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT1, context)
        if (product != 0):
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT2, context)
        if (product != 0):
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT3, context)
        if (product != 0):
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT4, context)
        if (product != 0):
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT5, context)
        if (product != 0):
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT6, context)
        if (product != 0):
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT7, context)
        if (product != 0):
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT8, context)
        if (product != 0):
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT9, context)
        if (product != 0):
            commands.append("-" + lascanopy.PRODUCTS[product])
        array = self.parameterAsString(parameters, lascanopy.COUNTS, context).split()
        if (len(array) > 1):
            commands.append("-c")
            for a in array:
                commands.append(a)
        array = self.parameterAsString(parameters, lascanopy.DENSITIES, context).split()
        if (len(array) > 1):
            commands.append("-d")
            for a in array:
                commands.append(a)
        if (self.parameterAsBool(parameters, lascanopy.USE_TILE_BB, context)):
            commands.append("-use_tile_bb")
        if (self.parameterAsBool(parameters, lascanopy.FILES_ARE_PLOTS, context)):
            commands.append("-files_are_plots")
        self.addParametersRasterOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lascanopy'

    def displayName(self):
        return 'lascanopy'

    def group(self):
        return 'file - raster derivatives'

    def groupId(self):
        return 'file - raster derivatives'

    def createInstance(self):
        return lascanopy()

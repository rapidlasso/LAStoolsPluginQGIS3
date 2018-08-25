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
from ..LAStoolsUtils import LAStoolsUtils
from ..LAStoolsAlgorithm import LAStoolsAlgorithm

from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterNumber
from processing.core.parameters import ParameterString
from qgis.core import QgsProcessingParameterEnum


class lascanopy(LAStoolsAlgorithm):

    PLOT_SIZE = "PLOT_SIZE"
    HEIGHT_CUTOFF = "HEIGHT_CUTOFF"
    ATTRIBUTE = "ATTRIBUTE"
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
        self.name, self.i18n_name = self.trAlgorithm('lascanopy')
        self.group, self.i18n_group = self.trAlgorithm('LAStools')
        self.addParametersVerboseGUI()
        self.addParametersPointInputGUI()
        self.addParameter(QgsProcessingParameterNumber(lascanopy.PLOT_SIZE,
                                          self.tr("square plot size"), 0, None, 20))
        self.addParameter(QgsProcessingParameterNumber(lascanopy.HEIGHT_CUTOFF,
                                          self.tr("height cutoff / breast height"), 0, None, 1.37))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT1,
                                             self.tr("create"), lascanopy.PRODUCTS, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT2,
                                             self.tr("create"), lascanopy.PRODUCTS, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT3,
                                             self.tr("create"), lascanopy.PRODUCTS, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT4,
                                             self.tr("create"), lascanopy.PRODUCTS, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT5,
                                             self.tr("create"), lascanopy.PRODUCTS, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT6,
                                             self.tr("create"), lascanopy.PRODUCTS, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT7,
                                             self.tr("create"), lascanopy.PRODUCTS, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT8,
                                             self.tr("create"), lascanopy.PRODUCTS, 0))
        self.addParameter(QgsProcessingParameterEnum(lascanopy.PRODUCT9,
                                             self.tr("create"), lascanopy.PRODUCTS, 0))
        self.addParameter(ParameterString(lascanopy.COUNTS,
                                          self.tr("count rasters (e.g. 2.0 5.0 10.0 20.0)"), ""))
        self.addParameter(ParameterString(lascanopy.DENSITIES,
                                          self.tr("density rasters (e.g. 2.0 5.0 10.0 20.0)"), ""))
        self.addParameter(QgsProcessingParameterBoolean(lascanopy.USE_TILE_BB,
                                           self.tr("use tile bounding box (after tiling with buffer)"), False))
        self.addParameter(QgsProcessingParameterBoolean(lascanopy.FILES_ARE_PLOTS,
                                           self.tr("input file is single plot"), False))
        self.addParametersRasterOutputGUI()
        self.addParametersAdditionalGUI()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lascanopy")]
        self.addParametersVerboseCommands(parameters, context, commands)
        self.addParametersPointInputCommands(parameters, context, commands)
        plot_size = self.parameterAsInt(parameters, lascanopy.PLOT_SIZE)
        if plot_size != 20:
            commands.append("-step")
            commands.append(unicode(plot_size))
        height_cutoff = self.parameterAsInt(parameters, lascanopy.HEIGHT_CUTOFF)
        if height_cutoff != 1.37:
            commands.append("-height_cutoff")
            commands.append(unicode(height_cutoff))
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT1)
        if product != 0:
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT2)
        if product != 0:
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT3)
        if product != 0:
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT4)
        if product != 0:
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT5)
        if product != 0:
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT6)
        if product != 0:
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT7)
        if product != 0:
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT8)
        if product != 0:
            commands.append("-" + lascanopy.PRODUCTS[product])
        product = self.parameterAsInt(parameters, lascanopy.PRODUCT9)
        if product != 0:
            commands.append("-" + lascanopy.PRODUCTS[product])
        array = self.parameterAsInt(parameters, lascanopy.COUNTS).split()
        if (len(array) > 1):
            commands.append("-c")
            for a in array:
                commands.append(a)
        array = self.parameterAsInt(parameters, lascanopy.DENSITIES).split()
        if (len(array) > 1):
            commands.append("-d")
            for a in array:
                commands.append(a)
        if (self.parameterAsInt(parameters, lascanopy.USE_TILE_BB)):
            commands.append("-use_tile_bb")
        if (self.parameterAsInt(parameters, lascanopy.FILES_ARE_PLOTS)):
            commands.append("-files_are_plots")
        self.addParametersRasterOutputCommands(parameters, context, commands)
        self.addParametersAdditionalCommands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'laszip'

    def displayName(self):
        return 'laszip'

    def group(self):
        return 'LAStools'

    def groupId(self):
        return 'LAStools'

    def createInstance(self):
        return laszip()
	
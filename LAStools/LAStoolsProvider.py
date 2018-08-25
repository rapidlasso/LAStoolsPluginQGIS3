# -*- coding: utf-8 -*-

"""
/***************************************************************************
    LAStoolsProvider.py
    ---------------------
    This script initializes the valid providers, depending on Wine and OS.
    ---------------------    
    Date                 : January 2017, August 2018
    Copyright            : (C) 2017 Boundless, http://boundlessgeo.com
                           (C) 2018 rapidlasso GmbH, http://rapidlasso.com
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
__date__ = 'January 2017'
__copyright__ = '(C) 2017, Boundless, http://boundlessgeo.com'

__author__ = 'Martin Isenburg'
__date__ = 'August 2018'
__copyright__ = '(C) 2018, rapidlasso GmbH, http://rapidlasso.com'

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingProvider
from .LAStoolsUtils import LAStoolsUtils
from .LAStools.lasinfo import lasinfo
from .LAStools.lasview import lasview
from .LAStools.laszip import laszip
from .LAStoolsProduction.laszipPro import laszipPro
from .LAStoolsPipelines.hugeFileGroundClassify import hugeFileGroundClassify
from . import resources

class LAStoolsProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """

        # LAStools for processing single files
		
        self.algs = [lasinfo(), lasview(), laszip(), laszipPro(), hugeFileGroundClassify()]

        for alg in self.algs:
            self.addAlgorithm( alg )

    def icon(self):
        return QIcon(":/plugins/LAStools/LAStools.png")

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'lastools'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "LAStools") and localised.
        """
        return 'LAStools'

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "LAStools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return 'LAStools LiDAR and point cloud processing'

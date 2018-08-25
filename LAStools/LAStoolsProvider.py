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
from processing.core.ProcessingConfig import Setting, ProcessingConfig

from .LAStoolsUtils import LAStoolsUtils
#from .LAStools.blast2dem import blast2dem
from .LAStools.las2las_filter import las2las_filter
from .LAStools.las2las_project import las2las_project
from .LAStools.las2las_transform import las2las_transform
#from .LAStools.las2tin import las2tin
from .LAStools.lasground import lasground
from .LAStools.lasheight import lasheight
from .LAStools.lasindex import lasindex
from .LAStools.lasinfo import lasinfo
from .LAStools.lasnoise import lasnoise
from .LAStools.lassort import lassort
from .LAStools.lasthin import lasthin
from .LAStools.lasview import lasview
from .LAStools.laszip import laszip
from .LAStools.shp2las import shp2las
from .LAStoolsProduction.laszipPro import laszipPro
from .LAStoolsPipelines.hugeFileGroundClassify import hugeFileGroundClassify
from . import resources

class LAStoolsProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def load(self):
        """In this method we add settings needed to configure our
        provider.
        """
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        ProcessingConfig.addSetting(Setting(self.name(), 'LASTOOLS_ACTIVATED', 'Activate', True))
        ProcessingConfig.addSetting(Setting(self.name(), 'LASTOOLS_FOLDER', 'LAStools folder', "C:\LAStools", valuetype=Setting.FOLDER))
        ProcessingConfig.addSetting(Setting(self.name(), 'WINE_FOLDER', 'Wine folder', "", valuetype=Setting.FOLDER))
        ProcessingConfig.readSettings()
        self.refreshAlgorithms()
        return True

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        ProcessingConfig.removeSetting('LASTOOLS_ACTIVATED')
        ProcessingConfig.removeSetting('LASTOOLS_FOLDER')
        ProcessingConfig.removeSetting('WINE_FOLDER')
        pass

    def isActive(self):
        """Return True if the provider is activated and ready to run algorithms"""
        return ProcessingConfig.getSetting('LASTOOLS_ACTIVATED')

    def setActive(self, active):
        ProcessingConfig.setSettingValue('LASTOOLS_ACTIVATED', active)        
        
    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """

        # LAStools for processing single files
        
        self.algs = [las2las_filter(), las2las_project(), las2las_transform(), lasground(), lasheight(), lasindex(), lasinfo(), lasnoise(), lassort(), lasthin(), lasview(), laszip(), shp2las(), laszipPro(), hugeFileGroundClassify()]

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

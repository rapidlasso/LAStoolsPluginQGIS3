# -*- coding: utf-8 -*-

"""
/***************************************************************************
    __init__.py
    ---------------------
    This script initializes the plugin, making it known to QGIS.
    ---------------------    
    Date                 : January 2017, August 2018
    Copyright            : (C) 2017 Boundless
                           (C) 2018 rapidlasso GmbH, https://rapidlasso.de
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
__copyright__ = '(C) 2017 Boundless'

__author__ = 'Martin Isenburg'
__date__ = 'August 2018'
__copyright__ = '(C) 2018 rapidlasso GmbH, https://rapidlasso.de'

__author__ = 'Jochen Keil'
__date__ = 'March 2023'
__copyright__ = '(C) 2023 rapidlasso GmbH, https://rapidlasso.de'

def classFactory(iface):
    from .LAStoolsPlugin import LAStoolsPlugin
    return LAStoolsPlugin(iface)

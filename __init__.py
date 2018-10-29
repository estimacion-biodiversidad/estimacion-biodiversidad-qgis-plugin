# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EstimacionBiodiversidad
                                 A QGIS plugin
 Complemento para la estimación de la biodiversidad
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-10-28
        copyright            : (C) 2018 by CRBio
        email                : mfvargas@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load EstimacionBiodiversidad class from file EstimacionBiodiversidad.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .estimacion_biodiversidad import EstimacionBiodiversidad
    return EstimacionBiodiversidad(iface)

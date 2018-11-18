# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EstimacionBiodiversidad
                                 A QGIS plugin
 Complemento para la estimación de la biodiversidad
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-10-28
        git sha              : $Format:%H$
        copyright            : (C) 2018 by CRBio
        email                : mfvargas@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QMessageBox

# Initialize Qt resources from file resources.py
from .resources import *
from qgis.core import *
# Import the code for the dialog
from .estimacion_biodiversidad_dialog import EstimacionBiodiversidadDialog
import os.path, sys

from osgeo import ogr

#sys.path.append(r'C:\Code\Python\lib')
#import ogr2ogr

import csv


class EstimacionBiodiversidad:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'EstimacionBiodiversidad_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = EstimacionBiodiversidadDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Estimación de la Biodiversidad')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'EstimacionBiodiversidad')
        self.toolbar.setObjectName(u'EstimacionBiodiversidad')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('EstimacionBiodiversidad', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/estimacion_biodiversidad/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Estimación de la biodiversidad'),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.dlg.tb_outDB.clicked.connect(self.saveOutDB)
        self.dlg.tb_inOccurrenceFile.clicked.connect(self.openInOccurrenceFile)
        self.dlg.tb_inDistributionFile.clicked.connect(self.openInDistributionFile)
        self.dlg.tb_inThematicAreaFile.clicked.connect(self.openInThematicAreaFile)       

        self.dlg.pb_createDB.clicked.connect(self.createDB)               
        self.dlg.pb_loadInOccurrenceFile.clicked.connect(self.loadInOccurrenceFile)               
        self.dlg.pb_loadInDistributionFile.clicked.connect(self.loadInDistributionFile)        

    def saveOutDB(self):
        outDB = str(QFileDialog.getSaveFileName(caption="Guardar base de datos SQLite como",
                                                  filter="SQLite (*.sqlite)")[0])
        self.setOutDBLineEdit(outDB)            

    def setOutDBLineEdit(self, text):
	    self.dlg.le_outDB.setText(text)        
        
    def openInOccurrenceFile(self):
        inOccurrenceFile = str(QFileDialog.getOpenFileName(caption="Abrir TXT", 
                                                 filter="TXT (*.txt)")[0])       
        self.setInOccurrenceFileLineEdit(inOccurrenceFile)                                                             
                                                 
    def setInOccurrenceFileLineEdit(self, text):
	    self.dlg.le_inOccurrenceFile.setText(text)

    def openInDistributionFile(self):
        inDistributionFile = str(QFileDialog.getOpenFileName(caption="Abrir SHP", 
                                                 filter="SHP (*.shp)")[0])       
        self.setInDistributionFileLineEdit(inDistributionFile)                                                             
                                                 
    def setInDistributionFileLineEdit(self, text):
	    self.dlg.le_inDistributionFile.setText(text)        
        
    def openInThematicAreaFile(self):
        inThematicAreaFile = str(QFileDialog.getOpenFileName(caption="Abrir shapefile", 
                                                 filter="Shapefiles (*.shp)")[0])       
        self.setInThematicAreaFileLineEdit(inThematicAreaFile)                                                             
                                                 
    def setInThematicAreaFileLineEdit(self, text):
	    self.dlg.le_inThematicAreaFile.setText(text)        
        
    def setVariables(self):   
        self.outDB              = self.dlg.le_outDB.text()
        self.inOccurrenceFile   = self.dlg.le_inOccurrenceFile.text()
        self.inDistributionFile = self.dlg.le_inDistributionFile.text()
        self.inThematicAreaFile = self.dlg.le_inThematicAreaFile.text()        
        
    def createDB_old(self):
        # TABLE CREATION
        
        # Taxon table
        taxonDef  = "field=taxon_id:int?"
        taxonDef += "field=scientific_name:string"

        taxonLayer = QgsVectorLayer(taxonDef, 'taxon', "memory")    

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.actionOnExistingFile = QgsVectorFileWriter.AppendToLayerNoNewFields 
        options.driverName = 'GPKG'
        options.layerName  = 'taxon'
        
        # add test features
        provider = taxonLayer.dataProvider()
        feat = QgsFeature()
        feat.setAttributes([1, 'Ara ambiguus'])
        provider.addFeatures([feat])
        
        write_result, error_message = QgsVectorFileWriter.writeAsVectorFormat(taxonLayer, self.outDB, options)
        # self.assertEqual(write_result, QgsVectorFileWriter.NoError, error_message)

        
        # Taxon_occurrence table
        taxon_occurrenceDef  =  "Point?"
        taxon_occurrenceDef += "crs=epsg:4326&"
        taxon_occurrenceDef += "field=taxon_occurrence_id:int&"
        taxon_occurrenceDef += "field=taxon_id:int"

        taxon_occurrenceLayer = QgsVectorLayer(taxon_occurrenceDef, 'taxon_occurrence', "memory")    

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.actionOnExistingFile = QgsVectorFileWriter.AppendToLayerNoNewFields 
        options.driverName = 'GPKG'
        options.layerName  = 'taxon_occurrence'
        
        # add test features
        provider = taxon_occurrenceLayer.dataProvider()
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(-84, 10)))
        feat.setAttributes([1, 1])
        provider.addFeatures([feat])
        
        write_result, error_message = QgsVectorFileWriter.writeAsVectorFormat(taxon_occurrenceLayer, self.outDB, options)
        # self.assertEqual(write_result, QgsVectorFileWriter.NoError, error_message)

        
        # Taxon_area table
        taxon_areaDef  =  "Polygon?"
        taxon_areaDef += "crs=epsg:4326&"
        taxon_areaDef += "field=taxon_area_id:int&"
        taxon_areaDef += "field=taxon_id:int"

        taxon_areaLayer = QgsVectorLayer(taxon_areaDef, 'taxon_area', "memory")    

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.actionOnExistingFile = QgsVectorFileWriter.AppendToLayerNoNewFields 
        options.driverName = 'GPKG'
        options.layerName  = 'taxon_area'
        
        # add test features
        provider = taxon_areaLayer.dataProvider()
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(-84, 10), QgsPointXY(-84, 9.8), QgsPointXY(-83.8, 10)]]))
        feat.setAttributes([1, 1])
        provider.addFeatures([feat])
        
        write_result, error_message = QgsVectorFileWriter.writeAsVectorFormat(taxon_areaLayer, self.outDB, options)
        # self.assertEqual(write_result, QgsVectorFileWriter.NoError, error_message)

    def createDB_old2(self):
        # Database creation
        if not os.path.exists(self.outDB):
            print("Creating " + self.outDB + "...")

            drv = ogr.GetDriverByName('SQLite')
            if drv is None:
                raise Exception('Could not find driver')
                
            dsOut = drv.CreateDataSource(self.outDB, ['SPATIALITE=YES'])
            if dsOut is None:
               raise Exception('Could not create ' + self.outDB)
            print(self.outDB + " created!\n")
        else:
            print("Opening " + self.outDB + "...")
            dsOut = ogr.Open(self.outDB, 1)
            if dsOut is None:
                raise Exception('Could not open ' + self.outDB)
            else:
                print(self.outDB + " opened!\n")

        # taxon table creation
        print("Creating taxon table...")
        query  =  "CREATE TABLE taxon ("
        query +=  "taxon_id         INTEGER,"
        query +=  "scientific_name  TEXT,"
        query +=  "kingdom_id       INTEGER,"
        query +=  "phylum_id        INTEGER,"
        query +=  "class_id         INTEGER,"
        query +=  "order_id         INTEGER,"
        query +=  "family_id        INTEGER,"
        query +=  "genus_id         INTEGER,"
        query +=  "taxon_rank_id    INTEGER,"
        query +=  "parent_name_id   INTEGER,"                 
        query +=  "accepted_name_id INTEGER"
        query +=  ")"
        print(query)             
        dsOut.ExecuteSQL(query)
        print("Text and numbers columns of the taxon table have been created!\n")   
        # THIS IS WEIRD...IT SEEMS WE NEED TO DEFINE A SPATIAL COLUMN IN ORDER TO CREATE THE TABLE
        query = "SELECT AddGeometryColumn('taxon', 'GEOMETRY', 4326, 'POINT', 'XY')"
        print(query)     
        dsOut.ExecuteSQL(query)
        print("Spatial columns of the taxon table have been created!\n")     

        #test
        query = "INSERT INTO taxon (taxon_id, scientific_name) VALUES (1, 'Animalia')"
        dsOut.ExecuteSQL(query)
        
                
        # taxon_occurrence table creation
        print("Creating taxon_occurrence table...")
        query  =  "CREATE TABLE taxon_occurrence ("
        query +=  "taxon_occurrence_id INTEGER,"
        query +=  "taxon_id            INTEGER,"
        query +=  "scientific_name     TEXT"        
        query +=  ")"
        print(query)             
        dsOut.ExecuteSQL(query)
        print("Text and numbers columns of the taxon_occurrence table have been created!\n")             
        query = "SELECT AddGeometryColumn('taxon_occurrence', 'GEOMETRY', 4326, 'POINT', 'XY')"
        print(query)     
        dsOut.ExecuteSQL(query)
        print("Spatial columns of the taxon_occurrence table have been created!\n")     

        # test
        #QgsMessageLog.logMessage("INSERT INTO taxon_occurrence (taxon_occurrence_id, taxon_id, GEOMETRY) VALUES(1, 1, ST_GeomFromText('POINT(-84 10)', 4326))", 'EstimacionBiodiversidad', level=Qgis.Info)
        #query = "INSERT INTO taxon_occurrence (taxon_occurrence_id, taxon_id, GEOMETRY) VALUES(1, 1, ST_GeomFromText('POINT(-84 10)', 4326));"
        #dsOut.ExecuteSQL(query)        
        
        shapefile = self.inOccurrenceFile
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataSource = driver.Open(shapefile, 0)
        layer = dataSource.GetLayer()

        i = 0
        for feature in layer:
            QgsMessageLog.logMessage(str(i), 'EstimacionBiodiversidad', level=Qgis.Info)
            query = "INSERT INTO taxon_occurrence (taxon_occurrence_id, taxon_id, scientific_name, GEOMETRY) VALUES({}, {}, '{}', ST_GeomFromText('POINT ({} {})', 4326));".format(str(feature.GetField("gbifID")), str(feature.GetField("speciesKey")), str(feature.GetField("species")), str(feature.GetField("decimalLon")), str(feature.GetField("decimalLat")))
            QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)
            dsOut.ExecuteSQL(query)        
            i = i + 1
            if i >= 40000:
                break


        # thematic_area table creation
        print("Creating thematic_area table...")
        query  =  "CREATE TABLE thematic_area ("
        query +=  "thematic_area_id         INTEGER,"
        query +=  "layer_id                 INTEGER,"        
        query +=  "name                     TEXT,"
        query +=  "area                     INTEGER,"        
        query +=  "spp_richness_occurrences INTEGER,"                
        query +=  "occurrences_spp_names    TEXT"                        
        query +=  ")"
        print(query)             
        dsOut.ExecuteSQL(query)
        print("Text and numbers columns of the thematic_area table have been created!\n")             
        query = "SELECT AddGeometryColumn('thematic_area', 'GEOMETRY', 4326, 'POLYGON', 'XY')"
        print(query)     
        dsOut.ExecuteSQL(query)
        print("Spatial columns of the thematic_area table have been created!\n")     

        # test
        #QgsMessageLog.logMessage("INSERT INTO taxon_occurrence (taxon_occurrence_id, taxon_id, GEOMETRY) VALUES(1, 1, ST_GeomFromText('POINT(-84 10)', 4326))", 'EstimacionBiodiversidad', level=Qgis.Info)
        #query = "INSERT INTO taxon_occurrence (taxon_occurrence_id, taxon_id, GEOMETRY) VALUES(1, 1, ST_GeomFromText('POINT(-84 10)', 4326));"
        #dsOut.ExecuteSQL(query)        
        
        shapefile = self.inThematicAreaFile
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataSource = driver.Open(shapefile, 0)
        layer = dataSource.GetLayer()

        i = 0
        for feature in layer:
            #QgsMessageLog.logMessage(str(i), 'EstimacionBiodiversidad', level=Qgis.Info)
            geometry    = feature.geometry()
            geometryWKT = geometry.ExportToWkt()
            #QgsMessageLog.logMessage(geometryWKT, 'EstimacionBiodiversidad', level=Qgis.Info)
            query = "INSERT INTO thematic_area (thematic_area_id, layer_id, name, area, spp_richness_occurrences, GEOMETRY) VALUES({}, 1, '{}', 0, 0, ST_GeomFromText('{}', 4326));".format(str(i), str(feature.GetField("contrato")), geometryWKT)
            QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)
            dsOut.ExecuteSQL(query)        
            i = i + 1
            if i >= 1000:
                break        

                
        # Species richness calculation
        QgsMessageLog.logMessage("Calculating species richness...", 'EstimacionBiodiversidad', level=Qgis.Info)
        query  =  "UPDATE thematic_area"
        query +=  "    SET spp_richness_occurrences = ("
        query +=  "        SELECT Count(DISTINCT taxon_id)"        
        query +=  "        FROM taxon_occurrence o"
        query +=  "        WHERE ST_Contains(thematic_area.Geometry, o.Geometry)"        
        query +=  "    )"                
        print(query)             
        dsOut.ExecuteSQL(query)

        # Species occurrences names
        QgsMessageLog.logMessage("Generating species names from occurrences...", 'EstimacionBiodiversidad', level=Qgis.Info)
        query  =  "UPDATE thematic_area"
        query +=  "    SET occurrences_spp_names = ("
        query +=  "        SELECT Group_concat(DISTINCT scientific_name)"        
        query +=  "        FROM taxon_occurrence o"
        query +=  "        WHERE ST_Contains(thematic_area.Geometry, o.Geometry)"        
        query +=  "    )"                
        print(query)             
        dsOut.ExecuteSQL(query)        
        
        dsOut = None

    def createDB(self):
        self.setVariables()
        driverName = "SQLite"
        
        # =================
        # Database creation
        # =================
        QgsMessageLog.logMessage("Creating " + self.outDB + "...", 'EstimacionBiodiversidad', level=Qgis.Info)

        drv = ogr.GetDriverByName(driverName)
        if drv is None:
            QgsMessageLog.logMessage("Could not find driver " + self.outDB, 'EstimacionBiodiversidad', level=Qgis.Info)
            QMessageBox.information(None, "", "Could not find driver " + self.outDB)
            return
            
        dsOut = drv.CreateDataSource(self.outDB, ['SPATIALITE=YES'])
        if dsOut is None:
            QgsMessageLog.logMessage("Could not create " + self.outDB, 'EstimacionBiodiversidad', level=Qgis.Info)
            QMessageBox.information(None, "", "Could not create " + self.outDB)
            return
           
        QgsMessageLog.logMessage("Empty " + self.outDB + " created", 'EstimacionBiodiversidad', level=Qgis.Info)

        # ==============
        # Table creation
        # ==============
                
        # "taxon" table creation
        QgsMessageLog.logMessage("Creating taxon table...", 'EstimacionBiodiversidad', level=Qgis.Info)
        query  =  "CREATE TABLE taxon ("
        query +=  "taxon_id         INTEGER,"
        query +=  "scientific_name  TEXT,"
        query +=  "kingdom_id       INTEGER,"
        query +=  "phylum_id        INTEGER,"
        query +=  "class_id         INTEGER,"
        query +=  "order_id         INTEGER,"
        query +=  "family_id        INTEGER,"
        query +=  "genus_id         INTEGER,"
        query +=  "taxon_rank_id    INTEGER,"
        query +=  "parent_name_id   INTEGER,"                 
        query +=  "accepted_name_id INTEGER"
        query +=  ")"
        QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)        
        dsOut.ExecuteSQL(query)
        QgsMessageLog.logMessage("Text and numbers columns of the taxon table have been created", 'EstimacionBiodiversidad', level=Qgis.Info)                
        # THIS IS WEIRD...IT SEEMS WE NEED TO DEFINE A SPATIAL COLUMN IN ORDER TO CREATE THE TABLE
        query = "SELECT AddGeometryColumn('taxon', 'GEOMETRY', 4326, 'POINT', 'XY')"
        QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)        
        dsOut.ExecuteSQL(query)
        QgsMessageLog.logMessage("Spatial columns of the taxon table have been created", 'EstimacionBiodiversidad', level=Qgis.Info)                

        # "taxon_occurrence" table creation
        QgsMessageLog.logMessage("Creating taxon_occurrence table...", 'EstimacionBiodiversidad', level=Qgis.Info)
        query  =  "CREATE TABLE taxon_occurrence ("
        query +=  "taxon_occurrence_id INTEGER,"
        query +=  "taxon_id            INTEGER,"
        query +=  "scientific_name     TEXT"         # this column needs to be removed because it is already defined in the taxon table
        query +=  ")"
        QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)        
        dsOut.ExecuteSQL(query)
        QgsMessageLog.logMessage("Text and numbers columns of the taxon_occurrence table have been created", 'EstimacionBiodiversidad', level=Qgis.Info)                
        query = "SELECT AddGeometryColumn('taxon_occurrence', 'GEOMETRY', 4326, 'POINT', 'XY')"
        QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)        
        dsOut.ExecuteSQL(query)
        QgsMessageLog.logMessage("Spatial columns of the taxon_occurrence table have been created", 'EstimacionBiodiversidad', level=Qgis.Info)                

        # "taxon_occurrence" table creation
        QgsMessageLog.logMessage("Creating taxon_occurrence table...", 'EstimacionBiodiversidad', level=Qgis.Info)
        query  =  "CREATE TABLE taxon_occurrence ("
        query +=  "taxon_occurrence_id INTEGER,"
        query +=  "taxon_id            INTEGER,"
        query +=  "scientific_name     TEXT"         # this column needs to be removed because it is already defined in the taxon table
        query +=  ")"
        QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)        
        dsOut.ExecuteSQL(query)
        QgsMessageLog.logMessage("Text and numbers columns of the taxon_occurrence table have been created", 'EstimacionBiodiversidad', level=Qgis.Info)                
        query = "SELECT AddGeometryColumn('taxon_occurrence', 'GEOMETRY', 4326, 'POINT', 'XY')"
        QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)        
        dsOut.ExecuteSQL(query)
        QgsMessageLog.logMessage("Spatial columns of the taxon_occurrence table have been created", 'EstimacionBiodiversidad', level=Qgis.Info)                

        # "taxon_distribution" table creation
        QgsMessageLog.logMessage("Creating taxon_distribution table...", 'EstimacionBiodiversidad', level=Qgis.Info)
        query  =  "CREATE TABLE taxon_distribution ("
        query +=  "taxon_distribution_id INTEGER,"
        query +=  "taxon_id              INTEGER,"
        query +=  "scientific_name       TEXT"         # this column needs to be removed because it is already defined in the taxon table
        query +=  ")"
        QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)        
        dsOut.ExecuteSQL(query)
        QgsMessageLog.logMessage("Text and numbers columns of the taxon_distribution table have been created", 'EstimacionBiodiversidad', level=Qgis.Info)                
        query = "SELECT AddGeometryColumn('taxon_distribution', 'GEOMETRY', 4326, 'MULTIPOLYGON', 'XY')"
        QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)        
        dsOut.ExecuteSQL(query)
        QgsMessageLog.logMessage("Spatial columns of the taxon_distribution table have been created", 'EstimacionBiodiversidad', level=Qgis.Info)                
              
        dsOut = None
        QgsMessageLog.logMessage(self.outDB + " created!", 'EstimacionBiodiversidad', level=Qgis.Info)        
        QMessageBox.information(None, "", self.outDB + " created!")
        
    def loadInOccurrenceFile(self):
        self.setVariables()
        
        QgsMessageLog.logMessage("Opening " + self.outDB + "...", 'EstimacionBiodiversidad', level=Qgis.Info)        
        dsOut = ogr.Open(self.outDB, 1)
        if dsOut is None:
            QMessageBox.information(None, "", "Could not open " + self.outDB)
        else:
            QgsMessageLog.logMessage(self.outDB + " opened!", 'EstimacionBiodiversidad', level=Qgis.Info)    

        outLayer     = dsOut.GetLayerByName("taxon_occurrence")
        outLayerDefn = outLayer.GetLayerDefn()
        
        with open(self.inOccurrenceFile, encoding="utf8") as f:
            records = csv.reader(f, delimiter='\t')
            
            i = 0
            for record in records:
                # QgsMessageLog.logMessage(str(i) + " " + str(record), 'EstimacionBiodiversidad', level=Qgis.Info)        
                if i == 0: # header
                    QgsMessageLog.logMessage(str(record), 'EstimacionBiodiversidad', level=Qgis.Info)        
                else:
                    #QgsMessageLog.logMessage(str(i), 'EstimacionBiodiversidad', level=Qgis.Info)        
                    QgsMessageLog.logMessage(str(i) + " " + record[133] + " " + record[132], 'EstimacionBiodiversidad', level=Qgis.Info)  

                    # Aproach based on SQL
                    # query = "INSERT INTO taxon_occurrence (taxon_occurrence_id, taxon_id, scientific_name, GEOMETRY) VALUES({}, {}, '{}', ST_GeomFromText('POINT ({} {})', 4326));".format(1, 1, "Homo sapiens", record[133], record[132])                    
                    # QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)
                    # dsOut.ExecuteSQL(query)  

                    # Aproach not based on SQL
                    outFeature   = ogr.Feature(outLayerDefn)                            
                    outFeature.SetField("taxon_occurrence_id", 1)
                    outFeature.SetField("taxon_id",            1)
                    outFeature.SetField("scientific_name",     "Homo sapiens")
                    wkt = "POINT({} {})".format(record[133], record[132])
                    point = ogr.CreateGeometryFromWkt(wkt)
                    outFeature.SetGeometry(point)
                    outLayer.CreateFeature(outFeature)
                    
                i = i + 1
                
                if i >= 1000:
                    break
                    
        dsOut = None
        QgsMessageLog.logMessage("Taxon occurrence layer loaded!", 'EstimacionBiodiversidad', level=Qgis.Info)        
        QMessageBox.information(None, "", "Taxon occurrence layer loaded!")

    def loadInDistributionFile(self):
        self.setVariables()
        
        QgsMessageLog.logMessage("Opening " + self.outDB + "...", 'EstimacionBiodiversidad', level=Qgis.Info)        
        dsOut = ogr.Open(self.outDB, 1)
        if dsOut is None:
            QMessageBox.information(None, "", "Could not open " + self.outDB)
        else:
            QgsMessageLog.logMessage(self.outDB + " opened!", 'EstimacionBiodiversidad', level=Qgis.Info)    

        outLayer     = dsOut.GetLayerByName("taxon_distribution")
        outLayerDefn = outLayer.GetLayerDefn()
        
        inShapefile  = self.inDistributionFile
        driver       = ogr.GetDriverByName("ESRI Shapefile")
        dataSource   = driver.Open(inShapefile, 0)
        inLayer      = dataSource.GetLayer()
            
        i = 0
        for feature in inLayer:
            QgsMessageLog.logMessage(str(i), 'EstimacionBiodiversidad', level=Qgis.Info)        

            # Aproach based on SQL
            geometry    = feature.geometry()
            if geometry.GetGeometryType() == ogr.wkbPolygon:
                QMessageBox.information(None, "", feature.GetField("sciname") + " " + str(geometry.GetGeometryType()) + "Singlepart!")                
                geometry = ogr.ForceToMultiPolygon(geometry)
            geometryWKT = geometry.ExportToWkt()
            query = "INSERT INTO taxon_distribution (taxon_distribution_id, taxon_id, scientific_name, GEOMETRY) VALUES({}, {}, '{}', ST_GeomFromText('{}', 4326));".format(1, 1, str(feature.GetField("sciname")), geometryWKT)            
            QgsMessageLog.logMessage(query, 'EstimacionBiodiversidad', level=Qgis.Info)
            dsOut.ExecuteSQL(query)  

            # Aproach not based on SQL
            # outFeature   = ogr.Feature(outLayerDefn)                            
            # outFeature.SetField("taxon_occurrence_id", 1)
            # outFeature.SetField("taxon_id",            1)
            # outFeature.SetField("scientific_name",     "Homo sapiens")
            # wkt = "POINT({} {})".format(record[133], record[132])
            # point = ogr.CreateGeometryFromWkt(wkt)
            # outFeature.SetGeometry(point)
            # outLayer.CreateFeature(outFeature)
                
            i = i + 1
            if i >= 1000:
                break
                    
        dsOut = None
        QgsMessageLog.logMessage("Taxon distribution layer loaded!", 'EstimacionBiodiversidad', level=Qgis.Info)        
        QMessageBox.information(None, "", "Taxon distribution layer loaded!")        
        
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Estimación de la Biodiversidad'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            self.setVariables()
            self.createDB()

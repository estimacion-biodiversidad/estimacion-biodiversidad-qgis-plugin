# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IdentifyToolDialog
                                 A QGIS plugin
 tool for clicking on feature
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-11-16
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Jose
        email                : doe@doe.com
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

import os

from PyQt5 import uic
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QDialog, QWidget, QVBoxLayout, QScrollArea,\
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QFrame

from PyQt5.QtCore import QRect, Qt, QFile

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'identify_tool_dialog_base.ui'))


class IdentifyToolDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(IdentifyToolDialog, self).__init__(parent)
        #self.setupUi(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.resize(1200,700)

        # attributes
        self.filename = None

        self.totalColumns = {
            "all_occurrence": "Riqueza total\npor registros de presencia",
            "all_occurrence_names": "Todas las especies\npor registros de presencia",
            "all_distribution": "Riqueza total\npor áreas de distribución",
            "all_distribution_names": "Todas las especies\npor áreas de distribución",

            "mammalia_occurrence": "Riqueza de Mammalia\npor registros de presencia",
            "mammalia_occurrence_names": "Especies de Mammalia\npor registros de presencia",
            "mammalia_distribution": "Riqueza de Mammalia\npor áreas de distribución",
            "mammalia_distribution_names": "Especies de Mammalia\npor áreas de distribución",

            "reptilia_occurrence": "Riqueza de Reptilia\npor registros de presencia",
            "reptilia_occurrence_names": "Especies de Reptilia\nnpor registros de presencia",
            "reptilia_distribution": "Riqueza de Reptilia\npor áreas de distribución",
            "reptilia_distribution_names": "Especies de Reptilia\npor áreas de distribución",

            "amphibia_occurrence": "Riqueza de Amphibia\npor registros de presencia",
            "amphibia_occurrence_names": "Especies de Amphibia\npor registros de presencia",
            "amphibia_distribution": "Riqueza de Amphibia\npor áreas de distribución",
            "amphibia_distribution_names": "Especies de Amphibia)\npor áreas de distribución",

            "aves_occurrence": "Riqueza de Aves\npor registros de presencia",
            "aves_occurrence_names": "Especies de Aves\npor registros de presencia",
            "aves_distribution": "Riqueza de Aves\npor áreas de distribución",
            "aves_distribution_names": "Especies de Aves\npor áreas de distribución",

            "plantae_occurrence": "Riqueza de Plantae\npor registros de presencia",
            "plantae_occurrence_names": "Especies de Plantae\npor registros de presencia",
            "plantae_distribution": "Riqueza de Plantae\npor áreas de distribución",
            "plantae_distribution_names": "Especies de Plantae\npor áreas de distribución",

            "all_iucn_threatened_occurrence": "Riqueza total de especies\namenazadas (IUCN)\npor registros de presencia",
            "all_iucn_threatened_occurrence_names": "Todas las especies\namenazadas (IUCN)\npor registros de presencia",
            "all_iucn_threatened_distribution": "Riqueza total de especies\namenazadas (IUCN)\npor áreas de distribución",
            "all_iucn_threatened_distribution_names": "Todas las especies\namenazadas (IUCN)\npor áreas de distribución",

            "mammalia_iucn_threatened_occurrence": "Riqueza de Mammalia\namenazadas (IUCN)\npor registros de presencia",
            "mammalia_iucn_threatened_occurrence_names": "Especies de Mammalia\namenazadas (IUCN)\npor registros de presencia",
            "mammalia_iucn_threatened_distribution": "Riqueza de Mammalia\namenazadas (IUCN)\npor áreas de distribución",
            "mammalia_iucn_threatened_distribution_names": "Especies de Mammalia\namenazadas (IUCN)\npor áreas de distribución",

            "reptilia_iucn_threatened_occurrence": "Riqueza de Reptilia\namenazadas (IUCN)\npor registros de presencia",
            "reptilia_iucn_threatened_occurrence_names": "Especies de Reptilia\namenazadas (IUCN)\npor registros de presencia",
            "reptilia_iucn_threatened_distribution": "Riqueza de Reptilia\namenazadas (IUCN)\npor áreas de distribución",
            "reptilia_iucn_threatened_distribution_names": "Especies de Reptilia\namenazadas (IUCN)\npor áreas de distribución",

            "amphibia_iucn_threatened_occurrence": "Riqueza de Amphibia\namenazadas (IUCN)\npor registros de presencia",
            "amphibia_iucn_threatened_occurrence_names": "Especies de Amphibia\namenazadas (IUCN)\npor registros de presencia",
            "amphibia_iucn_threatened_distribution": "Riqueza de Amphibia\namenazadas (IUCN)\npor áreas de distribución",
            "amphibia_iucn_threatened_distribution_names": "Especies de Amphibia\namenazadas (IUCN)\npor áreas de distribución",

            "aves_iucn_threatened_occurrence": "Riqueza de Aves\namenazadas (IUCN)\npor registros de presencia",
            "aves_iucn_threatened_occurrence_names": "Especies de Aves\namenazadas (IUCN)\npor registros de presencia",
            "aves_iucn_threatened_distribution": "Riqueza de Aves\namenazadas (IUCN)\npor áreas de distribución",
            "aves_iucn_threatened_distribution_names": "Especies de Aves\namenazadas (IUCN)\npor áreas de distribución",

            "plantae_iucn_threatened_occurrence": "Riqueza de Plantae\namenazadas (IUCN)\npor registros de presencia",
            "plantae_iucn_threatened_occurrence_names": "Especies de Plantae\namenazadas (IUCN)\npor registros de presencia",
            "plantae_iucn_threatened_distribution": "Riqueza de Plantae\namenazadas (IUCN)\npor áreas de distribución",
            "plantae_iucn_threatened_distribution_names": "Especies de Plantae\namenazadas (IUCN)\npor áreas de distribución",

            "all_lcvs_pe_occurrence": "Riqueza total de especies\nen peligro de extinción\npor registros de presencia",
            "all_lcvs_pe_occurrence_names": "Todas las especies\nen peligro de extinción\npor registros de presencia",
            "all_lcvs_pe_distribution": "Riqueza total de especies\nen peligro de extinción\npor áreas de distribución",
            "all_lcvs_pe_distribution_names": "Todas las especies\nen peligro de extinción\npor áreas de distribución",

            "mammalia_lcvs_pe_occurrence": "Riqueza de Mammalia\nen peligro de extinción\npor registros de presencia",
            "mammalia_lcvs_pe_occurrence_names": "Especies de Mammalia\nen peligro de extinción\npor registros de presencia",
            "mammalia_lcvs_pe_distribution": "Riqueza de Mammalia\nen peligro de extinción\npor áreas de distribución",
            "mammalia_lcvs_pe_distribution_names": "Especies de Mammalia\nen peligro de extinción\npor áreas de distribución",

            "reptilia_lcvs_pe_occurrence": "Riqueza de Reptilia\nen peligro de extinción\npor registros de presencia",
            "reptilia_lcvs_pe_occurrence_names": "Especies de Reptilia\nen peligro de extinción\npor registros de presencia",
            "reptilia_lcvs_pe_distribution": "Riqueza de Reptilia\en peligro de extinción\npor áreas de distribución",
            "reptilia_lcvs_pe_distribution_names": "Especies de Reptilia\nen peligro de extinción\npor áreas de distribución",

            "amphibia_lcvs_pe_occurrence": "Riqueza de Amphibia\nen peligro de extinción\npor registros de presencia",
            "amphibia_lcvs_pe_occurrence_names": "Especies de Amphibia\nen peligro de extinción\npor registros de presencia",
            "amphibia_lcvs_pe_distribution": "Riqueza de Amphibia\en peligro de extinción\npor áreas de distribución",
            "amphibia_lcvs_pe_distribution_names": "Especies de Amphibia\nen peligro de extinción\npor áreas de distribución",

            "aves_lcvs_pe_occurrence": "Riqueza de Aves\nen peligro de extinción\npor registros de presencia",
            "aves_lcvs_pe_occurrence_names": "Especies de Aves\nen peligro de extinción\npor registros de presencia",
            "aves_lcvs_pe_distribution": "Riqueza de Aves\nen peligro de extinción\npor áreas de distribución",
            "aves_lcvs_pe_distribution_names": "Especies de Aves\nen peligro de extinción\npor áreas de distribución",

            "plantae_lcvs_pe_occurrence": "Riqueza de Plantae\nen peligro de extinción\npor registros de presencia",
            "plantae_lcvs_pe_occurrence_names": "Especies de Plantae\nen peligro de extinción\npor registros de presencia",
            "plantae_lcvs_pe_distribution": "Riqueza de Plantae\nen peligro de extinción\npor áreas de distribución",
            "plantae_lcvs_pe_distribution_names": "Especies de Plantae\nen peligro de extinción\npor áreas de distribución",

            "all_lcvs_pr_occurrence": "Riqueza total de especies\ncon poblaciones reducidas\npor registros de presencia",
            "all_lcvs_pr_occurrence_names": "Todas las especies\ncon poblaciones reducidas\npor registros de presencia",
            "all_lcvs_pr_distribution": "Riqueza total de especies\ncon poblaciones reducidas\npor áreas de distribución",
            "all_lcvs_pr_distribution_names": "Todas las especies\ncon poblaciones reducidas\npor áreas de distribución",

            "mammalia_lcvs_pr_occurrence": "Riqueza de Mammalia\ncon poblaciones reducidas\npor registros de presencia",
            "mammalia_lcvs_pr_occurrence_names": "Especies de Mammalia\ncon poblaciones reducidas\npor registros de presencia",
            "mammalia_lcvs_pr_distribution": "Riqueza de Mammalia\ncon poblaciones reducidas\npor áreas de distribución",
            "mammalia_lcvs_pr_distribution_names": "Especies de Mammalia\ncon poblaciones reducidas\npor áreas de distribución",

            "reptilia_lcvs_pr_occurrence": "Riqueza de Reptilia\ncon poblaciones reducidas\npor registros de presencia",
            "reptilia_lcvs_pr_occurrence_names": "Especies de Reptilia\ncon poblaciones reducidas\npor registros de presencia",
            "reptilia_lcvs_pr_distribution": "Riqueza de Reptilia\con poblaciones reducidas\npor áreas de distribución",
            "reptilia_lcvs_pr_distribution_names": "Especies de Reptilia\ncon poblaciones reducidas\npor áreas de distribución",

            "amphibia_lcvs_pr_occurrence": "Riqueza de Amphibia\ncon poblaciones reducidas\npor registros de presencia",
            "amphibia_lcvs_pr_occurrence_names": "Especies de Amphibia\ncon poblaciones reducidas\npor registros de presencia",
            "amphibia_lcvs_pr_distribution": "Riqueza de Amphibia\con poblaciones reducidas\npor áreas de distribución",
            "amphibia_lcvs_pr_distribution_names": "Especies de Amphibia\ncon poblaciones reducidas\npor áreas de distribución",

            "aves_lcvs_pr_occurrence": "Riqueza de Aves\ncon poblaciones reducidas\npor registros de presencia",
            "aves_lcvs_pr_occurrence_names": "Especies de Aves\ncon poblaciones reducidas\npor registros de presencia",
            "aves_lcvs_pr_distribution": "Riqueza de Aves\ncon poblaciones reducidas\npor áreas de distribución",
            "aves_lcvs_pr_distribution_names": "Especies de Aves\ncon poblaciones reducidas\npor áreas de distribución",

            "plantae_lcvs_pr_occurrence": "Riqueza de Plantae\ncon poblaciones reducidas\npor registros de presencia",
            "plantae_lcvs_pr_occurrence_names": "Especies de Plantae\ncon poblaciones reducidas\npor registros de presencia",
            "plantae_lcvs_pr_distribution": "Riqueza de Plantae\ncon poblaciones reducidas\npor áreas de distribución",
            "plantae_lcvs_pr_distribution_names": "Especies de Plantae\ncon poblaciones reducidas\npor áreas de distribución",

            "all_lcvs_ve_occurrence": "Riqueza total de especies\nvedadas\npor registros de presencia",
            "all_lcvs_ve_occurrence_names": "Todas las especies\nvedadas\npor registros de presencia",
            "all_lcvs_ve_distribution": "Riqueza total de especies\nvedadas\npor áreas de distribución",
            "all_lcvs_ve_distribution_names": "Todas las especies\nvedadas\npor áreas de distribución",

            "plantae_lcvs_ve_occurrence": "Riqueza de Plantae\nvedadas\npor registros de presencia",
            "plantae_lcvs_ve_occurrence_names": "Especies de Plantae\nvedadas\npor registros de presencia",
            "plantae_lcvs_ve_distribution": "Riqueza de Plantae\nvedadas\npor áreas de distribución",
            "plantae_lcvs_ve_distribution_names": "Especies de Plantae\nvedadas\npor áreas de distribución"
        }

    def showDialog(self, layer, columnList, progress, progressInfo, fonafifoUrl):
        self.layer=layer
        self.columnList=columnList
        progress.setVisible(False)
        progressInfo.setVisible(False)

        MAX_FOOTER = 600

        # FONAFIFO logo
        pic = QLabel(self)
        pic.setGeometry(600, MAX_FOOTER-30, 150, 50)
        pixmap = QPixmap()
        pixmap.load(fonafifoUrl);
        pic.setPixmap(pixmap)

        self.labelHeader = QLabel(self)
        self.labelHeader.setText("Resultados")
        self.labelHeader.setStyleSheet('color: #076F00')
        self.labelHeader.move(20, 20)
        newfont = QFont("Times", 20, QFont.Bold)
        self.labelHeader.setFont(newfont)

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.HLine)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.frame.move(5,55);
        self.frame.resize(1955,5)

        self.buttonDescargar = QPushButton('Descargar estadísticas (CSV)', self)
        self.buttonDescargar.move(20, 590)
        self.buttonDescargar.resize(200, 30)
        self.buttonDescargar.clicked.connect(self.downloadCSV)

        self.buttonCerrar = QPushButton('Cerrar', self)
        self.buttonCerrar.move(270, 590)
        self.buttonCerrar.resize(200, 30)
        self.buttonCerrar.clicked.connect(self.close)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(1150, 500)
        self.tableWidget.move(20, 60)


        self.tableWidget.setRowCount(layer.selectedFeatureCount())
        # we add 1 because column "name" was incluyed previously
        self.tableWidget.setColumnCount(len(columnList)+1)

        # construir las demas columnas dinamicamente segun seleccion del usuario
        self.buildColumns()

        self.fillColumns()





        self.show()

    #def close(self):
    #    self.columnList.clear()
    #    self.done(1)

    def downloadCSV(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Guardar Resultados","","CSV Files (*.csv)", options=options)
        if fileName:
            file = open(fileName, 'w')

            file.write('Area' + '\t')
            for column in self.columnList:
                tempStr = (str(self.totalColumns[column])).replace('\n', '');
                file.write(tempStr + '\t')

            file.write('\n')

            found_features = self.layer.selectedFeatures()

            for found_feature in found_features:
                file.write(str(found_feature["name"]) + '\t')

                for column in self.columnList:
                    file.write(str(found_feature[column]) + '\t')

                file.write('\n')

            file.close()

    def buildColumns(self):
        columnCount = 1
        for column in self.columnList:
            headerItem = QTableWidgetItem(self.totalColumns[column])
            self.tableWidget.setHorizontalHeaderItem(columnCount, headerItem)
            if (columnCount % 2) == 0:
                self.tableWidget.setColumnWidth(columnCount, 300)
            else:
                self.tableWidget.setColumnWidth(columnCount, 150)
            columnCount=columnCount+1

        #self.tableWidget.setColumnWidth(0, 100)
        #self.tableWidget.setColumnWidth(len(self.columnList)+1, 150)
        #self.tableWidget.setColumnWidth(len(self.columnList)+2, 350)
        #self.tableWidget.setColumnWidth(len(self.columnList)+3, 150)
        #self.tableWidget.setColumnWidth(len(self.columnList)+4, 350)

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem('Área'))
        self.tableWidget.setSortingEnabled(True)

    def fillColumns(self):

        # msgBox = QMessageBox()
        # msgBox.setText(str(self.columnList));
        # # msgBox.setText(str(found_feature[column]));
        # msgBox.exec();


        found_features = self.layer.selectedFeatures()

        rowCount = 0;
        columnCount = 1
        for found_feature in found_features:
            nameItem = QTableWidgetItem(str(found_feature["name"]))
            if (rowCount % 2) != 0:
                nameItem.setBackground(QtGui.QColor(240, 240, 240))
            self.tableWidget.setItem(rowCount, 0, nameItem)

            for column in self.columnList:
                if(str(found_feature[column])=='NULL'):
                    nullItem = QTableWidgetItem("--")
                    if (rowCount % 2) != 0:
                        nullItem.setBackground(QtGui.QColor(240, 240, 240))
                    self.tableWidget.setItem(rowCount, columnCount, nullItem)
                else:
                    item = QTableWidgetItem();
                    if (rowCount % 2) != 0:
                        item.setBackground(QtGui.QColor(240, 240, 240))
                    item.setData(Qt.DisplayRole, found_feature[column]);
                    self.tableWidget.setItem(rowCount, columnCount, item);
                columnCount = columnCount + 1

            rowCount = rowCount + 1
            columnCount = 1
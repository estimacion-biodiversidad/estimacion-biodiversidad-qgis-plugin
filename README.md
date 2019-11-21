# Complemento de QGIS: herramienta para estimación de biodiversidad

La herramienta **Estimación de Biodiversidad**, es un complemento de [QGIS](https://qgis.org/) desarrollado para ser utilizado, en primera instancia, en un proceso de análisis y comercialización del servicio de protección de biodiversidad en fincas con contrato de [Pago por Servicios Ambientales (PSA)](https://www.fonafifo.go.cr/es/servicios/pago-de-servicios-ambientales/) del [Fondo Nacional de Financiamiento Forestal (Fonafifo)](https://www.fonafifo.go.cr/). Adicionalmente, podría ser utilizado en actividades de monitoreo, de priorización de zonas para el desarrollo de acciones de control, de manejo o de intervención, entre otras.

## Descarga del código fuente
```terminal
$ git clone https://github.com/estimacion-biodiversidad/estimacion-biodiversidad-qgis-plugin.git
```

## Puesta en producción
Para compilar y poner en producción el complemento, se recomienda utilizar la herramienta [Plugin Builder Tool (pb_tool)](http://g-sherman.github.io/plugin_build_tool/).

### Instalación de pb_tool
```terminal
# Actualización del instalador de paquetes pip
$ python3 -m pip install --upgrade pip

# Instalación de pb_tool
$ python3 -m pip install pb_tool
```

### Puesta en producción del complemento
```terminal
$ pb_tool deploy
```

El comando anterior compila los archivos ```.PY``` a ```.PYC``` y los coloca en el directorio de producción, junto con el resto de archivos requeridos (ayuda en línea, formas de entrada de datos, metadatos, etc.). El directorio de producción (en el que se almacenan los complementos de QGIS) está especificado en la propiedad ```plugin_path``` del archivo ```pb_tool.cfg``` (ej. ```C:\Users\mfvargas\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins```) y puede consultarse también en la opción de menú de QGIS ```Settings - User Profiles - Open Active Profile Folder```. Para que este directorio exista, debe haber al menos un complemento instalado.

Para ver el nuevo complemento en el menú de QGIS, debe cerrarse el programa y abrirse nuevamente. El nuevo complemento debe estar en el menú de complementos (o cualquier otro que se haya especificado) y sus íconos deben ser visibles en la barra de herramientas.

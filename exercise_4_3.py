# Import modules
from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import *
import os

folder_path = r"C:\IFGI\2026_SS\Python in QGIS and ArcGIS\Muenster"
project_path = r"C:\IFGI\2026_SS\Python in QGIS and ArcGIS\Exercise_4_3"

contents = os.listdir(folder_path)

project = QgsProject.instance()
project.read(project_path)

for content in contents:
    if content[-4:] == '.shp':
        file_path = folder_path + "\\" + content
        base_name = os.path.basename(file_path)
        new_layer = QgsVectorLayer(file_path, base_name[:-4], 'ogr')
        if (new_layer.isValid()):
            project.addMapLayer(new_layer)

project.write()


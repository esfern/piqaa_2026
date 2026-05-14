from qgis.utils import iface
import processing

schools = QgsProject.instance().mapLayersByName('Schools')[0]
city_districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]

parameters = {
    'POLYGONS': city_districts,
    'POINTS': schools,
    'FIELD': 'NUMPOINTS',
    'OUTPUT': 'TEMPORARY_OUTPUT'
}

result = processing.run("native:countpointsinpolygon", parameters)
output_layer = result['OUTPUT']

# We only got the counts for the districts from the Muenster_City_Districts Layer
# In the example solution it seems like those counts were grouped by P_District
# We didnt do that ¯\_(ツ)_/¯
for feature in output_layer.getFeatures():
    attributes = feature.attributes()
    name = feature['Name']
    count = feature['NUMPOINTS']
    print(f"{name}: {count}")

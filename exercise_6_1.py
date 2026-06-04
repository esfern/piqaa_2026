import csv
import sys

# Create multipolygon layer in memory
layer = QgsVectorLayer("multipolygon", "temp_standard_land_value_muenster", "memory")

# Set CRS
crs = QgsCoordinateReferenceSystem("EPSG:25832")
layer.setCrs(crs)

# Add fields to layer
provider = layer.dataProvider()
provider.addAttributes([
    QgsField("standard_land_value", QVariant.Double),
    QgsField("type", QVariant.String),
    QgsField("district", QVariant.String)
])
layer.updateFields()

# Open CSV file
with open("C:\\IFGI\\2026_SS\\Python in QGIS and ArcGIS\\Data for Session 6\\standard_land_value_muenster.csv", newline='') as csvfile:
    # Increase field size limit, since some lines are very long
    csv.field_size_limit(1310720)
    # Read CSV file
    spamreader = csv.reader(csvfile, delimiter=';')
    
    features = []
    
    for index, row in enumerate(spamreader):
        # Skip header row
        if index == 0:
            continue
        
        # Create new feature with attributes and geometry
        feature = QgsFeature(layer.fields())
        feature.setAttribute("standard_land_value", float(row[0].replace(',', '.')))
        feature.setAttribute("type", row[1])
        feature.setAttribute("district", row[2])
        feature.setGeometry(QgsGeometry.fromWkt(row[3]))
        
        # Add feature to features list
        features.append(feature)

# Add features to layer
provider.addFeatures(features)

# Add layer to project
QgsProject.instance().addMapLayer(layer)
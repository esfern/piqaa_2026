parent = iface.mainWindow()

sCoords, bOk = QInputDialog.getText(parent, "Coordinates", "Enter coordinates as latitude, longitude", text = "51.96066, 7.62476")

# Get districts layer
districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]

if bOk and sCoords:
    # split input string into lat/lon values 
    parts = sCoords.split(",")
    
    try: # try-except for invalid input
        # parse lat/lon to float
        lat = float(parts[0].strip())
        lon = float(parts[1].strip())
        
        # transform WGS84 to ETRS89 32N
        crs_wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
        crs_etrs89 = QgsCoordinateReferenceSystem("EPSG:25832")
        transform = QgsCoordinateTransform(crs_wgs84, crs_etrs89, QgsProject.instance())

        # build a WGS84 point, reproject it to ETRS89 32N, and wrap it as QgsGeometry
        point_wgs84 = QgsPointXY(lon, lat)
        point_etrs89 = transform.transform(point_wgs84)
        point_geom = QgsGeometry.fromPointXY(point_etrs89)
        
        # find the district the input point falls within
        result = ""
        for district in districts.getFeatures():
            district_geom = district.geometry()
            if point_geom.within(district_geom):
                result = district
                break

        # display dialogue for result(within or outside Münster)
        if result:
            district_name = result.attributes()[3]
            QMessageBox.information(parent, "Result", f"The coordinates {lon}, {lat} fall within the district of {district_name}")
        else:
            QMessageBox.information(parent, "Result", f"The coordinates {lon}, {lat} fall outside the city of Münster")

    # if user input is invalid then display warning dialogue
    except:
        QMessageBox.warning(parent, "Warning", f"The input {sCoords} is invalid")

    


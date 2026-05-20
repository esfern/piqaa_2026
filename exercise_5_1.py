districts_names = [] #list to store district names

# Select city districts layer
city_districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]

# create request for ordering by Name alphabetically in ascending order
request = qgis.core.QgsFeatureRequest()
clause = qgis.core.QgsFeatureRequest.OrderByClause('Name')
orderby = qgis.core.QgsFeatureRequest.OrderBy([clause])
request.setOrderBy(orderby)

# iterate through city district features to get all Names
for feature in city_districts.getFeatures(request):
    name = feature['Name']
    districts_names.append(name)

parent = iface.mainWindow() # Main Window for dialogs

# Display drop down dialog
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ", districts_names)


if bOk:
    # Create a mapCanvas() instance
    mc = iface.mapCanvas()

    # Create a QgsDistanceArea() instance
    da = QgsDistanceArea()

    # Set the ellipsoid for correct measurment
    da.setEllipsoid("ETRS89")
    
    # Create Name filter 
    selected_district_request = QgsFeatureRequest()
    selected_district_request.setFilterExpression(f"Name = '{sDistrict}'")
    
    # Use name filter to access the selected district feature
    selected_district_feature = list(city_districts.getFeatures(selected_district_request))[0]    
    
    schools = QgsProject.instance().mapLayersByName('Schools')[0]
    selected_district_geom = selected_district_feature.geometry()
    district_schools = ""
    
    schools_features = schools.getFeatures(request)
    ids = []
    for index, school in enumerate(schools_features):
        school_geom = school.geometry()
        if school_geom.within(selected_district_geom):
            school_attrs = school.attributes()
            ids.append(school_attrs[0])
            district_schools += f"{school_attrs[1]}, {school_attrs[2]}"
            if index != schools.featureCount() - 1:
                district_schools += "\n\n"
            
    print(district_schools)
    print(f"Number in {', '.join(str(i) for i in ids)}")
    schools.selectByExpression(f"Number in ({', '.join(str(i) for i in ids)})", QgsVectorLayer.SetSelection)
   
    mc.zoomToSelected()
    QMessageBox.information(parent, f"Schools in {sDistrict}", district_schools)
    
else:
    QMessageBox.warning(parent, "Schools", "User cancelled")



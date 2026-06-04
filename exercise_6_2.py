# Get pool and district layers
pools = QgsProject.instance().mapLayersByName('public_swimming_pools')[0]
city_districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
provider = pools.dataProvider()

# Add new field
provider.addAttributes([
    QgsField("district", QVariant.String, len = 50)
])
pools.updateFields()

# Iterate over pools
for pool in pools.getFeatures():
    pool_id = pool.id()

    district_name = "unknown"

    # Get the name of the district the pool is in
    for district in city_districts.getFeatures():
        if pool.geometry().within(district.geometry()):
            district_name = district.attributes()[3]
            break
    
    # Add the district name to the district field
    attributes = pool.attributes()
    provider.changeAttributeValues({
        pool_id: {
            0: attributes[0],
            1: "Hallenbad" if attributes[1] == "H" else "Freibad",
            2: district_name
        }
    })
from qgis.utils import iface

mc = iface.mapCanvas()
layers = QgsProject.instance().mapLayersByName('Schools')
layer = layers[0]
print(layer.getFeatures())
schools = layer.getFeatures()
for school in schools:
    attributes = school.attributes()
    name = attributes[1]
    point = geometry.asPoint()
    x = point.x()
    y = point.y()
    print(f"{name}: {x}, {y}")
"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from typing import Any, Optional
import os
import time
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterEnum,
    QgsProject,
    QgsProcessingParameterFolderDestination,
)
from qgis import processing
from qgis.utils import iface


def get_sorted_district_names():
    """
    Returns an alphabetically sorted list of city district names
    from the 'Muenster_City_Districts' layer.
    
    Returns:
        list: Sorted list of district names
    """
    districts_names = []
    try:
        districts_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
        for district_feature in districts_layer.getFeatures():
            district_attrs = district_feature.attributes()
            district_name = district_attrs[3]  # "Name" column
            districts_names.append(district_name)
        districts_names.sort()
    except (IndexError, AttributeError) as e:
        raise QgsProcessingException(f"Could not load Muenster_City_Districts layer: {str(e)}")
    
    return districts_names


class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = "OUTPUT"
    SELECTED_NAME = "SELECTED_NAME"
    SELECTED_DATA_TYPE = "SELECTED_DATA_TYPE"

    def name(self) -> str:
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "createcitydistrictprofile"

    def displayName(self) -> str:
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return "Create City District Profile"

    def group(self) -> str:
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return "City District Analysis"

    def groupId(self) -> str:
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "citydistrictanalysis"

    def shortHelpString(self) -> str:
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it.
        """
        return "Creates a PDF profile for a selected city district including district information, household count, parcels, schools/pools, and a map image."

    def initAlgorithm(self, config: Optional[dict[str, Any]] = None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        
        # Get sorted district names using helper function
        districts_names = get_sorted_district_names()
        
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SELECTED_NAME,
                'Select a district',
                options=districts_names,
                optional=False
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.SELECTED_DATA_TYPE,
                'Decide on displayed data',
                options=["Pools", "Schools"],
                optional=False
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT,
                'Select output folder',
                optional=False
            )
        )

    def processAlgorithm(
        self,
        parameters: dict[str, Any],
        context,
        feedback,
    ) -> dict[str, Any]:
        try:
            # Get parameters
            selected_district_index = parameters[self.SELECTED_NAME]
            selected_data_type = parameters[self.SELECTED_DATA_TYPE]
            output_folder = parameters[self.OUTPUT]
            
            # Ensure output directory exists
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # Get all district names (sorted)
            districts_names = get_sorted_district_names()
            selected_district_name = districts_names[selected_district_index]
                        
            # Get the districts layer
            districts_layer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
            
            # Find the selected district feature
            district_feature = None
            for feature in districts_layer.getFeatures():
                if feature.attributes()[3] == selected_district_name:
                    district_feature = feature
                    break
            
            if not district_feature:
                raise QgsProcessingException(f"District '{selected_district_name}' not found in layer 'Muenster_City_Districts'.")
            
            # Extract district information
            district_attrs = district_feature.attributes()
            district_name = district_attrs[3]
            parent_district = district_attrs[4]
            
            # Calculate area from geometry
            district_geom = district_feature.geometry()
            area_m2 = district_geom.area()
            area_km2 = area_m2 / 1_000_000

            # Count households
            house_numbers_layer = QgsProject.instance().mapLayersByName('House_Numbers')[0]
            household_count = 0
            for feature in house_numbers_layer.getFeatures():
                geom = feature.geometry()
                if geom.intersects(district_geom):
                    household_count += 1
            
            # Count parcels
            parcels_layer = QgsProject.instance().mapLayersByName('Muenster_Parcels')[0]
            parcel_count = 0
            for feature in parcels_layer.getFeatures():
                geom = feature.geometry()
                if geom.intersects(district_geom):
                    parcel_count += 1
            
            # Count schools or pools
            if selected_data_type == 0:
                layer_name = 'public_swimming_pools'
            else:
                layer_name = 'Schools'
            
            data_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
            data_count = 0
            for feature in data_layer.getFeatures():
                geom = feature.geometry()
                if geom.intersects(district_geom):
                    data_count += 1
            
            data_type_name = "Pools" if selected_data_type == 0 else "Schools"
            
            # Create map image
            map_image_path = os.path.join(output_folder, f"{district_name}_map.png")
            self._create_map_image(district_feature, districts_layer, map_image_path)
            
            # Create PDF
            pdf_path = os.path.join(output_folder, f"{district_name}_profile.pdf")
            self._create_pdf(
                pdf_path,
                district_name,
                parent_district,
                area_km2,
                household_count,
                parcel_count,
                data_count,
                data_type_name,
                map_image_path,
            )
                        
            return {self.OUTPUT: output_folder}
        
        except Exception as e:
            raise QgsProcessingException(f"Error creating district profile: {str(e)}")
    
    def _create_map_image(self, district_feature, districts_layer, output_path):
        # Select district feature in canvas, zoom to selection, wait, then save image.
        canvas = iface.mapCanvas()
        canvas.setCurrentLayer(districts_layer)

        districts_layer.removeSelection()
        districts_layer.selectByIds([district_feature.id()])

        canvas.zoomToSelected(districts_layer)
        canvas.refresh()

        # Give the canvas time to draw before exporting the image.
        time.sleep(5)
        canvas.saveAsImage(output_path)

        districts_layer.removeSelection()
    
    def _create_pdf(self, pdf_path, district_name, parent_district, area_km2, household_count, parcel_count, data_count, data_type_name, map_image_path):
        # Create PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        elements = []
        
        # Use default style only and plain line breaks.
        styles = getSampleStyleSheet()
        lines = [
            f"{district_name} - District Profile",
            "",
            f"District Name: {district_name}",
            f"Parent District: {parent_district}",
            f"Area: {area_km2:.2f} km²",
            f"Number of Households: {household_count}",
            f"Number of Parcels: {parcel_count}",
            f"Number of {data_type_name}: {data_count}",
            "",
            "District Map:",
        ]

        for line in lines:
            elements.append(Paragraph(line, styles['Normal']))
            elements.append(Spacer(1, 6))
        
        # Add map image if it exists
        if os.path.exists(map_image_path):
            try:
                img = Image(map_image_path, width=150*mm, height=112.5*mm)
                elements.append(img)
            except Exception as e:
                elements.append(Paragraph(f"Could not load map image: {str(e)}", styles['Normal']))
        
        # Add timestamp
        elements.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(elements)

    def createInstance(self):
        return self.__class__()

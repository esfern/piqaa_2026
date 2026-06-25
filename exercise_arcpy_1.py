import arcpy
import os

# Set the workspace
arcpy.env.workspace = r"C:\Users\npinkern\Documents\exercise_arcpy_1.gdb"
# Make code rerunable
arcpy.env.overwriteOutput = True

SIZES = {"mast": "300 Meters", "mobile_antenna": "50 Meters", "building_antenna": "100  Meters"}

def create_buffers():
    # Lists all feature classes of type point
    point_fcs = arcpy.ListFeatureClasses(feature_type="Point")
    
    fields = ["SHAPE@", "status", "type"]
    # initiate the insert curser
    with arcpy.da.InsertCursor("active_assets", fields) as i_cur:
        # Iterate over each feature class
        for fc in point_fcs:
            if fc == "active_assets":
                continue # never read the target
            # Search for status:active features in feature class
            with arcpy.da.SearchCursor(fc, fields, where_clause="status = 'active'") as s_cur:
                for row in s_cur:
                    i_cur.insertRow(row) # insert feature into active_assets
        i_cur.delete() # Remove the insert cursor

    # empty array for all buffer layer paths
    buffers = []

    # Create a buffer layer for each feature class
    for t, dist in SIZES.items():
        lyr = f"lyr_{t}"
        arcpy.management.MakeFeatureLayer("active_assets", lyr, f"type = '{t}'")
        out = os.path.join(arcpy.env.workspace, f"buf_{t}")
        arcpy.analysis.Buffer(lyr, out, dist) # Create the buffer in output
        buffers.append(out)

    arcpy.management.Merge(buffers, "coverage") # Merge buffer layers into one layer named "coverage"

if __name__ == "__main__":
    create_buffers()
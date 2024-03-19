import os
import csv
from qgis.core import QgsVectorLayer

# Set the directory where your shapefiles are located
shapefile_directory = "D:/project/shape_files"

# Define the output CSV file path
output_csv_path = "D:/project/shape_info.csv"

# Open the CSV file for writing
with open(output_csv_path, mode='w', newline='') as csv_file:
    fieldnames = ['Layer Name', 'File Path', 'Data Source', 'Feature Count', 'Encoding', 'Geometry', 'Layer CRS']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through subfolders and shapefiles
    for root, dirs, files in os.walk(shapefile_directory):
        for file in files:
            if file.endswith('.shp'):
                shapefile_path = os.path.join(root, file)

                # Extract the Layer Name from the shapefile's base name (without the .shp extension)
                layer_name = os.path.splitext(os.path.basename(shapefile_path))[0]

                # Create a QgsVectorLayer
                layer = QgsVectorLayer(shapefile_path, layer_name, 'ogr')

                if layer.isValid():
                    provider = layer.dataProvider()
                    if provider:
                        geomTypeString = QgsWkbTypes.displayString(int(layer.wkbType()))

                        # Remove the file name from the path to get the directory path
                        file_path = os.path.dirname(shapefile_path)

                        writer.writerow({
                            'Layer Name': layer_name,
                            'File Path': file_path,
                            'Data Source': provider.dataSourceUri(),
                            'Feature Count': provider.featureCount(),
                            'Encoding': provider.encoding(),
                            'Geometry': geomTypeString,
                            'Layer CRS': layer.crs().authid()
                        })
                    else:
                        print("Data provider not available for layer:", layer_name)
                else:
                    print("Invalid layer:", layer_name)

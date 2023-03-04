import os
import xml.etree.ElementTree as ET
import csv

def get_header_row(with_bounding_box = True, classes=[]):
    result = ["filename"]
    if with_bounding_box:
        result.extend(["class", "xmin", "ymin", "xmax", "ymax"])
    else:
        result.extend(classes)

    return result
    
def xml_to_csv(xml_dir_path, output_csv_path, image_path, with_bounding_box = False, check_image_exists = True, create_empty_rows = True, classes=['Gun','Knife','Wrench','Pliers','Scissors']):
    # Get a list of all the XML files in the directory
    xml_files = [os.path.join(xml_dir_path, f) for f in os.listdir(xml_dir_path) if f.endswith('.xml')]
    jpeg_files = set([f for f in os.listdir(image_path) if f.endswith('.jpg')])
    missing_files = set()
    processed_files = set()
    
    # Create a list to hold all the rows of data
    data_rows = []
    
    # Loop through each XML file in the directory
    for xml_file in xml_files:
        # Parse the XML file
        tree = ET.parse(xml_file)
        annotation = tree.getroot()
        filename = annotation.find("filename").text
        if check_image_exists and filename not in jpeg_files:
            print("Missing image: {}".format(filename))
            missing_files.add(filename)
            continue
        processed_files.add(filename)
        objects = annotation.findall("object")

        # A row for each object found in the image (with it's coordinates)
        if with_bounding_box:
            for object in objects:
                row = []
                row.append(filename)
                object_name = object.find("name")
                if object_name is None:
                    continue
                bndbox = object.find("bndbox")
                bound_box = [i.text for i in bndbox]
                row.append(object_name.text)
                row.extend(bound_box)
                data_rows.append(row)

        # One row per image, with '1' for every found object and '0' if not found in the image
        else:
            row = []
            row.append(filename)
            objects_found = set()
            for object in objects:
                object_name = object.find("name")
                if object_name is None:
                    continue
                objects_found.add(object_name.text)
            
            class_values = []
            for object_class in classes:
                 class_values.append(1 if object_class in objects_found else 0)
            row.extend(class_values)
            data_rows.append(row)

    # If we're just tagging each image and whatever we saw in it, we need to make sure
    # we have all negative images tagged as well (the image name and 0's for all classes)
    if create_empty_rows and not with_bounding_box:
        no_annotated_files = [f for f in jpeg_files if f not in processed_files]
        for no_annotated_file in no_annotated_files:
            values = [no_annotated_file]
            values.extend([0 for i in classes])
            data_rows.append(values)
    
    # Write the data rows to a CSV file
    with open(output_csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = get_header_row(with_bounding_box, classes)
        writer.writerow(header)
        writer.writerows(data_rows)
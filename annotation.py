from utils.xml_to_csv import xml_to_csv

xml_dir_path = './Annotation/'
output_csv_path = './annotation.csv'
image_path = './dataset/JPEGImage'

xml_to_csv(xml_dir_path, output_csv_path, image_path)

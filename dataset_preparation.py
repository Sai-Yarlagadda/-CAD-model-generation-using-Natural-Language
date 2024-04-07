import os
import shutil
import csv

def directory_prep(source_directory = 'dataset/mechanical_parts', 
                   destination_directory = 'dataset/all_images'):
    """
    After downloading the dataset, get all the images into one folder using this function. 
    """

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    CAD_directories = os.listdir(source_directory)
    for CAD_directory in CAD_directories:
        directory_folder = os.path.join(source_directory, CAD_directory)
        png_files = [f for f in os.listdir(directory_folder) if f.endswith('.png') or f.endswith('.jpg')]

        if 'JPEG' in os.listdir(directory_folder):
            directory_folder = os.path.join(directory_folder, 'JPEG')
            png_files.extend([f for f in os.listdir(directory_folder) if f.endswith('.png') or f.endswith('.jpg')])
            if 'IMAGE' in os.listdir(directory_folder):
                directory_folder = os.path.join(directory_folder, 'IMAGE')
                png_files.extend([f for f in os.listdir(directory_folder) if f.endswith('.png') or f.endswith('.jpg')])

        for index, png_file in enumerate(png_files, start=1):
            source_path = os.path.join(directory_folder, png_file)
            new_filename = f'{CAD_directory}_{index}.png' 
            destination_path = os.path.join(destination_directory, new_filename)
            shutil.copy(source_path, destination_path)

def csv_preparation(source_filepath):
    if not os.path.isdir(source_filepath):
        print(f'Not a filepath')

    png_files = os.listdir(source_filepath)
    with open('dataset.csv', 'w', newline='') as csv_file:
        csvwriter = csv.writer(csv_file)
    
        for filename in png_files:
            csvwriter.writerow([filename])

if __name__ == '__main__':
    csv_preparation('dataset/all_images')
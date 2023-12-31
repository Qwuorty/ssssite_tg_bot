import zipfile
import os

def make_zips():
    file_names = os.listdir('folders')

    for number in range(len(file_names)//1000+1):
        folder_paths = file_names[number*1000:min((number+1)*1000,len(file_names))]
        zip_file_name = f'zips/check{number}.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zipf:
            for folder_path in folder_paths:
                for root, _, files in os.walk('folders/'+folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, os.path.dirname(folder_path)))
    return 1
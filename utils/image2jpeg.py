import argparse
import glob
import subprocess
import re
import logging
import traceback
import os
from PIL import Image


def image2jpeg(path_images):
    file_list = glob.glob(f"{path_images}/*.jpeg")
    print(len(file_list))
    for file_obj in file_list:
        try:
            jpg_str = subprocess.check_output(['file', file_obj]).decode()
            if re.search('TIFF image data', jpg_str, re.IGNORECASE) or re.search('Web/P image', jpg_str, re.IGNORECASE) or re.search('PNG image data', jpg_str, re.IGNORECASE) or re.search('Png patch', jpg_str, re.IGNORECASE):
                try:
                    image = Image.open(file_obj)
                    image_converting = image.convert("RGB")
                    image_converting.save(file_obj, "JPEG", quality=100)
                    #subprocess.run(['rm', file_obj])
                    print("Found JPEG hiding as other type, conversion successful:", file_obj)
                except:
                    print("Found PNG hiding as other type, no conversion:", file_obj)

        except Exception as e:
            logging.error(traceback.format_exc())

    print("Cleaning JPEGs done")


def folders_image2jpeg(path_folders):
    list_path_folders = [x[0] for x in os.walk(path_folders)][1:]
    for path_folder in list_path_folders:
        print(f"verifying images in {path_folder}")
        print("-" * 50)
        image2jpeg(path_folder)


parser = argparse.ArgumentParser()
parser.add_argument("-path", "-p", type=str, help="path images or images folders")
parser.add_argument("-has_directories", "-d", help="to analyze to directories with images", action="store_true", default=False)

args = parser.parse_args()

path = args.path
has_directories = args.has_directories

if has_directories:
    folders_image2jpeg(path)
else:
    image2jpeg(path)


#image2jpeg("./images/conflicto armado en colombia")
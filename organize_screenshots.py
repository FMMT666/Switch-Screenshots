# Renan Greca, 2017
# This code is free to distribute and alter.

# Place this script in the same directory as the Switch's Album folder.
# View README.md for more details.
# More information: https://github.com/RenanGreca/Switch-Screenshots

import argparse
import json
import os
import sys
from collections import namedtuple
from shutil import copy2


# List of allowed extensions for files
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".mp4"]
TIMESTAMP_LEN = 16
GAME_ID_LEN = 32

# Argument parser
parser = argparse.ArgumentParser(description='''Nintendo Switch screenshot organizer.
                    Identifies images and creates new directory structure based on game title.
                    More information: https://github.com/RenanGreca/Switch-Screenshots''')
parser.add_argument('-i', '--input_dir', type=str, required=False, default='./Album/',
                    help='(str) Path to the Album directory. Default: ./Album/')
parser.add_argument('-o', '--output_dir', type=str, required=False, default='./Output/',
                    help='(str) Desired output directory. Default: ./Output/')


GameImage = namedtuple("GameImage", ("path", "timestamp", "game_id", "extension"))

# Create a list of all the image/video files in the Album directory.
# Thanks to L. Teder
# https://stackoverflow.com/a/36898903
def list_images(dir):
    r = []
    for root, _, files in os.walk(dir):
        for name in files:
            path = os.path.join(root, name)
            _, extension = os.path.splitext(path)
            if extension in ALLOWED_EXTENSIONS:
                timestamp = name[0:TIMESTAMP_LEN]
                game_id= name[TIMESTAMP_LEN + 1:TIMESTAMP_LEN + GAME_ID_LEN + 1]
                game_image = GameImage(path=path, timestamp=timestamp, extension=extension, game_id=game_id)
                r.append(game_image)
    return r


def organize_screenshots(game_ids, input_dir, output_dir):
    images = list_images(input_dir)
    count = len(images)

    not_found = set()
    # Iterate over images
    for idx, image in enumerate(images):
        folder_name = image.game_id
        if image.game_id in game_ids:
            # If the ID was in the JSON file, the directory is named with the title
            folder_name = game_ids[image.game_id]
        else:
            not_found.add(image.game_id)

        # Create the directory and copy the file
        path = os.path.join(output_dir, folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
        copy2(image.path, path)

        # Print progress indicator
        sys.stdout.write("\r"+str(idx+1)+"/"+str(count))
        sys.stdout.flush()

    if len(not_found):
        print("\nNames not found for the following game IDs:")
        print("\n".join(sorted(not_found)))

if __name__ == '__main__':
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir

    # Load game IDs file
    with open('game_ids.json') as data_file:
        game_ids = json.load(data_file)

    organize_screenshots(game_ids, input_dir, output_dir)

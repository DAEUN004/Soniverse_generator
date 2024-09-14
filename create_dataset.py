from utils.openai import generate_image
from utils.openai import caption_image
import os
import json
import csv
import unidecode

import argparse
import random
import datetime
from urllib.request import urlretrieve
'''
generate_image(prompt, size='1024x1024', img_model='dall-e-2')
caption_image(url)

'''
def write_json_as_csv(json_in, csv_out):

    with open(csv_out, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['file_name','text'])

        for k in json_in.keys():
            text = unidecode(json_in[k])
            assert text.isascii()
            csv_writer.writerow([k, text])

def load_from_csv(csv_file):

    meta = {}
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read column headers
        for row in reader:
            meta.update({row[0]: row[1]})

    return meta

def generate_filename():
    return datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S_" + str(random.randint(0, 1000)) + '.png')

def generate_dataset(prompt, dataset_folder, meta, num_datapoints, img_size, img_model):

    if meta is None:
        meta = {}

    for i in range(num_datapoints):

        image_url = generate_image(prompt=prompt, size=img_size, img_model=img_model)
        print("done")
        caption = caption_image(image_url)
        print("done")
            
        print("GENERATED:")
        print(caption)

        img_filename = os.path.join('my_dataset/data', generate_filename())
            
        urlretrieve(image_url, img_filename)
            
        meta.update({img_filename: caption})
    return meta


if __name__ == "__main__":

    # Replace parser arguments with predefined values
    # prompt_file = 'example_prompt.txt'  # Text file containing the text prompt
    output_folder = 'my_dataset'        # Output folder to save the dataset
    img_size = '1024x1024'                # Image size
    num_datapoints = 1              # Number of datapoints to generate
    img_model = 'dall-e-2'              # Image model to use

    # Ensure the output folders exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'data'), exist_ok=True)

    # # Read prompt from the file
    # with open(prompt_file, "r") as txt_file:
    #     prompt = txt_file.read()
    prompt = "a front view of an AI engineer in the style of a block game. The AI engineer should be in the centre of the image and it should not be cut off. The background should be as epic as possible. The title word should be I AM AN AI ENGINEER."


    # Metadata file path
    metadata_csv_file = os.path.join(output_folder, 'metadata.csv')

    # Check if metadata CSV already exists
    if os.path.exists(metadata_csv_file):
        print("Metadata found, updating the current meta with new files")
        meta = load_from_csv(metadata_csv_file)
    else:
        meta = None

    # Generate the dataset
    meta = generate_dataset(
        prompt=prompt, 
        dataset_folder=output_folder,
        meta=meta,
        num_datapoints=num_datapoints, 
        img_size=img_size, 
        img_model=img_model
    )

    print("Done creating dataset. Dataset size is currently " + str(len(meta)) + " files")

    # Write metadata to CSV
    write_json_as_csv(meta, metadata_csv_file)
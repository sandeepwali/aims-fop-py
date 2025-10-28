import os
import glob
import requests
import base64
import threading
from datetime import datetime
from shutil import copy2
from os.path import join, dirname, realpath, basename, splitext

import common

# Constants
INPUT_DIR = "input"
SERVICE_URL = "http://localhost:8000/generate-image/"
semaphore = threading.Semaphore(5)  # Limit to 5 threads

def send_request(xml_content, xslt_content):
    """Send POST request to the service and get the PNG image."""
    response = requests.post(SERVICE_URL, json={"xml": xml_content, "xslt": xslt_content})

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return None
    
    return base64.b64decode(response.json()['image'])

def threaded_invoke(xml_file, xsl_file, out_path):
    """Threaded version of the send_request logic."""
    with semaphore:
        base_xml_file = basename(xml_file)
        base_xsl_file_without_extension = splitext(basename(xsl_file))[0]
        png_path = join(out_path, f"{base_xsl_file_without_extension}_{splitext(base_xml_file)[0]}.png")

        with open(xml_file, 'r', encoding='utf-8') as f_xml, open(xsl_file, 'r', encoding='utf-8') as f_xslt:
            logger.info(f"Sending {xml_file} {xsl_file}")
            image_data = send_request(f_xml.read(), f_xslt.read())

            if image_data:
                output_filename = png_path
                logger.info(f"Writing {output_filename}...")
                with open(output_filename, 'wb') as out_file:
                    out_file.write(image_data)

def invoke_image_generation(xml_files, xsl_file, out_path):
    """Invokes image generation for given XML files using XSL files."""
    threads = []

    for xml_file in xml_files:
        thread = threading.Thread(target=threaded_invoke, args=(xml_file, xsl_file, out_path))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def main():
    script_dir = dirname(realpath(__file__))
    input_dir = join(script_dir, "input")
    xsl_files = glob.glob(join(input_dir, '**', '*.xsl'), recursive=True)

    logger.info(f"Found {len(xsl_files)} Xsl File(s)")

    for xsl_file in xsl_files:
        xsl_folder = basename(dirname(xsl_file))
        out_path = join(script_dir, "output", f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_{xsl_folder}')
        os.makedirs(out_path, exist_ok=True)
        dest_path = join(out_path, basename(xsl_file))
        copy2(xsl_file, dest_path)
        
        xml_files = glob.glob(join(dirname(xsl_file), '*.xml'))
        invoke_image_generation(xml_files, xsl_file, out_path)

        # Copying the generated files to out_path instead of moving them.
        for file in xml_files:
            dest_path = join(out_path, basename(file))
            if not os.path.exists(dest_path):  # Avoid overwriting
                copy2(file, dest_path)

if __name__ == "__main__":
    logger = common.set_logger(log_file="./logs/send_request.log")
    main()

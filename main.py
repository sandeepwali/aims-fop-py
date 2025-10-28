import os
import glob
import logging
import threading
from datetime import datetime
from shutil import copy2
from os.path import join, dirname, realpath, basename, splitext

import common
import fop

# Setting up a global logger variable
logger = logging.getLogger()

def invoke_image_generation(xml_files, xsl_file, script_root, out_path):
    """
    Invokes image generation for given XML files using XSL files.

    Args:
    - xml_files: List of paths to XML files.
    - xsl_file: Path to the XSL file.
    - script_root: Root directory of the script.
    - out_path: Output directory to save generated images.

    Returns: None
    """
    jar_bin = join(script_root, "bin")
    threads = []

    for xml_file in xml_files:
        base_xml_file = basename(xml_file)
        base_xsl_file_without_extension = splitext(basename(xsl_file))[0]
        png_path = join(out_path, f"{base_xsl_file_without_extension}_{splitext(base_xml_file)[0]}.png")

        thread = threading.Thread(target=fop.generate_image, args=(jar_bin, xml_file, xsl_file, png_path))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def main():
    """
    Main execution function.

    Returns: None
    """
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
        invoke_image_generation(xml_files, xsl_file, script_dir, out_path)

        # Copying the generated files to out_path instead of moving them.
        for file in xml_files:
            dest_path = join(out_path, basename(file))
            if not os.path.exists(dest_path):  # Avoid overwriting
                copy2(file, dest_path)

if __name__ == "__main__":
    logger = common.set_logger(log_file="./logs/main.log")
    main()

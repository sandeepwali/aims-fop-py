import logging
import os
from subprocess import call, CalledProcessError

def generate_image(jar_bin, xml_path, xsl_path, png_path):
    """
    Generates image using FOP.

    Args:
    - jar_bin: Path to the directory containing fop.jar.
    - xml_path: Path to the input XML file.
    - xsl_path: Path to the XSL file.
    - png_path: Path to save the generated PNG image.

    Returns: None
    """
    logging.info(f"Generating image {png_path}")
    
    cmd = ["java", "-jar", os.path.join(jar_bin, "fop.jar"), "-c", "conf.xml", "-xml", xml_path, "-xsl", xsl_path, "-png", png_path]
    
    try:
        # Use cwd parameter to execute the command in the jar_bin directory.
        call(cmd, cwd=jar_bin)
    except CalledProcessError:
        logging.error(f"Error executing command for {xml_path} using {xsl_path}.")
    except Exception as e:
        logging.error(f"Unexpected error generating image for {xml_path} using {xsl_path}. Error: {str(e)}")

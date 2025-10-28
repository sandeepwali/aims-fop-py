from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, Body
from starlette.responses import JSONResponse

from subprocess import call, Popen, PIPE
import os
import base64
import tempfile
import uvicorn
import logging

logger = logging.getLogger()

app = FastAPI()

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
JAR_BIN = os.path.join(SCRIPT_DIR, "bin")

@app.post("/generate-image/")
async def generate_image(data: dict = Body(...)):
    try:
        xml_data = data.get('xml')
        xslt_data = data.get('xslt')
        # Create temporary files for XML, XSLT, and PNG
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as xml_file:
            xml_file.write(xml_data.encode())

        with tempfile.NamedTemporaryFile(suffix=".xsl", delete=False) as xslt_file:
            xslt_file.write(xslt_data.encode())

        png_path = f"{xml_file.name}.png"

        logger.info(f"Generating images {xml_file.name}, {xslt_file.name} to {png_path}")

        # Run the Java command to generate PNG
        process = Popen([
            "java", "-jar", os.path.join(JAR_BIN, "fop.jar"), 
            "-c", "conf.xml", 
            "-xml", xml_file.name, 
            "-xsl", xslt_file.name, 
            "-png", png_path
        ], cwd=JAR_BIN, stdout=PIPE, stderr=PIPE)

        stdout, stderr = process.communicate()

        if stdout:
            logger.info(stdout.decode())

        if stderr:
            logger.error(stderr.decode())

        if process.returncode != 0:
            raise HTTPException(status_code=500, detail="Failed to generate image")

        # Read and encode the generated PNG
        with open(png_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

        # Cleanup temporary files
        os.remove(xml_file.name)
        os.remove(xslt_file.name)
        os.remove(png_path)

        return {"image": encoded_string}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

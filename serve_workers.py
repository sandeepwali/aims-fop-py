import uvicorn
import common  # Import the common module to initialize and set up logging

# Set up the logger using the function from common.py and specify the log file as 'serve.log'
logger = common.set_logger(log_file="./logs/serve.log")

# Now you can use the logger for any logging needs in this script:
logger.info("Starting the server...")

if __name__ == "__main__":
    uvicorn.run("serve:app", host="0.0.0.0", port=8000, workers=10, log_config=None)  # Set log_config=None to disable Uvicorn's default logging

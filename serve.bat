@echo off

:: Start the serve.py script in the background
start /B python.exe serve.py

:: Wait for 1 second (1000 milliseconds)
timeout /T 1 /NOBREAK

:: Execute the send_request.py script
python.exe send_request.py

:: Kill all python instances
taskkill /IM python.exe /F

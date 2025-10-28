@echo off

:: Start the serve.py script in the background
start /B python.exe serve_workers.py

:: Wait for 5 seconds
timeout /T 5 /NOBREAK

:: Execute the send_request.py script
python.exe send_request.py

:: Kill all python instances
taskkill /IM python.exe /F

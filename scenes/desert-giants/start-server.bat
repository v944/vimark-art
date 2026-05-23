@echo off
cd /d "%~dp0"
echo Starting local server on port 8080...
echo Open http://localhost:8080 in your browser
echo.
python3 -m http.server 8080
pause

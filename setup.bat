@echo off
echo Setting up The Automator...

call npm install
cd frontend
call npm install
cd ..

cd backend
call pip install -r requirements.txt
call python -m playwright install chromium
cd ..

if not exist "config" mkdir config
if not exist "media" mkdir media
if not exist "data" mkdir data
if not exist "logs" mkdir logs

if not exist "config\.env" (
    copy "config\.env.example" "config\.env" >nul 2>&1
    if not exist "config\.env" echo # Add your API keys to config/.env > config\.env
)

echo.
echo Setup complete!
echo.
echo NEXT STEPS:
echo 1. Edit config\.env and add your API keys
echo 2. Run: npm start
echo.
echo Required keys to get started:
echo   - ANTHROPIC_API_KEY (for content generation)
echo   - At least one platform API (Instagram, TikTok, etc.)
echo.

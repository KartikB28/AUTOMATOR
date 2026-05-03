#!/bin/bash
echo "Setting up The Automator..."

npm install
cd frontend && npm install && cd ..

cd backend
pip install -r requirements.txt
python -m playwright install chromium
cd ..

mkdir -p config media data logs
if [ ! -f config/.env ]; then
    cp config/.env.example config/.env 2>/dev/null || echo "# Add your API keys to config/.env" > config/.env
fi

echo ""
echo "Setup complete!"
echo ""
echo "NEXT STEPS:"
echo "1. Edit config/.env and add your API keys"
echo "2. Run: npm start"
echo ""
echo "Required keys to get started:"
echo "  - ANTHROPIC_API_KEY (for content generation)"
echo "  - At least one platform API (Instagram, TikTok, etc.)"
echo ""

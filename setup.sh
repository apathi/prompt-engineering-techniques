#!/bin/bash
# Setup script for prompt engineering implementations

echo "Setting up prompt engineering implementations..."

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To activate the environment manually:"
echo "source .venv/bin/activate"
echo ""
echo "To test the implementation:"
echo "python test_batch1.py"
#!/bin/bash

# Name of the virtual environment directory
VENV_DIR=".venv"

# Check if the virtual environment directory already exists
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment '$VENV_DIR' already exists. Activating..."
else
    echo "Creating virtual environment '$VENV_DIR'..."
    # Create the virtual environment
    python3 -m venv "$VENV_DIR"
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment. Make sure python3-venv is installed."
        exit 1
    fi
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Create requirements.txt on the fly if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "Creating requirements.txt..."
    cat << EOF > requirements.txt
telethon
pysocks
python-socks[asyncio]
EOF
fi

# Install the required packages
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "------------------------------------------------"
echo "Setup complete! Virtual environment is active."
echo "To activate it manually in the future, run:"
echo "source $VENV_DIR/bin/activate"
echo "------------------------------------------------"
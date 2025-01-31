#!/bin/bash

OS=$(uname)

# Linux or Mac
if [ "$OS" = "Linux" ] || [ "$OS" = "Darwin" ]; then
    echo "Detected $OS. Running PyInstaller to create a standalone executable."
else
    echo "The installation script is not implemented for $OS."
    exit 1
fi

if ! [ -x "$(command -v uv)" ]; then
    echo "uv not found. Please install uv before running this script."
    exit 1
fi

# Check for custom installation path
if [ -z "$1" ]; then
    INSTALL_PATH="$HOME/.local/bin"
else
    INSTALL_PATH="$1"
fi

# Activate the virtual environment
uv venv
source .venv/bin/activate

# Install pyinstaller within the new virtual environment
uv add pyinstaller

# Call the tool
pyinstaller --onefile --name fob src/fob/__init__.py

# Copy the executable to the custom installation path
echo "Copying the executable to $INSTALL_PATH..."

mkdir -p "$INSTALL_PATH"
cp dist/fob "$INSTALL_PATH"

# Clean up
echo "Cleaning up..."
rm -r dist build fob.spec

echo "Installation complete. The 'fob' command is now available in $INSTALL_PATH. If not, please check that $INSTALL_PATH is in your PATH environment variable."

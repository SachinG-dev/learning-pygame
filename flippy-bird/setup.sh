#!/bin/bash

# Update package list (for Linux users)
echo "Updating package list..."
sudo apt update -y 2>/dev/null || echo "Skipping update on non-Linux system."

# Install system dependencies for OpenCV (only needed for Linux)
echo "Installing system dependencies for OpenCV..."
sudo apt install -y libgl1-mesa-glx libglib2.0-0 2>/dev/null || echo "Skipping system dependencies."

# Install Python virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required Python packages
echo "Installing required Python packages..."
pip install pygame opencv-python mediapipe numpy

# Print success message
echo "✅ All required packages installed successfully!"
echo "Run the game with: source venv/bin/activate && python game.py"

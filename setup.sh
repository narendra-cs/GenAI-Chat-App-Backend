#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

echo "\nSetup complete! Your virtual environment is ready to use.\n"
echo "To activate the virtual environment, run:"
echo "source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate\n"

echo "To run the FastAPI server:"
echo "uvicorn app.main:app --reload\n"

echo "To run tests:"
echo "pytest\n"

echo "To format code:"
echo "black ."
echo "isort ."
echo "flake8"
echo "mypy ."

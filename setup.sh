#!/bin/bash
# Setup script for nanoleaf-local test rig

echo "======================================"
echo "Nanoleaf CoAP Test Rig Setup"
echo "======================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed."
    echo "Please install pip for Python 3."
    exit 1
fi

# Determine pip command
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
else
    PIP_CMD="pip"
fi

echo "Using pip: $PIP_CMD"
echo ""

# Install dependencies
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "Setup Complete!"
    echo "======================================"
    echo ""
    echo "Next steps:"
    echo "1. Set your environment variables:"
    echo "   export NANOLEAF_IPV6='your-device-ipv6-address'"
    echo "   export NANOLEAF_TOKEN='your-access-token'"
    echo ""
    echo "2. Run the test rig:"
    echo "   python3 test_rig.py interactive  # For interactive mode"
    echo "   python3 test_rig.py test         # For automated tests"
    echo "   python3 example.py               # For a simple example"
    echo ""
    echo "See README.md for detailed documentation."
else
    echo ""
    echo "Error: Failed to install dependencies."
    echo "Please check the error messages above."
    exit 1
fi

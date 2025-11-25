#!/usr/bin/env bash
#
# setup_nixtla_env.sh
#
# Convenience helper for Nixtla Baseline Lab – automated Nixtla OSS environment setup.
#
# Purpose:
#   - Check that Python 3 and pip are available
#   - Install Nixtla open-source dependencies from scripts/requirements.txt
#   - Optionally create a dedicated virtualenv with --venv flag
#   - Verify installations by printing versions
#
# Usage:
#   ./scripts/setup_nixtla_env.sh            # Install into current environment
#   ./scripts/setup_nixtla_env.sh --venv     # Create .venv-nixtla-baseline and install there
#
# Intended for local development and demo use.
#

set -euo pipefail

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Parse arguments
USE_VENV=false
if [[ "${1:-}" == "--venv" ]]; then
    USE_VENV=true
fi

echo -e "${GREEN}=== Nixtla Baseline Lab – Environment Setup ===${NC}"
echo ""

# Check that we're in the plugin directory
if [[ ! -f "scripts/requirements.txt" ]]; then
    echo -e "${RED}ERROR: scripts/requirements.txt not found.${NC}"
    echo "Please run this script from the plugin root:"
    echo "  cd plugins/nixtla-baseline-lab"
    echo "  ./scripts/setup_nixtla_env.sh"
    exit 1
fi

# Check Python 3
echo -e "${YELLOW}[1/5] Checking for Python 3...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: python3 not found.${NC}"
    echo ""
    echo "Please install Python 3.8+ before running this script:"
    echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  - macOS: brew install python3"
    echo "  - See: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Found: ${PYTHON_VERSION}${NC}"
echo ""

# Check pip
echo -e "${YELLOW}[2/5] Checking for pip...${NC}"
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo -e "${RED}ERROR: pip not found.${NC}"
    echo ""
    echo "Please install pip before running this script:"
    echo "  - Ubuntu/Debian: sudo apt-get install python3-pip"
    echo "  - macOS: python3 -m ensurepip"
    echo "  - See: https://pip.pypa.io/en/stable/installation/"
    exit 1
fi

PIP_VERSION=$(python3 -m pip --version 2>/dev/null || pip3 --version)
echo -e "${GREEN}✓ Found: ${PIP_VERSION}${NC}"
echo ""

# Handle virtualenv creation if requested
if [[ "$USE_VENV" == true ]]; then
    echo -e "${YELLOW}[3/5] Creating virtualenv (.venv-nixtla-baseline)...${NC}"

    if [[ -d ".venv-nixtla-baseline" ]]; then
        echo "Virtual environment already exists. Skipping creation."
    else
        python3 -m venv .venv-nixtla-baseline
        echo -e "${GREEN}✓ Created .venv-nixtla-baseline${NC}"
    fi

    echo "Activating virtualenv..."
    # shellcheck disable=SC1091
    source .venv-nixtla-baseline/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
    echo ""
else
    echo -e "${YELLOW}[3/5] Using current Python environment...${NC}"
    echo "(To use a dedicated virtualenv, run: ./scripts/setup_nixtla_env.sh --venv)"
    echo ""
fi

# Install dependencies
echo -e "${YELLOW}[4/5] Installing Nixtla OSS dependencies from requirements.txt...${NC}"
echo "This may take 1-2 minutes..."
echo ""

python3 -m pip install --upgrade pip
python3 -m pip install -r scripts/requirements.txt

echo ""
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Verify installations
echo -e "${YELLOW}[5/5] Verifying installations...${NC}"
echo ""

# Check statsforecast
if python3 -m pip show statsforecast &> /dev/null; then
    STATSFORECAST_VERSION=$(python3 -m pip show statsforecast | grep "Version:" | cut -d' ' -f2)
    echo -e "${GREEN}✓ statsforecast ${STATSFORECAST_VERSION}${NC}"
else
    echo -e "${RED}✗ statsforecast not found${NC}"
fi

# Check datasetsforecast
if python3 -m pip show datasetsforecast &> /dev/null; then
    DATASETSFORECAST_VERSION=$(python3 -m pip show datasetsforecast | grep "Version:" | cut -d' ' -f2)
    echo -e "${GREEN}✓ datasetsforecast ${DATASETSFORECAST_VERSION}${NC}"
else
    echo -e "${RED}✗ datasetsforecast not found${NC}"
fi

# Check pandas
if python3 -m pip show pandas &> /dev/null; then
    PANDAS_VERSION=$(python3 -m pip show pandas | grep "Version:" | cut -d' ' -f2)
    echo -e "${GREEN}✓ pandas ${PANDAS_VERSION}${NC}"
else
    echo -e "${RED}✗ pandas not found${NC}"
fi

# Check numpy
if python3 -m pip show numpy &> /dev/null; then
    NUMPY_VERSION=$(python3 -m pip show numpy | grep "Version:" | cut -d' ' -f2)
    echo -e "${GREEN}✓ numpy ${NUMPY_VERSION}${NC}"
else
    echo -e "${RED}✗ numpy not found${NC}"
fi

echo ""
echo -e "${GREEN}=== Setup Complete ===${NC}"
echo ""

if [[ "$USE_VENV" == true ]]; then
    echo "Virtual environment created at: .venv-nixtla-baseline/"
    echo ""
    echo "To activate it manually in the future:"
    echo "  source .venv-nixtla-baseline/bin/activate"
    echo ""
fi

echo "Next steps:"
echo "  1. In Claude Code, run: /nixtla-baseline-m4 horizon=7 series_limit=5"
echo "  2. Ask Claude: \"Which baseline model performed best overall in the last run?\""
echo ""
echo -e "${GREEN}Ready to run Nixtla baselines!${NC}"

exit 0

#!/usr/bin/env bash
#
# Development Environment Setup Script
# Sets up the local development environment for Claude Code Plugins for Nixtla
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored output
print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version | cut -d' ' -f2)
        print_info "Found Python $python_version"

        # Check if version is 3.9 or higher
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3,9) else 1)'; then
            print_info "Python version is compatible"
        else
            print_error "Python 3.9 or higher is required"
            exit 1
        fi
    else
        print_error "Python 3 is not installed"
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    if [ -d "venv" ]; then
        print_warn "Virtual environment already exists"
    else
        print_info "Creating virtual environment..."
        python3 -m venv venv
        print_info "Virtual environment created"
    fi
}

# Activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."
    # Note: This won't actually activate in the parent shell
    # User needs to run: source venv/bin/activate
    print_warn "Run 'source venv/bin/activate' to activate the virtual environment"
}

# Install dependencies
install_deps() {
    print_info "Installing dependencies..."

    if [ -f "venv/bin/pip" ]; then
        venv/bin/pip install --upgrade pip setuptools wheel
        venv/bin/pip install -r requirements-dev.txt
        print_info "Dependencies installed"
    else
        print_error "Virtual environment not found. Please create it first."
        exit 1
    fi
}

# Setup pre-commit hooks
setup_precommit() {
    if [ -f "venv/bin/pre-commit" ]; then
        print_info "Setting up pre-commit hooks..."
        venv/bin/pre-commit install
        print_info "Pre-commit hooks installed"
    else
        print_warn "Pre-commit not found, skipping hook setup"
    fi
}

# Create .env file
create_env_file() {
    if [ -f ".env" ]; then
        print_warn ".env file already exists"
    else
        print_info "Creating .env file..."
        cat > .env << 'EOF'
# Nixtla API Configuration
NIXTLA_API_KEY=your-api-key-here

# Cloud Provider Configuration (Optional)
# AWS_ACCESS_KEY_ID=your-aws-key
# AWS_SECRET_ACCESS_KEY=your-aws-secret
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
# AZURE_STORAGE_CONNECTION_STRING=your-connection-string

# Environment
ENV=development

# Logging
LOG_LEVEL=INFO
EOF
        print_info ".env file created - please update with your API keys"
    fi
}

# Main setup flow
main() {
    print_info "Setting up development environment for Claude Code Plugins for Nixtla"
    echo ""

    check_python
    create_venv
    install_deps
    setup_precommit
    create_env_file

    echo ""
    print_info "Setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Activate the virtual environment: source venv/bin/activate"
    echo "2. Update .env with your API keys"
    echo "3. Run tests: pytest"
    echo "4. Start developing!"
}

# Run main function
main "$@"
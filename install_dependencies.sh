#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 E-commerce Chatbot - Dependency Installation${NC}"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found. Please install Python 3.9+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo -e "${RED}❌ pip not found. Please install pip${NC}"
    exit 1
fi

echo -e "${GREEN}✓ pip found${NC}"

# Upgrade pip
echo -e "${YELLOW}📦 Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install requirements
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All dependencies installed successfully!${NC}"
else
    echo -e "${RED}❌ Error installing dependencies${NC}"
    exit 1
fi

# Verify installations
echo -e "${YELLOW}🔍 Verifying installations...${NC}"

python3 -c "import streamlit; print(f'✓ Streamlit {streamlit.__version__}')" 2>/dev/null || echo "❌ Streamlit verification failed"
python3 -c "import pymongo; print(f'✓ PyMongo {pymongo.__version__}')" 2>/dev/null || echo "❌ PyMongo verification failed"
python3 -c "import langchain; print(f'✓ LangChain {langchain.__version__}')" 2>/dev/null || echo "❌ LangChain verification failed"

echo -e "${GREEN}=================================================="
echo -e "✅ Setup complete!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Create .streamlit/secrets.toml with your API keys"
echo "2. Run: streamlit run streamlit_app.py"
echo "=================================================="

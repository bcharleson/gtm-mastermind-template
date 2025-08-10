#!/bin/bash

# GTM Alpha Template Setup Script
# This script helps you quickly set up a new GTM Alpha project for a client

echo "🚀 GTM Alpha Project Setup"
echo "========================="

# Get client information
read -p "Enter client name: " CLIENT_NAME
read -p "Enter industry (saas/ecommerce/financial/healthcare/other): " INDUSTRY
read -p "Enter primary product name: " PRODUCT_NAME
read -p "Enter project directory name: " PROJECT_DIR

# Create project directory
if [ -d "../$PROJECT_DIR" ]; then
    echo "❌ Directory ../$PROJECT_DIR already exists!"
    exit 1
fi

echo "📁 Creating project directory: ../$PROJECT_DIR"
cp -r . "../$PROJECT_DIR"
cd "../$PROJECT_DIR"

# Remove the setup script from the new directory
rm setup_new_client.sh

# Function to replace placeholders in a file
replace_placeholders() {
    local file=$1
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/\[CLIENT_NAME\]/$CLIENT_NAME/g" "$file"
        sed -i '' "s/\[INDUSTRY\]/$INDUSTRY/g" "$file"
        sed -i '' "s/\[PRODUCT_NAME\]/$PRODUCT_NAME/g" "$file"
        sed -i '' "s/\[START_DATE\]/$(date +%Y-%m-%d)/g" "$file"
    else
        # Linux
        sed -i "s/\[CLIENT_NAME\]/$CLIENT_NAME/g" "$file"
        sed -i "s/\[INDUSTRY\]/$INDUSTRY/g" "$file"
        sed -i "s/\[PRODUCT_NAME\]/$PRODUCT_NAME/g" "$file"
        sed -i "s/\[START_DATE\]/$(date +%Y-%m-%d)/g" "$file"
    fi
}

# Replace placeholders in documentation files
echo "📝 Customizing documentation for $CLIENT_NAME..."
replace_placeholders "docs/PROJECT_PLAN.md"
replace_placeholders "README.md"
replace_placeholders "config/research_prompts.py"

# Create initial .env file
echo "🔐 Creating .env file..."
cp .env.example .env

# Initialize git repository
echo "📦 Initializing git repository..."
git init
git add .
git commit -m "Initial commit for $CLIENT_NAME GTM Alpha project"

# Create virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv

# Final instructions
echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. cd ../$PROJECT_DIR"
echo "2. source venv/bin/activate"
echo "3. pip install -r requirements.txt"
echo "4. Edit .env with your API keys"
echo "5. Review and customize docs/PROJECT_PLAN.md"
echo "6. Start building your GTM Alpha solution!"
echo ""
echo "📚 Don't forget to read docs/TEMPLATE_INSTRUCTIONS.md for detailed customization guide."
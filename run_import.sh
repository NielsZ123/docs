#!/bin/bash

# Kordiam Excel Importer - Easy Run Script
# This script helps you run the importer without storing credentials in files

echo "Kordiam Excel Importer"
echo "====================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo

# Check for required files
if [ ! -f "kordiam_excel_importer.py" ]; then
    echo "Error: kordiam_excel_importer.py not found!"
    exit 1
fi

if [ ! -f "kordiam_mapping.json" ]; then
    echo "Error: kordiam_mapping.json not found!"
    exit 1
fi

# Get credentials if not set as environment variables
if [ -z "$KORDIAM_CLIENT_ID" ]; then
    echo "Enter your Kordiam OAuth2 credentials:"
    read -p "Client ID: " KORDIAM_CLIENT_ID
    export KORDIAM_CLIENT_ID
fi

if [ -z "$KORDIAM_CLIENT_SECRET" ]; then
    read -s -p "Client Secret: " KORDIAM_CLIENT_SECRET
    export KORDIAM_CLIENT_SECRET
    echo
fi

# Get Excel file path
if [ -z "$1" ]; then
    echo
    read -p "Enter path to Excel file: " EXCEL_FILE
else
    EXCEL_FILE="$1"
fi

# Check if Excel file exists
if [ ! -f "$EXCEL_FILE" ]; then
    echo "Error: Excel file '$EXCEL_FILE' not found!"
    exit 1
fi

echo
echo "Configuration:"
echo "- Client ID: $KORDIAM_CLIENT_ID"
echo "- Client Secret: [HIDDEN]"
echo "- Excel file: $EXCEL_FILE"
echo

# Ask for dry run
read -p "Run in dry-run mode first? (y/n): " DRY_RUN

echo
echo "Starting import..."

if [ "$DRY_RUN" = "y" ] || [ "$DRY_RUN" = "Y" ]; then
    echo "Running in DRY-RUN mode (no actual elements will be created)..."
    python3 kordiam_excel_importer.py "$EXCEL_FILE" --dry-run
    
    echo
    read -p "Dry run completed. Run actual import? (y/n): " REAL_RUN
    
    if [ "$REAL_RUN" = "y" ] || [ "$REAL_RUN" = "Y" ]; then
        echo "Running ACTUAL import..."
        python3 kordiam_excel_importer.py "$EXCEL_FILE"
    else
        echo "Import cancelled."
    fi
else
    echo "Running ACTUAL import..."
    python3 kordiam_excel_importer.py "$EXCEL_FILE"
fi

echo "Done!"
# 🚀 Quick Start Guide - Kordiam Excel Importer

This guide shows you exactly how to run the Kordiam Excel Importer with your OAuth2 credentials **without** storing them in files.

## Prerequisites

- Python 3.7 or higher
- Your Kordiam OAuth2 credentials (client_id and client_secret)
- An Excel file with data to import

## Method 1: Easy Run Scripts (Recommended)

### For Linux/Mac:
```bash
# Make the script executable (first time only)
chmod +x run_import.sh

# Run the importer - it will ask for your credentials
./run_import.sh your_excel_file.xlsx

# Or run without specifying file (it will ask)
./run_import.sh
```

### For Windows:
```cmd
# Just double-click run_import.bat or run from command prompt
run_import.bat your_excel_file.xlsx

# Or run without specifying file (it will ask)
run_import.bat
```

The script will:
1. Set up the virtual environment automatically
2. Ask for your OAuth2 credentials securely
3. Ask which Excel file to import
4. Offer to run in dry-run mode first
5. Show you exactly what will be created

## Method 2: Environment Variables

### Linux/Mac:
```bash
# Set your credentials as environment variables
export KORDIAM_CLIENT_ID="your_client_id_here"
export KORDIAM_CLIENT_SECRET="your_client_secret_here"

# Run the importer
source venv/bin/activate
python3 kordiam_excel_importer.py your_file.xlsx --dry-run
```

### Windows (Command Prompt):
```cmd
# Set your credentials as environment variables
set KORDIAM_CLIENT_ID=your_client_id_here
set KORDIAM_CLIENT_SECRET=your_client_secret_here

# Run the importer
venv\Scripts\activate
python kordiam_excel_importer.py your_file.xlsx --dry-run
```

### Windows (PowerShell):
```powershell
# Set your credentials as environment variables
$env:KORDIAM_CLIENT_ID="your_client_id_here"
$env:KORDIAM_CLIENT_SECRET="your_client_secret_here"

# Run the importer
venv\Scripts\Activate.ps1
python kordiam_excel_importer.py your_file.xlsx --dry-run
```

## Method 3: Command Line Arguments

```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Run with credentials as command line arguments
python3 kordiam_excel_importer.py your_file.xlsx \
  --client-id "your_client_id" \
  --client-secret "your_client_secret" \
  --dry-run
```

## Method 4: Manual Setup

### 1. Set up Python environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare your Excel file:

Your Excel file should have columns that match the mapping in `kordiam_mapping.json`. Use `kordiam_example.xlsx` as a template.

### 3. Run the importer:

```bash
# Test first with dry-run
python3 kordiam_excel_importer.py your_file.xlsx --dry-run

# If dry-run looks good, run for real
python3 kordiam_excel_importer.py your_file.xlsx
```

## 🔧 Configuration Options

### Excel File Mapping
Edit `kordiam_mapping.json` to match your Excel column names:

```json
{
  "element_fields": {
    "Your_Title_Column": "title",
    "Your_Slug_Column": "slug"
  },
  "tasks": {
    "Your_Status_Column": "status",
    "Your_Format_Column": "format"
  }
}
```

### Command Line Options

```bash
python3 kordiam_excel_importer.py [OPTIONS] EXCEL_FILE

Options:
  --client-id TEXT        OAuth2 client ID
  --client-secret TEXT    OAuth2 client secret  
  --base-url TEXT         Kordiam base URL [default: https://kordiam.app]
  --config TEXT           Config file path [default: config.json]
  --mapping TEXT          Mapping file path [default: kordiam_mapping.json]
  --sheet TEXT            Excel sheet name (optional)
  --dry-run              Test run without creating elements
  --log-level [DEBUG|INFO|WARNING|ERROR]  Logging level [default: INFO]
```

## 🧪 Testing Your Setup

### 1. Test with the example file:
```bash
python3 kordiam_excel_importer.py kordiam_example.xlsx --dry-run
```

### 2. Check the generated JSON:
The dry-run will show you exactly what JSON will be sent to Kordiam API.

### 3. Verify your mapping:
Make sure your Excel columns are correctly mapped to Kordiam fields.

## 🔍 Troubleshooting

### Authentication Issues:
- **Error: "Failed to obtain access token"**
  - Check your client_id and client_secret are correct
  - Verify your credentials are active in Kordiam
  - Try with `--log-level DEBUG` to see detailed OAuth2 flow

### Excel File Issues:
- **Error: "No valid data found"**
  - Check your Excel column names match the mapping exactly
  - Verify you have data in the required columns
  - Use `kordiam_example.xlsx` as a reference

### Validation Issues:
- **Error: "Element must contain at least one of: publication, task, or group"**
  - Ensure your Excel has data for tasks, publications, or groups
  - Check the mapping configuration includes these sections

### Getting Help:
```bash
# See detailed logging
python3 kordiam_excel_importer.py your_file.xlsx --dry-run --log-level DEBUG

# Check what credentials are being used
python3 kordiam_excel_importer.py your_file.xlsx --dry-run --log-level INFO
```

## 🎯 Quick Example

```bash
# 1. Use the easy run script
./run_import.sh kordiam_example.xlsx

# 2. Enter your credentials when prompted:
#    Client ID: your_actual_client_id
#    Client Secret: your_actual_client_secret

# 3. Choose "y" for dry-run first

# 4. Review the output, then choose "y" to run for real
```

## 📁 Required Files

Make sure you have these files in your directory:
- `kordiam_excel_importer.py` - Main script
- `kordiam_mapping.json` - Field mapping configuration  
- `requirements.txt` - Python dependencies
- `run_import.sh` or `run_import.bat` - Easy run scripts
- Your Excel file with data to import

That's it! You're ready to import your Excel data into Kordiam! 🎉
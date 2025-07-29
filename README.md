# Kordiam Excel Importer

A Python script that reads data from Excel files and creates elements in Kordiam via its REST API.

## Features

- **Excel Reading**: Supports both `.xlsx` and `.xls` files
- **Flexible Mapping**: Configurable column mapping between Excel and Kordiam fields
- **API Integration**: Full REST API client for Kordiam with authentication
- **Error Handling**: Comprehensive error handling and logging
- **Dry Run Mode**: Test imports without making actual API calls
- **Detailed Logging**: Complete audit trail of import operations
- **Data Transformation**: Automatic data type handling (dates, numbers, text)

## Installation

1. **Clone or download the script files**

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### 1. API Configuration (`config.json`)

Update the `config.json` file with your Kordiam API credentials:

```json
{
  "base_url": "https://api.kordiam.app",
  "api_key": "YOUR_ACTUAL_API_KEY",
  "headers": {
    "Authorization": "Bearer YOUR_ACTUAL_API_KEY",
    "Content-Type": "application/json",
    "Accept": "application/json"
  },
  "timeout": 30
}
```

**Important**: Replace `YOUR_ACTUAL_API_KEY` with your real Kordiam API key.

### 2. Column Mapping (`column_mapping.json`)

Configure how Excel columns map to Kordiam API fields:

```json
{
  "Name": "name",
  "Description": "description",
  "Type": "type",
  "Status": "status",
  "Priority": "priority",
  "Owner": "owner",
  "Created Date": "created_date",
  "Updated Date": "updated_date"
}
```

**Key Points**:
- Left side: Exact Excel column names (case-sensitive)
- Right side: Kordiam API field names
- Refer to Kordiam API documentation for valid field names

## Usage

### Basic Usage

```bash
python3 kordiam_excel_importer.py your_excel_file.xlsx
```

### Advanced Usage

```bash
# Specify custom config and mapping files
python3 kordiam_excel_importer.py data.xlsx --config custom_config.json --mapping custom_mapping.json

# Import specific sheet
python3 kordiam_excel_importer.py data.xlsx --sheet "Sheet2"

# Dry run (test without creating elements)
python3 kordiam_excel_importer.py data.xlsx --dry-run

# Verbose logging
python3 kordiam_excel_importer.py data.xlsx --log-level DEBUG
```

### Command Line Options

- `excel_file`: Path to the Excel file (required)
- `--config`: Path to config file (default: `config.json`)
- `--mapping`: Path to column mapping file (default: `column_mapping.json`)
- `--sheet`: Specific Excel sheet name (optional, uses first sheet if not specified)
- `--dry-run`: Test run without creating elements
- `--log-level`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)

## Example Excel File

The script includes an example Excel file (`example_data.xlsx`) with sample data:

| Name | Description | Type | Status | Priority | Owner | Created Date | Updated Date |
|------|-------------|------|--------|----------|-------|--------------|--------------|
| Project Alpha | Main project for Q1 deliverables | Project | Active | High | John Doe | 2024-01-15 | 2024-01-20 |
| Task Beta | Critical task requiring immediate attention | Task | Pending | Critical | Jane Smith | 2024-01-20 | 2024-01-21 |

## How It Works

1. **Read Excel File**: The script reads your Excel file using pandas
2. **Transform Data**: Each row is transformed according to your column mapping
3. **API Calls**: For each row, the script makes a POST request to create an element in Kordiam
4. **Logging**: All operations are logged with detailed information
5. **Results**: Summary of successful imports and any errors

## Data Type Handling

The script automatically handles various data types:

- **Text**: Strings are passed as-is
- **Numbers**: Integers and floats are preserved
- **Dates**: Automatically converted to ISO format (YYYY-MM-DD)
- **Empty Cells**: Skipped (not included in API request)

## Error Handling

- **File Errors**: Clear messages for missing or corrupted Excel files
- **API Errors**: Detailed logging of HTTP errors with response details
- **Data Errors**: Validation and transformation error reporting
- **Network Errors**: Timeout and connection error handling

## Logging

The script creates detailed log files with timestamps:
- Log file: `kordiam_import_YYYYMMDD_HHMMSS.log`
- Console output for real-time feedback
- Different log levels for various details

## API Endpoints

The script uses the following Kordiam API endpoints (update based on actual API):

- `POST /elements` - Create new elements
- `GET /elements/{id}` - Retrieve element details
- `PUT /elements/{id}` - Update existing elements

**Note**: You'll need to update the endpoint URLs in the script based on the actual Kordiam API documentation.

## Security Notes

- Never commit your API keys to version control
- Use environment variables for sensitive data in production
- Ensure your API key has appropriate permissions
- Test with dry-run mode first

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Make sure you're in the virtual environment: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

2. **API Authentication errors**
   - Verify your API key in `config.json`
   - Check the API base URL
   - Ensure your API key has proper permissions

3. **Excel file errors**
   - Verify file path and permissions
   - Check if Excel file is corrupted
   - Ensure column names match your mapping exactly

4. **Column mapping errors**
   - Excel column names are case-sensitive
   - Check for extra spaces in column names
   - Verify Kordiam API field names

### Getting Help

1. Check the log files for detailed error information
2. Use `--dry-run` to test your configuration
3. Try with `--log-level DEBUG` for maximum detail
4. Verify your Excel file with the provided example

## Customization

The script is designed to be easily customizable:

- **Authentication**: Modify the `KordiamConfig` class for different auth methods
- **Data Transformation**: Update `transform_row_to_element()` for custom logic
- **API Endpoints**: Change URLs in the `KordiamAPIClient` class
- **Error Handling**: Add custom error handling in the main import loop

## Contributing

To improve this script:

1. Update API endpoints based on actual Kordiam documentation
2. Add support for additional data types
3. Implement batch API calls for better performance
4. Add support for updating existing elements
5. Create a GUI version for non-technical users

## License

This script is provided as-is for integration with Kordiam. Modify and use according to your needs.

---

**Note**: This script was created based on general REST API patterns. You'll need to update the API endpoints and field mappings based on the actual Kordiam API documentation at https://api.kordiam.app/

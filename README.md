# Kordiam Excel Importer

A Python script that reads data from Excel files and creates elements in Kordiam via its REST API (v1.0.1).

## Features

- **Excel Reading**: Supports both `.xlsx` and `.xls` files
- **Kordiam API Integration**: Full integration with Kordiam API v1.0.1
- **Complex Data Mapping**: Maps Excel data to Kordiam's nested element structure
- **Task Support**: Creates tasks with deadlines, assignments, and status tracking
- **Publication Support**: Handles publication scheduling, platforms, and categories
- **Location & Events**: Optional support for location and event data
- **Validation**: Ensures elements meet Kordiam's requirements (must have publication, task, or group)
- **Dry Run Mode**: Test imports without making actual API calls
- **Detailed Logging**: Complete audit trail of import operations
- **Error Handling**: Comprehensive error handling and logging

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
  "base_url": "https://kordiam.app",
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

### 2. Element Mapping (`kordiam_mapping.json`)

Configure how Excel columns map to Kordiam's element structure. The mapping file supports:

- **Element Fields**: Basic element properties (title, slug, note, status)
- **Tasks**: Task assignments with deadlines and status
- **Publications**: Publication scheduling and platform assignments
- **Groups**: Group associations (optional)
- **Location**: Location information (optional)
- **Events**: Event timing (optional)

Example mapping structure:
```json
{
  "element_fields": {
    "Title": "title",
    "Slug": "slug",
    "Note": "note",
    "Element Status": "elementStatus"
  },
  "tasks": {
    "Task Status ID": "status",
    "Task Format ID": "format",
    "Assigned User ID": "user",
    "Task Deadline": "deadline",
    "Confirmation Status": "confirmationStatus"
  },
  "publications": {
    "Publication Status ID": "status",
    "Platform ID": "platform",
    "Category ID": "category",
    "Publication Date": "single"
  }
}
```

## Usage

### Basic Usage

```bash
python3 kordiam_excel_importer.py your_excel_file.xlsx
```

### Advanced Usage

```bash
# Specify custom config and mapping files
python3 kordiam_excel_importer.py data.xlsx --config config.json --mapping kordiam_mapping.json

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
- `--mapping`: Path to Kordiam mapping file (default: `kordiam_mapping.json`)
- `--sheet`: Specific Excel sheet name (optional, uses first sheet if not specified)
- `--dry-run`: Test run without creating elements
- `--log-level`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)

## Example Excel File

The script includes an example Excel file (`kordiam_example.xlsx`) with sample data that matches the Kordiam API structure:

| Title | Slug | Task Status ID | Task Format ID | Publication Status ID | Platform ID | Category ID |
|-------|------|----------------|----------------|-----------------------|-------------|-------------|
| Breaking: Local Election Results | local-election-results-2024 | 1 | 18 | 3 | 1 | 8 |
| Weather Update: Storm Warning | storm-warning-march-15 | 1 | 19 | 3 | 2 | 12 |

## Kordiam API Requirements

### Element Structure
According to Kordiam API documentation, elements must contain **at least one** of:
- **Publication platform**
- **Task**  
- **Group**

The script validates this requirement and will skip rows that don't meet it.

### Data Types and Formats

- **IDs**: Integer values (Status IDs, Platform IDs, User IDs, etc.)
- **Dates**: YYYY-MM-DD format or Excel date values
- **Times**: HH:MM format or Excel datetime values
- **Task Assignments**: Boolean array as comma-separated values ("true,false,true")
- **Confirmation Status**: Integer values (-2: Not requested, 0: Requested, 1: Confirmed, -1: Rejected)

## API Integration

The script uses the official Kordiam API endpoints:

- **Create Element**: `POST /api/v1_0_1/elements/`
- **Get Element**: `GET /api/v1_0_1/elements/{id}/`
- **Update Element**: `PUT /api/v1_0_1/elements/{id}/`

## Generated JSON Structure

The script generates JSON that matches Kordiam's API specification:

```json
{
  "elementStatus": 4,
  "slug": "story-slug",
  "title": "Story Title",
  "note": "Story notes",
  "tasks": [
    {
      "status": 1,
      "format": 18,
      "user": 5,
      "deadline": {
        "date": "2024-03-15",
        "time": "16:00"
      },
      "confirmationStatus": -2,
      "externalLink": "http://cms.example.com/story/123"
    }
  ],
  "publications": [
    {
      "status": 3,
      "platform": 1,
      "category": 8,
      "single": {
        "start": {
          "date": "2024-03-15",
          "time": "18:00"
        }
      },
      "assignments": [true]
    }
  ]
}
```

## Error Handling

- **File Errors**: Clear messages for missing or corrupted Excel files
- **API Errors**: Detailed logging of HTTP errors with response details
- **Validation Errors**: Checks for required element components
- **Data Type Errors**: Handles data conversion and validation
- **Network Errors**: Timeout and connection error handling

## Logging

The script creates detailed log files with timestamps:
- Log file: `kordiam_import_YYYYMMDD_HHMMSS.log`
- Console output for real-time feedback
- Different log levels for various details

## Troubleshooting

### Common Issues

1. **"Element must contain at least one of: publication, task, or group"**
   - Ensure your Excel has data mapped to tasks, publications, or groups
   - Check your mapping configuration

2. **API Authentication errors**
   - Verify your API key in `config.json`
   - Ensure your API key has proper permissions in Kordiam

3. **Invalid ID errors**
   - Check that Status IDs, Platform IDs, etc. exist in your Kordiam instance
   - Use valid integer values for all ID fields

4. **Date/Time format errors**
   - Use YYYY-MM-DD format for dates
   - Use HH:MM format for times
   - Excel datetime cells are automatically converted

### Getting Help

1. Use `--dry-run` to see the generated JSON structure
2. Check log files for detailed error information
3. Try with `--log-level DEBUG` for maximum detail
4. Verify your data with the provided `kordiam_example.xlsx`

## Validation and Testing

Before running actual imports:

1. **Test with dry-run**: `python3 kordiam_excel_importer.py your_file.xlsx --dry-run`
2. **Check the JSON output** to ensure it matches your expectations
3. **Verify IDs** exist in your Kordiam instance (platforms, categories, users, etc.)
4. **Start with small batches** for initial testing

## Security Notes

- Never commit your API keys to version control
- Use environment variables for sensitive data in production
- Ensure your API key has appropriate permissions
- Test with dry-run mode first

## License

This script is provided as-is for integration with Kordiam. Modify and use according to your needs.

---

**Built for Kordiam API v1.0.1** - Based on official API documentation at https://kordiam.app/api/v1_0_1/

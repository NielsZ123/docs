#!/usr/bin/env python3
"""
Usage Example for Kordiam Excel Importer
Demonstrates how to use the importer programmatically.
"""

from kordiam_excel_importer import KordiamConfig, KordiamImporter
import json

def example_usage():
    """Example of how to use the Kordiam importer in your own code."""
    
    # 1. Create configuration
    config = KordiamConfig(
        base_url="https://api.kordiam.app",
        api_key="YOUR_API_KEY_HERE",
        headers={
            "Authorization": "Bearer YOUR_API_KEY_HERE",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        timeout=30
    )
    
    # 2. Define column mapping
    column_mapping = {
        "Name": "name",
        "Description": "description",
        "Type": "type",
        "Status": "status",
        "Priority": "priority",
        "Owner": "owner"
    }
    
    # 3. Create importer
    importer = KordiamImporter(config)
    
    # 4. Run import (dry run for testing)
    try:
        results = importer.import_from_excel(
            excel_file="example_data.xlsx",
            column_mapping=column_mapping,
            sheet_name="Elements",  # Optional: specify sheet
            dry_run=True  # Set to False for actual import
        )
        
        # 5. Process results
        print(f"Import Results:")
        print(f"  Successful: {results['success']}")
        print(f"  Errors: {results['errors']}")
        
        if results['errors'] > 0:
            print("\nErrors encountered:")
            for detail in results['details']:
                if detail['status'] == 'error':
                    print(f"  Row {detail['row']}: {detail['error']}")
    
    except Exception as e:
        print(f"Import failed: {e}")

def batch_import_example():
    """Example of importing multiple files."""
    
    excel_files = [
        "file1.xlsx",
        "file2.xlsx", 
        "file3.xlsx"
    ]
    
    # Load config from file
    with open('config.json', 'r') as f:
        config_data = json.load(f)
    
    config = KordiamConfig(
        base_url=config_data['base_url'],
        api_key=config_data['api_key'],
        headers=config_data['headers'],
        timeout=config_data.get('timeout', 30)
    )
    
    # Load column mapping
    with open('column_mapping.json', 'r') as f:
        column_mapping = json.load(f)
    
    importer = KordiamImporter(config)
    
    total_success = 0
    total_errors = 0
    
    for excel_file in excel_files:
        try:
            print(f"\nProcessing {excel_file}...")
            results = importer.import_from_excel(
                excel_file=excel_file,
                column_mapping=column_mapping,
                dry_run=False  # Actual import
            )
            
            total_success += results['success']
            total_errors += results['errors']
            
            print(f"  {excel_file}: {results['success']} success, {results['errors']} errors")
            
        except FileNotFoundError:
            print(f"  {excel_file}: File not found, skipping")
        except Exception as e:
            print(f"  {excel_file}: Error - {e}")
    
    print(f"\nTotal Results:")
    print(f"  Files processed: {len(excel_files)}")
    print(f"  Total success: {total_success}")
    print(f"  Total errors: {total_errors}")

if __name__ == "__main__":
    print("Kordiam Excel Importer - Usage Examples")
    print("=" * 50)
    
    print("\n1. Basic Usage Example:")
    example_usage()
    
    print("\n2. Batch Import Example (uncomment to run):")
    print("   # batch_import_example()")
    
    print("\nDone!")
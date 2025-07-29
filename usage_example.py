#!/usr/bin/env python3
"""
Usage Example for Kordiam Excel Importer
Demonstrates how to use the importer programmatically with the actual Kordiam API structure.
"""

from kordiam_excel_importer import KordiamConfig, KordiamImporter
import json

def example_usage():
    """Example of how to use the Kordiam importer in your own code."""
    
    # 1. Create configuration
    config = KordiamConfig(
        base_url="https://kordiam.app",
        api_key="YOUR_API_KEY_HERE",
        headers={
            "Authorization": "Bearer YOUR_API_KEY_HERE",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        timeout=30
    )
    
    # 2. Define mapping configuration for Kordiam API structure
    mapping_config = {
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
            "Confirmation Status": "confirmationStatus",
            "External Link": "externalLink",
            "Task Note": "note"
        },
        "publications": {
            "Publication Status ID": "status",
            "Platform ID": "platform",
            "Category ID": "category",
            "Type ID": "type",
            "External ID": "externalId",
            "Publication Date": "single",
            "Task Assignments": "assignments",
            "CMS ID": "cms_id",
            "Scope": "scope"
        },
        "location": {
            "Location Name": "name",
            "City": "city",
            "Country": "country"
        }
    }
    
    # 3. Create importer
    importer = KordiamImporter(config)
    
    # 4. Run import (dry run for testing)
    try:
        results = importer.import_from_excel(
            excel_file="kordiam_example.xlsx",
            mapping_config=mapping_config,
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
        
        # Show a sample of generated data
        if results['details'] and results['details'][0]['status'] == 'success':
            print(f"\nSample generated JSON:")
            print(json.dumps(results['details'][0]['data'], indent=2))
    
    except Exception as e:
        print(f"Import failed: {e}")

def batch_import_example():
    """Example of importing multiple files with Kordiam structure."""
    
    excel_files = [
        "stories_batch1.xlsx",
        "stories_batch2.xlsx", 
        "events_data.xlsx"
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
    
    # Load Kordiam mapping configuration
    with open('kordiam_mapping.json', 'r') as f:
        mapping_config = json.load(f)
    
    importer = KordiamImporter(config)
    
    total_success = 0
    total_errors = 0
    
    for excel_file in excel_files:
        try:
            print(f"\nProcessing {excel_file}...")
            results = importer.import_from_excel(
                excel_file=excel_file,
                mapping_config=mapping_config,
                dry_run=True  # Change to False for actual import
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

def custom_mapping_example():
    """Example showing how to create custom mappings for specific use cases."""
    
    # Example: News story import with custom fields
    news_mapping = {
        "element_fields": {
            "Headline": "title",
            "Story_Slug": "slug",
            "Editorial_Notes": "note",
            "Status": "elementStatus"
        },
        "tasks": {
            "Reporter_ID": "user",
            "Task_Type": "format",
            "Status_ID": "status", 
            "Due_Date": "deadline",
            "Assignment_Notes": "note"
        },
        "publications": {
            "Pub_Status": "status",
            "Website_ID": "platform",
            "Section_ID": "category",
            "Story_Type": "type",
            "Publish_Time": "single",
            "Task_Assignment": "assignments"
        }
    }
    
    # Example: Event import with location data
    event_mapping = {
        "element_fields": {
            "Event_Title": "title",
            "Event_Slug": "slug",
            "Description": "note"
        },
        "tasks": {
            "Coordinator_ID": "user",
            "Task_Format": "format",
            "Task_Status": "status",
            "Setup_Deadline": "deadline"
        },
        "location": {
            "Venue_Name": "name",
            "Address": "street",
            "City": "city",
            "ZIP": "postalCode",
            "Country_Code": "country"
        },
        "event": {
            "Start_Date": "fromDate",
            "Start_Time": "fromTime",
            "End_Date": "toDate",
            "End_Time": "toTime"
        }
    }
    
    print("Custom mapping examples:")
    print("\n1. News Story Mapping:")
    print(json.dumps(news_mapping, indent=2))
    
    print("\n2. Event Mapping:")
    print(json.dumps(event_mapping, indent=2))

def validation_example():
    """Example showing validation and error handling."""
    
    config = KordiamConfig(
        base_url="https://kordiam.app",
        api_key="test_key",
        headers={"Authorization": "Bearer test_key", "Content-Type": "application/json"},
        timeout=30
    )
    
    # Example with missing required components (will fail validation)
    incomplete_mapping = {
        "element_fields": {
            "Title": "title",
            "Note": "note"
        }
        # Missing tasks, publications, or groups - will fail Kordiam validation
    }
    
    # Example with complete mapping
    complete_mapping = {
        "element_fields": {
            "Title": "title"
        },
        "tasks": {
            "Task Status ID": "status",
            "Task Format ID": "format"
        }
    }
    
    print("Validation Examples:")
    print("1. Incomplete mapping (will fail):", json.dumps(incomplete_mapping, indent=2))
    print("2. Complete mapping (will pass):", json.dumps(complete_mapping, indent=2))

if __name__ == "__main__":
    print("Kordiam Excel Importer - Usage Examples")
    print("=" * 50)
    
    print("\n1. Basic Usage Example:")
    example_usage()
    
    print("\n" + "="*50)
    print("2. Custom Mapping Examples:")
    custom_mapping_example()
    
    print("\n" + "="*50)
    print("3. Validation Examples:")
    validation_example()
    
    print("\n" + "="*50)
    print("4. Batch Import Example (files not included):")
    print("   # batch_import_example()")
    
    print(f"\nFor more examples, check:")
    print(f"- kordiam_example.xlsx (sample Excel file)")
    print(f"- kordiam_mapping.json (complete mapping configuration)")
    print(f"- Use --dry-run to test your configurations")
    
    print("\nDone!")
#!/usr/bin/env python3
"""
Usage Example for Kordiam Excel Importer
Demonstrates how to use the importer programmatically with OAuth2 authentication.
"""

from kordiam_excel_importer import KordiamConfig, KordiamImporter
import json

def example_usage():
    """Example of how to use the Kordiam importer with OAuth2 authentication."""
    
    # 1. Create configuration with OAuth2 client credentials
    config = KordiamConfig(
        base_url="https://kordiam.app",
        client_id="YOUR_CLIENT_ID_HERE",
        client_secret="YOUR_CLIENT_SECRET_HERE",
        token_endpoint="/api/token",
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
    
    # 3. Create importer (will automatically handle OAuth2 token)
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

def oauth2_example():
    """Example demonstrating OAuth2 authentication flow."""
    
    print("OAuth2 Authentication Flow:")
    print("="*40)
    
    # Configuration with OAuth2 credentials
    config = KordiamConfig(
        base_url="https://kordiam.app",
        client_id="your_client_id",
        client_secret="your_client_secret",
        token_endpoint="/api/token"
    )
    
    print(f"1. Token Request URL: {config.base_url}{config.token_endpoint}")
    print(f"2. Grant Type: client_credentials")
    print(f"3. Client ID: {config.client_id}")
    print(f"4. Client Secret: [HIDDEN]")
    print(f"5. Content-Type: application/x-www-form-urlencoded")
    
    print(f"\nRequest Body:")
    print(f"grant_type=client_credentials&client_id={config.client_id}&client_secret=***")
    
    print(f"\nExpected Response:")
    print(f"{{")
    print(f'  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",')
    print(f'  "token_type": "Bearer",')
    print(f'  "expires_in": 3600')
    print(f"}}")
    
    print(f"\nThe script will:")
    print(f"- Automatically request tokens when needed")
    print(f"- Cache tokens until they expire")
    print(f"- Refresh tokens with 5-minute buffer")
    print(f"- Add 'Authorization: Bearer <token>' to all API requests")

def batch_import_example():
    """Example of importing multiple files with OAuth2."""
    
    excel_files = [
        "stories_batch1.xlsx",
        "stories_batch2.xlsx", 
        "events_data.xlsx"
    ]
    
    # Load config from file (with OAuth2 credentials)
    with open('config.json', 'r') as f:
        config_data = json.load(f)
    
    config = KordiamConfig(
        base_url=config_data['base_url'],
        client_id=config_data['client_id'],
        client_secret=config_data['client_secret'],
        token_endpoint=config_data.get('token_endpoint', '/api/token'),
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
        client_id="test_client",
        client_secret="test_secret",
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
    print("Kordiam Excel Importer - Usage Examples with OAuth2")
    print("=" * 60)
    
    print("\n1. OAuth2 Authentication Example:")
    oauth2_example()
    
    print("\n" + "="*60)
    print("2. Basic Usage Example:")
    example_usage()
    
    print("\n" + "="*60)
    print("3. Custom Mapping Examples:")
    custom_mapping_example()
    
    print("\n" + "="*60)
    print("4. Validation Examples:")
    validation_example()
    
    print("\n" + "="*60)
    print("5. Batch Import Example (files not included):")
    print("   # batch_import_example()")
    
    print(f"\nFor more examples, check:")
    print(f"- kordiam_example.xlsx (sample Excel file)")
    print(f"- kordiam_mapping.json (complete mapping configuration)")
    print(f"- config.json (OAuth2 credentials)")
    print(f"- Use --dry-run to test your configurations")
    
    print("\nDone!")
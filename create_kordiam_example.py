#!/usr/bin/env python3
"""
Create example Excel file for Kordiam importer with correct column mappings.
This file generates sample data that matches the kordiam_mapping.json configuration.
"""

import pandas as pd
from datetime import datetime, timedelta

def create_kordiam_example():
    """Create an example Excel file with correct Kordiam column mappings."""
    
    # Sample data with exact column names from kordiam_mapping.json
    data = {
        # Basic Element Fields
        'Title': [
            'Breaking: Local Election Results Announced',
            'Weather Alert: Severe Storm Warning',
            'Community Event: Annual Festival Planning',
            'Sports Update: Championship Game Preview',
            'Health News: New Medical Center Opens'
        ],
        'Slug': [
            'local-election-results-2024',
            'storm-warning-march-15',
            'annual-festival-planning',
            'championship-game-preview',
            'new-medical-center-opens'
        ],
        'Note': [
            'Priority story for front page coverage',
            'Send push notification immediately',
            'Coordinate with events team',
            'Interview team coaches',
            'Get quotes from medical staff'
        ],
        'Element Status': [4, 4, 2, 3, 4],
        
        # Task Fields
        'Task Status ID': [1, 1, 2, 1, 3],
        'Task Format ID': [18, 19, 20, 18, 21],
        'Assigned User ID': [5, 3, 7, 5, 9],
        'Task Deadline': [
            datetime(2024, 3, 15, 16, 0),
            datetime(2024, 3, 15, 8, 0),
            datetime(2024, 4, 1, 12, 0),
            datetime(2024, 3, 20, 18, 0),
            datetime(2024, 3, 25, 14, 30)
        ],
        'Confirmation Status': [-2, 0, 1, -2, 1],
        'External Link': [
            'http://cms.example.com/election/2024',
            'http://weather.example.com/alerts/123',
            'http://events.example.com/festival/2024',
            'http://sports.example.com/championship',
            'http://health.example.com/medical-center'
        ],
        'External Link Title': [
            'Election Coverage System',
            'Weather Alert Portal',
            'Event Management',
            'Sports Coverage Hub',
            'Health News Portal'
        ],
        'Custom Upload Link': [
            'http://upload.example.com/election',
            'http://upload.example.com/weather',
            '',
            'http://upload.example.com/sports',
            ''
        ],
        'Task Note': [
            'Interview the mayor and key candidates',
            'Get meteorologist quote and safety tips',
            'Coordinate with festival organizers',
            'Schedule interviews with team coaches',
            'Tour new facilities and interview staff'
        ],
        
        # Publication Fields
        'Publication Status ID': [3, 3, 2, 3, 1],
        'Platform ID': [1, 2, 1, 3, 1],
        'Category ID': [8, 12, 5, 15, 10],
        'Type ID': [4, 5, 6, 4, 7],
        'External ID': ['ext_001', 'ext_002', 'ext_003', 'ext_004', 'ext_005'],
        'Publication Date': [
            datetime(2024, 3, 15, 18, 0),
            datetime(2024, 3, 15, 6, 0),
            datetime(2024, 4, 1, 10, 0),
            datetime(2024, 3, 20, 20, 0),
            datetime(2024, 3, 25, 16, 0)
        ],
        'Task Assignments': ['true', 'true', 'true', 'true', 'true'],
        'CMS ID': ['667', '668', '669', '670', '671'],
        'Published Content URL': [
            'https://news.example.com/election-results',
            'https://news.example.com/storm-warning',
            'https://news.example.com/festival-2024',
            'https://sports.example.com/championship',
            'https://health.example.com/medical-center'
        ],
        'Published Content Title': [
            'Election Results Live',
            'Storm Warning Alert',
            'Festival 2024 Preview',
            'Championship Coverage',
            'Medical Center Opening'
        ],
        'CMS Edit URL': [
            'https://cms.example.com/edit/election',
            'https://cms.example.com/edit/weather',
            'https://cms.example.com/edit/festival',
            'https://cms.example.com/edit/sports',
            'https://cms.example.com/edit/health'
        ],
        'CMS Edit Title': [
            'Edit Election Story',
            'Edit Weather Alert',
            'Edit Festival Story',
            'Edit Sports Story',
            'Edit Health Story'
        ],
        'Scope': [12.5, 8.0, 15.2, 10.0, 11.8],
        
        # Group Fields
        'Group IDs': ['5,8', '12', '5,8,15', '20', '8,12'],
        
        # Location Fields
        'Location Name': [
            'City Hall Main Auditorium',
            'Downtown Weather Station',
            'Central Park Festival Grounds',
            'Sports Complex Arena',
            'New Medical Center Building'
        ],
        'Street': [
            '123 Main Street',
            '456 Weather Ave',
            '789 Park Boulevard',
            '321 Sports Drive',
            '654 Health Street'
        ],
        'Postal Code': ['12345', '54321', '67890', '98765', '13579'],
        'Country': ['US', 'US', 'US', 'US', 'US'],
        'Directions': [
            'Enter through main entrance',
            'Use north parking lot',
            'Festival entrance on east side',
            'Use main arena entrance',
            'Patient entrance on ground floor'
        ],
        'City': ['Springfield', 'Springfield', 'Springfield', 'Springfield', 'Springfield'],
        'State Code': ['IL', 'IL', 'IL', 'IL', 'IL'],
        
        # Event Fields
        'Event Start Date': [
            datetime(2024, 3, 15, 19, 0),
            None,  # Weather alert has no specific event
            datetime(2024, 4, 1, 9, 0),
            datetime(2024, 3, 20, 19, 30),
            datetime(2024, 3, 25, 10, 0)
        ],
        'Event Start Time': [
            datetime(2024, 3, 15, 19, 0),
            None,
            datetime(2024, 4, 1, 9, 0),
            datetime(2024, 3, 20, 19, 30),
            datetime(2024, 3, 25, 10, 0)
        ],
        'Event End Date': [
            datetime(2024, 3, 15, 21, 0),
            None,
            datetime(2024, 4, 1, 18, 0),
            datetime(2024, 3, 20, 22, 0),
            datetime(2024, 3, 25, 12, 0)
        ],
        'Event End Time': [
            datetime(2024, 3, 15, 21, 0),
            None,
            datetime(2024, 4, 1, 18, 0),
            datetime(2024, 3, 20, 22, 0),
            datetime(2024, 3, 25, 12, 0)
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create Excel file with proper formatting
    with pd.ExcelWriter('kordiam_example.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Elements', index=False)
        
        # Get the worksheet to adjust column widths
        worksheet = writer.sheets['Elements']
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print("✅ Kordiam example Excel file 'kordiam_example.xlsx' created successfully!")
    print(f"📊 Contains {len(df)} sample rows with all mapped columns")
    print("\n📋 Column Summary:")
    print("- Basic Element Fields: Title, Slug, Note, Element Status")
    print("- Task Fields: Status, Format, User, Deadline, Confirmation, Links, Notes")
    print("- Publication Fields: Status, Platform, Category, Type, Dates, URLs, Scope")
    print("- Group Fields: Group IDs (comma-separated)")
    print("- Location Fields: Name, Address, Directions")
    print("- Event Fields: Start/End Dates and Times")
    print("\n🔧 Ready to use with: python3 kordiam_excel_importer.py kordiam_example.xlsx --dry-run")

if __name__ == "__main__":
    create_kordiam_example()
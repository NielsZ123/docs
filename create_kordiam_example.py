import pandas as pd
from datetime import datetime, timedelta

# Create sample data that matches Kordiam API structure
data = {
    # Basic element fields
    'Title': [
        'Breaking: Local Election Results',
        'Weather Update: Storm Warning',
        'Sports: Championship Game Tonight',
        'Community Event: Farmers Market'
    ],
    'Slug': [
        'local-election-results-2024',
        'storm-warning-march-15',
        'championship-game-tonight',
        'farmers-market-saturday'
    ],
    'Note': [
        'Priority story for front page',
        'Send push notification immediately',
        'Get photos from the game',
        'Include vendor list'
    ],
    'Element Status': [4, 4, 3, 2],
    
    # Task fields
    'Task Status ID': [1, 1, 2, 1],
    'Task Format ID': [18, 19, 18, 20],
    'Assigned User ID': [5, 3, 7, 5],
    'Task Deadline': [
        datetime(2024, 3, 15, 16, 0),
        datetime(2024, 3, 15, 8, 0),
        datetime(2024, 3, 15, 22, 0),
        datetime(2024, 3, 16, 10, 0)
    ],
    'Confirmation Status': [-2, 0, -2, -2],
    'External Link': [
        'http://cms.example.com/election/2024',
        'http://weather.example.com/alerts/123',
        'http://sports.example.com/game/456',
        'http://events.example.com/market/789'
    ],
    'Task Note': [
        'Interview the mayor',
        'Get meteorologist quote',
        'Stadium access arranged',
        'Confirm vendor participation'
    ],
    
    # Publication fields
    'Publication Status ID': [3, 3, 2, 1],
    'Platform ID': [1, 2, 1, 3],
    'Category ID': [8, 12, 15, 10],
    'Type ID': [4, 5, 4, 6],
    'External ID': ['ext_001', 'ext_002', 'ext_003', 'ext_004'],
    'Publication Date': [
        datetime(2024, 3, 15, 18, 0),
        datetime(2024, 3, 15, 6, 0),
        datetime(2024, 3, 16, 0, 0),
        datetime(2024, 3, 16, 8, 0)
    ],
    'Task Assignments': ['true', 'true', 'true', 'true'],
    'CMS ID': ['667', '668', '669', '670'],
    'Scope': [12.5, 8.0, 15.2, 5.0],
    
    # Location fields (optional)
    'Location Name': [
        'City Hall',
        'Weather Station',
        'Sports Arena',
        'Town Square'
    ],
    'City': ['Springfield', 'Springfield', 'Springfield', 'Springfield'],
    'Country': ['US', 'US', 'US', 'US'],
    
    # Event fields (optional)
    'Event Start Date': [
        datetime(2024, 3, 15, 19, 0),
        None,
        datetime(2024, 3, 15, 19, 30),
        datetime(2024, 3, 16, 9, 0)
    ],
    'Event End Date': [
        datetime(2024, 3, 15, 21, 0),
        None,
        datetime(2024, 3, 15, 22, 0),
        datetime(2024, 3, 16, 14, 0)
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel with proper formatting
with pd.ExcelWriter('kordiam_example.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Elements', index=False)
    
    # Get the workbook and worksheet
    workbook = writer.book
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
        adjusted_width = min(max_length + 2, 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width

print("Kordiam example Excel file 'kordiam_example.xlsx' created successfully!")
print("\nThis file contains sample data with the following structure:")
print("- Basic element fields (title, slug, note, status)")
print("- Task information (status, format, user, deadline)")
print("- Publication details (platform, category, publication date)")
print("- Location data (optional)")
print("- Event information (optional)")
print("\nUse this as a template for your own data import.")
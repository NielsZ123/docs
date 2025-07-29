import pandas as pd

# Create sample data
data = {
    'Name': ['Project Alpha', 'Task Beta', 'Item Gamma', 'Process Delta'],
    'Description': [
        'Main project for Q1 deliverables',
        'Critical task requiring immediate attention',
        'Regular maintenance item',
        'Business process optimization'
    ],
    'Type': ['Project', 'Task', 'Item', 'Process'],
    'Status': ['Active', 'Pending', 'Completed', 'In Progress'],
    'Priority': ['High', 'Critical', 'Medium', 'Low'],
    'Owner': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown'],
    'Created Date': pd.to_datetime(['2024-01-15', '2024-01-20', '2024-01-10', '2024-01-25']),
    'Updated Date': pd.to_datetime(['2024-01-20', '2024-01-21', '2024-01-15', '2024-01-26'])
}

# Create DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel('example_data.xlsx', index=False, sheet_name='Elements')

print("Example Excel file 'example_data.xlsx' created successfully!")
import pandas as pd

# Sample data for conference attendees
data = {
    'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown'],
    'email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com'],
    'reg_id': ['CONF-001', 'CONF-002', 'CONF-003', 'CONF-004'],
    'company': ['ABC Corp', 'XYZ Ltd', 'Tech Solutions', 'Innovate Inc'],
    'position': ['Developer', 'Manager', 'Analyst', 'Designer']
}

df = pd.DataFrame(data)
df.to_excel('example_attendees.xlsx', index=False)

print("Example Excel file 'example_attendees.xlsx' created successfully!")
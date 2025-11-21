from flask import Flask, request, jsonify, render_template
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import tempfile
import re

app = Flask(__name__)

# Gmail credentials from environment variables
GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')

if not GMAIL_USER or not GMAIL_APP_PASSWORD:
    raise ValueError("GMAIL_USER and GMAIL_APP_PASSWORD environment variables must be set")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview_data', methods=['POST'])
def preview_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        file.save(temp_file.name)
        temp_path = temp_file.name
    
    try:
        # Read Excel file
        df = pd.read_excel(temp_path)
        
        # Handle different Excel formats
        first_row = df.iloc[0] if len(df) > 0 else None
        if first_row is not None and 'Name' in str(first_row.iloc[0]):
            df_processed = df.iloc[1:].reset_index(drop=True)
            df_processed.columns = [str(col).lower() if pd.notna(col) else f'col_{i}' for i, col in enumerate(first_row)]
        else:
            df_processed = df.copy()
            df_processed.columns = [col.lower() for col in df_processed.columns]
        
        # Prepare preview data
        columns = list(df_processed.columns)
        total_records = len(df_processed)
        
        # Get first 5 rows for preview
        preview_rows = []
        for _, row in df_processed.head(5).iterrows():
            preview_rows.append({col: '' if pd.isna(val) else str(val) for col, val in row.items()})
        
        # Clean up temp file
        os.unlink(temp_path)
        
        return jsonify({
            'columns': columns,
            'total_records': total_records,
            'preview_rows': preview_rows
        })
    
    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        return jsonify({'error': str(e)}), 500

@app.route('/send_emails', methods=['POST'])
def send_emails():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    subject = request.form.get('subject', '')
    body_template = request.form.get('body', '')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        file.save(temp_file.name)
        temp_path = temp_file.name
    
    try:
        # Read Excel file
        df = pd.read_excel(temp_path)
        
        # Handle different Excel formats - check if first row contains headers
        first_row = df.iloc[0] if len(df) > 0 else None
        if first_row is not None and 'Name' in str(first_row.iloc[0]):
            # Custom format for paper request emails.xlsx
            df = df.iloc[1:].reset_index(drop=True)  # Skip header
            df.columns = [str(col).lower() if pd.notna(col) else f'col_{i}' for i, col in enumerate(first_row)]
        else:
            # Standard format - convert column names to lowercase
            df.columns = [col.lower() for col in df.columns]
        
        sent_count = 0
        failed_count = 0
        
        # Setup SMTP
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        
        for _, row in df.iterrows():
            row_dict = {k.lower(): v for k, v in row.to_dict().items()}
            # Replace placeholders (case-insensitive)
            body = body_template
            placeholders = re.findall(r'\{(\w+)\}', body)
            for placeholder in placeholders:
                key = placeholder.lower()
                if key in row_dict:
                    val = row_dict[key]
                    replacement = '' if pd.isna(val) else str(val)
                    body = body.replace(f'{{{placeholder}}}', replacement)
            
            # Assume 'email' column exists, or try other columns
            recipient = row_dict.get('email') or row_dict.get('col_2') or row_dict.get('hbtu')
            if recipient and not pd.isna(recipient):
                recipient = str(recipient).strip()
                if '[at]' in recipient:
                    recipient = recipient.split(' (')[0].replace('[at]', '@').replace('[dot]', '.')
            else:
                recipient = None
            
            if not recipient:
                failed_count += 1
                continue
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = GMAIL_USER
            msg['To'] = str(recipient).strip()
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            try:
                server.sendmail(GMAIL_USER, str(recipient).strip(), msg.as_string())
                sent_count += 1
            except Exception as e:
                failed_count += 1
        
        server.quit()
        
        # Clean up temp file
        os.unlink(temp_path)
        
        return jsonify({
            'sent': sent_count,
            'failed': failed_count
        })
    
    except Exception as e:
        os.unlink(temp_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
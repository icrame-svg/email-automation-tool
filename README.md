# Bulk Email Sender for Conference

A simple web application to send bulk emails using an Excel file with placeholders for personalization.

## Features

- Upload Excel file with attendee data
- Compose email with placeholders like {name}, {email}, {reg_id}
- Send personalized emails via Gmail SMTP
- Bootstrap-based clean UI

## Setup

1. Clone or download this project.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up Gmail App Password:
   - Go to your Google Account settings
   - Enable 2-Factor Authentication
   - Generate an App Password for this app
   - Edit `app.py` and replace `GMAIL_USER` and `GMAIL_APP_PASSWORD` with your Gmail address and app password.

4. Run the app:
   ```
   python app.py
   ```

5. Open your browser to `http://127.0.0.1:5000/`

## Usage

1. Prepare an Excel file (.xlsx) with attendee data. The tool supports flexible column formats:
   - **Standard format**: Columns named `name`, `email`, `reg_id`, etc. (case-insensitive)
   - **Header row format**: First row contains "Name", "Email" as headers, data starts from second row

2. Upload the Excel file.

3. Enter the email subject.

4. Compose the email body using placeholders like `{name}`, `{email}`, `{reg_id}` for personalization.

5. Click "Send Emails" to send personalized emails to all recipients.

## Example Excel Formats

### Format 1: Standard columns
| name     | email             | reg_id |
|----------|-------------------|--------|
| John Doe | john@example.com  | 123    |
| Jane Smith| jane@example.com | 124    |

### Format 2: With header row
| Name     | Email             |
|----------|-------------------|
| John Doe | john@example.com  |
| Jane Smith| jane@example.com |

## Example Email Body

```
Dear {name},

Thank you for registering for the conference with registration ID {reg_id}.

Your company: {company}

Best regards,
Conference Team
```

## Security Note

This app uses hardcoded Gmail credentials for simplicity. In production, use environment variables or a secure configuration.

## License

MIT

## Deploy frontend to GitHub Pages (static test)

You can publish the frontend UI as a static site on GitHub Pages for quick UI testing. This static copy only provides a preview of the interface; backend features (Excel parsing on the server, sending emails) require running the Flask app locally or hosting the backend separately.

Steps to publish the static preview using the repository's `docs/` folder:

1. Commit the `docs/` folder to your repository (this project already contains a `docs/` static copy).

2. Push to GitHub and enable Pages from the `main` branch using the `docs/` folder. From the repo on GitHub: Settings → Pages → Source → Choose `main` branch and `/docs` folder → Save.

Alternatively, use the CLI (`git` + GitHub web UI for enabling Pages) — example commands (run from your repo root):

```bash
git add docs
git commit -m "Add static frontend for GitHub Pages preview"
git push origin main
```

3. Wait a minute or two. Your site will be available at `https://<your-username>.github.io/<your-repo>/` (or the repository's Pages URL shown in Settings).

Local testing (full functionality)
---------------------------------
To test the full app (file preview and email sending) you must run the Flask server locally because the static Pages site cannot run the Python backend or send emails.

```bash
pip install -r requirements.txt
# Edit app.py to set your Gmail address and an app password
python app.py
# Open http://127.0.0.1:5000/ in your browser
```

Notes
- The static preview falls back to sample data when the backend is not available so you can test the UI and layout on GitHub Pages.
- For production email sending, use a hosted backend (Render, Railway, Fly) or run the Flask app on a server and secure credentials with environment variables.
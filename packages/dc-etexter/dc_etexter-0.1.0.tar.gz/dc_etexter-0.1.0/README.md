# text-alert

> Send an SMS text alert using Python

## Requirements

- Python 3.11+ (required for reading toml files)
- A configured Gmail Account (see below)
---

## Step 1. Install this Module

Add this to your requirements.txt and install. 

```
git+https://github.com/denisecase/text-alert.git
```

## Step 2. Add .env.toml To your Python Project

Create a new .env.toml file in your Python project (or add these entries).
- Update the outgoing email address to your gmail address.
- Update the sms address for texts to your number, using your carrier's gateway (see .env.example.toml or do a search).
- We'll create an app password later.  

```
# SMTP Email Configuration
outgoing_email_host = "smtp.gmail.com"
outgoing_email_port = 587
outgoing_email_address = "yourname@gmail.com"
outgoing_email_password = "aaaabbbbccccdddd"

# SMS Configuration
sms_address_for_texts = "1112224444@msg.fi.google.com"
```

## Step 3. Add .env.toml To .gitignore

Ensure your secrets are not published by adding an entry in .gitignore:

```
.env.toml
```

## Step 4. Gmail - Enable IMAP

 - Open Gmail.
 - Click Settings or ⚙️ in the top-right.
 - Then click "See all settings".
 - Navigate to "Forwarding and POP/IMAP".
 - Under "IMAP access", select "Enable IMAP".
-  Click "Save Changes".

## Step 5. Gmail - Generate an App Password

If your account has 2FA enabled, you must generate an App Password:
- Go to <https://support.google.com/accounts/answer/185833?hl=en> 
- Click on "Create and manage your app passwords".
- Sign in and navigate to Account "Security" / "App Passwords"
- Create an app password - name it (e.g., "PythonTextAlerts"). 
- Generate and copy the 16-character password.
- Paste the 16-char as your password in .env.toml file. 
  - Remove any spaces
  - Keep it private - ensure your .env.toml file is listed in .gitignore

## Step 6. Import and Use in a Python Script

Once installed and your .env.toml file is ready, you can use it in your code. 

```python
from dc_etexter import send_text

message = "Testing text alerts from Python."

try:
    send_text(body=message)
    print(f"SUCCESS. Text sent: {message}")
except RuntimeError as e:
    print(f"ERROR:  Sending failed: {e}")
```
---

## Testing

To run this file locally for testing, fork & clone the repo, add .env.toml. 
Open the project repository in VS Code, open a PowerShell terminal and run 

```
pytest
py dc_etexter\etexter.py
```

## A Note on Organization

pip requires a folder/package to install. 

Repository Name: text-alert
  - Uses dashes (-) as allowed in GitHub repository names.
  - Cannot be used as a Python package name due to dashes.
  - Has no effect on Python package imports.

Package (Folder) Name: dc_etexter
  - Uses underscores (_) to ensure compatibility with Python imports.
  - Becomes an installable package when  __init__.py file is added.

File Name: etexter.py
  - The file name with a .py extension.
  - Can be executed as a script. 
  - We avoid using the file name in imports if we set up __init__.py correctly. 

pyproject.toml
  - [project] name = "dc_etexter"`
  - Used for installation (`pip install dc_etexter`).
  - The package folder should match.

```toml
[project]
name = "dc_etexter" # install name

version = "0.1.0"

[tool.setuptools]
packages = ["dc_etexter"] # list of package folders
```
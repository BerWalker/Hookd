# PhishingTool

A cybersecurity phishing platform built with Flask.

## Features

- User authentication (login/register)
- **Forgot Password functionality** - Secure password reset via email
- Dashboard interface
- Modern, responsive UI with Tailwind CSS

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in a `.env` file:
   ```env
   FLASK_SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///instance/phishing_tool.db
   
   # Email configuration for password reset
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

4. Run the database migration (if upgrading from an older version):
   ```bash
   python migrate_db.py
   ```

5. Start the application:
   ```bash
   python app.py
   ```

## Email Configuration

The forgot password feature requires email configuration to send password reset links. Here's how to set it up:

### Gmail Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
3. Use the generated app password in your `.env` file

### Other Email Providers
You can use any SMTP provider. Update the `MAIL_SERVER`, `MAIL_PORT`, and other settings accordingly in your `.env` file.

## Forgot Password Feature

The forgot password functionality includes:

1. **Forgot Password Page** (`/auth/forgot-password`)
   - Users enter their email address
   - System sends a secure reset link via email

2. **Password Reset Page** (`/auth/reset-password/<token>`)
   - Users set a new password using the reset token
   - Tokens expire after 1 hour for security

3. **Security Features**
   - Secure token generation using `secrets` module
   - Token expiration after 1 hour
   - Tokens are cleared after use
   - Email validation and error handling

## Project Structure

```
PhishingTool/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── extensions.py         # Flask extensions
├── migrate_db.py         # Database migration script
├── requirements.txt      # Python dependencies
├── controllers/          # Route controllers
│   ├── auth_controller.py
│   └── main_controller.py
├── forms/               # WTForms
│   └── auth_form.py
├── models/              # Database models
│   └── user.py
├── services/            # Business logic
│   └── auth_service.py
├── templates/           # HTML templates
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── forgot_password.html
│   │   └── reset_password.html
│   ├── main/
│   │   └── dashboard.html
│   └── base.html
├── static/              # Static files
└── utils/               # Utility functions
    └── security.py
```

## Usage

1. Register a new account
2. Log in with your credentials
3. If you forget your password, click "Forgot your password?" on the login page
4. Enter your email address to receive a reset link
5. Click the link in your email to reset your password

## Security Notes

- Passwords are hashed using bcrypt
- Reset tokens are cryptographically secure
- Tokens expire after 1 hour
- Email addresses are validated
- CSRF protection is enabled
- Secure redirect handling
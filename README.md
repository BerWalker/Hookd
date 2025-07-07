# Hookd

A cybersecurity phishing platform built with Flask.

## Features

- User authentication (login/register)
- **Forgot Password functionality** — Secure password reset via email
- Dashboard interface
- Modern, responsive UI with Tailwind CSS

## Quick Start

> **Requirements:**
> - [Docker](https://www.docker.com/get-started)
> - [Docker Compose](https://docs.docker.com/compose/)

1. Clone the repository
2. Copy the example environment file:
   ```bash
   cp env.example .env
   ```
3. Edit the `.env` file to set your secrets and email credentials
4. Start the application:
   ```bash
   docker compose up --build --no-deps --force-recreate
   ```
5. Access Hookd at [http://localhost:5000](http://localhost:5000) (or as configured)

> **Note:** You do **not** need to manually install Python requirements or run any migration scripts. All dependencies and setup are handled automatically by Docker.

## Environment Configuration

Copy the example environment file to `.env`:

```bash
cp env.example .env
```

Then edit `.env` to set your secrets and email credentials. The following variables are required:

```env
FLASK_SECRET_KEY="secret-key-123456789"

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

DB_NAME=hookd
DB_USER=hookd_user
DB_PASSWORD=hookd_password
```

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

- **Forgot Password Page** (`/auth/forgot-password`): Users enter their email address to receive a secure reset link
- **Password Reset Page** (`/auth/reset-password/<token>`): Users set a new password using the reset token (expires after 1 hour)
- **Security:** Secure token generation, expiration, and validation

## Project Structure

```
Hookd/
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── extensions.py          # Flask extensions
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker Compose 
├── Dockerfile             # Docker container 
├── .dockerignore          # Docker ignore file
├── .gitignore             # Git ignore file
├── controllers/           # Route controllers
│   ├── auth_controller.py
│   ├── health_controller.py
│   └── main_controller.py
├── forms/                 # WTForms
│   └── auth_form.py
├── models/                # Database models
│   └── user.py
├── services/              # Business logic
│   └── auth_service.py
├── templates/             # HTML templates
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── forgot_password.html
│   │   └── reset_password.html
│   ├── main/
│   │   └── dashboard.html
│   └── base.html
├── static/                # Static files
│   ├── favicon.ico
│   ├── logo_full.png
│   ├── logo_shortcut.png
│   └── logo_symbol.png
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── security.py
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
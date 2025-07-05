# Project Structure

```
urlShortner/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── setup_xampp.py        # XAMPP MySQL setup helper
├── test_auth.py          # Authentication test script (legacy)
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
├── PROJECT_STRUCTURE.md  # This file
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI/CD
├── templates/            # HTML templates
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   └── error.html       # Error page
├── static/              # Static files
│   └── styles.css       # CSS styles
└── test/                # Unit tests
    └── test_app.py      # Comprehensive test suite
```

## File Descriptions

### Core Application
- **`app.py`**: Main Flask application with all routes and database logic
- **`requirements.txt`**: Python package dependencies
- **`setup_xampp.py`**: Helper script for XAMPP MySQL configuration

### Templates
- **`templates/index.html`**: Home page with URL shortening form
- **`templates/login.html`**: User login page
- **`templates/register.html`**: User registration page
- **`templates/error.html`**: 404 error page

### Static Files
- **`static/styles.css`**: CSS styling for the application

### Testing
- **`test/test_app.py`**: Comprehensive unit tests for all functionality
- **`test_auth.py`**: Legacy authentication test (can be removed)

### Configuration
- **`.env`**: Environment variables (not in repo, created by setup script)
- **`.gitignore`**: Git ignore rules
- **`.github/workflows/ci.yml`**: GitHub Actions CI/CD pipeline

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### URLs Table
```sql
CREATE TABLE urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    long_url TEXT NOT NULL,
    short_code VARCHAR(255) UNIQUE NOT NULL,
    user VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_short_code (short_code),
    INDEX idx_user (user)
);
```

## Features Implemented

✅ **Core Functionality**
- Anonymous URL shortening
- User registration and login
- Custom URL codes for registered users
- URL redirection
- Session management

✅ **Technical Features**
- MySQL database with raw SQL
- Flask backend
- HTML/CSS frontend (no frameworks)
- Comprehensive unit tests
- GitHub Actions CI/CD
- Environment variable configuration
- XAMPP integration

✅ **Development Features**
- Git version control
- Proper project structure
- Documentation
- Error handling
- Security considerations 
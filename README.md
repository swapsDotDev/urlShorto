# URL Shortener

A Flask-based URL shortening service similar to TinyURL, built with MySQL (no ORM) and vanilla HTML/CSS.

## Requirements

### Core Features
- **Anonymous URL Creation**: Users can create short URLs without registration
- **User Authentication**: Login/registration system for additional features
- **Custom URL Codes**: Registered users can create custom short codes
- **URL Redirection**: Short URLs redirect to original long URLs
- **Session Management**: Secure user sessions with Flask sessions

### Technical Requirements
- **Backend**: Flask (Python)
- **Database**: MySQL with raw SQL (no ORM)
- **Frontend**: HTML/CSS only (no JavaScript frameworks)
- **Testing**: Comprehensive unit tests with pytest
- **CI/CD**: GitHub Actions for automated testing

### Development Workflow
- **Git Branches**: Feature branches for isolated development
- **Pull Requests**: Code review through PRs
- **GitHub Issues**: Issue tracking for features and bugs
- **Automated Testing**: Tests run on every PR and merge

## Features

- ✅ Anonymous short URL creation
- ✅ User registration and login
- ✅ Custom short URL for registered users
- ✅ Session-based authentication
- ✅ URL redirection
- ✅ Error handling
- ✅ Plain HTML/CSS frontend
- ✅ Raw SQL database operations (MySQL)
- ✅ Environment variable configuration
- ✅ Comprehensive unit tests
- ✅ GitHub Actions CI

## Prerequisites

- Python 3.7+
- MySQL Server 5.7+ or MySQL 8.0+ (or XAMPP for development)
- MySQL user with CREATE DATABASE privileges

## Quick Setup (Recommended)

### Option 1: XAMPP Setup (Easiest for Development)
1. **Download XAMPP:** https://www.apachefriends.org/download.html
2. **Install XAMPP** with default settings
3. **Start XAMPP Control Panel** and start MySQL service
4. **Run the XAMPP setup helper:**
   ```bash
   python setup_xampp.py
   ```
5. **Start the application:**
   ```bash
   python app.py
   ```

## Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd urlShortner
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up MySQL database:**
   - **Option A:** Use XAMPP (recommended)
     - Install and start XAMPP
     - Start MySQL service in XAMPP Control Panel
   - **Option B:** Install MySQL Server manually
   - Run the setup helper: `python setup_xampp.py`

4. **Set up environment variables:**
   - The setup script will create a `.env` file automatically
   - Or create manually with your MySQL credentials:
   ```
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=urlshortener
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Initialize the database:**
```bash
python app.py
```

6. **Run the application:**
```bash
python app.py
```

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app
```

**Note**: Tests require a MySQL server running with the credentials specified in your `.env` file.

## API Endpoints

- `GET /` - Home page with URL shortening form
- `POST /` - Create short URL
- `GET /<code>` - Redirect to original URL
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /register` - Registration page
- `POST /register` - Create new user account
- `GET /logout` - Logout user

## Database Schema

### Users Table
- `id` (INT AUTO_INCREMENT PRIMARY KEY)
- `username` (VARCHAR(255) UNIQUE NOT NULL)
- `password` (VARCHAR(255) NOT NULL)
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

### URLs Table
- `id` (INT AUTO_INCREMENT PRIMARY KEY)
- `long_url` (TEXT NOT NULL)
- `short_code` (VARCHAR(255) UNIQUE NOT NULL)
- `user` (VARCHAR(255)) - NULL for anonymous users
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- `idx_short_code` (INDEX on short_code)
- `idx_user` (INDEX on user)

## Environment Variables

- `SECRET_KEY`: Flask secret key for session management
- `DB_HOST`: MySQL server host (default: localhost)
- `DB_USER`: MySQL username (default: root)
- `DB_PASSWORD`: MySQL password
- `DB_NAME`: MySQL database name (default: urlshortener)
- `FLASK_ENV`: Flask environment (development/production)
- `FLASK_DEBUG`: Enable/disable debug mode

## Security Notes

- Never commit your `.env` file to version control
- Generate a strong random secret key for production
- Use environment variables for all sensitive configuration
- Passwords are stored in plain text (should be hashed in production)
- Use a dedicated MySQL user with minimal required privileges

## Database Management

### Using XAMPP (Recommended)
- **Start MySQL:** Open XAMPP Control Panel → Start MySQL
- **Stop MySQL:** Open XAMPP Control Panel → Stop MySQL
- **Access phpMyAdmin:** http://localhost/phpmyadmin
- **Default credentials:** root (no password)
- **MySQL data directory:** `C:\xampp\mysql\data`

## Development Workflow

1. Create feature branch: `git checkout -b feature/feature-name`
2. Implement feature with tests
3. Create pull request
4. Run tests via GitHub Actions
5. Code review and merge

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

## Troubleshooting

### MySQL Connection Issues
- Ensure MySQL server is running
- Verify database credentials in `.env` file
- Check MySQL user has CREATE DATABASE privileges
- For test failures, ensure test database can be created

### XAMPP Issues
- Make sure XAMPP MySQL service is started
- Check if port 3306 is free
- Default credentials: root (no password)
- Access phpMyAdmin at: http://localhost/phpmyadmin

import pytest
import mysql.connector
import tempfile
import os
from app import app, init_db, get_db, DB_CONFIG

@pytest.fixture
def client():
    """Create a test client with a test database."""
    # Create a test database configuration
    test_db_config = DB_CONFIG.copy()
    test_db_config['database'] = 'test_urlshortener'
    
    # Override the database config for testing
    app.config['TEST_DB_CONFIG'] = test_db_config
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Create test database
    create_test_db(test_db_config)
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
    
    # Cleanup test database
    cleanup_test_db(test_db_config)

def create_test_db(config):
    """Create test database."""
    create_config = config.copy()
    del create_config['database']
    
    try:
        conn = mysql.connector.connect(**create_config)
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {config['database']}")
        cursor.execute(f"CREATE DATABASE {config['database']}")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error creating test database: {err}")
        raise

def cleanup_test_db(config):
    """Clean up test database."""
    create_config = config.copy()
    del create_config['database']
    
    try:
        conn = mysql.connector.connect(**create_config)
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {config['database']}")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error cleaning up test database: {err}")

@pytest.fixture
def auth_client(client):
    """Create a test client with a logged-in user."""
    # Register and login a test user
    client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    return client

# Homepage Tests
def test_homepage_get(client):
    """Test homepage loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Simple URL Shortener' in response.data
    assert b'Enter the long URL' in response.data

def test_homepage_with_login_link(client):
    """Test homepage shows login link when not authenticated."""
    response = client.get('/')
    assert b'Login' in response.data
    assert b'Register' in response.data

def test_homepage_with_logout_link(auth_client):
    """Test homepage shows logout link when authenticated."""
    response = auth_client.get('/')
    assert b'Logged in as' in response.data
    assert b'Logout' in response.data
    assert b'Custom short code' in response.data

# Anonymous URL Creation Tests
def test_anonymous_url_creation(client):
    """Test anonymous users can create short URLs."""
    response = client.post('/', data={
        'long_url': 'https://example.com'
    })
    assert response.status_code == 200
    assert b'Your short URL:' in response.data

def test_anonymous_url_creation_invalid_url(client):
    """Test anonymous URL creation with invalid URL."""
    response = client.post('/', data={
        'long_url': 'not-a-valid-url'
    })
    assert response.status_code == 200

# User Registration Tests
def test_register_page(client):
    """Test registration page loads."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_user_registration_success(client):
    """Test successful user registration."""
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpass'
    })
    assert response.status_code == 302  # Redirect to login
    assert b'Registration successful' in client.get('/login').data

def test_user_registration_duplicate_username(client):
    """Test registration with existing username."""
    # Register first user
    client.post('/register', data={
        'username': 'duplicate',
        'password': 'pass1'
    })
    
    # Try to register with same username
    response = client.post('/register', data={
        'username': 'duplicate',
        'password': 'pass2'
    })
    assert response.status_code == 200
    assert b'Username already exists' in response.data

# User Login Tests
def test_login_page(client):
    """Test login page loads."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_user_login_success(client):
    """Test successful user login."""
    # Register user first
    client.post('/register', data={
        'username': 'loginuser',
        'password': 'loginpass'
    })
    
    # Login
    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'loginpass'
    })
    assert response.status_code == 302  # Redirect to home
    assert b'Login successful' in client.get('/').data

def test_user_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post('/login', data={
        'username': 'nonexistent',
        'password': 'wrongpass'
    })
    assert response.status_code == 200
    assert b'Invalid credentials' in response.data

# Logout Tests
def test_logout(auth_client):
    """Test user logout."""
    response = auth_client.get('/logout')
    assert response.status_code == 302  # Redirect to home
    assert b'You have been logged out' in auth_client.get('/').data

# Custom URL Creation Tests
def test_custom_url_creation_authenticated(auth_client):
    """Test authenticated users can create custom URLs."""
    response = auth_client.post('/', data={
        'long_url': 'https://example.com',
        'custom_code': 'mycustom'
    })
    assert response.status_code == 200
    assert b'Your short URL:' in response.data
    assert b'mycustom' in response.data

def test_custom_url_creation_duplicate(auth_client):
    """Test custom URL creation with duplicate code."""
    # Create first custom URL
    auth_client.post('/', data={
        'long_url': 'https://example1.com',
        'custom_code': 'duplicate'
    })
    
    # Try to create second with same code
    response = auth_client.post('/', data={
        'long_url': 'https://example2.com',
        'custom_code': 'duplicate'
    })
    assert response.status_code == 302  # Redirect
    assert b'Custom code already taken' in auth_client.get('/').data

def test_custom_url_creation_anonymous(client):
    """Test anonymous users cannot create custom URLs."""
    response = client.post('/', data={
        'long_url': 'https://example.com',
        'custom_code': 'anonymous'
    })
    # Should still work but without custom code
    assert response.status_code == 200
    assert b'Your short URL:' in response.data

# URL Redirection Tests
def test_url_redirection(client):
    """Test short URL redirects to original URL."""
    # Create a short URL
    response = client.post('/', data={
        'long_url': 'https://httpbin.org/status/200'
    })
    
    # Extract the short code from response
    short_url = response.data.decode().split('Your short URL: <a href="')[1].split('"')[0]
    short_code = short_url.split('/')[-1]
    
    # Test redirection
    redirect_response = client.get(f'/{short_code}')
    assert redirect_response.status_code == 302

def test_url_redirection_nonexistent(client):
    """Test redirection for non-existent short code."""
    response = client.get('/nonexistent')
    assert response.status_code == 404

# Session Management Tests
def test_session_persistence(auth_client):
    """Test user session persists across requests."""
    response = auth_client.get('/')
    assert b'Logged in as testuser' in response.data
    
    # Make another request
    response = auth_client.get('/')
    assert b'Logged in as testuser' in response.data

def test_session_clear_after_logout(auth_client):
    """Test session is cleared after logout."""
    # Verify logged in
    response = auth_client.get('/')
    assert b'Logged in as testuser' in response.data
    
    # Logout
    auth_client.get('/logout')
    
    # Verify logged out
    response = auth_client.get('/')
    assert b'Login' in response.data
    assert b'Register' in response.data

# Database Tests
def test_database_initialization(client):
    """Test database tables are created correctly."""
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        
        # Check users table
        cursor.execute("SHOW TABLES LIKE 'users'")
        assert cursor.fetchone() is not None
        
        # Check urls table
        cursor.execute("SHOW TABLES LIKE 'urls'")
        assert cursor.fetchone() is not None
        
        cursor.close()
        conn.close()

# Error Handling Tests
def test_missing_form_data(client):
    """Test handling of missing form data."""
    response = client.post('/', data={})
    assert response.status_code == 400  # Bad request

def test_invalid_http_methods(client):
    """Test invalid HTTP methods return appropriate errors."""
    response = client.put('/')
    assert response.status_code == 405  # Method not allowed
    
    response = client.delete('/')
    assert response.status_code == 405  # Method not allowed

# Flash Message Tests
def test_flash_messages_display(client):
    """Test flash messages are displayed correctly."""
    # Trigger a flash message by trying to login with invalid credentials
    client.post('/login', data={
        'username': 'invalid',
        'password': 'invalid'
    })
    
    response = client.get('/login')
    assert b'Invalid credentials' in response.data

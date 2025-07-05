import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database():
    """Test MySQL database connection and user operations"""
    
    db_config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', ''),
        'database': os.environ.get('DB_NAME', 'urlshortener'),
        'charset': 'utf8mb4'
    }
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SHOW TABLES LIKE 'users'")
        assert cursor.fetchone() is not None, "Users table not found. Run the app first to create it."
        
        print("✅ Users table found")
        
        test_username = "test_user_12345"
        test_password = "test_password_12345"
        
        cursor.execute("DELETE FROM users WHERE username = %s", (test_username,))
        
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                      (test_username, test_password))
        conn.commit()
        print("✅ Test user created successfully")
        
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                      (test_username, test_password))
        user = cursor.fetchone()
        assert user is not None, "User authentication test failed"
        print("✅ User authentication test passed")
        
        cursor.execute("DELETE FROM users WHERE username = %s", (test_username,))
        conn.commit()
        print("✅ Test user cleaned up")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL connection failed: {err}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure XAMPP MySQL is running")
        print("2. Check your .env file configuration")
        print("3. Verify database 'urlshortener' exists")
        raise
    except ImportError:
        print("❌ mysql-connector-python not installed. Run: pip install mysql-connector-python")
        raise
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        raise

def test_url_operations():
    """Test URL table operations"""
    
    db_config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', ''),
        'database': os.environ.get('DB_NAME', 'urlshortener'),
        'charset': 'utf8mb4'
    }
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SHOW TABLES LIKE 'urls'")
        assert cursor.fetchone() is not None, "URLs table not found. Run the app first to create it."
        
        print("✅ URLs table found")
        
        test_long_url = "https://example.com/test"
        test_short_code = "test123"
        
        cursor.execute("DELETE FROM urls WHERE short_code = %s", (test_short_code,))
        
        cursor.execute("INSERT INTO urls (long_url, short_code, user) VALUES (%s, %s, %s)", 
                      (test_long_url, test_short_code, None))
        conn.commit()
        print("✅ Test URL created successfully")
        
        cursor.execute("SELECT long_url FROM urls WHERE short_code = %s", (test_short_code,))
        url = cursor.fetchone()
        assert url is not None and url[0] == test_long_url, "URL redirection test failed"
        print("✅ URL redirection test passed")
        
        cursor.execute("DELETE FROM urls WHERE short_code = %s", (test_short_code,))
        conn.commit()
        print("✅ Test URL cleaned up")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ URL operations test failed: {e}")
        raise

if __name__ == "__main__":
    print("Testing MySQL authentication and URL functionality...")
    print("=" * 50)
    
    try:
        test_database()
        
        test_url_operations()
        
        print("\n🎉 All tests passed! MySQL integration is working correctly.")
        print("💡 You can now run: python app.py")
    except Exception as e:
        print(f"\n💥 Some tests failed: {e}")
        print("🔧 Make sure XAMPP MySQL is running and .env file is configured.") 
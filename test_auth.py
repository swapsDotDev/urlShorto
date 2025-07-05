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
        if not cursor.fetchone():
            print("❌ Users table not found. Run the app first to create it.")
            return False
        
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
        if user:
            print("✅ User authentication test passed")
        else:
            print("❌ User authentication test failed")
            return False
        
        cursor.execute("DELETE FROM users WHERE username = %s", (test_username,))
        conn.commit()
        print("✅ Test user cleaned up")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL connection failed: {err}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure XAMPP MySQL is running")
        print("2. Check your .env file configuration")
        print("3. Verify database 'urlshortener' exists")
        return False
    except ImportError:
        print("❌ mysql-connector-python not installed. Run: pip install mysql-connector-python")
        return False
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

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
        if not cursor.fetchone():
            print("❌ URLs table not found. Run the app first to create it.")
            return False
        
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
        if url and url[0] == test_long_url:
            print("✅ URL redirection test passed")
        else:
            print("❌ URL redirection test failed")
            return False
        
        cursor.execute("DELETE FROM urls WHERE short_code = %s", (test_short_code,))
        conn.commit()
        print("✅ Test URL cleaned up")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ URL operations test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing MySQL authentication and URL functionality...")
    print("=" * 50)
    
    auth_success = test_database()
    
    url_success = test_url_operations()
    
    if auth_success and url_success:
        print("\n🎉 All tests passed! MySQL integration is working correctly.")
        print("💡 You can now run: python app.py")
    else:
        print("\n💥 Some tests failed. Check the issues above.")
        print("🔧 Make sure XAMPP MySQL is running and .env file is configured.") 
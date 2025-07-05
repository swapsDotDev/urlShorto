import os
import socket
from dotenv import load_dotenv

def create_env_file():
    """Create .env file with XAMPP MySQL configuration."""
    env_content = """# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# XAMPP MySQL Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=urlshortener
"""
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Backing up to .env.backup")
        os.rename('.env', '.env.backup')
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with XAMPP MySQL configuration")

def check_mysql_port():
    """Check if MySQL port is accessible."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 3306))
        sock.close()
        
        if result == 0:
            print("✅ MySQL port 3306 is accessible")
            return True
        else:
            print("❌ MySQL port 3306 is not accessible")
            print("   Make sure XAMPP MySQL service is started")
            return False
    except Exception as e:
        print(f"❌ Error checking MySQL port: {e}")
        return False

def main():
    """Main setup function."""
    print("🔧 XAMPP MySQL Setup Helper")
    print("=" * 30)
    
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        create_env_file()
    else:
        print("✅ .env file already exists")
    
    print("🔍 Checking MySQL port...")
    if check_mysql_port():
        print("\n🎉 Setup complete!")
        print("💡 Next steps:")
        print("1. Run: python test_auth.py (to test database)")
        print("2. Run: python app.py (to start the application)")
        print("3. Access phpMyAdmin at: http://localhost/phpmyadmin")
    else:
        print("\n❌ MySQL is not running.")
        print("📋 Please:")
        print("1. Start XAMPP Control Panel")
        print("2. Start MySQL service")
        print("3. Run this script again")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python
"""
Simplified setup script for Guftaho improvements
Run this after installing the requirements.txt
"""

import os
import sys
import shutil
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        'logs',
        'static/css',
        'static/js', 
        'static/images',
        'media/poets',
        'media/books',
        'whoosh_index',
        'staticfiles',
    ]
    
    print("📁 Creating project directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   Created: {directory}")

def setup_env_file():
    """Set up environment file"""
    if not Path('.env').exists():
        if Path('.env.example').exists():
            shutil.copy('.env.example', '.env')
            print("📝 Created .env file from .env.example")
            print("   ⚠️  Please edit .env file and update the SECRET_KEY and other settings")
        else:
            print("⚠️  .env.example not found. Creating basic .env file...")
            with open('.env', 'w', encoding='utf-8') as f:
                f.write('''# Django Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Cache Settings
CACHE_TTL=60
''')
            print("   ⚠️  Please edit .env file and set a proper SECRET_KEY")
    else:
        print("✅ .env file already exists")

def backup_existing_files():
    """Backup existing files before replacing them"""
    files_to_backup = [
        'guftaho/settings.py',
        'poetry/admin.py',
        'poetry/views.py',
        'poetry/urls.py',
    ]
    
    print("💾 Creating backups of existing files...")
    for file_path in files_to_backup:
        if Path(file_path).exists():
            backup_path = f"{file_path}.backup"
            shutil.copy(file_path, backup_path)
            print(f"   Backed up: {file_path} -> {backup_path}")

def apply_improvements():
    """Apply the new improved files"""
    replacements = [
        ('guftaho/settings_new.py', 'guftaho/settings.py'),
        ('poetry/admin_new.py', 'poetry/admin.py'),
        ('poetry/views_new.py', 'poetry/views.py'),
        ('poetry/urls_new.py', 'poetry/urls.py'),
    ]
    
    print("🔄 Applying improvements...")
    for source, destination in replacements:
        if Path(source).exists():
            shutil.copy(source, destination)
            print(f"   Applied: {source} -> {destination}")
        else:
            print(f"   ⚠️  Source file not found: {source}")

def print_next_steps():
    """Print the next steps for the user"""
    print("\n" + "=" * 50)
    print("🎉 Basic setup completed!")
    print("\nNext steps (run these commands manually):")
    print("\n1. Update your .env file with proper values:")
    print("   - Set a secure SECRET_KEY")
    print("   - Configure database if needed")
    
    print("\n2. Create new migrations and apply them:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    
    print("\n3. Create a superuser:")
    print("   python manage.py createsuperuser")
    
    print("\n4. Load sample data (optional):")
    print("   python manage.py load_sample_data")
    
    print("\n5. Build search index:")
    print("   python manage.py rebuild_index --noinput")
    
    print("\n6. Collect static files:")
    print("   python manage.py collectstatic --noinput")
    
    print("\n7. Start the development server:")
    print("   python manage.py runserver")
    
    print("\n8. Visit your enhanced site:")
    print("   http://127.0.0.1:8000 - Main site")
    print("   http://127.0.0.1:8000/admin - Admin interface")
    print("   http://127.0.0.1:8000/api - API endpoints")
    
    print("\n📚 New Features Available:")
    print("   • Enhanced admin with statistics")
    print("   • User favorites system")
    print("   • Reading history tracking")
    print("   • Advanced search and filtering")
    print("   • REST API endpoints")
    print("   • Performance optimizations")

def main():
    print("🚀 Guftaho Project Improvements Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    try:
        create_directories()
        setup_env_file()
        backup_existing_files()
        apply_improvements()
        print_next_steps()
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        print("Please check the error and try again or apply changes manually.")
        sys.exit(1)

if __name__ == '__main__':
    main()
import os
import logging
import urllib.parse
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from utils.timezone import utc_to_ist

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def get_database_uri():
    """Get database URI - PostgreSQL primary, with SQL Server and MySQL support"""

    # PostgreSQL (primary database)
    postgres_url = os.environ.get("DATABASE_URL")
    if postgres_url:
        return postgres_url

    # Direct PostgreSQL configuration for local development
    return "postgresql://gtn_user:gtn_password_2024@localhost:5432/gtn_helpdesk"


# Create the app
app = Flask(__name__)
# Generate a secure session secret if not provided
session_secret = os.environ.get("SESSION_SECRET")
if not session_secret:
    import secrets
    session_secret = secrets.token_hex(32)
    logging.info("Generated temporary session secret - please set SESSION_SECRET environment variable for production")
app.secret_key = session_secret
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database - PostgreSQL primary database
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

def utc_to_ist(dt):
    """Convert UTC datetime to IST"""
    if dt:
        from datetime import timezone, timedelta
        # IST is UTC+5:30
        ist_timezone = timezone(timedelta(hours=5, minutes=30))
        if dt.tzinfo is None:
            # Assume UTC if no timezone info
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(ist_timezone)
    return dt

@app.template_filter('to_ist')
def to_ist_filter(dt):
    if dt:
        converted_dt = utc_to_ist(dt)
        if converted_dt:
            return converted_dt.strftime('%Y-%m-%d %H:%M:%S')
    return ''

# Add custom Jinja2 filter for line breaks
@app.template_filter('nl2br')
def nl2br_filter(s):
    """Convert newlines to <br> tags"""
    return s.replace('\n', '<br>\n') if s else s


with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    db.create_all()
    logging.info("Database tables created")
    
    # Create default master data
    from models import User, MasterDataCategory, MasterDataPriority, MasterDataStatus, EmailSettings, TimezoneSettings, BackupSettings
    from werkzeug.security import generate_password_hash
    
    # Create default categories
    if MasterDataCategory.query.count() == 0:
        categories = [
            MasterDataCategory(name='Hardware', description='Hardware related issues', is_active=True),
            MasterDataCategory(name='Software', description='Software related issues', is_active=True)
        ]
        for category in categories:
            db.session.add(category)
    
    # Create default priorities
    if MasterDataPriority.query.count() == 0:
        priorities = [
            MasterDataPriority(name='Low', description='Low priority issues', level=1, color_code='#28a745', is_active=True),
            MasterDataPriority(name='Medium', description='Medium priority issues', level=2, color_code='#ffc107', is_active=True),
            MasterDataPriority(name='High', description='High priority issues', level=3, color_code='#fd7e14', is_active=True),
            MasterDataPriority(name='Critical', description='Critical priority issues', level=4, color_code='#dc3545', is_active=True)
        ]
        for priority in priorities:
            db.session.add(priority)
    
    # Create default statuses
    if MasterDataStatus.query.count() == 0:
        statuses = [
            MasterDataStatus(name='Open', description='Newly created tickets', color_code='#007bff', is_active=True),
            MasterDataStatus(name='In Progress', description='Tickets being worked on', color_code='#ffc107', is_active=True),
            MasterDataStatus(name='Resolved', description='Resolved tickets', color_code='#28a745', is_active=True),
            MasterDataStatus(name='Closed', description='Closed tickets', color_code='#6c757d', is_active=True)
        ]
        for status in statuses:
            db.session.add(status)
    
    # Create default departments
    from models import MasterDataDepartment
    if MasterDataDepartment.query.count() == 0:
        departments = [
            MasterDataDepartment(name='Engineering', code='ENG', description='Engineering Department - Design and development', is_active=True),
            MasterDataDepartment(name='Information Technology', code='IT', description='Information Technology Department - System administration and support', is_active=True),
            MasterDataDepartment(name='Human Resources', code='HR', description='Human Resources Department - Employee management and recruitment', is_active=True),
            MasterDataDepartment(name='Finance', code='FIN', description='Finance Department - Financial planning and accounting', is_active=True),
            MasterDataDepartment(name='Operations', code='OPS', description='Operations Department - Daily operations and logistics', is_active=True),
            MasterDataDepartment(name='Quality Assurance', code='QA', description='Quality Assurance Department - Testing and quality control', is_active=True)
        ]
        for department in departments:
            db.session.add(department)
    
    # Create default email settings
    if EmailSettings.query.count() == 0:
        email_settings = EmailSettings(
            smtp_server='smtp.gmail.com',
            smtp_port=587,
            smtp_username='your-email@gmail.com',
            smtp_password='your-app-password',
            use_tls=True,
            from_email='',
            from_name='GTN IT Helpdesk',
            is_active=False  # Set to False until properly configured
        )
        db.session.add(email_settings)
    
    # Create default timezone settings
    if TimezoneSettings.query.count() == 0:
        timezone_settings = TimezoneSettings(
            timezone_name='Asia/Kolkata',
            display_name='Indian Standard Time (IST)',
            utc_offset='+05:30',
            is_active=True
        )
        db.session.add(timezone_settings)
    
    # Create default backup settings
    if BackupSettings.query.count() == 0:
        backup_settings = BackupSettings(
            backup_frequency='daily',
            backup_time=datetime.strptime('02:00', '%H:%M').time(),
            backup_location='/backups',
            max_backups=30,
            compress_backups=True,
            include_attachments=True,
            email_notifications=True,
            notification_email='admin@company.com',
            is_active=False  # Set to False until properly configured
        )
        db.session.add(backup_settings)
    
    # Create default users if they don't exist
    if User.query.count() == 0:
        # Create super admin
        super_admin = User(
            username='superadmin',
            email='superadmin@gtn.com',
            first_name='Super',
            last_name='Admin',
            department='IT Administration',
            role='super_admin'
        )
        super_admin.set_password('admin123')
        db.session.add(super_admin)
        
        # Create HOD for Engineering department
        hod_engineering = User(
            username='hodeng',
            email='hod.engineering@gtn.com',
            first_name='Engineering',
            last_name='HOD',
            department='Engineering',
            role='hod'
        )
        hod_engineering.set_password('hod123')
        db.session.add(hod_engineering)
        
        # Create HOD for IT department
        hod_it = User(
            username='hodit',
            email='hod.it@gtn.com',
            first_name='IT',
            last_name='HOD',
            department='IT',
            role='hod'
        )
        hod_it.set_password('hod123')
        db.session.add(hod_it)
        

        
        # Create test users in different departments
        test_user_eng = User(
            username='testuser_eng',
            email='testuser.eng@gtn.com',
            first_name='Test',
            last_name='Engineer',
            department='Engineering',
            role='user'
        )
        test_user_eng.set_password('user123')
        db.session.add(test_user_eng)
        
        test_user_it = User(
            username='testuser_it',
            email='testuser.it@gtn.com',
            first_name='Test',
            last_name='ITUser',
            department='IT',
            role='user'
        )
        test_user_it.set_password('user123')
        db.session.add(test_user_it)
        
        logging.info("Default users created: Super Admin, HODs, and Test Users")
    
    try:
        db.session.commit()
        logging.info("Default master data created successfully")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating default data: {e}")

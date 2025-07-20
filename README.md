# GTN Engineering IT Helpdesk System

A comprehensive Flask-based IT helpdesk management system with modern UI/UX design, simplified role structure, and professional-grade features. Built for Replit with PostgreSQL integration and real-time dashboard functionality.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-v15+-blue.svg)
![Bootstrap](https://img.shields.io/badge/bootstrap-v5.3+-purple.svg)

## 🌟 Key Features

### **Two-Tier Access System**
- **User Role**: Create and track personal tickets, view ticket history, read-only profile access
- **Super Admin Role**: Complete system control, user management, ticket assignment, analytics, master data management

### **Modern UI/UX Design**
- **Hero Landing Page**: Gradient backgrounds, floating animations, professional branding
- **Responsive Login**: Modern form design with floating labels and animated backgrounds
- **Dashboard Analytics**: Visual charts and real-time statistics
- **Mobile-First**: Fully responsive design for all devices

### **Comprehensive Ticket Management**
- **Complete Lifecycle**: From creation to resolution with status tracking
- **File Attachments**: Support for images, PDF, Word, Excel files
- **Assignment System**: Intelligent routing to Super Admins
- **Comment System**: Collaborative discussions and updates
- **Email Notifications**: Automatic alerts for assignments and updates

### **Advanced Features**
- **Excel Reports**: Comprehensive data export with IST timezone
- **Search & Filter**: Advanced ticket filtering capabilities
- **Real-time Updates**: Live dashboard refresh and notifications
- **System Detection**: Automatic IP and system name capture
- **Audit Trail**: Complete ticket history with assignment tracking

### **Master Data Management** (Super Admin Only)
- **Ticket Categories**: Hardware, Software categories with descriptions
- **Priority Levels**: Low, Medium, High, Critical with color coding
- **Ticket Statuses**: Open, In Progress, Resolved, Closed with visual indicators
- **Email Settings**: SMTP configuration for automated notifications
- **Timezone Settings**: System-wide timezone configuration (Default: IST)
- **Backup Settings**: Database backup scheduling and management

## 🗄️ Database Schema

### **Core Tables** (12 Tables Total)

#### **Users Table**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(100),
    specialization VARCHAR(50), -- Hardware or Software support
    role VARCHAR(50) NOT NULL DEFAULT 'user', -- 'user' or 'super_admin'
    ip_address VARCHAR(45),
    system_name VARCHAR(100),
    profile_image VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Tickets Table**
```sql
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(20) UNIQUE NOT NULL, -- GTN-000001 format
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Open',
    user_name VARCHAR(100) NOT NULL, -- Full name captured at creation
    user_ip_address VARCHAR(45),
    user_system_name VARCHAR(100),
    image_filename VARCHAR(255), -- For file attachments
    user_id INTEGER REFERENCES users(id) NOT NULL,
    assigned_to INTEGER REFERENCES users(id),
    assigned_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);
```

#### **Ticket Comments Table**
```sql
CREATE TABLE ticket_comments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER REFERENCES tickets(id) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Attachments Table**
```sql
CREATE TABLE attachments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER REFERENCES tickets(id) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Master Data Tables**

#### **Master Categories Table**
```sql
CREATE TABLE master_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Master Priorities Table**
```sql
CREATE TABLE master_priorities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(200),
    level INTEGER NOT NULL, -- 1=Low, 2=Medium, 3=High, 4=Critical
    color_code VARCHAR(7), -- Hex color for UI
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Master Statuses Table**
```sql
CREATE TABLE master_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(200),
    color_code VARCHAR(7), -- Hex color for UI
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **System Configuration Tables**

#### **Email Settings Table**
```sql
CREATE TABLE email_settings (
    id SERIAL PRIMARY KEY,
    smtp_server VARCHAR(100) NOT NULL DEFAULT 'smtp.gmail.com',
    smtp_port INTEGER NOT NULL DEFAULT 587,
    smtp_username VARCHAR(100) NOT NULL,
    smtp_password VARCHAR(200) NOT NULL,
    use_tls BOOLEAN DEFAULT TRUE,
    from_email VARCHAR(100),
    from_name VARCHAR(100) DEFAULT 'GTN IT Helpdesk',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Timezone Settings Table**
```sql
CREATE TABLE timezone_settings (
    id SERIAL PRIMARY KEY,
    timezone_name VARCHAR(50) NOT NULL DEFAULT 'Asia/Kolkata',
    display_name VARCHAR(100) NOT NULL DEFAULT 'Indian Standard Time (IST)',
    utc_offset VARCHAR(10) NOT NULL DEFAULT '+05:30',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Backup Settings Table**
```sql
CREATE TABLE backup_settings (
    id SERIAL PRIMARY KEY,
    backup_frequency VARCHAR(20) NOT NULL DEFAULT 'daily',
    backup_time TIME NOT NULL DEFAULT '02:00:00',
    backup_location VARCHAR(200) DEFAULT '/backups',
    max_backups INTEGER NOT NULL DEFAULT 30,
    compress_backups BOOLEAN DEFAULT TRUE,
    include_attachments BOOLEAN DEFAULT TRUE,
    email_notifications BOOLEAN DEFAULT TRUE,
    notification_email VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Email Notification Logs Table**
```sql
CREATE TABLE email_notification_logs (
    id SERIAL PRIMARY KEY,
    to_email VARCHAR(100) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message_type VARCHAR(50) NOT NULL, -- 'ticket_created', 'ticket_assigned', 'ticket_updated'
    status VARCHAR(20) NOT NULL, -- 'sent', 'failed'
    error_message TEXT,
    ticket_id INTEGER REFERENCES tickets(id),
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

#### **Master Departments Table** (NEW)
```sql
CREATE TABLE master_departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(10) UNIQUE NOT NULL, -- Short code like ENG, IT, HR
    description VARCHAR(200),
    head_of_department_id INTEGER REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Email Notifications Table**
```sql
CREATE TABLE email_notifications (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER REFERENCES tickets(id),
    recipient_email VARCHAR(120) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, sent, failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP
);
```

#### **Timezone Settings Table**
```sql
CREATE TABLE timezone_settings (
    id SERIAL PRIMARY KEY,
    timezone_name VARCHAR(50) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    utc_offset VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Backup Settings Table**
```sql
CREATE TABLE backup_settings (
    id SERIAL PRIMARY KEY,
    backup_frequency VARCHAR(20) NOT NULL, -- daily, weekly, monthly
    backup_time TIME NOT NULL,
    backup_location VARCHAR(200),
    max_backups INTEGER DEFAULT 30,
    compress_backups BOOLEAN DEFAULT TRUE,
    include_attachments BOOLEAN DEFAULT TRUE,
    email_notifications BOOLEAN DEFAULT TRUE,
    notification_email VARCHAR(120),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Quick Start

### **Replit Deployment**
1. Fork this repository to your Replit account
2. PostgreSQL database is automatically provisioned
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python main.py`
5. Access at: `https://your-repl-name.replit.app`

### **Default Accounts**
- **Super Admin**: username: `superadmin`, password: `super123`
- **Test User**: username: `testuser`, password: `test123`

## 🎨 UI/UX Features

### **Landing Page**
- Modern hero section with gradient background
- Feature showcase with step-by-step process
- User role comparison section
- Call-to-action with smooth animations

### **Login Page**
- Split-screen design with branding
- Floating form labels
- Animated background shapes
- Role indicators and access information

### **User Dashboard**
- Personal ticket overview
- Quick ticket creation
- Status-based filtering
- Mobile-optimized layout

### **Super Admin Dashboard**
- System-wide statistics
- Visual analytics charts
- User management tools
- Advanced filtering options

## 🔧 Technical Architecture

### **Backend Stack**
- **Flask 2.3+**: Web framework with blueprints
- **SQLAlchemy**: ORM with PostgreSQL support
- **Flask-WTF**: Secure form handling with CSRF protection
- **Werkzeug**: Password hashing and security utilities
- **Gunicorn**: Production WSGI server

### **Frontend Stack**
- **Bootstrap 5.3**: Responsive CSS framework
- **Remix Icons**: Modern icon library
- **Chart.js**: Data visualization
- **Vanilla JavaScript**: Client-side interactivity

### **Database Support**
- **PostgreSQL**: Primary production database
- **Connection Pooling**: Optimized database performance
- **IST Timezone**: Indian Standard Time support

## 📱 Responsive Design

### **Mobile Features**
- Touch-friendly interface
- Responsive navigation
- Optimized forms
- Mobile ticket creation
- Swipe-friendly dashboards

### **Desktop Features**
- Full-screen dashboards
- Advanced filtering
- Bulk operations
- Multi-panel views
- Keyboard shortcuts

## 🔐 Security Features

### **Authentication & Authorization**
- Session-based authentication
- Role-based access control
- CSRF protection on all forms
- Secure password hashing

### **Data Protection**
- SQL injection prevention
- XSS protection
- File upload validation
- IP address logging

## 📈 Analytics & Reporting

### **Dashboard Metrics**
- Total tickets by status
- Category distribution
- Priority analysis
- Resolution time tracking

### **Export Features**
- Excel reports with IST timestamps
- Filtered data export
- User activity reports
- System usage analytics

## 🛠️ Development

### **Project Structure**
```
├── main.py              # Application entry point
├── app.py               # Flask configuration and database setup
├── routes.py            # URL routing and view functions
├── models.py            # SQLAlchemy database models
├── forms.py             # WTForms form definitions
├── templates/           # Jinja2 HTML templates
│   ├── auth/           # Authentication templates
│   ├── master_data/    # Master data management templates
│   ├── tickets/        # Ticket-related templates
│   └── users/          # User management templates
├── static/             # Static assets
│   ├── style.css       # Main stylesheet
│   └── uploads/        # File attachments storage
├── utils/              # Utility modules
│   └── email.py        # Email notification system
├── README.md           # Main documentation
├── README_Database_Schema.md    # Database documentation
├── README_Master_Data.md        # Master data guide
└── README_PostgreSQL_Setup.md   # Database setup guide
```

### **Environment Variables**
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Flask session encryption key

## 📞 Support

### **Getting Help**
- Review the documentation in this README
- Check the database schema section
- Examine the codebase structure
- Test with default accounts

### **Common Issues**
- Database connection: Check PostgreSQL status
- File uploads: Verify uploads directory permissions
- SMTP errors: Configure email settings in utils/email.py



### Supported Platforms
- **Development**: Windows, macOS, Linux
- **Production**: Linux (Ubuntu 20.04+, CentOS 8+), Windows Server
- **Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+



## Installation Guide

### Development Setup

1. **Install Python 3.11+**
   ```bash
   python --version  # Verify installation
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-wtf flask-login
   pip install werkzeug email-validator openpyxl psycopg2-binary
   pip install gunicorn pymysql pyodbc
   ```

4. **Configure Database**
   - PostgreSQL: See [PostgreSQL Setup Guide](README_PostgreSQL_Setup.md)
   - SQL Server: Configure connection string with pyodbc
   - MySQL: Configure connection string with PyMySQL

### Production Deployment

1. **Configure Environment Variables**
   ```bash
   export DATABASE_URL="your-production-database-url"
   export SESSION_SECRET="secure-production-secret"
   export FLASK_ENV="production"
   ```

2. **Start with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
   ```

3. **Setup Reverse Proxy** (Nginx recommended)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

## Configuration

### Database Configuration

The system supports multiple database backends with automatic detection:

```python
# Priority order: PostgreSQL > SQL Server > MySQL
DATABASE_URL = "postgresql://user:pass@host:port/db"  # Primary
SQL_SERVER_URL = "mssql+pyodbc://user:pass@host:port/db?driver=..."
MYSQL_URL = "mysql+pymysql://user:pass@host:port/db"
```

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Primary database connection | None | Yes |
| `SESSION_SECRET` | Flask session secret key | None | Yes |
| `SQL_SERVER_HOST` | SQL Server hostname | None | No |
| `SQL_SERVER_DATABASE` | SQL Server database name | gtn_helpdesk | No |
| `MYSQL_URL` | MySQL connection URL | None | No |

### Application Settings

```python
# In app.py - customize as needed
app.config.update({
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ENGINE_OPTIONS': {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    },
    'WTF_CSRF_ENABLED': True,
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024  # 16MB max file upload
})
```



### User Roles & Permissions

| Feature | User | Super Admin |
|---------|------|-------------|
| Create Tickets | ✅ | ✅ |
| View Own Tickets | ✅ | ✅ |
| View All Tickets | ❌ | ✅ |
| Assign Tickets | ❌ | ✅ |
| Manage Users | ❌ | ✅ |
| Reports Dashboard | ❌ | ✅ |
| Excel Export | ❌ | ✅ |
| System Settings | ❌ | ✅ |

### Creating Your First Ticket

1. **Login** as a regular user
2. **Navigate** to "New Ticket" 
3. **Fill out the form**:
   - Title: Descriptive summary
   - Description: Detailed problem description
   - Category: Hardware/Software
   - Priority: Low/Medium/High/Critical
   - System Name: Auto-detected or manual entry
   - File Attachments: Upload images, PDF, Word documents, or Excel files
5. **Submit** - Ticket number will be generated automatically

### Admin Workflow

1. **Dashboard Overview**: View all tickets and statistics
2. **Ticket Assignment**: Assign tickets to appropriate admins
3. **Status Updates**: Update ticket status as work progresses
4. **Comment System**: Add internal notes and user communication
5. **Resolution**: Mark tickets as resolved with solution details

## API Documentation

### Database Models

#### User Model
```python
class User(db.Model):
    id = Integer (Primary Key)
    username = String(80) (Unique, NOT NULL)
    email = String(120) (Unique, NOT NULL)
    password_hash = String(256) (NOT NULL)
    first_name = String(50) (NOT NULL)
    last_name = String(50) (NOT NULL)
    department = String(100) (Optional)
    role = String(50) (NOT NULL, Default: 'User')  # user, admin, super_admin
    is_admin = Boolean (Default: False)
    ip_address = String(45) (Optional, IPv4/IPv6)
    system_name = String(100) (Optional)
    profile_image = String(200) (Optional)
    created_at = DateTime (Default: UTC now)
```

#### Ticket Model
```python
class Ticket(db.Model):
    id = Integer (Primary Key)
    title = String(200) (NOT NULL)
    description = Text (NOT NULL)
    category = String(50) (NOT NULL)  # Hardware, Software
    priority = String(20) (NOT NULL)  # Low, Medium, High, Critical
    status = String(20) (NOT NULL, Default: 'Open')  # Open, In Progress, Resolved, Closed
    user_name = String(100) (NOT NULL)  # Full name of ticket creator
    user_ip_address = String(45) (Optional)  # IP at creation
    user_system_name = String(100) (Optional)  # System name at creation
    image_filename = String(255) (Optional)  # Uploaded file
    user_id = Integer (Foreign Key, NOT NULL → users.id)
    assigned_to = Integer (Foreign Key, Optional → users.id)
    assigned_by = Integer (Foreign Key, Optional → users.id)
    created_at = DateTime (Default: UTC now)
    updated_at = DateTime (Auto-update on changes)
    resolved_at = DateTime (Optional, set when resolved)
```

#### Comment Model
```python
class TicketComment(db.Model):
    id = Integer (Primary Key)
    ticket_id = Integer (Foreign Key, NOT NULL → tickets.id)
    user_id = Integer (Foreign Key, NOT NULL → users.id)
    comment = Text (NOT NULL)
    created_at = DateTime (Default: UTC now)
```

#### Attachment Model
```python
class Attachment(db.Model):
    id = Integer (Primary Key)
    ticket_id = Integer (Foreign Key, NOT NULL → tickets.id)
    filename = String(255) (NOT NULL)
    uploaded_at = DateTime (Default: UTC now)
```

### Key Routes

| Route | Method | Description | Access Level |
|-------|--------|-------------|--------------|
| `/` | GET | Homepage | Public |
| `/user-login` | GET/POST | User authentication | Public |
| `/admin-login` | GET/POST | Admin authentication | Public |
| `/user-dashboard` | GET | User ticket overview | User+ |
| `/admin-dashboard` | GET | Admin ticket management | Admin+ |
| `/super-admin-dashboard` | GET | System overview | Super Admin |
| `/create-ticket` | GET/POST | New ticket creation | User+ |
| `/ticket/<id>` | GET | Ticket details | Owner/Admin+ |
| `/reports-dashboard` | GET | Analytics dashboard | Super Admin |
| `/download-excel-report` | GET | Excel export | Super Admin |

## Advanced Features

### System Information Capture

The application automatically captures:
- **IP Address**: Real client IP (handles proxy forwarding)
- **System Name**: Operating system and browser detection
- **User Agent**: Browser and device information
- **Session Data**: Login time and activity tracking

### Intelligent Assignment System

- **Category-Based**: Routes tickets to specialized teams
- **Workload Balancing**: Distributes tickets evenly among admins
- **Priority Handling**: Escalates critical issues automatically
- **Department Matching**: Assigns based on user department

### File Attachment System

- **Multiple File Types**: Support for images (JPG, PNG, GIF, BMP), PDF documents, Word files (.doc, .docx), and Excel spreadsheets (.xls, .xlsx)
- **Multiple Files**: Upload multiple attachments per ticket
- **Secure Storage**: Files stored with unique timestamps to prevent conflicts
- **Admin Access**: Only administrators can view and download attachments for security
- **File Validation**: Automatic file type validation and size limits

### Reporting & Analytics

- **Visual Charts**: Category, priority, and status breakdowns
- **Export Capabilities**: Excel files with complete ticket data
- **Performance Metrics**: Resolution times and response rates
- **Historical Data**: Trend analysis and reporting

### Security Features

- **Password Hashing**: Werkzeug secure password storage
- **CSRF Protection**: Form submission security
- **Session Management**: Secure user session handling
- **Input Validation**: WTForms data validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check database status
systemctl status postgresql  # Linux
net start postgresql-x64-16  # Windows

# Verify connection string
psql -U username -d database_name -h localhost
```

#### Application Won't Start
```bash
# Check Python version
python --version

# Verify dependencies
pip list | grep -E "(flask|sqlalchemy|wtf)"

# Check environment variables
echo $DATABASE_URL
echo $SESSION_SECRET
```

#### Permission Denied Errors
```bash
# Check file permissions
chmod 755 main.py
chmod 644 *.html *.css *.js

# Database permissions
GRANT ALL PRIVILEGES ON DATABASE gtn_helpdesk TO username;
```

### Performance Optimization

#### Database Optimization
```sql
-- Add indexes for better query performance
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_category ON tickets(category);
CREATE INDEX idx_tickets_user_id ON tickets(user_id);
CREATE INDEX idx_tickets_created_at ON tickets(created_at);
```

#### Application Tuning
```python
# Configure connection pooling
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 20,
    'pool_recycle': 300,
    'pool_pre_ping': True,
    'max_overflow': 30
}
```

## Development

### Project Structure
```
gtn-helpdesk-system/
├── main.py                 # Application entry point
├── app.py                  # Flask app configuration
├── routes.py               # URL routing and views
├── models.py               # Database models
├── forms.py                # WTForms definitions
├── static/                 # CSS, JS, images
│   ├── style.css          # Custom styling
│   ├── script.js          # Client-side functionality
│   └── gtn_logo.jpg       # Company logo
├── templates/              # Jinja2 HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Homepage
│   ├── user_dashboard.html # User interface
│   ├── admin_dashboard.html # Admin interface
│   └── ...
├── README.md              # This file
├── README_PostgreSQL_Setup.md # Database setup guide
└── requirements.txt       # Python dependencies
```

### Adding New Features

1. **Database Changes**: Update models.py and run migrations
2. **Forms**: Add new form classes in forms.py
3. **Routes**: Create new endpoints in routes.py
4. **Templates**: Design HTML interfaces in templates/
5. **Styling**: Update static/style.css for new components

### Code Style Guidelines

- **Python**: Follow PEP 8 standards
- **HTML**: Use semantic markup and proper indentation
- **CSS**: Use CSS custom properties and BEM methodology
- **JavaScript**: ES6+ features with proper error handling

## Deployment Options

### Docker Deployment (Recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### Systemd Service (Linux)
```ini
[Unit]
Description=GTN Helpdesk System
After=network.target

[Service]
Type=exec
User=www-data
WorkingDirectory=/opt/gtn-helpdesk
Environment=DATABASE_URL=postgresql://...
Environment=SESSION_SECRET=...
ExecStart=/opt/gtn-helpdesk/venv/bin/gunicorn --bind 0.0.0.0:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Windows Service
Use NSSM (Non-Sucking Service Manager) or similar tools to run as Windows service.

## Support & Maintenance

### Backup Strategy
```bash
# Daily database backup
pg_dump -U username gtn_helpdesk > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz /path/to/app
```

### Monitoring
- **Application Logs**: Check Flask application logs
- **Database Performance**: Monitor query execution times
- **System Resources**: CPU, memory, and disk usage
- **User Activity**: Login patterns and ticket creation rates

### Updates & Patches
1. **Test Environment**: Always test updates in staging
2. **Database Migration**: Use proper migration scripts
3. **Backup First**: Create full backup before updates
4. **Gradual Rollout**: Deploy to small user groups first



## License

This project is proprietary software developed for GTN Engineering (India) Ltd.

## Contact

For technical support or questions:
- **Email**: it-support@gtnengineering.com
- **Internal Helpdesk**: Use this system to create tickets
- **Emergency**: Contact IT department directly

---

**GTN Engineering (India) Ltd - IT Team**  
*Professional IT Support Solutions*

Last Updated: June 27, 2025  
Version: 2.1.0
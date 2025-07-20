# GTN Engineering IT Helpdesk - IIS Windows Server Deployment Guide

A comprehensive guide for deploying the GTN Engineering IT Helpdesk System on Windows Server using Internet Information Services (IIS) with professional-grade configuration.

![Windows Server](https://img.shields.io/badge/windows%20server-2019%2B-blue.svg)
![IIS](https://img.shields.io/badge/IIS-10.0%2B-green.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-15%2B-blue.svg)

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows Server 2019/2022 (recommended) or Windows 10/11 Pro
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 50GB free space
- **Network**: Static IP address (recommended for production)

### Software Dependencies
- **IIS 10.0+** with required modules
- **Python 3.11+** with pip package manager
- **PostgreSQL 15+** database server
- **Visual C++ Redistributable** (for Python packages)

## 🔧 Step 1: Windows Server Setup

### 1.1 Enable IIS with Required Features

Open **Server Manager** and install IIS with the following features:

```powershell
# Run as Administrator in PowerShell
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServer
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CommonHttpFeatures
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpErrors
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpLogging
Enable-WindowsOptionalFeature -Online -FeatureName IIS-Security
Enable-WindowsOptionalFeature -Online -FeatureName IIS-RequestFiltering
Enable-WindowsOptionalFeature -Online -FeatureName IIS-StaticContent
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DefaultDocument
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DirectoryBrowsing
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIExtensions
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIFilter
```

### 1.2 Manual IIS Feature Installation (Alternative)

1. Open **Control Panel** → **Programs** → **Turn Windows features on or off**
2. Expand **Internet Information Services**
3. Expand **World Wide Web Services**
4. Enable the following:
   - **Application Development Features**:
     - ✅ CGI
     - ✅ ISAPI Extensions
     - ✅ ISAPI Filters
   - **Common HTTP Features**:
     - ✅ Default Document
     - ✅ Directory Browsing
     - ✅ HTTP Errors
     - ✅ HTTP Redirection
     - ✅ Static Content
   - **Health and Diagnostics**:
     - ✅ HTTP Logging
     - ✅ Request Monitor
   - **Security**:
     - ✅ Request Filtering
     - ✅ Basic Authentication (optional)
     - ✅ Windows Authentication (optional)

### 1.3 Verify IIS Installation

1. Open **Internet Information Services (IIS) Manager**
2. Navigate to **Default Web Site**
3. Browse to `http://localhost` - you should see the IIS welcome page

## 🐍 Step 2: Python Installation & Configuration

### 2.1 Install Python 3.11+

1. Download Python from [python.org](https://www.python.org/downloads/windows/)
2. **Important**: Check "Add Python to PATH" during installation
3. Choose "Custom Installation" and ensure these options are selected:
   - ✅ pip
   - ✅ py launcher
   - ✅ Add Python to environment variables

### 2.2 Verify Python Installation

```cmd
python --version
pip --version
```

### 2.3 Install Python Dependencies

```cmd
# Navigate to your project directory
cd C:\inetpub\wwwroot\gtn-helpdesk

# Install required packages
pip install flask==2.3.3
pip install flask-sqlalchemy==3.0.5
pip install flask-wtf==1.1.1
pip install flask-login==0.6.3
pip install werkzeug==2.3.7
pip install email-validator==2.0.0
pip install openpyxl==3.1.2
pip install psycopg2-binary==2.9.7
pip install gunicorn==21.2.0
pip install waitress==2.1.2
```

### 2.4 Install wfastcgi (Required for IIS)

```cmd
pip install wfastcgi
wfastcgi-enable
```

**Note the output path** - you'll need it for IIS configuration (e.g., `C:\Python311\python.exe|C:\Python311\Lib\site-packages\wfastcgi.py`)

## 🗄️ Step 3: PostgreSQL Database Setup

### 3.1 Install PostgreSQL

1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer with these settings:
   - **Port**: 5432 (default)
   - **Superuser Password**: Create a strong password
   - **Locale**: Default locale

### 3.2 Configure PostgreSQL

1. Open **pgAdmin 4** or **SQL Shell (psql)**
2. Create the database and user:

```sql
-- Connect as postgres superuser
CREATE DATABASE gtn_helpdesk_prod;
CREATE USER gtn_user WITH ENCRYPTED PASSWORD 'your_secure_password_2024';
GRANT ALL PRIVILEGES ON DATABASE gtn_helpdesk_prod TO gtn_user;

-- Connect to the gtn_helpdesk_prod database
\c gtn_helpdesk_prod

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO gtn_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gtn_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gtn_user;
```

### 3.3 Configure PostgreSQL for Network Access

Edit `C:\Program Files\PostgreSQL\15\data\postgresql.conf`:

```ini
listen_addresses = 'localhost'
port = 5432
max_connections = 100
```

Edit `C:\Program Files\PostgreSQL\15\data\pg_hba.conf`:

```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     trust
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```

Restart PostgreSQL service:

```cmd
net stop postgresql-x64-15
net start postgresql-x64-15
```

## 📁 Step 4: Application Deployment

### 4.1 Create Application Directory

```cmd
mkdir C:\inetpub\wwwroot\gtn-helpdesk
cd C:\inetpub\wwwroot\gtn-helpdesk
```

### 4.2 Deploy Application Files

Copy all application files to `C:\inetpub\wwwroot\gtn-helpdesk\`:

```
gtn-helpdesk/
├── main.py
├── app.py
├── routes.py
├── models.py
├── forms.py
├── templates/
├── static/
├── utils/
├── web.config (create this file)
└── uploads/ (create this directory)
```

### 4.3 Create Required Directories

```cmd
mkdir C:\inetpub\wwwroot\gtn-helpdesk\uploads
mkdir C:\inetpub\wwwroot\gtn-helpdesk\logs
```

### 4.4 Set Directory Permissions

1. Right-click on `C:\inetpub\wwwroot\gtn-helpdesk`
2. **Properties** → **Security** → **Edit**
3. Add **IIS_IUSRS** with **Full Control**
4. Add **IUSR** with **Read & Execute**
5. Ensure **uploads** directory has **Write** permissions for **IIS_IUSRS**

## ⚙️ Step 5: IIS Configuration

### 5.1 Create web.config File

Create `C:\inetpub\wwwroot\gtn-helpdesk\web.config`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" 
           path="*" 
           verb="*" 
           modules="FastCgiModule"
           scriptProcessor="C:\Python311\python.exe|C:\Python311\Lib\site-packages\wfastcgi.py"
           resourceType="Unspecified"
           requireAccess="Script" />
    </handlers>
    <defaultDocument>
      <files>
        <clear />
        <add value="main.py" />
      </files>
    </defaultDocument>
    <security>
      <requestFiltering>
        <requestLimits maxAllowedContentLength="52428800" />
      </requestFiltering>
    </security>
    <httpErrors>
      <remove statusCode="404" subStatusCode="-1" />
      <error statusCode="404" 
             prefixLanguageFilePath="" 
             path="/static/404.html" 
             responseMode="ExecuteURL" />
    </httpErrors>
  </system.webServer>
  <appSettings>
    <add key="PYTHONPATH" value="C:\inetpub\wwwroot\gtn-helpdesk" />
    <add key="WSGI_HANDLER" value="main.app" />
    <add key="WSGI_LOG" value="C:\inetpub\wwwroot\gtn-helpdesk\logs\wfastcgi.log" />
    <add key="DATABASE_URL" value="postgresql://gtn_user:your_secure_password_2024@localhost:5432/gtn_helpdesk_prod" />
    <add key="SESSION_SECRET" value="your-secure-session-secret-key-here" />
    <add key="FLASK_ENV" value="production" />
  </appSettings>
</configuration>
```

### 5.2 Configure FastCGI in IIS

1. Open **IIS Manager**
2. Click on **Server Name** (root level)
3. Double-click **FastCGI Settings**
4. Click **Add Application...**
5. Configure:
   - **Full Path**: `C:\Python311\python.exe`
   - **Arguments**: `C:\Python311\Lib\site-packages\wfastcgi.py`
   - **Environment Variables**:
     - `PYTHONPATH` = `C:\inetpub\wwwroot\gtn-helpdesk`
     - `WSGI_HANDLER` = `main.app`
     - `WSGI_LOG` = `C:\inetpub\wwwroot\gtn-helpdesk\logs\wfastcgi.log`

### 5.3 Create Application in IIS

1. In **IIS Manager**, expand **Sites**
2. Right-click **Default Web Site** → **Add Application**
3. Configure:
   - **Alias**: `gtn-helpdesk`
   - **Physical path**: `C:\inetpub\wwwroot\gtn-helpdesk`
   - **Application pool**: Create new pool named `GTN_Helpdesk_Pool`

### 5.4 Configure Application Pool

1. Click **Application Pools**
2. Right-click **GTN_Helpdesk_Pool** → **Advanced Settings**
3. Configure:
   - **.NET CLR Version**: No Managed Code
   - **Identity**: ApplicationPoolIdentity
   - **Load User Profile**: True
   - **Idle Time-out**: 20 minutes
   - **Maximum Worker Processes**: 1
   - **Start Mode**: AlwaysRunning

## 🔐 Step 6: Security Configuration

### 6.1 Configure SSL/HTTPS (Recommended)

1. In **IIS Manager**, click on your site
2. Double-click **SSL Settings**
3. Check **Require SSL**
4. Install SSL certificate:
   - **Self-signed** (development): Server Certificates → Create Self-Signed Certificate
   - **Production**: Obtain certificate from trusted CA

### 6.2 Configure Authentication

1. Double-click **Authentication**
2. Configure as needed:
   - **Anonymous Authentication**: Enabled (for public access)
   - **Windows Authentication**: Optional (for AD integration)
   - **Basic Authentication**: Disabled (less secure)

### 6.3 Configure Request Filtering

1. Double-click **Request Filtering**
2. **File Extensions** tab → Allow these extensions:
   - `.py`, `.css`, `.js`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`
3. **Request Limits** tab:
   - **Maximum allowed content length**: 50 MB
   - **Maximum URL length**: 4096
   - **Maximum query string**: 2048

## 🌍 Step 7: Environment Variables & Configuration

### 7.1 Set System Environment Variables

```cmd
# Set via Command Prompt (requires restart)
setx DATABASE_URL "postgresql://gtn_user:your_secure_password_2024@localhost:5432/gtn_helpdesk_prod" /M
setx SESSION_SECRET "your-secure-session-secret-key-here" /M
setx FLASK_ENV "production" /M
setx PYTHONPATH "C:\inetpub\wwwroot\gtn-helpdesk" /M
```

### 7.2 Generate Secure Session Secret

```cmd
python -c "import secrets; print('SESSION_SECRET=' + secrets.token_hex(32))"
```

### 7.3 Update Application Configuration

Modify `app.py` to use Windows-specific paths:

```python
import os
import logging
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging for Windows
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler('C:\\inetpub\\wwwroot\\gtn-helpdesk\\logs\\app.log'),
        logging.StreamHandler()
    ]
)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def get_database_uri():
    """Get database URI from environment or web.config"""
    return os.environ.get("DATABASE_URL") or \
           "postgresql://gtn_user:your_secure_password_2024@localhost:5432/gtn_helpdesk_prod"

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or "fallback-secret-change-in-production"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure uploads directory for Windows
app.config['UPLOAD_FOLDER'] = 'C:\\inetpub\\wwwroot\\gtn-helpdesk\\uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file upload

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Import routes and initialize database
with app.app_context():
    import models
    db.create_all()
    logging.info("Database tables created successfully")
```

## 🚀 Step 8: Testing & Deployment

### 8.1 Test Python Application

```cmd
cd C:\inetpub\wwwroot\gtn-helpdesk
python main.py
```

Should start without errors and show Flask development server.

### 8.2 Test Database Connection

```cmd
cd C:\inetpub\wwwroot\gtn-helpdesk
python -c "from app import db; print('Database connection successful')"
```

### 8.3 Test IIS Deployment

1. Open browser and navigate to: `http://localhost/gtn-helpdesk`
2. Should display the GTN Engineering IT Helpdesk homepage
3. Test login functionality with default credentials:
   - **Super Admin**: `superadmin` / `admin123`
   - **Test User**: `testuser` / `user123`

### 8.4 Check Error Logs

Monitor these log files for issues:

```
C:\inetpub\wwwroot\gtn-helpdesk\logs\wfastcgi.log
C:\inetpub\wwwroot\gtn-helpdesk\logs\app.log
C:\Windows\System32\LogFiles\HTTPERR\httperr1.log
```

## 🔧 Step 9: Performance Optimization

### 9.1 Configure Output Caching

Add to `web.config` under `<system.webServer>`:

```xml
<caching>
  <profiles>
    <add extension=".css" policy="CacheForTimePeriod" kernelCachePolicy="CacheForTimePeriod" duration="01:00:00" />
    <add extension=".js" policy="CacheForTimePeriod" kernelCachePolicy="CacheForTimePeriod" duration="01:00:00" />
    <add extension=".png" policy="CacheForTimePeriod" kernelCachePolicy="CacheForTimePeriod" duration="24:00:00" />
    <add extension=".jpg" policy="CacheForTimePeriod" kernelCachePolicy="CacheForTimePeriod" duration="24:00:00" />
  </profiles>
</caching>
```

### 9.2 Enable Compression

```xml
<httpCompression>
  <dynamicTypes>
    <clear />
    <add enabled="true" mimeType="text/*" />
    <add enabled="true" mimeType="message/*" />
    <add enabled="true" mimeType="application/javascript" />
    <add enabled="false" mimeType="*/*" />
  </dynamicTypes>
  <staticTypes>
    <clear />
    <add enabled="true" mimeType="text/*" />
    <add enabled="true" mimeType="message/*" />
    <add enabled="true" mimeType="application/javascript" />
    <add enabled="true" mimeType="application/atom+xml" />
    <add enabled="true" mimeType="application/xaml+xml" />
  </staticTypes>
</httpCompression>
```

### 9.3 Configure Application Warm-up

1. Install **Application Initialization** module in IIS
2. Add to `web.config`:

```xml
<system.webServer>
  <applicationInitialization doAppInitAfterRestart="true">
    <add initializationPage="/" />
  </applicationInitialization>
</system.webServer>
```

## 📊 Step 10: Monitoring & Maintenance

### 10.1 Setup Logging

Create `C:\inetpub\wwwroot\gtn-helpdesk\logging.conf`:

```ini
[loggers]
keys=root,werkzeug,sqlalchemy

[handlers]
keys=fileHandler,consoleHandler

[formatters]
keys=fileFormatter,consoleFormatter

[logger_root]
level=INFO
handlers=fileHandler,consoleHandler

[logger_werkzeug]
level=INFO
handlers=fileHandler
qualname=werkzeug
propagate=0

[logger_sqlalchemy]
level=WARN
handlers=fileHandler
qualname=sqlalchemy.engine
propagate=0

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=fileFormatter
args=('C:\\inetpub\\wwwroot\\gtn-helpdesk\\logs\\app.log', 'a')

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=consoleFormatter
args=(sys.stdout,)

[formatter_fileFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S

[formatter_consoleFormatter]
format=%(levelname)s - %(message)s
```

### 10.2 Create Backup Scripts

Create `C:\Scripts\backup_gtn_helpdesk.bat`:

```batch
@echo off
setlocal

:: Set variables
set BACKUP_DIR=C:\Backups\GTN_Helpdesk
set DATE_STAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%
set TIME_STAMP=%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%DATE_STAMP%_%TIME_STAMP: =0%

:: Create backup directory
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

:: Backup database
echo Backing up PostgreSQL database...
"C:\Program Files\PostgreSQL\15\bin\pg_dump.exe" -h localhost -U gtn_user -d gtn_helpdesk_prod > %BACKUP_DIR%\database_backup_%TIMESTAMP%.sql

:: Backup application files
echo Backing up application files...
robocopy "C:\inetpub\wwwroot\gtn-helpdesk" "%BACKUP_DIR%\app_backup_%TIMESTAMP%" /E /XD logs __pycache__ .git

:: Cleanup old backups (keep last 7 days)
forfiles /p %BACKUP_DIR% /m *.* /d -7 /c "cmd /c del @path"

echo Backup completed: %TIMESTAMP%
```

### 10.3 Schedule Automated Backups

1. Open **Task Scheduler**
2. Create **Basic Task**:
   - **Name**: GTN Helpdesk Backup
   - **Trigger**: Daily at 2:00 AM
   - **Action**: Start a program
   - **Program**: `C:\Scripts\backup_gtn_helpdesk.bat`

### 10.4 Performance Monitoring

Monitor these performance counters:

- **Web Service** → Requests/Sec
- **Process** → % Processor Time (python.exe)
- **Memory** → Available MBytes
- **PhysicalDisk** → % Disk Time

## 🔒 Step 11: Security Hardening

### 11.1 Firewall Configuration

```cmd
# Allow HTTP (port 80)
netsh advfirewall firewall add rule name="HTTP Inbound" dir=in action=allow protocol=TCP localport=80

# Allow HTTPS (port 443)
netsh advfirewall firewall add rule name="HTTPS Inbound" dir=in action=allow protocol=TCP localport=443

# Allow PostgreSQL (port 5432) - Local only
netsh advfirewall firewall add rule name="PostgreSQL Local" dir=in action=allow protocol=TCP localport=5432 remoteip=127.0.0.1
```

### 11.2 Hide Server Information

Add to `web.config`:

```xml
<system.webServer>
  <security>
    <requestFiltering removeServerHeader="true" />
  </security>
  <httpProtocol>
    <customHeaders>
      <remove name="X-Powered-By" />
      <add name="X-Frame-Options" value="SAMEORIGIN" />
      <add name="X-Content-Type-Options" value="nosniff" />
      <add name="X-XSS-Protection" value="1; mode=block" />
      <add name="Strict-Transport-Security" value="max-age=31536000; includeSubDomains" />
    </customHeaders>
  </httpProtocol>
</system.webServer>
```

### 11.3 Restrict File Access

```xml
<location path="web.config">
  <system.webServer>
    <security>
      <requestFiltering>
        <hiddenSegments>
          <add segment="web.config" />
        </hiddenSegments>
      </requestFiltering>
    </security>
  </system.webServer>
</location>

<location path="logs">
  <system.webServer>
    <security>
      <requestFiltering>
        <hiddenSegments>
          <add segment="logs" />
        </hiddenSegments>
      </requestFiltering>
    </security>
  </system.webServer>
</location>
```

## 🚨 Troubleshooting

### Common Issues & Solutions

#### 1. **500 Internal Server Error**

**Check**: `wfastcgi.log` and Windows Event Log

**Solutions**:
- Verify `web.config` syntax
- Check Python path in FastCGI settings
- Ensure all dependencies are installed
- Verify database connection string

#### 2. **Python Module Not Found**

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```cmd
# Reinstall packages in correct Python environment
pip install flask flask-sqlalchemy flask-wtf flask-login
```

#### 3. **Database Connection Failed**

**Error**: `connection to server at "localhost" failed`

**Solutions**:
- Verify PostgreSQL service is running: `net start postgresql-x64-15`
- Check connection string in environment variables
- Verify user permissions in PostgreSQL

#### 4. **File Upload Issues**

**Error**: File uploads failing

**Solutions**:
- Check uploads directory permissions
- Verify `MAX_CONTENT_LENGTH` in `web.config`
- Ensure disk space is available

#### 5. **Performance Issues**

**Symptoms**: Slow response times

**Solutions**:
- Increase application pool memory limits
- Enable output caching
- Optimize database queries
- Add database connection pooling

### Log File Locations

| Log Type | Location |
|----------|----------|
| Application Logs | `C:\inetpub\wwwroot\gtn-helpdesk\logs\app.log` |
| FastCGI Logs | `C:\inetpub\wwwroot\gtn-helpdesk\logs\wfastcgi.log` |
| IIS Logs | `C:\inetpub\logs\LogFiles\W3SVC1\` |
| Windows Event Log | Event Viewer → Windows Logs → Application |
| PostgreSQL Logs | `C:\Program Files\PostgreSQL\15\data\log\` |

## 🎯 Production Checklist

### Pre-Deployment
- [ ] Windows Server patched and updated
- [ ] IIS installed with required modules
- [ ] Python 3.11+ installed with all dependencies
- [ ] PostgreSQL installed and configured
- [ ] SSL certificate obtained and installed
- [ ] Firewall rules configured
- [ ] Backup solution implemented

### Security
- [ ] Default passwords changed
- [ ] Session secret key generated
- [ ] Database user permissions restricted
- [ ] File system permissions configured
- [ ] Request filtering enabled
- [ ] Security headers configured

### Performance
- [ ] Application pool optimized
- [ ] Output caching enabled
- [ ] Compression configured
- [ ] Connection pooling enabled
- [ ] Monitoring tools configured

### Maintenance
- [ ] Automated backups scheduled
- [ ] Log rotation configured
- [ ] Update procedures documented
- [ ] Disaster recovery plan created

## 📞 Support & Maintenance

### Regular Maintenance Tasks

#### Daily
- Monitor application logs for errors
- Check system resource usage
- Verify backup completion

#### Weekly
- Review security logs
- Update Windows patches
- Check database performance

#### Monthly
- Update Python packages
- Review access logs
- Test backup restoration
- Review security configuration

### Emergency Contacts

- **IT Team**: it-support@gtnengineering.com
- **Database Issues**: Contact PostgreSQL administrator
- **Server Issues**: Contact Windows Server administrator

## 📄 License & Support

This deployment guide is part of the GTN Engineering IT Helpdesk System, proprietary software developed for GTN Engineering (India) Ltd.

For technical support with Windows Server deployment:
- **Internal IT Team**: Use the helpdesk system
- **Windows Server Issues**: Contact system administrator
- **Database Issues**: Contact database administrator

---

**GTN Engineering (India) Ltd - IT Infrastructure Team**  
*Professional Windows Server Deployment Solutions*

Last Updated: June 29, 2025
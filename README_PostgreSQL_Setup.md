# PostgreSQL Setup Guide for GTN Engineering IT Helpdesk

Comprehensive setup guide for PostgreSQL database integration with the GTN Engineering IT Helpdesk System, optimized for Replit deployment and local development.

## Overview

The GTN Engineering IT Helpdesk System uses PostgreSQL as its primary production database with automatic provisioning in Replit environment. This guide covers both Replit deployment and local development setup.

## Replit Environment (Recommended)

### Automatic PostgreSQL Provisioning

The Replit environment automatically provides:

- **PostgreSQL Database**: Pre-configured and ready to use
- **Environment Variables**: Automatically set connection parameters
- **Connection Pooling**: Optimized for web application performance
- **Backup Management**: Handled by Replit infrastructure

### Available Environment Variables

```bash
DATABASE_URL=postgresql://username:password@host:port/database
PGHOST=your-postgres-host
PGPORT=5432
PGUSER=your-username
PGPASSWORD=your-password
PGDATABASE=your-database-name
```

### Verification Steps

1. Check database connection status:
```python
# In your Replit console
python -c "
import os
print('Database URL:', os.environ.get('DATABASE_URL', 'Not set'))
print('PG Host:', os.environ.get('PGHOST', 'Not set'))
print('PG Database:', os.environ.get('PGDATABASE', 'Not set'))
"
```

2. Test database connectivity:
```python
# Run this in Replit shell
python -c "
from app import db
try:
    db.create_all()
    print('✅ Database connection successful!')
    print('✅ Tables created successfully!')
except Exception as e:
    print(f'❌ Database error: {e}')
"
```

## Local Development Setup

### Prerequisites

- **Python 3.11+**: Required for Flask application
- **PostgreSQL 15+**: Database server
- **Administrative Access**: For installation and configuration

### Windows Installation

1. **Download PostgreSQL**:
   - Visit: https://www.postgresql.org/download/windows/
   - Download PostgreSQL 15.x or higher
   - Run installer as Administrator

2. **Installation Configuration**:
   ```
   Installation Directory: C:\Program Files\PostgreSQL\15
   Data Directory: C:\Program Files\PostgreSQL\15\data
   Password: [Set strong password for postgres user]
   Port: 5432 (default)
   Locale: Default or your preference
   ```

3. **Verify Installation**:
   ```cmd
   # Open Command Prompt as Administrator
   cd "C:\Program Files\PostgreSQL\15\bin"
   psql -U postgres -h localhost
   # Enter password when prompted
   # You should see: postgres=#
   ```

### macOS Installation

1. **Using Homebrew** (Recommended):
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install PostgreSQL
   brew install postgresql@15
   
   # Start PostgreSQL service
   brew services start postgresql@15
   ```

2. **Using PostgreSQL.app**:
   - Download from: https://postgresapp.com/
   - Drag to Applications folder
   - Launch and initialize

### Linux Installation (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start and enable PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -u postgres psql
```

## Database Configuration

### Create GTN Helpdesk Database

```sql
-- Connect as postgres superuser
psql -U postgres

-- Create database
CREATE DATABASE gtn_helpdesk;

-- Create dedicated user (recommended)
CREATE USER gtn_user WITH PASSWORD 'gtn_password_2024';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE gtn_helpdesk TO gtn_user;


-- Connect to new database
\c gtn_helpdesk

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO gtn_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gtn_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gtn_user;

-- Exit
\q
```

### Environment Configuration

Create `.env` file in project root:

```env
# Database Configuration
DATABASE_URL=postgresql://helpdesk_admin:secure_password_here@localhost:5432/gtn_helpdesk

# Flask Configuration
FLASK_APP=main.py
FLASK_ENV=development
SESSION_SECRET=your_very_long_random_secret_key_here

# Optional: Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@domain.com
SMTP_PASSWORD=your-app-password
```

### Install Python Dependencies

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Install all project dependencies
pip install -r requirements.txt
```

## Database Schema Creation

### Automatic Schema Creation

The application automatically creates all required tables on first run:

```bash
# Run the application
python main.py

# Tables are created automatically:
# - users
# - tickets  
# - ticket_comments
# - attachments
```

### Manual Schema Verification

```sql
-- Connect to database
psql -U helpdesk_admin -d gtn_helpdesk

-- List all tables
\dt

-- Check table structures
\d users
\d tickets
\d ticket_comments
\d attachments

-- Verify relationships
\d+ tickets
```

### Expected Database Schema

```sql
-- Users table (simplified two-tier roles)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(100),
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    ip_address VARCHAR(45),
    system_name VARCHAR(100),
    profile_image VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tickets table with assignment tracking
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Open',
    user_name VARCHAR(100) NOT NULL,
    user_ip_address VARCHAR(45),
    user_system_name VARCHAR(100),
    image_filename VARCHAR(255),
    user_id INTEGER REFERENCES users(id) NOT NULL,
    assigned_to INTEGER REFERENCES users(id),
    assigned_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);
```

## Performance Optimization

### PostgreSQL Configuration

Edit `postgresql.conf` for better performance:

```ini
# Memory Settings
shared_buffers = 256MB                    # 25% of available RAM
effective_cache_size = 1GB                # 75% of available RAM
work_mem = 8MB                            # Per connection memory
maintenance_work_mem = 64MB               # Maintenance operations

# Connection Settings
max_connections = 100                     # Concurrent connections
listen_addresses = 'localhost'           # Security restriction

# Performance Settings
random_page_cost = 1.1                   # SSD optimization
effective_io_concurrency = 200           # SSD optimization
checkpoint_completion_target = 0.9       # Checkpoint tuning
wal_buffers = 16MB                        # WAL buffer size

# Logging (for development)
log_statement = 'all'                    # Log all SQL statements
log_duration = on                        # Log query duration
log_min_duration_statement = 1000       # Log slow queries (1 second+)
```

### Application-Level Optimization

```python
# app.py - Connection pooling configuration
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,                     # Connection pool size
    'pool_recycle': 300,                 # Recycle connections every 5 minutes
    'pool_pre_ping': True,               # Verify connections before use
    'pool_timeout': 20,                  # Timeout for getting connection
    'max_overflow': 20                   # Additional connections beyond pool_size
}
```

## Backup and Maintenance

### Automated Backup Script

**Windows Batch File** (`backup_helpdesk.bat`):
```batch
@echo off
set PGPASSWORD=secure_password_here
set BACKUP_DIR=C:\Backups\GTN_Helpdesk
set DATE=%date:~-4,4%%date:~-10,2%%date:~-7,2%

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

"C:\Program Files\PostgreSQL\15\bin\pg_dump" -U helpdesk_admin -h localhost gtn_helpdesk > "%BACKUP_DIR%\gtn_helpdesk_%DATE%.sql"

echo Backup completed: %BACKUP_DIR%\gtn_helpdesk_%DATE%.sql
```

**Linux/macOS Shell Script** (`backup_helpdesk.sh`):
```bash
#!/bin/bash
export PGPASSWORD='secure_password_here'
BACKUP_DIR="/home/backups/gtn_helpdesk"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

pg_dump -U helpdesk_admin -h localhost gtn_helpdesk > "$BACKUP_DIR/gtn_helpdesk_$DATE.sql"

echo "Backup completed: $BACKUP_DIR/gtn_helpdesk_$DATE.sql"

# Keep only last 7 days of backups
find "$BACKUP_DIR" -name "gtn_helpdesk_*.sql" -mtime +7 -delete
```

### Regular Maintenance

**Weekly Maintenance Script**:
```sql
-- Connect to database
\c gtn_helpdesk

-- Vacuum and analyze all tables
VACUUM ANALYZE;

-- Check database size
SELECT pg_size_pretty(pg_database_size('gtn_helpdesk')) AS database_size;

-- Check table sizes and row counts
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes
FROM pg_tables 
JOIN pg_stat_user_tables USING (tablename)
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check for slow queries (requires log analysis)
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

## Monitoring and Troubleshooting

### Connection Testing

**Python Test Script** (`test_db_connection.py`):
```python
import os
import psycopg2
from urllib.parse import urlparse

def test_connection():
    try:
        # Get database URL from environment
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in environment variables")
            return False
            
        # Parse URL
        url = urlparse(database_url)
        
        # Test connection
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        
        # Test query
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()
        print(f"✅ PostgreSQL version: {version[0]}")
        
        # Test application tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cur.fetchall()
        print(f"✅ Found {len(tables)} tables: {[t[0] for t in tables]}")
        
        # Close connections
        cur.close()
        conn.close()
        print("✅ Database connection test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
```

### Common Issues and Solutions

**Issue: Connection Refused**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # macOS
sc query postgresql-x64-15  # Windows

# Start PostgreSQL if stopped
sudo systemctl start postgresql  # Linux
brew services start postgresql@15  # macOS
net start postgresql-x64-15  # Windows
```

**Issue: Authentication Failed**
```sql
-- Check user exists and has permissions
\du  -- List all users
\l   -- List all databases

-- Reset user password if needed
ALTER USER helpdesk_admin PASSWORD 'new_secure_password';
```

**Issue: Database Does Not Exist**
```sql
-- List databases
\l

-- Create database if missing
CREATE DATABASE gtn_helpdesk;
```

### Performance Monitoring

**Monitor Active Connections**:
```sql
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    query
FROM pg_stat_activity
WHERE state = 'active';
```

**Check Index Usage**:
```sql
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

## Production Deployment Checklist

### Security Configuration

1. **Database Security**:
   - [ ] Use strong passwords for all database users
   - [ ] Configure `pg_hba.conf` for proper authentication
   - [ ] Enable SSL connections in production
   - [ ] Regular security updates

2. **Network Security**:
   - [ ] Configure firewall rules (allow only necessary connections)
   - [ ] Use connection pooling (pgbouncer recommended)
   - [ ] Monitor connection attempts

3. **Application Security**:
   - [ ] Set strong `SESSION_SECRET` in environment variables
   - [ ] Enable CSRF protection
   - [ ] Use environment variables for sensitive configuration

### Performance Configuration

1. **Database Tuning**:
   - [ ] Optimize PostgreSQL configuration for available hardware
   - [ ] Set up proper indexing strategy
   - [ ] Configure connection pooling

2. **Application Tuning**:
   - [ ] Enable SQLAlchemy query optimization
   - [ ] Implement database connection pooling
   - [ ] Set up query monitoring

### Backup and Recovery

1. **Backup Strategy**:
   - [ ] Set up automated daily backups
   - [ ] Test backup restoration procedures
   - [ ] Configure off-site backup storage
   - [ ] Document recovery procedures

2. **Monitoring**:
   - [ ] Set up database performance monitoring
   - [ ] Configure alerting for critical issues
   - [ ] Regular maintenance scheduling

This comprehensive guide ensures proper PostgreSQL setup and integration with the GTN Engineering IT Helpdesk System for both development and production environments.
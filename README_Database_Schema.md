# Database Schema Documentation

Comprehensive documentation for the GTN Engineering IT Helpdesk System database structure, optimized for PostgreSQL with simplified two-tier role system.

## Overview

The system uses a modern relational database architecture with **12 core tables** supporting user management, ticket lifecycle, collaborative comments, file attachments, comprehensive master data management, and email notification logging. Designed for PostgreSQL primary deployment with IST timezone support and optimized for Replit environment.

**Database Tables:**
1. **users** - User authentication and profile management
2. **tickets** - Core ticket lifecycle management
3. **ticket_comments** - Collaborative comment system
4. **attachments** - File attachment management
5. **master_categories** - Ticket category definitions (NEW)
6. **master_priorities** - Priority level configuration (NEW)
7. **master_statuses** - Status workflow definitions (NEW)
8. **master_departments** - Department management with HOD assignments (NEW)
9. **email_settings** - SMTP configuration (NEW)
10. **timezone_settings** - System timezone configuration (NEW)
11. **backup_settings** - Database backup configuration (NEW)
12. **email_notification_logs** - Email notification tracking (NEW)

## Database Architecture

### **Core Design Principles**
- **Simplified Role Structure**: Two-tier system (User and Super Admin)
- **Audit Trail**: Complete tracking of ticket assignments and modifications
- **Performance Optimized**: Strategic indexing and connection pooling
- **Security First**: Foreign key constraints and data validation
- **Timezone Aware**: IST (Indian Standard Time) support throughout

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
## Database Tables


### 1. Users Table (`users`)

Central user management with authentication and profile data.

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
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    ip_address VARCHAR(45),
    system_name VARCHAR(100),
    profile_image VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Field Specifications:**
- `id`: Auto-incrementing primary key
- `username`: Unique login identifier (3-80 chars, alphanumeric)
- `email`: Unique email with validation
- `password_hash`: Werkzeug-secured password hash (256 chars)
- `first_name`, `last_name`: Required name fields (2-50 chars each)
- `department`: Optional organizational unit (max 100 chars)
- `role`: Simplified roles (`user` or `super_admin`)
- `specialization`: Support expertise (`Hardware` or `Software`)
- `ip_address`: IPv4/IPv6 tracking (45 chars for IPv6)
- `system_name`: Computer/device identifier
- `profile_image`: Optional image filename
- `created_at`: Account creation timestamp (UTC, converted to IST in display)

**Indexes & Constraints:**
```sql
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### 2. Tickets Table (`tickets`)

Complete ticket lifecycle management with assignment tracking.

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

**Field Specifications:**
- `id`: Auto-incrementing primary key
- `ticket_number`: Unique ticket identifier in GTN-000001 format (required)
- `title`: Brief issue summary (5-200 chars)
- `description`: Detailed problem description (min 10 chars)
- `category`: Issue type (`Hardware`, `Software`)
- `priority`: Urgency (`Low`, `Medium`, `High`, `Critical`)
- `status`: Current state (`Open`, `In Progress`, `Resolved`, `Closed`)
- `user_name`: Cached creator name for performance
- `user_ip_address`: IP when ticket created
- `user_system_name`: System name when created
- `image_filename`: Optional attachment (supports multiple formats)
- `user_id`: Ticket creator reference
- `assigned_to`: Current assignee (Super Admin only)
- `assigned_by`: Who made the assignment
- `created_at`: Initial creation (UTC)
- `updated_at`: Last modification (UTC)
- `resolved_at`: Resolution timestamp (UTC, null if open)

**Indexes & Constraints:**
```sql
CREATE UNIQUE INDEX idx_tickets_ticket_number ON tickets(ticket_number);
CREATE INDEX idx_tickets_user_id ON tickets(user_id);
CREATE INDEX idx_tickets_assigned_to ON tickets(assigned_to);
CREATE INDEX idx_tickets_assigned_by ON tickets(assigned_by);
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_category ON tickets(category);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_created_at ON tickets(created_at);
```

### 3. Ticket Comments Table (`ticket_comments`)

Collaborative communication and ticket updates.

```sql
CREATE TABLE ticket_comments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER REFERENCES tickets(id) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Field Specifications:**
- `id`: Auto-incrementing comment identifier
- `ticket_id`: Parent ticket reference
- `user_id`: Comment author reference
- `comment`: Comment content (min 5 chars)
- `created_at`: Comment timestamp (UTC)

**Indexes & Constraints:**
```sql
CREATE INDEX idx_comments_ticket_id ON ticket_comments(ticket_id);
CREATE INDEX idx_comments_user_id ON ticket_comments(user_id);
CREATE INDEX idx_comments_created_at ON ticket_comments(created_at);
```

### 4. Attachments Table (`attachments`)

File attachment management for tickets.

```sql
CREATE TABLE attachments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER REFERENCES tickets(id) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Field Specifications:**
- `id`: Auto-incrementing attachment identifier
- `ticket_id`: Parent ticket reference
- `filename`: Secure stored filename with timestamp prefix
- `uploaded_at`: Upload timestamp (UTC)

**Indexes & Constraints:**
```sql
CREATE INDEX idx_attachments_ticket_id ON attachments(ticket_id);
CREATE INDEX idx_attachments_uploaded_at ON attachments(uploaded_at);
```

**Supported File Types:**
- **Images**: JPG, JPEG, PNG, GIF
- **Documents**: PDF, DOC, DOCX
- **Spreadsheets**: XLS, XLSX
- **Security**: File type validation and secure filename generation

## Relationship Mapping

### **User Relationships**
```sql
-- Users can create multiple tickets
users(id) ←→ tickets(user_id) [1:Many]

-- Users can be assigned multiple tickets (Super Admin only)
users(id) ←→ tickets(assigned_to) [1:Many]

-- Users can assign multiple tickets (Super Admin only)
users(id) ←→ tickets(assigned_by) [1:Many]

-- Users can author multiple comments
users(id) ←→ ticket_comments(user_id) [1:Many]
```

### **Ticket Relationships**
```sql
-- Tickets can have multiple comments
tickets(id) ←→ ticket_comments(ticket_id) [1:Many]

-- Tickets can have multiple attachments
tickets(id) ←→ attachments(ticket_id) [1:Many]
```

## Master Data Tables

### 5. Master Data Categories (`master_categories`)

Configurable ticket categories for system administrators.

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

**Default Data:**
- Hardware: Hardware-related issues and requests
- Software: Software-related issues and applications

### 6. Master Data Priorities (`master_priorities`)

Configurable priority levels with color coding and escalation levels.

```sql
CREATE TABLE master_priorities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(200),
    level INTEGER NOT NULL,
    color_code VARCHAR(7),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Default Data:**
- Low (Level 1): #28a745 (Green)
- Medium (Level 2): #ffc107 (Yellow)
- High (Level 3): #fd7e14 (Orange)
- Critical (Level 4): #dc3545 (Red)

### 7. Master Data Statuses (`master_statuses`)

Configurable ticket status workflow with color coding.

```sql
CREATE TABLE master_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(200),
    color_code VARCHAR(7),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Default Data:**
- Open: #007bff (Blue) - Newly created tickets
- In Progress: #ffc107 (Yellow) - Active work tickets
- Resolved: #28a745 (Green) - Completed tickets
- Closed: #6c757d (Gray) - Finalized tickets

### 8. Master Data Departments (`master_departments`)

Department management with HOD assignments.

```sql
CREATE TABLE master_departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(10) UNIQUE NOT NULL,
    description VARCHAR(200),
    head_of_department_id INTEGER REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Default Data:**
- Engineering (ENG): Design and development
- Information Technology (IT): System administration and support
- Human Resources (HR): Employee management and recruitment
- Finance (FIN): Financial planning and accounting
- Operations (OPS): Daily operations and logistics
- Quality Assurance (QA): Testing and quality control

## System Configuration Tables

### 9. Email Settings (`email_settings`)

SMTP configuration for automated email notifications.

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

### 10. Timezone Settings (`timezone_settings`)

System-wide timezone configuration.

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

### 11. Backup Settings (`backup_settings`)

Database backup configuration and scheduling.

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

### 12. Email Notification Logs (`email_notification_logs`)
CREATE TABLE master_priorities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(200),
    level INTEGER NOT NULL,
    color_code VARCHAR(7),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Default Data:**
- Low (Level 1): #28a745 - Low priority issues, can be addressed within a week
- Medium (Level 2): #ffc107 - Medium priority issues, should be addressed within 2-3 days
- High (Level 3): #fd7e14 - High priority issues, should be addressed within 24 hours
- Critical (Level 4): #dc3545 - Critical priority issues, requires immediate attention

### 7. Master Data Statuses (`master_statuses`)

Configurable ticket statuses with color coding for workflow management.

```sql
CREATE TABLE master_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(200),
    color_code VARCHAR(7),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Default Data:**
- Open: #6c757d - Newly created ticket awaiting assignment
- In Progress: #007bff - Ticket is being actively worked on
- Resolved: #28a745 - Issue has been resolved and awaits user confirmation
- Closed: #343a40 - Ticket has been completed and closed

### 8. Email Settings (`email_settings`)

SMTP configuration for automated email notifications.

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

### 9. Timezone Settings (`timezone_settings`)

System-wide timezone configuration for consistent time display.

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

### 10. Backup Settings (`backup_settings`)

Database backup configuration and scheduling management.

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

### 11. Email Notification Log (`email_notification_logs`)

Tracking and logging of email notifications sent by the system.

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
```

**Field Specifications:**
- `id`: Auto-incrementing log entry identifier
- `to_email`: Recipient email address
- `subject`: Email subject line
- `message_type`: Type of notification (`ticket_created`, `ticket_assigned`, `ticket_updated`)
- `status`: Email delivery status (`sent`, `failed`)
- `error_message`: Error details for failed emails
- `ticket_id`: Reference to related ticket (optional)
- `user_id`: Reference to related user (optional)
- `created_at`: Log entry timestamp (UTC)

**Indexes & Constraints:**
```sql
CREATE INDEX idx_email_logs_status ON email_notification_logs(status);
CREATE INDEX idx_email_logs_ticket_id ON email_notification_logs(ticket_id);
CREATE INDEX idx_email_logs_user_id ON email_notification_logs(user_id);
CREATE INDEX idx_email_logs_created_at ON email_notification_logs(created_at);
```

## Data Validation & Constraints

### **Application-Level Validation**
```python
# User validation
- Username: 3-80 characters, alphanumeric
- Email: Valid email format
- Password: Minimum 6 characters
- Names: 2-50 characters each

# Ticket validation
- Title: 5-200 characters
- Description: Minimum 10 characters
- Category: Hardware | Software
- Priority: Low | Medium | High | Critical
- Status: Open | In Progress | Resolved | Closed

# Comment validation
- Comment: Minimum 5 characters
```

### **Database-Level Constraints**
```sql
-- Role validation
ALTER TABLE users ADD CONSTRAINT chk_role 
CHECK (role IN ('user', 'super_admin'));

-- Category validation
ALTER TABLE tickets ADD CONSTRAINT chk_category 
CHECK (category IN ('Hardware', 'Software'));

-- Priority validation
ALTER TABLE tickets ADD CONSTRAINT chk_priority 
CHECK (priority IN ('Low', 'Medium', 'High', 'Critical'));

-- Status validation
ALTER TABLE tickets ADD CONSTRAINT chk_status 
CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Closed'));
```

## Performance Optimization

### **Query Performance**
- **Connection Pooling**: PostgreSQL optimization
- **Prepared Statements**: SQLAlchemy ORM optimization
- **Strategic Indexing**: High-frequency query columns
- **Query Caching**: Application-level result caching

### **Database Tuning**
```sql
-- PostgreSQL specific optimizations
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
```

## Security Implementation

### **Access Control**
- **Session-based Authentication**: Secure session management
- **Role-based Authorization**: Two-tier permission system
- **CSRF Protection**: All forms protected
- **SQL Injection Prevention**: ORM-based queries only

### **Data Protection**
- Password hashing with Werkzeug security
- Input validation at form and model levels
- File upload security with type validation
- IP address logging for security monitoring

## Backup & Maintenance

### **Backup Strategy**
```bash
# Daily automated backups
pg_dump -h localhost -U postgres -d gtn_helpdesk | gzip > backup_$(date +%Y%m%d).sql.gz
```

### **Maintenance Tasks**
```sql
-- Weekly vacuum and analyze
VACUUM ANALYZE;

-- Monthly statistics update
ANALYZE;

-- Index maintenance
REINDEX DATABASE gtn_helpdesk;
```

## Migration Procedures

### **Schema Versioning**
- Use SQLAlchemy-migrate for version control
- Test all migrations in development environment
- Backup before any schema changes
- Document all modifications with timestamps

## Monitoring & Analytics

### **Performance Metrics**
- Query execution time monitoring
- Connection pool utilization
- Database size growth tracking
- Index usage statistics

### **Business Intelligence**
```sql
-- Ticket resolution time by category
SELECT 
    category,
    AVG(EXTRACT(EPOCH FROM (resolved_at - created_at))/3600) as avg_hours
FROM tickets 
WHERE resolved_at IS NOT NULL
GROUP BY category;

-- User activity report
SELECT 
    u.username,
    COUNT(t.id) as tickets_created,
    COUNT(ta.id) as tickets_assigned
FROM users u
LEFT JOIN tickets t ON u.id = t.user_id
LEFT JOIN tickets ta ON u.id = ta.assigned_to
GROUP BY u.id, u.username;
```

This database schema provides enterprise-grade reliability while maintaining simplicity for the two-tier role system. The design supports scalability, performance, and comprehensive audit trails for professional IT helpdesk operations.
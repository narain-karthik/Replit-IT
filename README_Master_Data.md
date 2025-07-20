# Master Data Management Guide

## Overview

The Master Data Management system provides Super Admins with centralized control over all reference data and system configurations in the GTN Engineering IT Helpdesk. This comprehensive guide covers Categories, Priorities, Statuses, Email Settings, Timezone Settings, and Backup Settings that drive the helpdesk operations.

## Accessing Master Data

1. **Login as Super Admin** - Only Super Admin accounts have access to Master Data
2. **Navigate to Master Data** - Click "Master Data" in the top navigation menu
3. **Dashboard Overview** - View summary statistics and quick access to all management areas

## Master Data Components

### 1. Categories Management 📁

**Purpose**: Define ticket categories to classify support requests

**Database Table**: `master_categories`
**Current Categories in Database**:
- Hardware (computer issues, equipment problems)
- Software (application issues, system software)

**Database Structure**:
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

**How to Manage**:
1. Click "Manage" button in Categories section
2. Use the left form to add new categories
3. Fill required fields:
   - **Category Name**: Short, descriptive name
   - **Description**: Detailed explanation of category scope
   - **Active Status**: Enable/disable category
4. View existing categories in the table
5. Edit categories using the edit button

**Best Practices**:
- Keep category names clear and concise
- Ensure categories don't overlap in scope
- Deactivate instead of deleting categories with existing tickets

---

### 2. Priority Levels Management 🚩

**Purpose**: Set ticket priority levels with visual indicators

**Database Table**: `master_priorities`
**Current Priority Levels in Database**:
1. **Low** (Level 1) - Non-urgent issues
2. **Medium** (Level 2) - Standard business issues  
3. **High** (Level 3) - Important business impact
4. **Critical** (Level 4) - System down, urgent

**Database Structure**:
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

**How to Manage**:
1. Click "Manage" button in Priority Levels section
2. Create new priorities with:
   - **Priority Name**: Clear identifier
   - **Level**: Numeric ranking (1-4)
   - **Color Code**: Hex color for visual distinction
   - **Description**: When to use this priority
   - **Active Status**: Enable/disable priority
3. Use color picker for consistent visual branding

**Color Recommendations**:
- **Low**: Green (#28a745)
- **Medium**: Blue (#007bff)  
- **High**: Orange (#fd7e14)
- **Critical**: Red (#dc3545)

---

### 3. Status Types Management 📊

**Purpose**: Track ticket progression through workflow stages

**Database Table**: `master_statuses`
**Current Status Types in Database**:
- **Open** - New tickets awaiting review
- **In Progress** - Tickets being actively worked
- **Resolved** - Issues fixed, awaiting confirmation
- **Closed** - Tickets completed and closed

### 4. Email Settings Management 📧

**Purpose**: Configure SMTP settings for automated email notifications

**Database Table**: `email_settings`
**Database Structure**:
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

### 5. Timezone Settings Management 🌍

**Purpose**: Configure system-wide timezone settings

**Database Table**: `timezone_settings`
**Default Setting**: Asia/Kolkata (IST)
**Database Structure**:
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

### 6. Backup Settings Management 💾

**Purpose**: Configure database backup scheduling and management

**Database Table**: `backup_settings`
**Database Structure**:
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

### 7. Email Notification Logs 📝

**Purpose**: Track all email notifications sent by the system

**Database Table**: `email_notification_logs`
**Database Structure**:
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
- **Closed** - Completed tickets

**How to Manage**:
1. Click "Manage" button in Ticket Statuses section
2. Define status types with:
   - **Status Name**: Clear workflow stage name
   - **Color Code**: Visual indicator color
   - **Description**: What this status means
   - **Active Status**: Enable/disable status
3. Maintain logical workflow progression

**Color Recommendations**:
- **Open**: Blue (#007bff)
- **In Progress**: Yellow (#ffc107)
- **Resolved**: Green (#28a745)
- **Closed**: Gray (#6c757d)

---

### 4. System Users Management 👥

**Purpose**: Manage all system users and their access levels

**User Roles**:
- **User**: Can create tickets, view own tickets, read-only profile access
- **Super Admin**: Full system access, can manage all data and users

**How to Manage**:
1. Click "Manage" button in System Users section (redirects to User Management)
2. View user overview in Master Data dashboard
3. Monitor user statistics and recent additions

**User Management Functions**:
- Create new user accounts
- Edit user profiles and roles
- Monitor user activity and tickets
- Deactivate user accounts
- View user activity and tickets

---

### 5. Email Settings Management 📧

**Purpose**: Configure SMTP settings for automated email notifications

**How to Manage**:
1. Click "Manage" button in Email Settings section
2. Configure SMTP settings:
   - **SMTP Server**: Email server address (e.g., smtp.gmail.com)
   - **SMTP Port**: Server port (usually 587 for TLS)
   - **SMTP Username**: Email account username
   - **SMTP Password**: Email account password/app password
   - **Use TLS**: Enable secure connection
   - **From Email**: Sender email address (optional)
   - **From Name**: Display name for emails
   - **Active Status**: Enable/disable email notifications

**Best Practices**:
- Use app passwords for Gmail accounts
- Test email settings after configuration
- Keep SMTP credentials secure

---

### 6. Timezone Settings Management 🌍

**Purpose**: Configure system-wide timezone for consistent time display

**How to Manage**:
1. Click "Manage" button in Timezone Settings section  
2. Set timezone configuration:
   - **Timezone**: Select system timezone (e.g., Asia/Kolkata)
   - **Display Name**: Human-readable timezone name
   - **UTC Offset**: Timezone offset from UTC
   - **Active Status**: Enable/disable timezone

**Default Settings**:
- Asia/Kolkata (Indian Standard Time - IST)
- UTC Offset: +05:30

---

### 7. Backup Settings Management 💾

**Purpose**: Configure automated database backup scheduling

**How to Manage**:
1. Click "Manage" button in Backup Settings section
2. Configure backup parameters:
   - **Backup Frequency**: Daily, Weekly, or Monthly
   - **Backup Time**: Scheduled backup time (24-hour format)
   - **Backup Location**: Storage path for backup files
   - **Max Backups**: Number of backups to retain
   - **Compression**: Enable/disable backup compression
   - **Include Attachments**: Include file attachments in backup
   - **Email Notifications**: Send backup status emails
   - **Notification Email**: Email for backup notifications
   - **Active Status**: Enable/disable backup system

**Default Settings**:
- Daily backups at 02:00 AM
- Retain 30 backup files
- Compression enabled
- Include attachments enabled

---

### 8. System Settings Management ⚙️

**Purpose**: Configure system-wide parameters and behaviors

**Setting Types**:
- **Text**: Simple text values
- **Number**: Numeric configurations
- **Boolean**: True/false settings
- **JSON**: Complex configuration objects

**How to Manage**:
1. Click "Manage Settings" button in System Settings section
2. Add new settings with:
   - **Setting Key**: Unique identifier (use underscore_format)
   - **Setting Type**: Data type for validation
   - **Setting Value**: The actual configuration value
   - **Description**: What this setting controls
   - **Active Status**: Enable/disable setting

**Common Settings Examples**:
```
max_file_size (Number): 10485760
email_notifications (Boolean): true
session_timeout (Number): 3600
maintenance_mode (Boolean): false
allowed_file_types (JSON): ["jpg","png","pdf","doc","docx"]
support_email (Text): support@gtnengineering.com
```

---

## Master Data Workflow

### Initial Setup Process

1. **Configure Departments** - Set up organizational structure
2. **Define Categories** - Establish ticket classification system
3. **Set Priority Levels** - Create urgency framework with colors
4. **Configure Status Types** - Define workflow stages with colors
5. **Create User Accounts** - Add team members with appropriate roles
6. **Configure System Settings** - Set operational parameters

### Ongoing Management

1. **Regular Review** - Monthly review of all master data for relevance
2. **User Feedback** - Collect input from team on category/priority effectiveness
3. **Analytics Review** - Use reports to identify unused or problematic data
4. **Documentation Updates** - Keep descriptions current and helpful
5. **Access Control** - Regular audit of user roles and permissions

---

## Best Practices

### Data Consistency
- Use consistent naming conventions across all master data
- Maintain clear descriptions for all entries
- Implement logical color schemes that are accessible
- Regular cleanup of inactive/unused data

### User Experience
- Keep categories and statuses intuitive for end users
- Use meaningful priority levels that reflect business needs
- Ensure department structure matches organizational reality
- Provide clear guidance in descriptions

### System Performance
- Avoid creating excessive categories or statuses
- Deactivate rather than delete referenced data
- Monitor system settings impact on performance
- Regular backup of master data configurations

### Security
- Limit Master Data access to trusted Super Admins
- Document all changes with reasons
- Regular review of user roles and permissions
- Audit trail for sensitive configuration changes

---

## Troubleshooting

### Common Issues

**Categories Not Appearing in Ticket Forms**
- Check if category is marked as Active
- Verify category name doesn't contain special characters
- Restart application if needed

**Priority Colors Not Displaying**
- Ensure valid hex color codes are used
- Check browser cache and refresh
- Verify color accessibility standards

**Users Cannot Access Features**
- Confirm user role assignments
- Check department associations
- Verify account active status

**System Settings Not Taking Effect**
- Confirm setting is marked as Active
- Check setting value format matches type
- Application restart may be required for some settings

### Getting Support

For technical issues with Master Data management:
1. Check system logs for error messages
2. Verify database connectivity
3. Contact system administrator
4. Document issue details for support

---

## Quick Reference

### Navigation Path
**Home → Login (Super Admin) → Master Data → Select Component**

### Key Actions
- **Add**: Use forms on management pages
- **Edit**: Click edit buttons in data tables  
- **Activate/Deactivate**: Toggle status in forms
- **View**: Browse data tables and overview cards

### Color Picker Usage
- Click color field to open picker
- Enter hex codes directly (#ffffff)
- Use color names for common colors
- Test accessibility with contrast checkers

---

*Last Updated: June 29, 2025*  
*GTN Engineering (India) Ltd - IT Team*
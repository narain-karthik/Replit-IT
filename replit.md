# GTN Engineering IT Helpdesk System

## Overview

The GTN Engineering IT Helpdesk System is a comprehensive Flask-based web application designed to manage IT support tickets within an organization. The system features role-based access control with three distinct user levels (Super Admin, Admin, and User), automatic system information capture, and a complete ticket lifecycle management system.

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: Multi-database support with automatic detection
  - PostgreSQL: Primary production database (default)
  - SQL Server: Enterprise production database with pyodbc connector
  - MySQL: Alternative production database with PyMySQL connector
- **Authentication**: Session-based authentication with role-based access control
- **Server**: Gunicorn WSGI server for production deployment

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **CSS Framework**: Bootstrap 5.3.0 for responsive design
- **Icons**: Remix Icons for consistent iconography
- **JavaScript**: Vanilla JavaScript for client-side interactions

### Application Structure
```
├── main.py              # Application entry point
├── app.py               # Flask app configuration and initialization
├── routes.py            # URL routing and view functions
├── models.py            # Database models (User, Ticket, TicketComment)
├── forms.py             # WTForms form definitions
├── templates/           # Jinja2 HTML templates
└── static/             # CSS, JavaScript, and static assets
```

## Key Components

### Database Models
1. **User Model**: Handles user authentication, profile information, and role management
2. **Ticket Model**: Manages support tickets with full lifecycle tracking
3. **TicketComment Model**: Enables comment system for ticket updates

### Role-Based Access Control
- **Super Admin**: Full system access, user management, ticket oversight
- **Admin**: Ticket management, assignment capabilities
- **User**: Ticket creation and personal ticket management

### Automatic System Detection
- IP address capture for user tracking
- System name detection for better support context
- Integration with ticket creation process

### Forms and Validation
- WTForms integration for secure form handling
- Comprehensive validation for all user inputs
- CSRF protection enabled

## Data Flow

1. **User Authentication**: Session-based login with role verification
2. **Ticket Creation**: Users submit tickets with automatic system info capture
3. **Ticket Assignment**: Admins can assign tickets based on category specialization
4. **Ticket Management**: Status updates, comments, and resolution tracking
5. **Reporting**: Excel export functionality for administrative oversight

## External Dependencies

### Python Packages
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-WTF (form handling)
- Flask-Login (authentication)
- Werkzeug (WSGI utilities)
- Gunicorn (production server)
- email-validator (email validation)
- openpyxl (Excel export functionality)

### Frontend Dependencies
- Bootstrap 5.3.0 (CSS framework)
- Remix Icons (icon library)

### Development Dependencies
- SQLite (development database)
- PostgreSQL packages (production ready)

## Deployment Strategy

### Development Environment
- SQLite database for local development
- Flask development server with debug mode
- Hot reload enabled for rapid development

### Production Environment
- Gunicorn WSGI server with autoscale deployment
- PostgreSQL database support configured
- ProxyFix middleware for proper header handling
- Environment-based configuration management

### Container Configuration
- Replit configuration with multiple modules (web, python-3.11, nodejs-20)
- Nixpkgs for system dependencies (openssl, postgresql)
- Port configuration for external access

## Changelog

- June 28, 2025: Cleaned up project by removing unwanted files (__pycache__ directories, obsolete login templates, test upload files) and added comprehensive .gitignore
- June 28, 2025: Enhanced Super Admin privileges to allow full control over all user accounts including other Super Admin accounts
- June 28, 2025: Removed frontend restrictions that previously prevented Super Admins from editing/deleting other Super Admin accounts
- June 28, 2025: Fixed user role editing bug where 'super_admin' role wasn't properly saved due to form choice mismatch
- June 28, 2025: Enhanced SMTP email notification system with proper environment variable configuration and error handling
- June 28, 2025: Successfully completed migration from Replit Agent to Replit environment with automatic PostgreSQL provisioning
- June 27, 2025: Successfully completed migration from Replit Agent to Replit environment with automatic PostgreSQL provisioning
- June 27, 2025: Enhanced ticket history display with new streamlined format showing Created By, Assigned By, Assigned To, and Status with colored badges
- June 27, 2025: Fixed edit ticket page template errors and property access issues for improved stability
- June 27, 2025: Updated all README documentation to reflect Replit integration and recent feature enhancements
- June 27, 2025: Added "Assigned By" tracking to monitor who assigns tickets to admins
- June 27, 2025: Super admins can now add comments directly when editing ticket status
- June 27, 2025: Enhanced Excel export to include "Assigned By" column for better tracking
- June 27, 2025: Added assignment history display in ticket details view
- June 27, 2025: Restricted ticket editing permissions for all users (admins and super admins)
- June 27, 2025: Admins can now only update ticket status - title, category, priority, and description are read-only after creation
- June 27, 2025: Enhanced attachment display with file type icons (PDF, Word, Excel, images) and clean filename presentation
- June 27, 2025: Added attachment indicators in all dashboard views to show which tickets have files
- June 27, 2025: Enhanced file upload system to support PDF, Word (.doc, .docx), and Excel (.xls, .xlsx) files in addition to images
- June 27, 2025: Fixed ticket creation errors and improved multiple file attachment handling
- June 27, 2025: Updated all README documentation to reflect new file attachment capabilities
- June 26, 2025: Successfully migrated from Replit Agent to Replit environment with PostgreSQL database
- June 26, 2025: Enhanced Super Admin user management with complete CRUD functionality:
  - Added "View User Details" feature showing user info, created tickets, and assigned tickets
  - Added "Edit User" functionality for updating user profile information
  - Added "Delete User" feature with data integrity protection and safety checks
- June 23, 2025: Cleaned up project by removing unwanted files (__pycache__, attached_assets) and added .gitignore
- June 23, 2025: Removed Network and Other categories from all pages (admin dashboard, super admin dashboard, reports dashboard)
- June 23, 2025: Fixed ticket creation 500 errors by creating uploads directory and improving file handling
- June 23, 2025: Fixed dashboard 500 errors by adding image_filename column to database
- June 23, 2025: Successfully migrated from Replit Agent to Replit environment with enhanced image upload functionality
- June 23, 2025: Added secure image upload system for tickets with admin-only viewing capabilities
- June 23, 2025: Updated ticket categories to Hardware and Software only (removed Network and Other)
- June 23, 2025: Enhanced database schema with image_filename field for ticket attachments
- June 23, 2025: Updated documentation in README.md and README_PostgreSQL_Setup.md
- June 22, 2025: Completed migration to Replit environment with PostgreSQL as primary database
- June 22, 2025: Enhanced system name detection to capture accurate client information per ticket
- June 22, 2025: Implemented modern UI/UX design with CSS custom properties and professional styling
- June 22, 2025: Created comprehensive PostgreSQL setup guide for Windows systems
- June 22, 2025: Added Microsoft SQL Server integration with comprehensive setup guide and connection testing
- June 22, 2025: Updated comprehensive README.md with complete setup instructions, user guides, and troubleshooting
- June 22, 2025: Added Reports Dashboard with visual analytics, assignment editing functionality, and MySQL support
- June 21, 2025: Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.
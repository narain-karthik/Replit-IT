from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    specialization = db.Column(db.String(50), nullable=True)  # Hardware, Software
    role = db.Column(db.String(50), nullable=False, default='user')  # user, super_admin
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4/IPv6
    system_name = db.Column(db.String(100), nullable=True)
    profile_image = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with tickets
    tickets = db.relationship('Ticket', backref='user', lazy=True, foreign_keys='Ticket.user_id')
    assigned_tickets = db.relationship('Ticket', backref='assignee', lazy=True, foreign_keys='Ticket.assigned_to')
    assignments_made = db.relationship('Ticket', backref='assigner', lazy=True, foreign_keys='Ticket.assigned_by')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_super_admin(self):
        return self.role == 'super_admin'
    

    
    def __repr__(self):
        return f'<User {self.username}>'

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), nullable=False, unique=True)  # GTN-000001 format
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Hardware, Software, Network, Other
    priority = db.Column(db.String(20), nullable=False)  # Low, Medium, High, Critical
    status = db.Column(db.String(20), nullable=False, default='Open')  # Open, In Progress, Resolved, Closed
    
    # User system information captured at ticket creation
    user_name = db.Column(db.String(100), nullable=False)  # Full name of user who created ticket
    user_ip_address = db.Column(db.String(45), nullable=True)  # IP address when ticket was created
    user_system_name = db.Column(db.String(100), nullable=True)  # System name when ticket was created
    
    # Image attachment
    image_filename = db.Column(db.String(255), nullable=True)  # Filename of uploaded image
    attachments = db.relationship('Attachment', backref='ticket', lazy=True)

   # assigned_at = db.Column(db.DateTime)  # Add this line if not present

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    # Relationship with comments
    comments = db.relationship('TicketComment', backref='ticket', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Ticket {self.ticket_number}: {self.title}>'

class TicketComment(db.Model):
    __tablename__ = 'ticket_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='comments')
    
    def __repr__(self):
        return f'<Comment {self.id} on Ticket {self.ticket_id}>'

class Attachment(db.Model):
    __tablename__ = 'attachments'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


# Master Data Models
class MasterDataCategory(db.Model):
    """Master data for ticket categories"""
    __tablename__ = 'master_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MasterDataPriority(db.Model):
    """Master data for ticket priorities"""
    __tablename__ = 'master_priorities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    level = db.Column(db.Integer, nullable=False)  # 1=Low, 2=Medium, 3=High, 4=Critical
    color_code = db.Column(db.String(7), nullable=True)  # Hex color for UI
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MasterDataStatus(db.Model):
    """Master data for ticket statuses"""
    __tablename__ = 'master_statuses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    color_code = db.Column(db.String(7), nullable=True)  # Hex color for UI
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)





class EmailSettings(db.Model):
    """Email SMTP settings for notifications"""
    __tablename__ = 'email_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    smtp_server = db.Column(db.String(100), nullable=False, default='smtp.gmail.com')
    smtp_port = db.Column(db.Integer, nullable=False, default=587)
    smtp_username = db.Column(db.String(100), nullable=False)
    smtp_password = db.Column(db.String(200), nullable=False)
    use_tls = db.Column(db.Boolean, default=True)
    from_email = db.Column(db.String(100), nullable=True)
    from_name = db.Column(db.String(100), nullable=True, default='GTN IT Helpdesk')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TimezoneSettings(db.Model):
    """Timezone settings for the application"""
    __tablename__ = 'timezone_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    timezone_name = db.Column(db.String(50), nullable=False, default='Asia/Kolkata')
    display_name = db.Column(db.String(100), nullable=False, default='Indian Standard Time (IST)')
    utc_offset = db.Column(db.String(10), nullable=False, default='+05:30')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BackupSettings(db.Model):
    """Database backup settings and configurations"""
    __tablename__ = 'backup_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    backup_frequency = db.Column(db.String(20), nullable=False, default='daily')  # daily, weekly, monthly
    backup_time = db.Column(db.Time, nullable=False, default=datetime.strptime('02:00', '%H:%M').time())
    backup_location = db.Column(db.String(200), nullable=True, default='/backups')
    max_backups = db.Column(db.Integer, nullable=False, default=30)
    compress_backups = db.Column(db.Boolean, default=True)
    include_attachments = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    notification_email = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EmailNotificationLog(db.Model):
    """Log of email notifications sent/failed"""
    __tablename__ = 'email_notification_logs'

    id = db.Column(db.Integer, primary_key=True)
    to_email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message_type = db.Column(db.String(50), nullable=False)  # 'ticket_created', 'ticket_assigned', 'ticket_updated'
    status = db.Column(db.String(20), nullable=False)  # 'sent', 'failed'
    error_message = db.Column(db.Text, nullable=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ticket = db.relationship('Ticket', backref='notification_logs')
    user = db.relationship('User', backref='notification_logs')


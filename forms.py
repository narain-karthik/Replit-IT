from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField, EmailField, PasswordField, BooleanField, IntegerField, TimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange
from datetime import time
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[], validators=[DataRequired()])
    system_name = StringField('System Name', render_kw={'placeholder': 'Enter your computer/system name'})
    image = FileField('Upload Files (Optional)', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx'], 'Images, PDF, Word, and Excel files only!')], render_kw={'multiple': True})
    submit = SubmitField('Create Ticket')
    
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        from models import MasterDataCategory, MasterDataPriority
        
        # Load categories from master data
        categories = MasterDataCategory.query.filter_by(is_active=True).all()
        self.category.choices = [(cat.name, cat.name) for cat in categories]
        
        # Load priorities from master data
        priorities = MasterDataPriority.query.filter_by(is_active=True).order_by(MasterDataPriority.level).all()
        self.priority.choices = [(pri.name, pri.name) for pri in priorities]

class UpdateTicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[], validators=[DataRequired()])
    status = SelectField('Status', choices=[], validators=[DataRequired()])
    submit = SubmitField('Update Ticket')
    
    def __init__(self, *args, **kwargs):
        super(UpdateTicketForm, self).__init__(*args, **kwargs)
        from models import MasterDataCategory, MasterDataPriority, MasterDataStatus
        
        # Load categories from master data
        categories = MasterDataCategory.query.filter_by(is_active=True).all()
        self.category.choices = [(cat.name, cat.name) for cat in categories]
        
        # Load priorities from master data
        priorities = MasterDataPriority.query.filter_by(is_active=True).order_by(MasterDataPriority.level).all()
        self.priority.choices = [(pri.name, pri.name) for pri in priorities]
        
        # Load statuses from master data
        statuses = MasterDataStatus.query.filter_by(is_active=True).all()
        self.status.choices = [(stat.name, stat.name) for stat in statuses]

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Add Comment')

class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    department = StringField('Department', validators=[Length(max=100)])
    specialization = SelectField('Specialization', choices=[
        ('', 'Select Specialization'),
        ('Hardware', 'Hardware Support'),
        ('Software', 'Software Support')
    ], validators=[Optional()])
    role = SelectField('Role', choices=[
        ('user', 'User'),
        ('hod', 'HOD (Head of Department)'),
        ('super_admin', 'Super Admin')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class UserProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    role = SelectField('Role', choices=[
        ('user', 'User'),
        ('hod', 'HOD (Head of Department)'),
        ('super_admin', 'Super Admin')
    ], validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    department = StringField('Department', validators=[Length(max=100)])
    specialization = SelectField('Specialization', choices=[
        ('', 'Select Specialization'),
        ('Hardware', 'Hardware Support'),
        ('Software', 'Software Support')
    ], validators=[Optional()])
    system_name = StringField('System Name', validators=[Length(max=100)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6, max=128)])
    submit = SubmitField('Update Profile')

class AssignTicketForm(FlaskForm):
    assigned_to = SelectField('Assign To', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Ticket')
    
    def __init__(self, *args, **kwargs):
        super(AssignTicketForm, self).__init__(*args, **kwargs)
        self.assigned_to.choices = [(user.id, user.full_name) for user in User.query.filter(User.role.in_(['super_admin'])).all()]


# Master Data Forms
class MasterDataCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[Length(max=200)])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Category')


class MasterDataPriorityForm(FlaskForm):
    name = StringField('Priority Name', validators=[DataRequired(), Length(min=2, max=20)])
    description = TextAreaField('Description', validators=[Length(max=200)])
    level = SelectField('Level', choices=[
        (1, '1 - Low'),
        (2, '2 - Medium'),
        (3, '3 - High'),
        (4, '4 - Critical')
    ], coerce=int, validators=[DataRequired()])
    color_code = StringField('Color Code', validators=[Length(max=7)], render_kw={'placeholder': '#007bff'})
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Priority')


class MasterDataStatusForm(FlaskForm):
    name = StringField('Status Name', validators=[DataRequired(), Length(min=2, max=20)])
    description = TextAreaField('Description', validators=[Length(max=200)])
    color_code = StringField('Color Code', validators=[Length(max=7)], render_kw={'placeholder': '#28a745'})
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Status')





class EmailSettingsForm(FlaskForm):
    smtp_server = StringField('SMTP Server', validators=[DataRequired(), Length(min=5, max=100)], 
                             render_kw={'placeholder': 'smtp.gmail.com'})
    smtp_port = IntegerField('SMTP Port', validators=[DataRequired()], default=587)
    smtp_username = StringField('SMTP Username/Email', validators=[DataRequired(), Email()],
                               render_kw={'placeholder': 'your-email@gmail.com'})
    smtp_password = PasswordField('SMTP Password', validators=[DataRequired()],
                                 render_kw={'placeholder': 'Your app password'})
    use_tls = BooleanField('Use TLS/STARTTLS', default=True)
    from_email = StringField('From Email (Optional)', validators=[Optional(), Email()],
                            render_kw={'placeholder': 'noreply@company.com'})
    from_name = StringField('From Name', validators=[Length(max=100)], default='GTN IT Helpdesk',
                           render_kw={'placeholder': 'GTN IT Helpdesk'})
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Email Settings')

class TimezoneSettingsForm(FlaskForm):
    timezone_name = SelectField('Timezone', choices=[
        ('Asia/Kolkata', 'Asia/Kolkata (IST)'),
        ('America/New_York', 'America/New_York (EST/EDT)'),
        ('America/Los_Angeles', 'America/Los_Angeles (PST/PDT)'),
        ('Europe/London', 'Europe/London (GMT/BST)'),
        ('Europe/Berlin', 'Europe/Berlin (CET/CEST)'),
        ('Asia/Dubai', 'Asia/Dubai (GST)'),
        ('Asia/Singapore', 'Asia/Singapore (SGT)'),
        ('Asia/Tokyo', 'Asia/Tokyo (JST)'),
        ('Australia/Sydney', 'Australia/Sydney (AEST/AEDT)'),
        ('UTC', 'UTC (Coordinated Universal Time)')
    ], validators=[DataRequired()])
    display_name = StringField('Display Name', validators=[DataRequired(), Length(min=5, max=100)],
                              render_kw={'placeholder': 'Indian Standard Time (IST)'})
    utc_offset = StringField('UTC Offset', validators=[DataRequired(), Length(min=3, max=10)],
                            render_kw={'placeholder': '+05:30'})
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Timezone Settings')

class BackupSettingsForm(FlaskForm):
    backup_frequency = SelectField('Backup Frequency', choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ], validators=[DataRequired()])
    backup_time = TimeField('Backup Time', validators=[DataRequired()], default=time(2, 0),
                           render_kw={'placeholder': '02:00'})
    backup_location = StringField('Backup Location', validators=[Length(max=200)], default='/backups',
                                 render_kw={'placeholder': '/backups'})
    max_backups = IntegerField('Maximum Backups to Keep', validators=[DataRequired(), NumberRange(min=1, max=365)], 
                              default=30)
    compress_backups = BooleanField('Compress Backups', default=True)
    include_attachments = BooleanField('Include File Attachments', default=True)
    email_notifications = BooleanField('Email Notifications', default=True)
    notification_email = StringField('Notification Email', validators=[Optional(), Email()],
                                    render_kw={'placeholder': 'admin@company.com'})
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Backup Settings')

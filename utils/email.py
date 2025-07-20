import smtplib
from email.mime.text import MIMEText
from flask import current_app
import logging


def get_email_settings():
    """Get email settings from Master Data"""
    try:
        from models import EmailSettings
        settings = EmailSettings.query.filter_by(is_active=True).first()
        
        if settings:
            return {
                'smtp_server': settings.smtp_server,
                'smtp_port': settings.smtp_port,
                'smtp_username': settings.smtp_username,
                'smtp_password': settings.smtp_password,
                'use_tls': settings.use_tls,
                'from_email': settings.from_email or settings.smtp_username,
                'from_name': settings.from_name or 'GTN IT Helpdesk'
            }
        else:
            logging.error("No active email settings found in Master Data. Please configure email settings in Master Data.")
            return None
    except Exception as e:
        logging.error(f"Error getting email settings: {e}")
        return None


def log_email_notification(to_email, subject, message_type, status, error_message=None, ticket_id=None, user_id=None):
    """Log email notification to database"""
    try:
        from flask import current_app
        with current_app.app_context():
            from models import EmailNotificationLog
            from app import db
            
            log_entry = EmailNotificationLog(
                to_email=to_email,
                subject=subject,
                message_type=message_type,
                status=status,
                error_message=error_message,
                ticket_id=ticket_id,
                user_id=user_id
            )
            db.session.add(log_entry)
            db.session.commit()
            logging.info(f"Email notification logged: {status} to {to_email}")
    except Exception as e:
        logging.error(f"Failed to log email notification: {e}")

def send_assignment_email(to_email, ticket_id, assignee_name):
    """Send ticket assignment email using Master Data email settings"""
    subject = f"You have been assigned Ticket #{ticket_id}"
    
    try:
        # Get email settings from Master Data
        email_settings = get_email_settings()
        
        logging.info(f"Attempting to send assignment email to {to_email} for ticket #{ticket_id}")
        logging.info(f"Using SMTP server: {email_settings['smtp_server']}:{email_settings['smtp_port']}")
        
        # Email content
        body = f"Hello {assignee_name},\n\nYou have been assigned to Ticket #{ticket_id}. Please check the portal for details.\n\nBest regards,\n{email_settings['from_name']}"

        # Create message with UTF-8 encoding
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = f"{email_settings['from_name']} <{email_settings['from_email']}>"
        msg['To'] = to_email

        # Send email with detailed logging
        with smtplib.SMTP(email_settings['smtp_server'], email_settings['smtp_port']) as server:
            logging.info("SMTP connection established")
            
            if email_settings['use_tls']:
                server.starttls()
                logging.info("TLS enabled")
                
            server.login(email_settings['smtp_username'], email_settings['smtp_password'])
            logging.info("SMTP authentication successful")
            
            server.sendmail(email_settings['from_email'], [to_email], msg.as_string())
            logging.info("Email sent successfully")
            
        # Log successful email (handle test case and extract numeric ID from ticket numbers)
        if ticket_id == "TEST":
            log_ticket_id = None
        elif isinstance(ticket_id, str) and ticket_id.startswith("GTN-"):
            # Extract numeric part from GTN-000001 format
            try:
                log_ticket_id = int(ticket_id.split("-")[1])
            except (IndexError, ValueError):
                log_ticket_id = None
        else:
            log_ticket_id = ticket_id
        log_email_notification(to_email, subject, 'ticket_assigned', 'sent', ticket_id=log_ticket_id)
        logging.info(f"Assignment email sent successfully to {to_email} for ticket #{ticket_id}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP Authentication failed: {e}. Check Gmail app password or enable 2-factor authentication"
        logging.error(error_msg)
        # Handle ticket ID conversion for error logging
        if ticket_id == "TEST":
            log_ticket_id = None
        elif isinstance(ticket_id, str) and ticket_id.startswith("GTN-"):
            try:
                log_ticket_id = int(ticket_id.split("-")[1])
            except (IndexError, ValueError):
                log_ticket_id = None
        else:
            log_ticket_id = ticket_id
        log_email_notification(to_email, subject, 'ticket_assigned', 'failed', error_msg, log_ticket_id)
        return False
    except smtplib.SMTPRecipientsRefused as e:
        error_msg = f"Recipient email rejected: {e}"
        logging.error(error_msg)
        # Handle ticket ID conversion for error logging
        if ticket_id == "TEST":
            log_ticket_id = None
        elif isinstance(ticket_id, str) and ticket_id.startswith("GTN-"):
            try:
                log_ticket_id = int(ticket_id.split("-")[1])
            except (IndexError, ValueError):
                log_ticket_id = None
        else:
            log_ticket_id = ticket_id
        log_email_notification(to_email, subject, 'ticket_assigned', 'failed', error_msg, log_ticket_id)
        return False
    except smtplib.SMTPServerDisconnected as e:
        error_msg = f"SMTP server disconnected: {e}"
        logging.error(error_msg)
        # Handle ticket ID conversion for error logging
        if ticket_id == "TEST":
            log_ticket_id = None
        elif isinstance(ticket_id, str) and ticket_id.startswith("GTN-"):
            try:
                log_ticket_id = int(ticket_id.split("-")[1])
            except (IndexError, ValueError):
                log_ticket_id = None
        else:
            log_ticket_id = ticket_id
        log_email_notification(to_email, subject, 'ticket_assigned', 'failed', error_msg, log_ticket_id)
        return False
    except Exception as e:
        error_msg = f"Failed to send assignment email: {e} (Type: {type(e).__name__})"
        logging.error(error_msg)
        # Handle ticket ID conversion for error logging
        if ticket_id == "TEST":
            log_ticket_id = None
        elif isinstance(ticket_id, str) and ticket_id.startswith("GTN-"):
            try:
                log_ticket_id = int(ticket_id.split("-")[1])
            except (IndexError, ValueError):
                log_ticket_id = None
        else:
            log_ticket_id = ticket_id
        log_email_notification(to_email, subject, 'ticket_assigned', 'failed', error_msg, log_ticket_id)
        return False


def send_notification_email(to_email, subject, body, ticket_id=None, message_type='general'):
    """Send general notification email using Master Data email settings"""
    try:
        # Get email settings from Master Data
        email_settings = get_email_settings()
        
        # Create message with UTF-8 encoding
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = f"{email_settings['from_name']} <{email_settings['from_email']}>"
        msg['To'] = to_email

        # Send email
        with smtplib.SMTP(email_settings['smtp_server'], email_settings['smtp_port']) as server:
            if email_settings['use_tls']:
                server.starttls()
            server.login(email_settings['smtp_username'], email_settings['smtp_password'])
            server.sendmail(email_settings['from_email'], [to_email], msg.as_string())
            
        # Log successful notification
        log_ticket_id = extract_ticket_id(ticket_id) if ticket_id else None
        log_email_notification(to_email, subject, message_type, 'sent', ticket_id=log_ticket_id)
        logging.info(f"Notification email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        error_msg = f"Failed to send notification email: {e}"
        logging.error(error_msg)
        log_ticket_id = extract_ticket_id(ticket_id) if ticket_id else None
        log_email_notification(to_email, subject, message_type, 'failed', error_msg, log_ticket_id)
        return False


def extract_ticket_id(ticket_id):
    """Extract numeric ticket ID from various formats"""
    if ticket_id == "TEST":
        return None
    elif isinstance(ticket_id, str) and ticket_id.startswith("GTN-"):
        try:
            return int(ticket_id.split("-")[1])
        except (IndexError, ValueError):
            return None
    else:
        return ticket_id


def send_ticket_creation_notification(ticket):
    """Send notification when a ticket is created"""
    try:
        # Email to user who created the ticket
        subject = f"Ticket Created: {ticket.ticket_number}"
        body = f"""Hello {ticket.user_name},

Your support ticket has been successfully created with the following details:

Ticket Number: {ticket.ticket_number}
Title: {ticket.title}
Category: {ticket.category}
Priority: {ticket.priority}
Status: {ticket.status}
Description: {ticket.description}

We will review your ticket and assign it to the appropriate team member shortly. 
You will receive email notifications for all updates to your ticket.

Best regards,
GTN IT Helpdesk Team"""
        
        result = send_notification_email(ticket.user.email, subject, body, ticket.ticket_number, 'ticket_created')
        return result
        
    except Exception as e:
        logging.error(f"Error sending ticket creation notification: {e}")
        return False


def send_ticket_assignment_notification(ticket, assignee, assigner):
    """Send notifications when a ticket is assigned"""
    try:
        results = []
        
        # 1. Email to the assignee
        subject = f"Ticket Assigned: {ticket.ticket_number}"
        body = f"""Hello {assignee.full_name},

You have been assigned to work on the following ticket:

Ticket Number: {ticket.ticket_number}
Title: {ticket.title}
Category: {ticket.category}
Priority: {ticket.priority}
Status: {ticket.status}
Assigned By: {assigner.full_name}
Created By: {ticket.user_name}

Description: {ticket.description}

Please review the ticket details and update the status as you work on it.

Best regards,
GTN IT Helpdesk Team"""
        
        result1 = send_notification_email(assignee.email, subject, body, ticket.ticket_number, 'ticket_assigned')
        results.append(result1)
        
        # 2. Email to the ticket creator
        subject = f"Ticket Update: {ticket.ticket_number} - Assigned"
        body = f"""Hello {ticket.user_name},

Your ticket has been assigned to a team member:

Ticket Number: {ticket.ticket_number}
Title: {ticket.title}
Status: {ticket.status}
Assigned To: {assignee.full_name}
Assigned By: {assigner.full_name}

Our team is now working on your request. You will receive updates as progress is made.

Best regards,
GTN IT Helpdesk Team"""
        
        result2 = send_notification_email(ticket.user.email, subject, body, ticket.ticket_number, 'ticket_updated')
        results.append(result2)
        
        return all(results)
        
    except Exception as e:
        logging.error(f"Error sending ticket assignment notifications: {e}")
        return False


def send_ticket_status_update_notification(ticket, old_status, updated_by):
    """Send notification when ticket status changes"""
    try:
        results = []
        
        # 1. Email to ticket creator
        subject = f"Ticket Update: {ticket.ticket_number} - Status Changed"
        body = f"""Hello {ticket.user_name},

Your ticket status has been updated:

Ticket Number: {ticket.ticket_number}
Title: {ticket.title}
Previous Status: {old_status}
Current Status: {ticket.status}
Updated By: {updated_by.full_name}

{"Your ticket has been resolved! Please review the solution and let us know if you need any further assistance." if ticket.status == 'Resolved' else "We are continuing to work on your request."}

Best regards,
GTN IT Helpdesk Team"""
        
        result1 = send_notification_email(ticket.user.email, subject, body, ticket.ticket_number, 'ticket_updated')
        results.append(result1)
        
        # 2. Email to assignee if different from updater
        if ticket.assigned_to and ticket.assigned_to != updated_by.id:
            subject = f"Ticket Update: {ticket.ticket_number} - Status Changed"
            body = f"""Hello {ticket.assignee.full_name},

A ticket assigned to you has been updated:

Ticket Number: {ticket.ticket_number}
Title: {ticket.title}
Previous Status: {old_status}
Current Status: {ticket.status}
Updated By: {updated_by.full_name}

Please review the ticket for any additional actions needed.

Best regards,
GTN IT Helpdesk Team"""
            
            result2 = send_notification_email(ticket.assignee.email, subject, body, ticket.ticket_number, 'ticket_updated')
            results.append(result2)
        
        return all(results)
        
    except Exception as e:
        logging.error(f"Error sending ticket status update notifications: {e}")
        return False


def send_ticket_comment_notification(ticket, comment, commenter):
    """Send notification when a comment is added to a ticket"""
    try:
        results = []
        
        # 1. Email to ticket creator (if not the commenter)
        if ticket.user_id != commenter.id:
            subject = f"Ticket Update: {ticket.ticket_number} - New Comment"
            body = f"""Hello {ticket.user_name},

A new comment has been added to your ticket:

Ticket Number: {ticket.ticket_number}
Title: {ticket.title}
Comment By: {commenter.full_name}
Comment: {comment}

You can view the full ticket details in the portal.

Best regards,
GTN IT Helpdesk Team"""
            
            result1 = send_notification_email(ticket.user.email, subject, body, ticket.ticket_number, 'ticket_comment')
            results.append(result1)
        
        # 2. Email to assignee (if different from commenter and ticket creator)
        if ticket.assigned_to and ticket.assigned_to != commenter.id and ticket.assigned_to != ticket.user_id:
            subject = f"Ticket Update: {ticket.ticket_number} - New Comment"
            body = f"""Hello {ticket.assignee.full_name},

A new comment has been added to a ticket assigned to you:

Ticket Number: {ticket.ticket_number}
Title: {ticket.title}
Comment By: {commenter.full_name}
Comment: {comment}

Please review the comment and respond if necessary.

Best regards,
GTN IT Helpdesk Team"""
            
            result2 = send_notification_email(ticket.assignee.email, subject, body, ticket.ticket_number, 'ticket_comment')
            results.append(result2)
        
        return all(results)
        
    except Exception as e:
        logging.error(f"Error sending ticket comment notifications: {e}")
        return False

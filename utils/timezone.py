from datetime import timedelta
from sqlalchemy import text

try:
    import pytz
    HAS_PYTZ = True
except ImportError:
    HAS_PYTZ = False

def get_timezone_settings():
    """Get timezone settings from database"""
    try:
        from app import db
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT timezone_name, utc_offset FROM timezone_settings WHERE is_active = true LIMIT 1"))
            row = result.fetchone()
            if row:
                return row[0], row[1]  # timezone_name, utc_offset
    except:
        pass
    # Default to IST if no settings found
    return 'Asia/Kolkata', '+05:30'

def utc_to_ist(dt):
    """Convert a UTC datetime to configured timezone (defaults to IST)."""
    if dt is None:
        return None
    
    try:
        timezone_name, utc_offset = get_timezone_settings()
        
        # If we have a timezone name, use pytz for proper conversion
        if timezone_name and HAS_PYTZ:
            try:
                utc_dt = dt.replace(tzinfo=pytz.UTC)
                target_tz = pytz.timezone(timezone_name)
                return utc_dt.astimezone(target_tz).replace(tzinfo=None)
            except:
                pass
        
        # Fallback to manual offset calculation
        if utc_offset.startswith('+'):
            hours, minutes = map(int, utc_offset[1:].split(':'))
            return dt + timedelta(hours=hours, minutes=minutes)
        elif utc_offset.startswith('-'):
            hours, minutes = map(int, utc_offset[1:].split(':'))
            return dt - timedelta(hours=hours, minutes=minutes)
    except:
        pass
    
    # Final fallback to IST
    return dt + timedelta(hours=5, minutes=30)

def format_datetime_for_timezone(dt):
    """Format datetime according to timezone settings"""
    if dt is None:
        return ''
    converted_dt = utc_to_ist(dt)
    if converted_dt is None:
        return ''
    return converted_dt.strftime('%Y-%m-%d %H:%M:%S')
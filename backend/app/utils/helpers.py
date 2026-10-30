# Get Current and Custom Datetime

from datetime import date, datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

def get_current_ist():
    return datetime.now(IST)

def get_ist_datetime(days_offset=0, hour=00, minute=00):
    return (get_current_ist() + timedelta(days=days_offset)).replace(hour=hour, minute=minute, second=00, microsecond=00)

# Format Date and Datatime

def format_date(date_value):
    if date_value is None:
        return "-"
    return date_value.strftime("%d-%m-%Y")

def format_datetime(datetime_value):
    if datetime_value is None:
        return "-"
    return datetime_value.strftime("%d-%m-%Y %H:%M:%S")

def format_display_date(date_value):
    if date_value is None:
        return "-"
    return date_value.strftime("%d %b %Y")

def format_display_date_range(start_date_value, end_date_value):
    if start_date_value is None or end_date_value is None:
        return "-"
    return f"{format_display_date(start_date_value)} - {format_display_date(end_date_value)}"

def format_display_datetime(datetime_value):
    if datetime_value is None:
        return "-"
    return f"{format_display_date(datetime_value.date())} {datetime_value.strftime('%I:%M %p').lstrip('0')}"

def format_display_datetime_range(start_datetime_value, end_datetime_value):
    if start_datetime_value is None or end_datetime_value is None:
        return "-"
    if start_datetime_value.date() == end_datetime_value.date():
        return f"{format_display_date(start_datetime_value.date())} {start_datetime_value.strftime('%I:%M %p').lstrip('0')} - {end_datetime_value.strftime('%I:%M %p').lstrip('0')}"
    return f"{format_display_date(start_datetime_value.date())} {start_datetime_value.strftime('%I:%M %p').lstrip('0')} - {format_display_date(end_datetime_value.date())} {end_datetime_value.strftime('%I:%M %p').lstrip('0')}"

# Hash and Verify Password

from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)

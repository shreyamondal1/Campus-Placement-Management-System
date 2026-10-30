import re
from app.utils.helpers import IST, get_current_ist, date, datetime
from app.utils.errors import ValidationError

def validate_string(value, field_name):
    if value is None or not isinstance(value, str) or value.strip() == "":
        raise ValidationError(f"{field_name} must be a non-empty string.")

def validate_number(value, field_name):
    if value is None or not isinstance(value, (int, float)):
        raise ValidationError(f"{field_name} must be a number.")

def validate_username(username):
    validate_string(username, "Username")
    if not 2 <= len(username) <= 50:
        raise ValidationError("Username must be between 2 and 50 characters.")
    if not re.fullmatch(r"[a-z][a-z0-9_-]*[a-z0-9]", username):
        raise ValidationError("Username may contain only lowercase letters, numbers, underscores and hyphens.")

def validate_email(email):
    validate_string(email, "Email")
    if not 8 <= len(email) <= 100:
        raise ValidationError("Email must be between 8 and 100 characters.")
    if " " in email:
        raise ValidationError("Email cannot contain spaces.")
    if not re.fullmatch(r"^[a-z][a-z0-9_-]*[a-z0-9]@[a-z][a-z_-]*[a-z]\.[a-z]{2,}$", email):
        raise ValidationError("Invalid email format.")
    prefix, suffix = email.split("@")
    domain = suffix.split(".")[0]
    if "__" in prefix or "--" in prefix or "_-" in prefix or "-_" in prefix:
        raise ValidationError("Invalid prefix.")
    if "__" in domain or "--" in domain or "_-" in domain or "-_" in domain:
        raise ValidationError("Invalid domain.")

def validate_password(password):
    validate_string(password, "Password")
    if not 6 <= len(password) <= 255:
        raise ValidationError("Password must be between 6 and 255 characters.")
    if not re.fullmatch(r"[A-Za-z0-9!@#$%._-]+", password):
        raise ValidationError("Password may contain only letters, numbers and the special characters !, @, #, $, %, ., _, -.")

def validate_name(name):
    validate_string(name, "Name")
    if not 2 <= len(name) <= 100:
        raise ValidationError("Name must be between 2 and 100 characters.")
    if not re.fullmatch(r"[A-Za-z .-]+", name):
        raise ValidationError("Name may contain only letters, spaces, periods and hyphens.")

def validate_contact_number(contact_number):
    validate_string(contact_number, "Contact Number")
    if not len(contact_number) == 10:
        raise ValidationError("Contact Number must be exactly 10 characters.")
    if not re.fullmatch(r"[0-9]+", contact_number):
        raise ValidationError("Contact Number may contain only numbers.")

def validate_cgpa(cgpa):
    validate_number(cgpa, "CGPA")
    if not 0.00 <= cgpa <= 10.00:
        raise ValidationError("CGPA must be between 0.00 and 10.00.")

def validate_salary_package(salary):
    validate_number(salary, "Salary")
    if not salary >= 0.00:
        raise ValidationError("Salary must be a non-negative value.")

def validate_url(url):
    validate_string(url, "URL")
    if not 10 <= len(url) <= 200:
        raise ValidationError("URL must be between 10 and 200 characters.")
    if " " in url:
        raise ValidationError("URL cannot contain spaces.")
    if not re.fullmatch(r"^https?://(www\.)?[a-z]([a-z0-9-]*[a-z0-9])?(\.[a-z]([a-z0-9-]*[a-z0-9])?)+(/[A-Za-z0-9._/-]*)?$", url):
        raise ValidationError("Invalid url format.")

def validate_year(year, minimum=2000, maximum=2100):
    validate_number(year, "Year")
    if not isinstance(year, int):
        raise ValidationError("Year must be an integer.")
    if not minimum <= year <= maximum:
        raise ValidationError(f"Year must be between {minimum} and {maximum}.")

def validate_future_date(date_value):
    if date_value < get_current_ist().date():
        raise ValidationError("Date cannot be in the past.")

def validate_future_datetime(datetime_value):
    if datetime_value < get_current_ist():
        raise ValidationError("Datetime cannot be in the past.")

def validate_dates(start_date, end_date):
    if start_date >= end_date:
        raise ValidationError("Start date must be before end date.")
    
def validate_datetimes(start_datetime, end_datetime):
    if start_datetime >= end_datetime:
        raise ValidationError("Start datetime must be before end datetime.")

def parse_date(date_value):
    if not date_value:
        raise ValidationError("Date is required.")
    try:
        return date.fromisoformat(date_value)
    except ValueError:
        raise ValidationError("Invalid date format.")

def parse_datetime(datetime_value):
    if not datetime_value:
        raise ValidationError("Datetime is required.")
    try:
        return datetime.fromisoformat(datetime_value).replace(tzinfo=IST)
    except ValueError:
        raise ValidationError("Invalid datetime format.")

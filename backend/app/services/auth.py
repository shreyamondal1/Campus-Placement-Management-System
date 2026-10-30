from app.database.models import db, User, Company, Student
from app.utils.errors import AuthenticationError, AuthorizationError, ConflictError
from app.utils.helpers import hash_password, verify_password
from app.utils.validators import validate_username, validate_email, validate_password
from app.integrations.processing.cache.dashboard import clear_dashboard_cache

def register_user(username, email, password, role):

    validate_username(username)
    validate_email(email)
    validate_password(password)

    if role not in ["Company", "Student"]:
        raise AuthorizationError("Registration not permitted.")

    if User.query.filter((User.username == username) | (User.email == email)).first():
        raise ConflictError("User already exists.")

    user = User(
        username=username,
        email=email,
        password=hash_password(password),
        role=role
    )

    db.session.add(user)
    db.session.flush()

    if role == "Company":
        profile = Company(
            user_id=user.id,
            name="",
            website="",
            hr_contact_name="",
            hr_contact_number=""
        )

    elif role == "Student":
        profile = Student(
            user_id=user.id,
            name="",
            contact_number="",
            degree="",
            department="",
            graduation_year=2000,
            cgpa=0.00,
            resume=""
        )

    db.session.add(profile)
    db.session.commit()
    clear_dashboard_cache(all_companies=True, all_students=True)

    return user

def login_user(username_or_email, password, role):

    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    if user is None:
        raise AuthenticationError("User does not exist.")

    if not verify_password(user.password, password):
        raise AuthenticationError("Invalid credentials.")
    
    if user.role != role:
        raise AuthorizationError("Access denied. Please navigate to the authorized login page.")

    if user.status == "Blacklisted":
        raise AuthorizationError("Account blacklisted. Please contact the administrator.")

    if user.status == "Disabled":
        raise AuthorizationError("Account disabled. Please contact the administrator.")
    
    if user.role == "Company":
        if user.company.approval_status == "Pending":
            raise AuthorizationError("Registration yet to be approved.")

        if user.company.approval_status == "Rejected":
            raise AuthorizationError("Registration not approved.")

    return user

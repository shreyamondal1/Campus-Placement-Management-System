from flask_sqlalchemy import SQLAlchemy
from app.utils.helpers import get_current_ist

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False) # Admin, Company, Student
    status = db.Column(db.String(20), default="Active") # Active, Blacklisted, Disabled
    created_at = db.Column(db.DateTime, default=get_current_ist)
    updated_at = db.Column(db.DateTime, default=get_current_ist, onupdate=get_current_ist)
    company = db.relationship('Company', backref='user', uselist=False, cascade="all")
    student = db.relationship('Student', backref='user', uselist=False, cascade="all")

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    industry = db.Column(db.String(100))
    type = db.Column(db.String(100)) # Product-Based, Service-Based, Consulting, Government, Startup, Non-Profit, Other
    website = db.Column(db.String(200), nullable=False)
    hr_contact_name = db.Column(db.String(100), nullable=False)
    hr_contact_number = db.Column(db.String(20), nullable=False)
    approval_status = db.Column(db.String(20), default="Pending") # Pending, Approved, Rejected
    drives = db.relationship('Drive', backref='company', cascade="all")

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Numeric(4, 2), nullable=False)
    skills = db.Column(db.Text)
    certifications = db.Column(db.Text)
    achievements = db.Column(db.Text)
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    portfolio = db.Column(db.String(200))
    resume = db.Column(db.String(200), nullable=False)
    applications = db.relationship('Application', backref='student', cascade="all")
    educations = db.relationship('Education', backref='student', cascade="all")
    experiences = db.relationship('Experience', backref='student', cascade="all")
    projects = db.relationship('Project', backref='student', cascade="all")

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="CASCADE"), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    coursework = db.Column(db.Text, nullable=False)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="CASCADE"), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    job_location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(20), nullable=False) # Permanent, Internship, Contract
    job_mode = db.Column(db.String(20), nullable=False) # Onsite, Remote, Hybrid
    salary_package = db.Column(db.Numeric(10, 2), nullable=False)
    eligibility_criteria = db.Column(db.Text)
    minimum_cgpa = db.Column(db.Numeric(4, 2))
    application_start = db.Column(db.DateTime, nullable=False)
    application_deadline = db.Column(db.DateTime, nullable=False)
    approval_status = db.Column(db.String(20), default="Pending") # Pending, Approved, Rejected
    created_at = db.Column(db.DateTime, default=get_current_ist)
    updated_at = db.Column(db.DateTime, default=get_current_ist, onupdate=get_current_ist)
    applications = db.relationship('Application', backref='drive', cascade="all")

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="CASCADE"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id', ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(20), default="Applied") # Applied, Shortlisted, Rejected
    created_at = db.Column(db.DateTime, default=get_current_ist)
    updated_at = db.Column(db.DateTime, default=get_current_ist, onupdate=get_current_ist)
    interview = db.relationship('Interview', backref='application', uselist=False, cascade="all")

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id', ondelete="CASCADE"), unique=True, nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    mode = db.Column(db.String(20), nullable=False) # Virtual, On-Campus, Off-Campus
    status = db.Column(db.String(20), default="Scheduled") # Scheduled, Selected, Not Selected
    created_at = db.Column(db.DateTime, default=get_current_ist)
    updated_at = db.Column(db.DateTime, default=get_current_ist, onupdate=get_current_ist)
    placement = db.relationship('Placement', backref='interview', uselist=False, cascade="all")

class Placement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id', ondelete="CASCADE"), unique=True, nullable=False)
    joining_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="Offered") # Offered, Accepted, Declined
    created_at = db.Column(db.DateTime, default=get_current_ist)
    updated_at = db.Column(db.DateTime, default=get_current_ist, onupdate=get_current_ist)

User.__table__.kwargs["sqlite_autoincrement"] = True
Company.__table__.kwargs["sqlite_autoincrement"] = True
Student.__table__.kwargs["sqlite_autoincrement"] = True
Drive.__table__.kwargs["sqlite_autoincrement"] = True
Education.__table__.kwargs["sqlite_autoincrement"] = True
Experience.__table__.kwargs["sqlite_autoincrement"] = True
Project.__table__.kwargs["sqlite_autoincrement"] = True
Application.__table__.kwargs["sqlite_autoincrement"] = True
Interview.__table__.kwargs["sqlite_autoincrement"] = True
Placement.__table__.kwargs["sqlite_autoincrement"] = True

Application.__table__.append_constraint(db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),)

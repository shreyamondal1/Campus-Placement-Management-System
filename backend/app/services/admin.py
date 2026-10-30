from app.database.models import db, User, Company, Student, Drive, Application, Interview, Placement
from app.utils.errors import NotFoundError, ConflictError
from app.utils.helpers import IST, get_current_ist, format_display_datetime, format_display_date_range, format_display_datetime_range, hash_password
from app.utils.validators import validate_username, validate_email, validate_password
from app.integrations.processing.cache.dashboard import clear_dashboard_cache
from app.integrations.processing.task.notification import get_admin_notification_cache, clear_admin_notification_cache
from pathlib import Path
from flask import send_from_directory
import re

def get_admin_dashboard():

    total_companies = Company.query.count()
    total_students = Student.query.count()
    total_drives = Drive.query.count()
    total_applications = Application.query.count()

    pending_companies = Company.query.filter(Company.approval_status == "Pending").count()
    approved_companies = Company.query.filter(Company.approval_status == "Approved").count()
    rejected_companies = Company.query.filter(Company.approval_status == "Rejected").count()

    pending_drives = Drive.query.filter(Drive.approval_status == "Pending").count()
    approved_drives = Drive.query.filter(Drive.approval_status == "Approved").count()
    rejected_drives = Drive.query.filter(Drive.approval_status == "Rejected").count()

    active_companies = Company.query.join(User).filter(User.status == "Active").count()
    disabled_companies = Company.query.join(User).filter(User.status == "Disabled").count()
    blacklisted_companies = Company.query.join(User).filter(User.status == "Blacklisted").count()

    active_students = Student.query.join(User).filter(User.status == "Active").count()
    disabled_students = Student.query.join(User).filter(User.status == "Disabled").count()
    blacklisted_students = Student.query.join(User).filter(User.status == "Blacklisted").count()

    salaries = sorted(float(drive.salary_package) for drive in Drive.query.join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active").all())
    average_salary = (round((sum(salaries) / len(salaries)) / 100000, 2) if salaries else 0)
    median_salary = (round((salaries[len(salaries) // 2] if len(salaries) % 2 else (salaries[(len(salaries) // 2) - 1] + salaries[len(salaries) // 2]) / 2) / 100000, 2) if salaries else 0)
    highest_salary = (round(max(salaries) / 100000, 2) if salaries else 0)

    applied_count = Application.query.count()
    shortlisted_count = Application.query.filter(Application.status == "Shortlisted").count()
    scheduled_count = Interview.query.count()
    selected_count = Interview.query.filter(Interview.status == "Selected").count()
    offered_count = Placement.query.count()
    accepted_count = Placement.query.filter(Placement.status == "Accepted").count()

    shortlist_rate = (round((shortlisted_count / applied_count) * 100, 2) if applied_count else 0)
    select_rate = (round((selected_count / scheduled_count) * 100, 2) if scheduled_count else 0)
    accept_rate = (round((accepted_count / offered_count) * 100, 2) if offered_count else 0)

    return {
        "platform": {
            "total_companies": total_companies,
            "total_students": total_students,
            "total_drives": total_drives,
            "total_applications": total_applications
        },
        "approval": {
            "companies": {
                "pending": pending_companies,
                "approved": approved_companies,
                "rejected": rejected_companies
            },
            "drives": {
                "pending": pending_drives,
                "approved": approved_drives,
                "rejected": rejected_drives
            }
        },
        "user": {
            "companies": {
                "active": active_companies,
                "disabled": disabled_companies,
                "blacklisted": blacklisted_companies
            },
            "students": {
                "active": active_students,
                "disabled": disabled_students,
                "blacklisted": blacklisted_students
            }
        },
        "placement": {
            "salary": {
                "average": average_salary,
                "median": median_salary,
                "highest": highest_salary
            },
            "rate": {
                "shortlist": shortlist_rate,
                "select": select_rate,
                "accept": accept_rate
            }
        }
    }

def get_all_companies():

    companies = Company.query.order_by(Company.name.asc()).all()

    return [
        {
            "id": company.id,
            "username": company.user.username,
            "email": company.user.email,
            "name": company.name,
            "website": company.website,
            "type": company.type,
            "industry": company.industry,
            "description": company.description,
            "user_status": company.user.status,
            "approval_status": company.approval_status
        }
        for company in companies
    ]

def get_all_students():

    students = Student.query.order_by(Student.name.asc()).all()

    return [
        {
            "id": student.id,
            "username": student.user.username,
            "email": student.user.email,
            "name": student.name,
            "degree": student.degree,
            "department": student.department,
            "graduation_year": student.graduation_year,
            "cgpa": student.cgpa,
            "linkedin": student.linkedin,
            "github": student.github,
            "portfolio": student.portfolio,
            "resume": student.resume,
            "user_status": student.user.status
        }
        for student in students
    ]

def get_company_drives(company_id):

    current_time = get_current_ist()

    company = Company.query.get(company_id)

    if not company:
        raise NotFoundError("Company not found.")

    drives = Drive.query.filter(Drive.company_id == company_id).order_by(Drive.job_title.asc()).all()

    return [
        {
            "id": drive.id,
            "job_title": drive.job_title,
            "job_location": drive.job_location,
            "job_type": drive.job_type,
            "job_mode": drive.job_mode,
            "salary_package": drive.salary_package,
            "minimum_cgpa": drive.minimum_cgpa,
            "drive_status": (
                "Upcoming" if current_time < drive.application_start.replace(tzinfo=IST)
                else "Ongoing" if current_time <= drive.application_deadline.replace(tzinfo=IST)
                else "Closed"
            ),
            "approval_status": drive.approval_status
        }
        for drive in drives
    ]

def get_drive_applications(company_id, drive_id):

    company = Company.query.get(company_id)

    if not company:
        raise NotFoundError("Company not found.")

    drive = Drive.query.filter(Drive.id == drive_id, Drive.company_id == company_id).first()

    if not drive:
        raise NotFoundError("Drive not found.")

    applications = Application.query.filter(Application.drive_id == drive_id).order_by(Application.id.asc()).all()

    return [
        {
            "id": application.id,
            "student_id": application.student.id,
            "student_name": application.student.name,
            "drive_id": application.drive.id,
            "job_title": application.drive.job_title,
            "company_id": application.drive.company.id,
            "company_name": application.drive.company.name,
            "application_status": application.status,
            "interview_status": application.interview.status if application.interview else "-",
            "placement_status": application.interview.placement.status if application.interview and application.interview.placement else "-"
        }
        for application in applications
    ]

def get_student_applications(student_id):

    student = Student.query.get(student_id)

    if not student:
        raise NotFoundError("Student not found.")

    applications = Application.query.filter(Application.student_id == student_id).order_by(Application.id.asc()).all()

    return [
        {
            "id": application.id,
            "student_id": application.student.id,
            "student_name": application.student.name,
            "drive_id": application.drive.id,
            "job_title": application.drive.job_title,
            "company_id": application.drive.company.id,
            "company_name": application.drive.company.name,
            "application_status": application.status,
            "interview_status": application.interview.status if application.interview else "-",
            "placement_status": application.interview.placement.status if application.interview and application.interview.placement else "-"
        }
        for application in applications
    ]

def get_application_details(application_id):

    current_time = get_current_ist()

    application = Application.query.get(application_id)

    if not application:
        raise NotFoundError("Application not found.")

    return {
        "company": {
            "id": application.drive.company.id,
            "name": application.drive.company.name,
            "email": application.drive.company.user.email,
            "hr_contact_name": application.drive.company.hr_contact_name,
            "hr_contact_number": application.drive.company.hr_contact_number,
            "website": application.drive.company.website,
            "type": application.drive.company.type,
            "industry": application.drive.company.industry,
            "description": application.drive.company.description,
            "user_status": application.drive.company.user.status,
            "approval_status": application.drive.company.approval_status
        },
        "student": {
            "id": application.student.id,
            "name": application.student.name,
            "email": application.student.user.email,
            "contact_number": application.student.contact_number,
            "degree": application.student.degree,
            "department": application.student.department,
            "graduation_year": application.student.graduation_year,
            "cgpa": application.student.cgpa,
            "linkedin": application.student.linkedin,
            "github": application.student.github,
            "portfolio": application.student.portfolio,
            "resume": application.student.resume,
            "skills": application.student.skills,
            "certifications": application.student.certifications,
            "achievements": application.student.achievements,
            "educations": [
                {
                    "id": education.id,
                    "degree": education.degree,
                    "institution": education.institution,
                    "duration": format_display_date_range(education.start_date, education.end_date),
                    "coursework": education.coursework
                }
                for education in application.student.educations
            ],
            "experiences": [
                {
                    "id": experience.id,
                    "role": experience.role,
                    "organization": experience.organization,
                    "tenure": format_display_date_range(experience.start_date, experience.end_date),
                    "description": experience.description
                }
                for experience in application.student.experiences
            ],
            "projects": [
                {
                    "id": project.id,
                    "name": project.name,
                    "link": project.link,
                    "description": project.description
                }
                for project in application.student.projects
            ],
            "user_status": application.student.user.status
        },
        "drive": {
            "id": application.drive.id,
            "job_title": application.drive.job_title,
            "job_description": application.drive.job_description,
            "job_location": application.drive.job_location,
            "job_type": application.drive.job_type,
            "job_mode": application.drive.job_mode,
            "salary_package": application.drive.salary_package,
            "eligibility_criteria": application.drive.eligibility_criteria,
            "minimum_cgpa": application.drive.minimum_cgpa,
            "drive_status": (
                "Upcoming" if current_time < application.drive.application_start.replace(tzinfo=IST)
                else "Ongoing" if current_time <= application.drive.application_deadline.replace(tzinfo=IST)
                else "Closed"
            ),
            "approval_status": application.drive.approval_status
        },
        "application": {
            "id": application.id,
            "application_status": application.status,
            "interview_status": application.interview.status if application.interview else "-",
            "placement_status": application.interview.placement.status if application.interview and application.interview.placement else "-",
            "interview_mode": application.interview.mode if application.interview else "-",
            "interview_datetime": format_display_datetime_range(application.interview.start_datetime, application.interview.end_datetime) if application.interview else "-",
            "joining_datetime": format_display_datetime(application.interview.placement.joining_datetime) if application.interview and application.interview.placement else "-"
        }
    }

def approve_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        raise NotFoundError("Company not found.")

    if company.approval_status == "Pending":
        company.approval_status = "Approved"

    db.session.commit()
    clear_dashboard_cache(company_id=company_id, all_students=True)

    return {"message": "Company approved successfully."}

def reject_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        raise NotFoundError("Company not found.")

    if company.approval_status == "Pending":
        company.approval_status = "Rejected"

    db.session.commit()
    clear_dashboard_cache(company_id=company_id, all_students=True)

    return {"message": "Company rejected successfully."}

def reapprove_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        raise NotFoundError("Company not found.")

    if company.approval_status == "Rejected":
        company.approval_status = "Approved"

    db.session.commit()
    clear_dashboard_cache(company_id=company_id, all_students=True)

    return {"message": "Company reapproved successfully."}

def disable_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        raise NotFoundError("Company not found.")

    if company.user.status == "Active":
        company.user.status = "Disabled"

    db.session.commit()
    clear_dashboard_cache(company_id=company_id, all_students=True)

    return {"message": "Company disabled successfully."}

def enable_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        raise NotFoundError("Company not found.")

    if company.user.status == "Disabled":
        company.user.status = "Active"

    db.session.commit()
    clear_dashboard_cache(company_id=company_id, all_students=True)

    return {"message": "Company enabled successfully."}

def blacklist_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        raise NotFoundError("Company not found.")

    if company.user.status == "Active":
        company.user.status = "Blacklisted"

    db.session.commit()
    clear_dashboard_cache(company_id=company_id, all_students=True)

    return {"message": "Company blacklisted successfully."}

def whitelist_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        raise NotFoundError("Company not found.")

    if company.user.status == "Blacklisted":
        company.user.status = "Active"

    db.session.commit()
    clear_dashboard_cache(company_id=company_id, all_students=True)

    return {"message": "Company whitelisted successfully."}

def delete_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        raise NotFoundError("Company not found.")

    db.session.delete(company.user)
    db.session.commit()
    clear_dashboard_cache(company_id=company_id, all_students=True)

    return {"message": "Company deleted successfully."}

def disable_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        raise NotFoundError("Student not found.")

    if student.user.status == "Active":
        student.user.status = "Disabled"

    db.session.commit()
    clear_dashboard_cache(student_id=student_id, all_companies=True)

    return {"message": "Student disabled successfully."}

def enable_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        raise NotFoundError("Student not found.")

    if student.user.status == "Disabled":
        student.user.status = "Active"

    db.session.commit()
    clear_dashboard_cache(student_id=student_id, all_companies=True)

    return {"message": "Student enabled successfully."}

def blacklist_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        raise NotFoundError("Student not found.")

    if student.user.status == "Active":
        student.user.status = "Blacklisted"

    db.session.commit()
    clear_dashboard_cache(student_id=student_id, all_companies=True)

    return {"message": "Student blacklisted successfully."}

def whitelist_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        raise NotFoundError("Student not found.")

    if student.user.status == "Blacklisted":
        student.user.status = "Active"

    db.session.commit()
    clear_dashboard_cache(student_id=student_id, all_companies=True)

    return {"message": "Student whitelisted successfully."}

def delete_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        raise NotFoundError("Student not found.")

    db.session.delete(student.user)
    db.session.commit()
    clear_dashboard_cache(student_id=student_id, all_companies=True)

    return {"message": "Student deleted successfully."}

def approve_drive(drive_id):

    drive = Drive.query.get(drive_id)

    if not drive:
        raise NotFoundError("Drive not found.")

    if drive.approval_status == "Pending":
        drive.approval_status = "Approved"

    db.session.commit()
    clear_dashboard_cache(company_id=drive.company_id, all_students=True)

    return {"message": "Drive approved successfully."}

def reject_drive(drive_id):

    drive = Drive.query.get(drive_id)

    if not drive:
        raise NotFoundError("Drive not found.")

    if drive.approval_status == "Pending":
        drive.approval_status = "Rejected"

    db.session.commit()
    clear_dashboard_cache(company_id=drive.company_id, all_students=True)

    return {"message": "Drive rejected successfully."}

def reapprove_drive(drive_id):

    drive = Drive.query.get(drive_id)

    if not drive:
        raise NotFoundError("Drive not found.")

    if drive.approval_status == "Rejected":
        drive.approval_status = "Approved"

    db.session.commit()
    clear_dashboard_cache(company_id=drive.company_id, all_students=True)

    return {"message": "Drive reapproved successfully."}

def get_admin_profile(user):

    return {
        "username": user.username,
        "email": user.email
    }

def update_admin_profile(user, data):

    validate_username(data["username"])
    validate_email(data["email"])
    validate_password(data["password"])

    if data["username"] != user.username:
        existing_user = User.query.filter(User.username == data["username"], User.id != user.id).first()
        if existing_user:
            raise ConflictError("Username already exists.")

    if data["email"] != user.email:
        existing_user = User.query.filter(User.email == data["email"], User.id != user.id).first()
        if existing_user:
            raise ConflictError("Email already exists.")

    user.username = data["username"]
    user.email = data["email"]
    user.password = hash_password(data["password"])

    db.session.commit()
    clear_dashboard_cache(all_companies=True, all_students=True)

    return get_admin_profile(user)

def start_admin_manual_export(user):

    from app.integrations.processing.task.celery import manual_admin_export

    manual_admin_export(user.id)

    return {"message": "Export generation started. You will be notified when it is ready."}

def get_admin_notification_summary():

    notifications = []

    NOTIFICATION_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "archived" / "notifications")

    for file in sorted(NOTIFICATION_DIRECTORY.glob("*_admin_*.html"), reverse=True):

        html = file.read_text(encoding="utf-8")

        notifications.append({
            "notification_filename": file.name,
            "notification_type": "_".join(file.stem.split("_")[3:]),
            "notification_subject": re.search(r"<title>(.*?)</title>", html).group(1),
            "notification_sent": re.search(r"<b>Sent:</b></td>\s*<td>(.*?)</td>", html).group(1),
            "attachment_exists": re.search(r"<b>Attachment:</b>", html) is not None
        })

    return notifications

def get_admin_notification_detail(notification_filename):

    NOTIFICATION_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "archived" / "notifications")

    notification_file = NOTIFICATION_DIRECTORY / notification_filename

    if not notification_file.exists():
        raise NotFoundError("Notification not found.")

    html = notification_file.read_text(encoding="utf-8")

    match = re.search(r"<b>Attachment:</b></td>\s*<td>(.*?)</td>", html)

    return {
        "notification_body": html,
        "attachment_filename": match.group(1) if match else ""
    }

def download_admin_notification_attachment(notification_filename, attachment_filename):

    NOTIFICATION_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "archived" / "notifications")
    
    notification_file = NOTIFICATION_DIRECTORY / notification_filename

    if not notification_file.exists():
        raise NotFoundError("Notification not found.")

    html = notification_file.read_text(encoding="utf-8")

    match = re.search(r"<b>Attachment:</b></td>\s*<td>(.*?)</td>", html)

    if match is None:
        raise NotFoundError("Attachment does not exist.")

    if match.group(1) != attachment_filename:
        raise NotFoundError("Invalid attachment.")

    notification_type = "_".join(notification_filename.split("_")[3:]).replace(".html", "")

    if notification_type == "manual_export":
        ATTACHMENT_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "generated" / "exports")

    elif notification_type == "monthly_report":
        ATTACHMENT_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "generated" / "reports")

    elif notification_type == "weekly_report":
        ATTACHMENT_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "generated" / "reports")

    else:
        raise NotFoundError("This notification has no downloadable attachment.")

    attachment_file = ATTACHMENT_DIRECTORY / attachment_filename

    if not attachment_file.exists():
        raise NotFoundError("Attachment not found.")

    return send_from_directory(ATTACHMENT_DIRECTORY, attachment_filename, as_attachment=True)

def get_admin_notification_status():

    status = get_admin_notification_cache()

    if status is None:
        
        return {
            "task_completed": False,
            "message": ""
        }

    clear_admin_notification_cache()

    return status

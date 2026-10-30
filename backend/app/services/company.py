from app.database.models import db, User, Student, Drive, Application, Interview, Placement
from app.utils.errors import NotFoundError, ValidationError, ConflictError
from app.utils.helpers import IST, get_current_ist, format_display_datetime, format_display_date_range, format_display_datetime_range, hash_password
from app.utils.validators import validate_username, validate_email, validate_password, validate_name, validate_contact_number, validate_url, validate_salary_package, validate_cgpa, parse_datetime, validate_future_datetime, validate_datetimes
from app.integrations.processing.cache.dashboard import clear_dashboard_cache
from app.integrations.processing.task.notification import get_company_notification_cache, clear_company_notification_cache
from pathlib import Path
from flask import send_from_directory
import re

def get_company_dashboard(company):

    total_drives = Drive.query.filter(Drive.company_id == company.id).count()
    total_applications = Application.query.join(Drive).join(Student).join(User).filter(Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active").count()

    pending_drives = Drive.query.filter(Drive.company_id == company.id, Drive.approval_status == "Pending").count()
    approved_drives = Drive.query.filter(Drive.company_id == company.id, Drive.approval_status == "Approved").count()
    rejected_drives = Drive.query.filter(Drive.company_id == company.id, Drive.approval_status == "Rejected").count()

    applied_count = Application.query.join(Drive).join(Student).join(User).filter(Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active").count()
    shortlisted_count = Application.query.join(Drive).join(Student).join(User).filter(Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active", Application.status == "Shortlisted").count()
    scheduled_count = Interview.query.join(Application).join(Drive).join(Student).join(User).filter(Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active").count()
    selected_count = Interview.query.join(Application).join(Drive).join(Student).join(User).filter(Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active", Interview.status == "Selected").count()
    offered_count = Placement.query.join(Interview).join(Application).join(Drive).join(Student).join(User).filter(Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active").count()
    accepted_count = Placement.query.join(Interview).join(Application).join(Drive).join(Student).join(User).filter(Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active", Placement.status == "Accepted").count()

    shortlist_rate = round((shortlisted_count / applied_count) * 100, 2) if applied_count else 0
    select_rate = round((selected_count / scheduled_count) * 100, 2) if scheduled_count else 0
    accept_rate = round((accepted_count / offered_count) * 100, 2) if offered_count else 0

    return {
        "platform": {
            "total_drives": total_drives,
            "total_applications": total_applications
        },
        "drive_approval": {
            "pending": pending_drives,
            "approved": approved_drives,
            "rejected": rejected_drives
        },
        "placement": {
            "count": {
                "shortlist": shortlisted_count,
                "select": selected_count,
                "accept": accepted_count
            },
            "rate": {
                "shortlist": shortlist_rate,
                "select": select_rate,
                "accept": accept_rate
            }
        }
    }

def get_drives(company):

    current_time = get_current_ist()

    drives = Drive.query.filter(Drive.company_id == company.id).order_by(Drive.job_title.asc()).all()

    return [
        {
            "id": drive.id,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "job_location": drive.job_location,
            "job_type": drive.job_type,
            "job_mode": drive.job_mode,
            "salary_package": drive.salary_package,
            "eligibility_criteria": drive.eligibility_criteria,
            "minimum_cgpa": drive.minimum_cgpa,
            "application_start": drive.application_start,
            "application_deadline": drive.application_deadline,
            "drive_status": (
                "Upcoming" if current_time < drive.application_start.replace(tzinfo=IST)
                else "Ongoing" if current_time <= drive.application_deadline.replace(tzinfo=IST)
                else "Closed"
            ),
            "approval_status": drive.approval_status
        }
        for drive in drives
    ]

def get_drive_applications(company, drive_id):

    drive = Drive.query.filter(Drive.id == drive_id, Drive.company_id == company.id).first()

    if not drive:
        raise NotFoundError("Drive not found.")

    applications = Application.query.join(Drive).join(Student).join(User).filter(Application.drive_id == drive_id, Drive.approval_status == "Approved", User.status == "Active").order_by(Application.id.asc()).all()

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
            "placement_status": application.interview.placement.status if application.interview and application.interview.placement else "-",
            "interview_mode": application.interview.mode if application.interview else "-",
            "interview_start_datetime": application.interview.start_datetime if application.interview else None,
            "interview_end_datetime": application.interview.end_datetime if application.interview else None,
            "joining_datetime": application.interview.placement.joining_datetime if application.interview and application.interview.placement else None,
            "interview_exists": application.interview is not None,
            "placement_exists": application.interview is not None and application.interview.placement is not None
        }
        for application in applications
    ]

def get_application_details(company, drive_id, application_id):

    current_time = get_current_ist()

    application = Application.query.join(Drive).join(Student).join(User).filter(Application.id == application_id, Application.drive_id == drive_id, Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active").first()

    if not application:
        raise NotFoundError("Application not found.")

    return {
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

def create_drive(company, data):

    application_start = parse_datetime(data["application_start"])
    application_deadline = parse_datetime(data["application_deadline"])

    validate_salary_package(data["salary_package"])
    if data.get("minimum_cgpa") is not None:
        validate_cgpa(data["minimum_cgpa"])

    validate_future_datetime(application_start)
    validate_future_datetime(application_deadline)
    validate_datetimes(application_start, application_deadline)

    drive = Drive(
        company_id=company.id,
        job_title=data["job_title"],
        job_description=data["job_description"],
        job_location=data["job_location"],
        job_type=data["job_type"],
        job_mode=data["job_mode"],
        salary_package=data["salary_package"],
        eligibility_criteria=data.get("eligibility_criteria"),
        minimum_cgpa=data.get("minimum_cgpa"),
        application_start=application_start,
        application_deadline=application_deadline
    )

    db.session.add(drive)
    db.session.commit()
    clear_dashboard_cache(company_id=company.id, all_students=True)

    return {"message": "Drive created successfully."}

def update_drive(company, drive_id, data):

    drive = Drive.query.filter(Drive.company_id == company.id, Drive.id == drive_id).first()

    if not drive:
        raise NotFoundError("Drive not found.")

    validate_salary_package(data["salary_package"])
    if data.get("minimum_cgpa") is not None:
        validate_cgpa(data["minimum_cgpa"])

    application_start = parse_datetime(data["application_start"])
    application_deadline = parse_datetime(data["application_deadline"])

    validate_future_datetime(application_start)
    validate_future_datetime(application_deadline)
    validate_datetimes(application_start, application_deadline)

    drive.job_title = data["job_title"]
    drive.job_description = data["job_description"]
    drive.job_location = data["job_location"]
    drive.job_type = data["job_type"]
    drive.job_mode = data["job_mode"]
    drive.salary_package = data["salary_package"]
    drive.eligibility_criteria = data.get("eligibility_criteria")
    drive.minimum_cgpa = data.get("minimum_cgpa")
    drive.application_start = application_start
    drive.application_deadline = application_deadline

    db.session.commit()
    clear_dashboard_cache(company_id=company.id, all_students=True)

    return {"message": "Drive updated successfully."}

def delete_drive(company, drive_id):

    drive = Drive.query.filter(Drive.company_id == company.id, Drive.id == drive_id).first()

    if not drive:
        raise NotFoundError("Drive not found.")

    db.session.delete(drive)
    db.session.commit()
    clear_dashboard_cache(company_id=company.id, all_students=True)

    return {"message": "Drive deleted successfully."}

def update_application_record(application, data, interview_start_datetime, interview_end_datetime):

    current_status = application.status
    new_status = data["application_status"]

    if current_status == "Applied":

        if new_status == "Applied":

            return
        
        if new_status == "Rejected":

            application.status = "Rejected"

            return
        
        if new_status == "Shortlisted":

            if not all([data.get("interview_mode"), interview_start_datetime, interview_end_datetime]):
                raise ValidationError("Interview details are required when shortlisting an application.")

            application.status = "Shortlisted"

            interview = Interview(
                application_id=application.id,
                start_datetime=interview_start_datetime,
                end_datetime=interview_end_datetime,
                mode=data["interview_mode"]
            )

            db.session.add(interview)

            return

    if current_status in ["Shortlisted", "Rejected"]:

        if new_status != current_status:
            raise ValidationError(f"Cannot change application status from '{current_status}' to '{new_status}'.")
        
        return

    raise ValidationError(f"Cannot change application status from '{current_status}' to '{new_status}'.")

def update_interview_record(application, data, interview_start_datetime, interview_end_datetime, joining_datetime):

    if not application.interview:
        return

    interview = application.interview

    current_status = interview.status
    new_status = data.get("interview_status", current_status)

    if current_status == "Scheduled":

        if interview_start_datetime:
            interview.start_datetime = interview_start_datetime

        if interview_end_datetime:
            interview.end_datetime = interview_end_datetime

        if data.get("interview_mode"):
            interview.mode = data["interview_mode"]

        if new_status == "Scheduled":
        
            return

        if new_status == "Not Selected":

            interview.status = "Not Selected"
        
            return

        if new_status == "Selected":

            if not joining_datetime:
                raise ValidationError("Joining date is required when selecting a candidate.")

            interview.status = "Selected"

            placement = Placement(
                interview_id=interview.id,
                joining_datetime=joining_datetime
            )

            db.session.add(placement)

            return

    if current_status in ["Selected", "Not Selected"]:
            
            if new_status != current_status:
                raise ValidationError(f"Cannot change interview status from '{current_status}' to '{new_status}'.")
            
            return

    raise ValidationError(f"Cannot change interview status from '{current_status}' to '{new_status}'.")

def update_placement_record(application, data, joining_datetime):

    if not application.interview:
        return

    if not application.interview.placement:
        return

    placement = application.interview.placement

    current_status = placement.status
    new_status = data.get("placement_status", current_status)

    if current_status == "Offered":
    
        if joining_datetime:
            placement.joining_datetime = joining_datetime

        if new_status == "Offered":
        
            return

        if new_status in ["Accepted", "Declined"]:

            placement.status = new_status
        
            return

    if current_status in ["Accepted", "Declined"]:
                
        if new_status != current_status:
            raise ValidationError(f"Cannot change placement status from '{current_status}' to '{new_status}'.")

        return

    raise ValidationError(f"Cannot change placement status from '{current_status}' to '{new_status}'.")

def update_application(company, application_id, data):

    application = Application.query.join(Drive).join(Student).join(User).filter(Application.id == application_id, Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active").first()

    if not application:
        raise NotFoundError("Application not found.")

    interview_start_datetime = None
    interview_end_datetime = None
    joining_datetime = None

    if data.get("interview_start_datetime"):
        interview_start_datetime = parse_datetime(data["interview_start_datetime"])
        validate_future_datetime(interview_start_datetime)

    if data.get("interview_end_datetime"):
        interview_end_datetime = parse_datetime(data["interview_end_datetime"])
        validate_future_datetime(interview_end_datetime)

    if interview_start_datetime and interview_end_datetime:
        validate_datetimes(interview_start_datetime, interview_end_datetime)

    if data.get("joining_datetime"):
        joining_datetime = parse_datetime(data["joining_datetime"])
        validate_future_datetime(joining_datetime)

    update_application_record(application, data, interview_start_datetime, interview_end_datetime)

    update_interview_record(application, data, interview_start_datetime, interview_end_datetime, joining_datetime)

    update_placement_record(application, data, joining_datetime)

    db.session.commit()
    clear_dashboard_cache(company_id=company.id, student_id=application.student_id)

    return {"message": "Application updated successfully."}

def get_company_profile(user):

    return {
        "username": user.username,
        "email": user.email,
        "name": user.company.name,
        "description": user.company.description,
        "industry": user.company.industry,
        "type": user.company.type,
        "website": user.company.website,
        "hr_contact_name": user.company.hr_contact_name,
        "hr_contact_number": user.company.hr_contact_number
    }

def update_company_profile(user, data):

    validate_username(data["username"])
    validate_email(data["email"])
    validate_password(data["password"])
    validate_name(data["name"])
    validate_contact_number(data["hr_contact_number"])
    validate_url(data["website"])

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

    company = user.company

    company.name = data["name"]
    company.description = data["description"]
    company.industry = data.get("industry")
    company.type = data.get("type")
    company.website = data["website"]
    company.hr_contact_name = data["hr_contact_name"]
    company.hr_contact_number = data["hr_contact_number"]

    db.session.commit()
    clear_dashboard_cache(all_companies=True, all_students=True)

    return get_company_profile(user)

def delete_company_profile(user):

    company = user.company

    db.session.delete(user)
    db.session.commit()
    clear_dashboard_cache(company_id=company.id, all_students=True)

    return {"message": "Company profile deleted successfully."}

def start_company_manual_export(user):

    from app.integrations.processing.task.celery import manual_company_export

    manual_company_export(user.id)

    return {"message": "Export generation started. You will be notified when it is ready."}

def get_company_notification_summary(company_id):

    notifications = []

    NOTIFICATION_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "archived" / "notifications")

    for file in sorted(NOTIFICATION_DIRECTORY.glob(f"*_company_{company_id}_*.html"), reverse=True):

        html = file.read_text(encoding="utf-8")

        notifications.append({
            "notification_filename": file.name,
            "notification_type": "_".join(file.stem.split("_")[4:]),
            "notification_subject": re.search(r"<title>(.*?)</title>", html).group(1),
            "notification_sent": re.search(r"<b>Sent:</b></td>\s*<td>(.*?)</td>", html).group(1),
            "attachment_exists": re.search(r"<b>Attachment:</b>", html) is not None
        })

    return notifications

def get_company_notification_detail(company_id, notification_filename):

    NOTIFICATION_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "archived" / "notifications")

    notification_file = NOTIFICATION_DIRECTORY / notification_filename

    if not notification_file.exists():
        raise NotFoundError("Notification not found.")

    expected = f"_company_{company_id}_"

    if expected not in notification_filename:
        raise NotFoundError("Notification not accessible.")

    html = notification_file.read_text(encoding="utf-8")
    
    match = re.search(r"<b>Attachment:</b></td>\s*<td>(.*?)</td>", html)
    
    return {
        "notification_body": html,
        "attachment_filename": match.group(1) if match else ""
    }

def download_company_notification_attachment(company_id, notification_filename, attachment_filename):

    NOTIFICATION_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "archived" / "notifications")
    
    notification_file = NOTIFICATION_DIRECTORY / notification_filename

    if not notification_file.exists():
        raise NotFoundError("Notification not found.")

    expected = f"_company_{company_id}_"

    if expected not in notification_filename:
        raise NotFoundError("Notification not accessible.")

    html = notification_file.read_text(encoding="utf-8")

    match = re.search(r"<b>Attachment:</b></td>\s*<td>(.*?)</td>", html)

    if match is None:
        raise NotFoundError("Attachment does not exist.")

    if match.group(1) != attachment_filename:
        raise NotFoundError("Invalid attachment.")

    notification_type = "_".join(notification_filename.split("_")[4:]).replace(".html", "")

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

def get_company_notification_status(company_id):

    status = get_company_notification_cache(company_id)

    if status is None:
        
        return {
            "task_completed": False,
            "message": ""
        }

    clear_company_notification_cache(company_id)

    return status

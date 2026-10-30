from app.database.models import db, User, Company, Drive, Application, Interview, Placement, Education, Experience, Project
from app.utils.errors import NotFoundError, ValidationError, ConflictError
from app.utils.helpers import IST, get_current_ist, format_display_datetime, format_display_datetime_range, hash_password
from app.utils.validators import validate_username, validate_email, validate_password, validate_name, validate_contact_number, validate_url, validate_cgpa, validate_year, parse_date, validate_dates
from app.integrations.processing.cache.dashboard import clear_dashboard_cache
from app.integrations.processing.task.notification import get_student_notification_cache, clear_student_notification_cache
from pathlib import Path
from flask import send_from_directory
import re

def get_student_dashboard(student):

    current_time = get_current_ist()

    total_drives = Drive.query.join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active").count()
    eligible_drives = Drive.query.join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", (Drive.minimum_cgpa == None) | (Drive.minimum_cgpa <= student.cgpa)).count()

    upcoming_drives = Drive.query.join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Drive.application_start > current_time).count()
    ongoing_drives = Drive.query.join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Drive.application_start <= current_time, Drive.application_deadline >= current_time).count()
    closed_drives = Drive.query.join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Drive.application_deadline < current_time).count()

    applied_count = Application.query.join(Drive).join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Application.student_id == student.id, Application.status == "Applied").count()
    shortlisted_count = Application.query.join(Drive).join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Application.student_id == student.id, Application.status == "Shortlisted").count()
    rejected_count = Application.query.join(Drive).join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Application.student_id == student.id, Application.status == "Rejected").count()
    scheduled_count = Interview.query.join(Application).join(Drive).join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Application.student_id == student.id, Interview.status == "Scheduled").count()
    selected_count = Interview.query.join(Application).join(Drive).join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Application.student_id == student.id, Interview.status == "Selected").count()
    not_selected_count = Interview.query.join(Application).join(Drive).join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Application.student_id == student.id, Interview.status == "Not Selected").count()
    offered_count = Placement.query.join(Interview).join(Application).join(Drive).join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Application.student_id == student.id, Placement.status == "Offered").count()
    accepted_count = Placement.query.join(Interview).join(Application).join(Drive).join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Application.student_id == student.id, Placement.status == "Accepted").count()
    declined_count = Placement.query.join(Interview).join(Application).join(Drive).join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Application.student_id == student.id, Placement.status == "Declined").count()

    shortlist_rate = round((shortlisted_count / (applied_count + shortlisted_count + rejected_count)) * 100, 2) if (applied_count + shortlisted_count + rejected_count) else 0
    selection_rate = round((selected_count / (scheduled_count + selected_count + not_selected_count)) * 100, 2) if (scheduled_count + selected_count + not_selected_count) else 0
    acceptance_rate = round((accepted_count / (offered_count + accepted_count + declined_count)) * 100, 2) if (offered_count + accepted_count + declined_count) else 0

    return {
        "platform": {
            "total_drives": total_drives,
            "eligible_drives": eligible_drives
        },
        "drive_phase": {
            "upcoming": upcoming_drives,
            "ongoing": ongoing_drives,
            "closed": closed_drives
        },
        "application": {
            "stage": {
                "applied": applied_count,
                "shortlisted": shortlisted_count,
                "rejected": rejected_count,
                "scheduled": scheduled_count,
                "selected": selected_count,
                "not_selected": not_selected_count,
                "offered": offered_count,
                "accepted": accepted_count,
                "declined": declined_count
            },
            "performance": {
                "shortlist": shortlist_rate,
                "selection": selection_rate,
                "acceptance": acceptance_rate
            }
        }
    }

def get_companies(student):

    companies = Company.query.join(User).filter(Company.approval_status == "Approved", User.status == "Active").order_by(Company.name.asc()).all()

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

def get_company_drives(student, company_id):

    current_time = get_current_ist()

    company = Company.query.join(User).filter(Company.id == company_id, Company.approval_status == "Approved", User.status == "Active").first()

    if not company:
        raise NotFoundError("Company not found.")

    drives = Drive.query.filter(Drive.company_id == company_id, Drive.approval_status == "Approved").order_by(Drive.job_title.asc()).all()

    applied_drive_ids = {application.drive_id for application in Application.query.join(Drive).filter(Application.student_id == student.id, Drive.company_id == company_id).all()}

    return [
        {
            "id": drive.id,
            "job_title": drive.job_title,
            "job_location": drive.job_location,
            "job_type": drive.job_type,
            "job_mode": drive.job_mode,
            "salary_package": drive.salary_package,
            "minimum_cgpa": drive.minimum_cgpa,
            "eligible_status": "Eligible" if drive.minimum_cgpa is None or drive.minimum_cgpa <= student.cgpa else "Not Eligible",
            "drive_status": (
                "Upcoming" if current_time < drive.application_start.replace(tzinfo=IST)
                else "Ongoing" if current_time <= drive.application_deadline.replace(tzinfo=IST)
                else "Closed"
            ),
            "approval_status": drive.approval_status,
            "application_exists": drive.id in applied_drive_ids
        }
        for drive in drives
    ]

def get_drive_details(student, company_id, drive_id):

    current_time = get_current_ist()

    drive = Drive.query.join(Company).join(User).filter(Drive.id == drive_id, Drive.company_id == company_id, Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active").first()

    if not drive:
        raise NotFoundError("Drive not found.")

    application = Application.query.filter(Application.student_id == student.id, Application.drive_id == drive.id).first()

    return {
        "company": {
            "id": drive.company.id,
            "name": drive.company.name,
            "email": drive.company.user.email,
            "hr_contact_name": drive.company.hr_contact_name,
            "hr_contact_number": drive.company.hr_contact_number,
            "website": drive.company.website,
            "type": drive.company.type,
            "industry": drive.company.industry,
            "description": drive.company.description,
            "user_status": drive.company.user.status,
            "approval_status": drive.company.approval_status
        },
        "drive": {
            "id": drive.id,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "job_location": drive.job_location,
            "job_type": drive.job_type,
            "job_mode": drive.job_mode,
            "salary_package": drive.salary_package,
            "eligibility_criteria": drive.eligibility_criteria,
            "minimum_cgpa": drive.minimum_cgpa,
            "eligible_status": "Eligible" if drive.minimum_cgpa is None or drive.minimum_cgpa <= student.cgpa else "Not Eligible",
            "drive_status": (
                "Upcoming" if current_time < drive.application_start.replace(tzinfo=IST)
                else "Ongoing" if current_time <= drive.application_deadline.replace(tzinfo=IST)
                else "Closed"
            )
        },
        "application": {
            "id": application.id if application else None,
            "application_status": application.status if application else "-",
            "interview_status": application.interview.status if application and application.interview else "-",
            "placement_status": application.interview.placement.status if application and application.interview and application.interview.placement else "-",
            "interview_mode": application.interview.mode if application and application.interview else "-",
            "interview_datetime": format_display_datetime_range(application.interview.start_datetime, application.interview.end_datetime) if application and application.interview else "-",
            "joining_datetime": format_display_datetime(application.interview.placement.joining_datetime) if application and application.interview and application.interview.placement else "-"
        }
    }

def apply_drive(student, drive_id):

    current_time = get_current_ist()

    drive = Drive.query.join(Company).join(User).filter(Drive.id == drive_id, Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active").first()

    if not drive:
        raise NotFoundError("Drive not found.")

    if current_time < drive.application_start.replace(tzinfo=IST):
        raise ValidationError("Applications have not opened yet.")

    if current_time > drive.application_deadline.replace(tzinfo=IST):
        raise ValidationError("Applications are already closed.")

    if drive.minimum_cgpa is not None and student.cgpa < drive.minimum_cgpa:
        raise ValidationError("You are not eligible for this drive.")

    application = Application.query.filter(Application.student_id == student.id, Application.drive_id == drive.id).first()

    if application:
        raise ValidationError("You have already applied for this drive.")

    application = Application(
        student_id=student.id,
        drive_id=drive.id
    )

    db.session.add(application)
    db.session.commit()
    clear_dashboard_cache(company_id=application.drive.company_id, student_id=student.id)

    return {"message": "Application submitted successfully."}

def withdraw_drive(student, drive_id):

    current_time = get_current_ist()

    application = Application.query.join(Drive).join(Company).join(User).filter(Application.student_id == student.id, Application.drive_id == drive_id, Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active").first()

    if not application:
        raise NotFoundError("Application not found.")

    drive = application.drive

    if current_time < drive.application_start.replace(tzinfo=IST) or current_time > drive.application_deadline.replace(tzinfo=IST):
        raise ValidationError("Application can no longer be modified.")

    if application.status != "Applied":
        raise ValidationError("Application has already been processed.")

    db.session.delete(application)
    db.session.commit()
    clear_dashboard_cache(company_id=application.drive.company_id, student_id=student.id)

    return {"message": "Application withdrawn successfully."}

def get_student_profile(user):

    return {
        "profile": {
            "username": user.username,
            "email": user.email,
            "name": user.student.name,
            "contact_number": user.student.contact_number,
            "degree": user.student.degree,
            "department": user.student.department,
            "graduation_year": user.student.graduation_year,
            "cgpa": user.student.cgpa,
            "skills": user.student.skills,
            "certifications": user.student.certifications,
            "achievements": user.student.achievements,
            "linkedin": user.student.linkedin,
            "github": user.student.github,
            "portfolio": user.student.portfolio,
            "resume": user.student.resume
        },
        "educations": [
            {
                "id": education.id,
                "degree": education.degree,
                "institution": education.institution,
                "start_date": education.start_date,
                "end_date": education.end_date,
                "coursework": education.coursework
            }
            for education in user.student.educations
        ],
        "experiences": [
            {
                "id": experience.id,
                "role": experience.role,
                "organization": experience.organization,
                "start_date": experience.start_date,
                "end_date": experience.end_date,
                "description": experience.description
            }
            for experience in user.student.experiences
        ],
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "link": project.link,
                "description": project.description
            }
            for project in user.student.projects
        ]
    }

def update_student_profile(user, data):

    profile = data["profile_update"]

    validate_username(profile["username"])
    validate_email(profile["email"])
    validate_password(profile["password"])
    validate_name(profile["name"])
    validate_contact_number(profile["contact_number"])
    validate_year(profile["graduation_year"])
    validate_cgpa(profile["cgpa"])
    if profile.get("linkedin") is not None:
        validate_url(profile["linkedin"])
    if profile.get("github") is not None:
        validate_url(profile["github"])
    if profile.get("portfolio") is not None:
        validate_url(profile["portfolio"])
    validate_url(profile["resume"])

    if profile["username"] != user.username:
        existing_user = User.query.filter(User.username == profile["username"], User.id != user.id).first()
        if existing_user:
            raise ConflictError("Username already exists.")

    if profile["email"] != user.email:
        existing_user = User.query.filter(User.email == profile["email"], User.id != user.id).first()
        if existing_user:
            raise ConflictError("Email already exists.")

    user.username = profile["username"]
    user.email = profile["email"]
    user.password = hash_password(profile["password"])

    student = user.student

    student.name = profile["name"]
    student.contact_number = profile["contact_number"]
    student.degree = profile["degree"]
    student.department = profile["department"]
    student.graduation_year = profile["graduation_year"]
    student.cgpa = profile["cgpa"]
    student.skills = profile.get("skills")
    student.certifications = profile.get("certifications")
    student.achievements = profile.get("achievements")
    student.linkedin = profile.get("linkedin")
    student.github = profile.get("github")
    student.portfolio = profile.get("portfolio")
    student.resume = profile["resume"]

    if "educations" in data:

        submitted_educations = []

        for education_data in data["educations"]:
            
            education_id = education_data.get("id")

            education_start_date = parse_date(education_data["start_date"])
            education_end_date = parse_date(education_data["end_date"])
            validate_dates(education_start_date, education_end_date)

            if education_id:
                education = Education.query.filter(Education.id == education_id, Education.student_id == student.id).first()

                if not education:
                    raise NotFoundError("Education not found.")

                education.degree = education_data["degree"]
                education.institution = education_data["institution"]
                education.start_date = education_start_date
                education.end_date = education_end_date
                education.coursework = education_data["coursework"]

                submitted_educations.append(education)

            else:
                education = Education(
                    student_id=student.id,
                    degree=education_data["degree"],
                    institution=education_data["institution"],
                    start_date=education_start_date,
                    end_date=education_end_date,
                    coursework=education_data["coursework"]
                )

                db.session.add(education)
                submitted_educations.append(education)

        for education in student.educations:
            if education not in submitted_educations:
                db.session.delete(education)

    if "experiences" in data:

        submitted_experiences = []

        for experience_data in data["experiences"]:

            experience_id = experience_data.get("id")

            experience_start_date = parse_date(experience_data["start_date"])
            experience_end_date = parse_date(experience_data["end_date"])
            validate_dates(experience_start_date, experience_end_date)

            if experience_id:
                experience = Experience.query.filter(Experience.id == experience_id, Experience.student_id == student.id).first()

                if not experience:
                    raise NotFoundError("Experience not found.")

                experience.role = experience_data["role"]
                experience.organization = experience_data["organization"]
                experience.start_date = experience_start_date
                experience.end_date = experience_end_date
                experience.description = experience_data["description"]

                submitted_experiences.append(experience)

            else:
                experience = Experience(
                    student_id=student.id,
                    role=experience_data["role"],
                    organization=experience_data["organization"],
                    start_date=experience_start_date,
                    end_date=experience_end_date,
                    description=experience_data["description"]
                )

                db.session.add(experience)
                submitted_experiences.append(experience)

        for experience in student.experiences:
            if experience not in submitted_experiences:
                db.session.delete(experience)

    if "projects" in data:

        submitted_projects = []

        for project_data in data["projects"]:

            project_id = project_data.get("id")

            if project_id:
                project = Project.query.filter(Project.id == project_id, Project.student_id == student.id).first()

                if not project:
                    raise NotFoundError("Project not found.")

                project.name = project_data["name"]
                project.link = project_data["link"]
                project.description = project_data["description"]

                submitted_projects.append(project)

            else:
                project = Project(
                    student_id=student.id,
                    name=project_data["name"],
                    link=project_data["link"],
                    description=project_data["description"]
                )

                db.session.add(project)
                submitted_projects.append(project)

        for project in student.projects:
            if project not in submitted_projects:
                db.session.delete(project)

    db.session.commit()
    clear_dashboard_cache(all_companies=True, all_students=True)

    return get_student_profile(user)

def delete_student_profile(user):

    student = user.student

    db.session.delete(user)
    db.session.commit()
    clear_dashboard_cache(student_id=student.id, all_companies=True)

    return {"message": "Student profile deleted successfully."}

def start_student_manual_export(user):

    from app.integrations.processing.task.celery import manual_student_export

    manual_student_export(user.id)

    return {"message": "Export generation started. You will be notified when it is ready."}

def get_student_notification_summary(student_id):

    notifications = []

    NOTIFICATION_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "archived" / "notifications")

    for file in sorted(NOTIFICATION_DIRECTORY.glob(f"*_student_{student_id}_*.html"), reverse=True):

        html = file.read_text(encoding="utf-8")

        notifications.append({
            "notification_filename": file.name,
            "notification_type": "_".join(file.stem.split("_")[4:]),
            "notification_subject": re.search(r"<title>(.*?)</title>", html).group(1),
            "notification_sent": re.search(r"<b>Sent:</b></td>\s*<td>(.*?)</td>", html).group(1),
            "attachment_exists": re.search(r"<b>Attachment:</b>", html) is not None
        })

    return notifications

def get_student_notification_detail(student_id, notification_filename):

    NOTIFICATION_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "archived" / "notifications")

    notification_file = NOTIFICATION_DIRECTORY / notification_filename

    if not notification_file.exists():
        raise NotFoundError("Notification not found.")

    expected = f"_student_{student_id}_"

    if expected not in notification_filename:
        raise NotFoundError("Notification not accessible.")

    html = notification_file.read_text(encoding="utf-8")

    match = re.search(r"<b>Attachment:</b></td>\s*<td>(.*?)</td>", html)

    return {
        "notification_body": html,
        "attachment_filename": match.group(1) if match else ""
    }

def download_student_notification_attachment(student_id, notification_filename, attachment_filename):

    NOTIFICATION_DIRECTORY = (Path(__file__).resolve().parents[1] / "integrations" / "storage" / "archived" / "notifications")
    
    notification_file = NOTIFICATION_DIRECTORY / notification_filename

    if not notification_file.exists():
        raise NotFoundError("Notification not found.")

    expected = f"_student_{student_id}_"

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

def get_student_notification_status(student_id):

    status = get_student_notification_cache(student_id)

    if status is None:
        
        return {
            "task_completed": False,
            "message": ""
        }

    clear_student_notification_cache(student_id)

    return status

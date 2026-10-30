from app.integrations.processing.task.celery import celery, app
from app.integrations.processing.task.notification import set_admin_notification_cache, set_company_notification_cache, set_student_notification_cache
from app.integrations.processing.mail.mailpit import send_mail
from app.integrations.processing.mail.export import build_manual_admin_export_mail, build_manual_admin_export, build_manual_company_export_mail, build_manual_company_export, build_manual_student_export_mail, build_manual_student_export, build_xlsx_export
from app.integrations.processing.mail.notification import save_notification
from app.database.models import User, Company, Student, Drive, Application
from app.utils.helpers import get_current_ist
from pathlib import Path

@celery.task
def send_manual_admin_export_mail(user_id):

    with app.app_context():

        current_time = get_current_ist()

        admin = User.query.get(user_id)
        if admin is None or admin.role != "Admin":
            return

        company_data = []

        companies = Company.query.join(User).all()

        for company in companies:

            drives = Drive.query.filter(Drive.company_id == company.id).all()

            if drives:

                for drive in drives:

                    company_data.append({
                        "company_id": company.id,
                        "username": company.user.username,
                        "user_status": company.user.status,
                        "account_created_at": company.user.created_at,
                        "name": company.name,
                        "email": company.user.email,
                        "website": company.website,
                        "hr_contact_name": company.hr_contact_name,
                        "hr_contact_number": company.hr_contact_number,
                        "approval_status": company.approval_status,
                        "industry": company.industry,
                        "type": company.type,
                        "drive_job_title": drive.job_title,
                        "drive_job_location": drive.job_location,
                        "drive_job_type": drive.job_type,
                        "drive_job_mode": drive.job_mode,
                        "drive_salary_package": drive.salary_package,
                        "drive_application_start": drive.application_start,
                        "drive_application_deadline": drive.application_deadline,
                        "drive_approval_status": drive.approval_status
                    })

            else:

                company_data.append({
                    "company_id": company.id,
                    "username": company.user.username,
                    "user_status": company.user.status,
                    "account_created_at": company.user.created_at,
                    "name": company.name,
                    "email": company.user.email,
                    "website": company.website,
                    "hr_contact_name": company.hr_contact_name,
                    "hr_contact_number": company.hr_contact_number,
                    "approval_status": company.approval_status,
                    "industry": company.industry,
                    "type": company.type,
                    "drive_job_title": "",
                    "drive_job_location": "",
                    "drive_job_type": "",
                    "drive_job_mode": "",
                    "drive_salary_package": "",
                    "drive_application_start": "",
                    "drive_application_deadline": "",
                    "drive_approval_status": ""
                })

        student_data = []

        students = Student.query.join(User).all()

        for student in students:

            student_data.append({
                "student_id": student.id,
                "username": student.user.username,
                "user_status": student.user.status,
                "account_created_at": student.user.created_at,
                "name": student.name,
                "email": student.user.email,
                "contact_number": student.contact_number,
                "degree": student.degree,
                "department": student.department,
                "graduation_year": student.graduation_year,
                "cgpa": student.cgpa,
                "skills": student.skills,
                "certifications": student.certifications,
                "achievements": student.achievements,
                "linkedin": student.linkedin,
                "github": student.github,
                "portfolio": student.portfolio,
                "resume": student.resume,
                "educations": [
                    {
                        "degree": education.degree,
                        "institution": education.institution
                    }
                    for education in student.educations
                ],
                "experiences": [
                    {
                        "role": experience.role,
                        "organization": experience.organization
                    }
                    for experience in student.experiences
                ],
                "projects": [
                    {
                        "name": project.name,
                        "link": project.link
                    }
                    for project in student.projects
                ]
            })

        drive_application_data = []

        applications = Application.query.all()

        for application in applications:

            drive_application_data.append({
                "company_name": application.drive.company.name,
                "drive_name": application.drive.job_title,
                "student_name": application.student.name,
                "application_status": application.status,
                "interview_status": application.interview.status if application.interview else "-",
                "placement_status": application.interview.placement.status if application.interview and application.interview.placement else "-"
            })

        export = build_manual_admin_export(company_data, student_data, drive_application_data)

        xlsx = build_xlsx_export(export)

        EXPORT_DIRECTORY = (Path(__file__).resolve().parents[2] / "storage" / "generated" / "exports")

        EXPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)

        timestamp = current_time.strftime("%Y%m%d_%H%M%S")

        filename = f"{timestamp}_admin_manual_export.xlsx"

        file = EXPORT_DIRECTORY / filename

        file.write_bytes(xlsx)

        subject, html = build_manual_admin_export_mail()

        save_notification(admin, "manual_export", subject, html, filename)

        send_mail(admin.email, subject, html, [{"filename": filename, "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "data": xlsx}])

        set_admin_notification_cache("Manual export ready. Check your inbox.")

@celery.task
def send_manual_company_export_mail(user_id):

    with app.app_context():

        current_time = get_current_ist()

        user = User.query.get(user_id)
        if user is None or user.role != "Company":
            return

        company = user.company

        company_application_data = []

        applications = Application.query.join(Drive).join(Student).join(User).filter(Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active").all()

        for application in applications:

            company_application_data.append({
                "drive_name": application.drive.job_title,
                "student_name": application.student.name,
                "application_status": application.status,
                "interview_status": application.interview.status if application.interview else "-",
                "placement_status": application.interview.placement.status if application.interview and application.interview.placement else "-"
            })

        export = build_manual_company_export(company_application_data)

        xlsx = build_xlsx_export(export)

        EXPORT_DIRECTORY = (Path(__file__).resolve().parents[2] / "storage" / "generated" / "exports")

        EXPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)

        timestamp = current_time.strftime("%Y%m%d_%H%M%S")

        filename = (f"{timestamp}_company_{company.id}_manual_export.xlsx")

        file = EXPORT_DIRECTORY / filename

        file.write_bytes(xlsx)

        subject, html = build_manual_company_export_mail(company)

        save_notification(company.user, "manual_export", subject, html, filename)

        send_mail(company.user.email, subject, html, [{"filename": filename, "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "data": xlsx}])

        set_company_notification_cache(company.id, "Manual export ready. Check your inbox.")

@celery.task
def send_manual_student_export_mail(user_id):

    with app.app_context():

        current_time = get_current_ist()

        user = User.query.get(user_id)
        if user is None or user.role != "Student":
            return

        student = user.student

        student_application_data = []

        applications = Application.query.join(Drive).join(Company).join(User).filter(Application.student_id == student.id, Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active").all()

        for application in applications:

            student_application_data.append({
                "company_name": application.drive.company.name,
                "drive_name": application.drive.job_title,
                "application_status": application.status,
                "interview_status": application.interview.status if application.interview else "-",
                "placement_status": application.interview.placement.status if application.interview and application.interview.placement else "-"
            })

        export = build_manual_student_export(student_application_data)

        xlsx = build_xlsx_export(export)

        EXPORT_DIRECTORY = (Path(__file__).resolve().parents[2] / "storage" / "generated" / "exports")

        EXPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)

        timestamp = current_time.strftime("%Y%m%d_%H%M%S")

        filename = (f"{timestamp}_student_{student.id}_manual_export.xlsx")

        file = EXPORT_DIRECTORY / filename

        file.write_bytes(xlsx)

        subject, html = build_manual_student_export_mail(student)

        save_notification(student.user, "manual_export", subject, html, filename)

        send_mail(student.user.email, subject, html, [{"filename": filename, "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "data": xlsx}])

        set_student_notification_cache(student.id, "Manual export ready. Check your inbox.")

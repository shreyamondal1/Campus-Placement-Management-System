from app.integrations.processing.task.celery import celery, app
from app.integrations.processing.task.notification import set_admin_notification_cache, set_company_notification_cache
from app.integrations.processing.mail.mailpit import send_mail
from app.integrations.processing.mail.report import build_monthly_admin_report_mail, build_monthly_admin_report, build_weekly_company_report_mail, build_weekly_company_report, build_pdf_report
from app.integrations.processing.mail.notification import save_notification
from app.database.models import User, Company, Student, Drive, Application, Interview, Placement
from app.utils.helpers import get_current_ist, get_ist_datetime
from pathlib import Path

@celery.task
def send_monthly_admin_report_mail():

    with app.app_context():

        current_time = get_current_ist()

        admin = User.query.filter(User.role == "Admin").first()
        if admin is None:
            return

        companies = Company.query.join(User).filter(User.status == "Active").all()
        students = Student.query.join(User).filter(User.status == "Active").all()
        drives = Drive.query.join(Company).join(User).filter(User.status == "Active").all()
        applications = []
        for application in Application.query.all():
            if (application.student.user.status == "Active" and application.drive.company.user.status == "Active"):
                applications.append(application)
        
        accepted_placements = []
        for placement in Placement.query.join(Interview).join(Application).join(Drive).filter(Placement.status == "Accepted").all():
            if (placement.interview.application.student.user.status == "Active" and placement.interview.application.drive.company.user.status == "Active"):
                accepted_placements.append(placement)

        salaries = [float(placement.interview.application.drive.salary_package) for placement in accepted_placements]

        if salaries:

            salaries.sort()
            average_salary = round(sum(salaries) / len(salaries), 2)
            highest_salary = round(max(salaries), 2)
            if len(salaries) % 2 == 1:
                median_salary = round(salaries[len(salaries) // 2], 2)
            else:
                median_salary = round((salaries[len(salaries) // 2 - 1] + salaries[len(salaries) // 2]) / 2, 2)
        
        else:

            average_salary = 0
            median_salary = 0
            highest_salary = 0

        summary = {
            "total_companies": len(companies),
            "total_students": len(students),
            "total_drives": len(drives),
            "total_applications": len(applications),
            "pending_companies": sum(company.approval_status == "Pending" for company in companies),
            "approved_companies": sum(company.approval_status == "Approved" for company in companies),
            "rejected_companies": sum(company.approval_status == "Rejected" for company in companies),
            "pending_drives": sum(drive.approval_status == "Pending" for drive in drives),
            "approved_drives": sum(drive.approval_status == "Approved" for drive in drives),
            "rejected_drives": sum(drive.approval_status == "Rejected" for drive in drives),
            "average_salary": average_salary,
            "median_salary": median_salary,
            "highest_salary": highest_salary
        }

        application_distribution = {
            "applied": sum(application.status == "Applied" for application in applications),
            "shortlisted": sum(application.status == "Shortlisted" for application in applications),
            "rejected": sum(application.status == "Rejected" for application in applications)
        }

        interview_distribution = {
            "scheduled": sum(application.interview is not None and application.interview.status == "Scheduled" for application in applications),
            "selected": sum(application.interview is not None and application.interview.status == "Selected" for application in applications),
            "not_selected": sum(application.interview is not None and application.interview.status == "Not Selected" for application in applications)
        }

        placement_distribution = {
            "offered": sum(application.interview is not None and application.interview.placement is not None and application.interview.placement.status == "Offered" for application in applications),
            "accepted": sum(application.interview is not None and application.interview.placement is not None and application.interview.placement.status == "Accepted" for application in applications),
            "declined": sum(application.interview is not None and application.interview.placement is not None and application.interview.placement.status == "Declined" for application in applications)
        }

        top_companies = []

        approved_companies = [company for company in companies if company.approval_status == "Approved" and company.user.status == "Active"]

        for company in approved_companies:

            company_applications = [application for application in applications if application.drive.company_id == company.id]
            interviews = sum(application.interview is not None for application in company_applications)
            placements = sum(application.interview is not None and application.interview.placement is not None for application in company_applications)

            top_companies.append({
                "company": company.name,
                "applications": len(company_applications),
                "interviews": interviews,
                "placements": placements
            })

        sorted_top_companies = []

        while top_companies:

            highest = top_companies[0]

            for company in top_companies:

                if company["applications"] > highest["applications"]:
                    highest = company

            sorted_top_companies.append(highest)

            top_companies.remove(highest)

        top_companies = sorted_top_companies[:10]

        top_drives = []

        approved_drives = [drive for drive in drives if drive.approval_status == "Approved" and drive.company.approval_status == "Approved" and drive.company.user.status == "Active"]

        for drive in approved_drives:

            drive_applications = [application for application in applications if application.drive_id == drive.id]
            interviews = sum(application.interview is not None for application in drive_applications)
            placements = sum(application.interview is not None and application.interview.placement is not None for application in drive_applications)

            top_drives.append({
                "company": drive.company.name,
                "drive": drive.job_title,
                "applications": len(drive_applications),
                "interviews": interviews,
                "placements": placements
            })

        sorted_top_drives = []

        while top_drives:

            highest = top_drives[0]

            for drive in top_drives:

                if drive["applications"] > highest["applications"]:
                    highest = drive

            sorted_top_drives.append(highest)

            top_drives.remove(highest)

        top_drives = sorted_top_drives[:10]

        report = build_monthly_admin_report(current_time, summary, application_distribution, interview_distribution, placement_distribution, top_companies, top_drives)

        pdf = build_pdf_report(report)

        REPORT_DIRECTORY = (Path(__file__).resolve().parents[2] / "storage" / "generated" / "reports")

        REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)

        timestamp = current_time.strftime("%Y%m%d_%H%M%S")

        filename = f"{timestamp}_admin_monthly_report.pdf"

        file = REPORT_DIRECTORY / filename

        file.write_bytes(pdf)

        subject, html = build_monthly_admin_report_mail()

        save_notification(admin, "monthly_report", subject, html, filename)

        send_mail(admin.email, subject, html, [{"filename": filename, "content_type": "application/pdf", "data": pdf}])

        set_admin_notification_cache("Monthly report generated. Check your inbox.")

@celery.task
def send_weekly_company_report_mail():

    with app.app_context():

        current_time = get_current_ist()
        past_7_days = get_ist_datetime(-7, 8, 00)

        companies = Company.query.join(User).filter(Company.approval_status == "Approved", User.status == "Active").all()

        for company in companies:

            drives = Drive.query.filter(Drive.company_id == company.id, Drive.approval_status == "Approved").all()

            applications = Application.query.join(Drive).join(Student).join(User).filter(Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active").all()

            recent_applications_db = Application.query.join(Drive).join(Student).join(User).filter(Drive.company_id == company.id, Drive.approval_status == "Approved", User.status == "Active", Application.created_at >= past_7_days).order_by(Application.created_at.desc()).all()

            summary = {
                "total_drives": len(drives),
                "total_applications": len(applications),
                "applied": sum(application.status == "Applied" for application in applications),
                "shortlisted": sum(application.status == "Shortlisted" for application in applications),
                "rejected": sum(application.status == "Rejected" for application in applications),
                "scheduled": sum(application.interview is not None and application.interview.status == "Scheduled" for application in applications),
                "selected": sum(application.interview is not None and application.interview.status == "Selected" for application in applications),
                "not_selected": sum(application.interview is not None and application.interview.status == "Not Selected" for application in applications),
                "offered": sum(application.interview is not None and application.interview.placement is not None and application.interview.placement.status == "Offered" for application in applications),
                "accepted": sum(application.interview is not None and application.interview.placement is not None and application.interview.placement.status == "Accepted" for application in applications),
                "declined": sum(application.interview is not None and application.interview.placement is not None and application.interview.placement.status == "Declined" for application in applications)
            }

            drive_breakdown = []

            for drive in drives:

                drive_applications = [application for application in applications if application.drive_id == drive.id]

                drive_breakdown.append({
                    "drive": drive.job_title,
                    "applications": len(drive_applications),
                    "applied": sum(application.status == "Applied" for application in drive_applications),
                    "shortlisted": sum(application.status == "Shortlisted" for application in drive_applications),
                    "rejected": sum(application.status == "Rejected" for application in drive_applications),
                    "scheduled": sum(application.interview is not None and application.interview.status == "Scheduled" for application in drive_applications),
                    "selected": sum(application.interview is not None and application.interview.status == "Selected" for application in drive_applications),
                    "not_selected": sum(application.interview is not None and application.interview.status == "Not Selected" for application in drive_applications),
                    "offered": sum(application.interview is not None and application.interview.placement is not None and application.interview.placement.status == "Offered" for application in drive_applications),
                    "accepted": sum(application.interview is not None and application.interview.placement is not None and application.interview.placement.status == "Accepted" for application in drive_applications),
                    "declined": sum(application.interview is not None and application.interview.placement is not None and application.interview.placement.status == "Declined" for application in drive_applications)
                })

            recent_applications = []

            for application in recent_applications_db:

                recent_applications.append({
                    "student": application.student.name,
                    "drive": application.drive.job_title,
                    "applied_on": application.created_at,
                    "application_status": application.status,
                    "interview_status": application.interview.status if application.interview else "-",
                    "placement_status": application.interview.placement.status if application.interview and application.interview.placement else "-"
                })

            report = build_weekly_company_report(company, current_time, summary, drive_breakdown, recent_applications)

            pdf = build_pdf_report(report)

            REPORT_DIRECTORY = (Path(__file__).resolve().parents[2] / "storage" / "generated" / "reports")

            REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)

            timestamp = current_time.strftime("%Y%m%d_%H%M%S")

            filename = (f"{timestamp}_company_{company.id}_weekly_report.pdf")

            file = REPORT_DIRECTORY / filename

            file.write_bytes(pdf)

            subject, html = build_weekly_company_report_mail(company)

            save_notification(company.user, "weekly_report", subject, html, filename)

            send_mail(company.user.email, subject, html, [{"filename": filename, "content_type": "application/pdf", "data": pdf}])

            set_company_notification_cache(company.id, "Weekly report generated. Check your inbox.")

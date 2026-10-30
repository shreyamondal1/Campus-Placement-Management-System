from app.integrations.processing.task.celery import celery, app
from app.integrations.processing.task.notification import set_student_notification_cache
from app.integrations.processing.mail.mailpit import send_mail
from app.integrations.processing.mail.reminder import build_daily_student_reminder_mail
from app.integrations.processing.mail.notification import save_notification
from app.database.models import User, Company, Student, Drive, Application
from app.utils.helpers import get_current_ist, get_ist_datetime

@celery.task
def send_daily_student_reminder_mail():

    with app.app_context():

        current_time = get_current_ist()
        next_24_hours = get_ist_datetime(1, 8, 00)

        students = Student.query.join(User).filter(User.status == "Active").all()

        drives = Drive.query.join(Company).join(User).filter(Drive.approval_status == "Approved", Company.approval_status == "Approved", User.status == "Active", Drive.application_deadline >= current_time, Drive.application_deadline <= next_24_hours).all()

        for student in students:

            applied_drive_ids = {application.drive_id for application in Application.query.filter(Application.student_id == student.id).all()}

            reminder_drives = []

            for drive in drives:

                if drive.minimum_cgpa is not None and student.cgpa < drive.minimum_cgpa:
                    continue

                if drive.id in applied_drive_ids:
                    continue

                reminder_drives.append(drive)

            subject, html = build_daily_student_reminder_mail(student, reminder_drives)

            save_notification(student.user, "daily_reminder", subject, html)

            send_mail(student.user.email, subject, html)

            set_student_notification_cache(student.id, "Daily reminder sent. Check your inbox.")

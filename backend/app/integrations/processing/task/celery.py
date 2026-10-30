from celery import Celery
from celery.schedules import crontab
from app.main import create_app

app = create_app()

celery = Celery("placementconnect", broker="redis://127.0.0.1:6379/1", backend="redis://127.0.0.1:6379/1")

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
    imports=[
        "app.integrations.processing.task.reminder",
        "app.integrations.processing.task.report",
        "app.integrations.processing.task.export",
        "app.integrations.processing.task.notification"
    ],
    beat_schedule={
        "monthly-admin-report": {
            "task": "app.integrations.processing.task.report.send_monthly_admin_report_mail",
            "schedule": crontab(hour=8, minute=0, day_of_month=1)
        },
        "weekly-company-report": {
            "task": "app.integrations.processing.task.report.send_weekly_company_report_mail",
            "schedule": crontab(hour=8, minute=0, day_of_week=1)
        },
        "daily-student-reminder": {
            "task": "app.integrations.processing.task.reminder.send_daily_student_reminder_mail",
            "schedule": crontab(hour=8, minute=0)
        }
    }
)

def manual_admin_export(user_id):
    celery.send_task(
        "app.integrations.processing.task.export.send_manual_admin_export_mail",
        args=[user_id]
    )

def manual_company_export(user_id):
    celery.send_task(
        "app.integrations.processing.task.export.send_manual_company_export_mail",
        args=[user_id]
    )

def manual_student_export(user_id):
    celery.send_task(
        "app.integrations.processing.task.export.send_manual_student_export_mail",
        args=[user_id]
    )

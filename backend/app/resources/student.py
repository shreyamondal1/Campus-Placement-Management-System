from flask import session, request
from flask_restx import Namespace, Resource, fields
from app.database.models import User
from app.schemas.student import platform_fields, drive_phase_fields, application_stage_fields, application_performance_fields, company_fields, drive_fields, company_data_fields, drive_data_fields, application_data_fields, message_fields, profile_fields, profile_update_fields, education_fields, experience_fields, project_fields, notification_summary_fields, notification_detail_fields, notification_status_fields
from app.services.student import get_student_dashboard, get_companies, get_company_drives, get_drive_details, apply_drive, withdraw_drive, get_student_profile, update_student_profile, delete_student_profile, start_student_manual_export, get_student_notification_summary, get_student_notification_detail, download_student_notification_attachment, get_student_notification_status
from app.utils.decorators import role_required
from app.integrations.processing.cache.dashboard import get_student_dashboard_cache, set_student_dashboard_cache

student = Namespace("student", path="/student")

platform_model = student.model("Platform", platform_fields)

drive_phase_model = student.model("DrivePhase", drive_phase_fields)

application_stage_model = student.model("ApplicationStage", application_stage_fields)
application_performance_model = student.model("ApplicationPerformance", application_performance_fields)
application_model = student.model(
    "Application",
    {
        "stage": fields.Nested(application_stage_model),
        "performance": fields.Nested(application_performance_model)
    }
)

student_dashboard_model = student.model(
    "StudentDashboard",
    {
        "platform": fields.Nested(platform_model),
        "drive_phase": fields.Nested(drive_phase_model),
        "application": fields.Nested(application_model)
    }
)

company_model = student.model("Company", company_fields)
drive_model = student.model("Drive", drive_fields)

company_data_model = student.model("CompanyData", company_data_fields)
drive_data_model = student.model("DriveData", drive_data_fields)
application_data_model = student.model("ApplicationData", application_data_fields)

drive_detail_model = student.model(
    "DriveDetail",
    {
        "company": fields.Nested(company_data_model),
        "drive": fields.Nested(drive_data_model),
        "application": fields.Nested(application_data_model)
    }
)

message_model = student.model("Message", message_fields)

profile_model = student.model("Profile", profile_fields)
profile_update_model = student.model("ProfileUpdate", profile_update_fields)
education_model = student.model("Education", education_fields)
experience_model = student.model("Experience", experience_fields)
project_model = student.model("Project", project_fields)
student_profile_model = student.model(
    "StudentProfile",
    {
        "profile": fields.Nested(profile_model),
        "educations": fields.List(fields.Nested(education_model)),
        "experiences": fields.List(fields.Nested(experience_model)),
        "projects": fields.List(fields.Nested(project_model))
    }
)
student_profile_update_model = student.model(
    "StudentProfileUpdate",
    {
        "profile_update": fields.Nested(profile_update_model),
        "educations": fields.List(fields.Nested(education_model)),
        "experiences": fields.List(fields.Nested(experience_model)),
        "projects": fields.List(fields.Nested(project_model))
    }
)

notification_summary_model = student.model("NotificationSummary", notification_summary_fields)
notification_detail_model = student.model("NotificationDetail", notification_detail_fields)
notification_status_model = student.model("NotificationStatus", notification_status_fields)

@student.route("/dashboard")
class StudentDashboardResource(Resource):

    @role_required("Student")
    @student.marshal_with(student_dashboard_model, code=200)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        cached = get_student_dashboard_cache(user.student.id)

        if cached is not None:
            return cached, 200

        data = get_student_dashboard(user.student)

        set_student_dashboard_cache(user.student.id, data)

        return data, 200

@student.route("/companies")
class StudentCompanyListResource(Resource):

    @role_required("Student")
    @student.marshal_list_with(company_model, code=200)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_companies(user.student), 200

@student.route("/companies/<int:company_id>/drives")
class StudentCompanyDriveListResource(Resource):

    @role_required("Student")
    @student.marshal_list_with(drive_model, code=200)

    def get(self, company_id):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_company_drives(user.student, company_id), 200

@student.route("/companies/<int:company_id>/drives/<int:drive_id>")
class StudentCompanyDriveDetailResource(Resource):

    @role_required("Student")
    @student.marshal_with(drive_detail_model, code=200)

    def get(self, company_id, drive_id):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_drive_details(user.student, company_id, drive_id), 200

@student.route("/drives/<int:drive_id>/apply")
class ApplyDriveResource(Resource):

    @role_required("Student")
    @student.marshal_with(message_model, code=200)

    def post(self, drive_id):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return apply_drive(user.student, drive_id), 200

@student.route("/drives/<int:drive_id>/withdraw")
class WithdrawDriveResource(Resource):

    @role_required("Student")
    @student.marshal_with(message_model, code=200)

    def delete(self, drive_id):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return withdraw_drive(user.student, drive_id), 200

@student.route("/profile")
class StudentProfileResource(Resource):

    @role_required("Student")
    @student.marshal_with(student_profile_model, code=200)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_student_profile(user), 200

    @role_required("Student")
    @student.expect(student_profile_update_model)
    @student.marshal_with(student_profile_model, code=200)
    
    def put(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        data = request.json

        return update_student_profile(user, data), 200

    @role_required("Student")
    @student.marshal_with(message_model, code=200)

    def delete(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)  

        return delete_student_profile(user), 200      

@student.route("/profile/export")
class StudentProfileExportResource(Resource):

    @role_required("Student")
    @student.marshal_with(message_model, code=202)

    def post(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return start_student_manual_export(user), 202

@student.route("/inbox")
class StudentInboxResource(Resource):

    @role_required("Student")
    @student.marshal_list_with(notification_summary_model)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_student_notification_summary(user.student.id), 200

@student.route("/inbox/notification/<string:notification_filename>")
class StudentInboxNotificationResource(Resource):

    @role_required("Student")
    @student.marshal_with(notification_detail_model)

    def get(self, notification_filename):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_student_notification_detail(user.student.id, notification_filename), 200

@student.route("/inbox/notification/<string:notification_filename>/attachment/<string:attachment_filename>")
class StudentInboxNotificationAttachmentResource(Resource):

    @role_required("Student")

    def get(self, notification_filename, attachment_filename):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return download_student_notification_attachment(user.student.id, notification_filename, attachment_filename)

@student.route("/inbox/status")
class StudentInboxStatusResource(Resource):

    @role_required("Student")
    @student.marshal_with(notification_status_model)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_student_notification_status(user.student.id), 200

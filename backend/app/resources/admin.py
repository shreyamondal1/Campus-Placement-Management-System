from flask import session, request
from flask_restx import Namespace, Resource, fields
from app.database.models import User
from app.schemas.admin import platform_fields, company_approval_fields, drive_approval_fields, company_user_fields, student_user_fields, placement_salary_fields, placement_rate_fields, company_fields, student_fields, drive_fields, application_fields, company_data_fields, student_data_fields, drive_data_fields, application_data_fields, education_data_fields, experience_data_fields, project_data_fields, message_fields, profile_fields, profile_update_fields, notification_summary_fields, notification_detail_fields, notification_status_fields
from app.services.admin import get_admin_dashboard, get_all_companies, get_all_students, get_company_drives, get_drive_applications, get_student_applications, get_application_details, approve_company, reject_company, reapprove_company, disable_company, enable_company, blacklist_company, whitelist_company, delete_company, disable_student, enable_student, blacklist_student, whitelist_student, delete_student, approve_drive, reject_drive, reapprove_drive, get_admin_profile, update_admin_profile, start_admin_manual_export, get_admin_notification_summary, get_admin_notification_detail, download_admin_notification_attachment, get_admin_notification_status
from app.utils.decorators import role_required
from app.integrations.processing.cache.dashboard import get_admin_dashboard_cache, set_admin_dashboard_cache

admin = Namespace("admin", path="/admin")

platform_model = admin.model("Platform", platform_fields)

company_approval_model = admin.model("CompanyApproval", company_approval_fields)
drive_approval_model = admin.model("DriveApproval", drive_approval_fields)
approval_model = admin.model(
    "Approval", 
    {
        "companies": fields.Nested(company_approval_model),
        "drives": fields.Nested(drive_approval_model)
    }
)

company_user_model = admin.model("CompanyUser", company_user_fields)
student_user_model = admin.model("StudentUser", student_user_fields)
user_model = admin.model(
    "User",
    {
        "companies": fields.Nested(company_user_model),
        "students": fields.Nested(student_user_model)
    }
)

placement_salary_model = admin.model("PlacementSalary", placement_salary_fields)
placement_rate_model = admin.model("PlacementRate", placement_rate_fields)
placement_model = admin.model(
    "Placement",
    {
        "salary": fields.Nested(placement_salary_model),
        "rate": fields.Nested(placement_rate_model)
    }
)

admin_dashboard_model = admin.model(
    "AdminDashboard",
    {
        "platform": fields.Nested(platform_model),
        "approval": fields.Nested(approval_model),
        "user": fields.Nested(user_model),
        "placement": fields.Nested(placement_model)
    }
)

company_model = admin.model("Company", company_fields)
student_model = admin.model("Student", student_fields)
drive_model = admin.model("Drive", drive_fields)
application_model = admin.model("Application", application_fields)

education_data_model = admin.model("EducationData", education_data_fields)
experience_data_model = admin.model("ExperienceData", experience_data_fields)
project_data_model = admin.model("ProjectData", project_data_fields)

company_data_model = admin.model("CompanyData", company_data_fields)
student_data_model = admin.model(
    "StudentData",
    {
        **student_data_fields,
        "educations": fields.List(fields.Nested(education_data_model)),
        "experiences": fields.List(fields.Nested(experience_data_model)),
        "projects": fields.List(fields.Nested(project_data_model))
    }
)
drive_data_model = admin.model("DriveData", drive_data_fields)
application_data_model = admin.model("ApplicationData", application_data_fields)

application_detail_model = admin.model(
    "ApplicationDetail",
    {
        "company": fields.Nested(company_data_model),
        "student": fields.Nested(student_data_model),
        "drive": fields.Nested(drive_data_model),
        "application": fields.Nested(application_data_model)
    }
)

message_model = admin.model("Message", message_fields)

profile_model = admin.model("Profile", profile_fields)
profile_update_model = admin.model("ProfileUpdate", profile_update_fields)

notification_summary_model = admin.model("NotificationSummary", notification_summary_fields)
notification_detail_model = admin.model("NotificationDetail", notification_detail_fields)
notification_status_model = admin.model("NotificationStatus", notification_status_fields)

@admin.route("/dashboard")
class AdminDashboardResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(admin_dashboard_model, code=200)

    def get(self):

        cached = get_admin_dashboard_cache()

        if cached is not None:
            return cached, 200

        data = get_admin_dashboard()

        set_admin_dashboard_cache(data)

        return data, 200

@admin.route("/companies")
class AdminCompanyListResource(Resource):

    @role_required("Admin")
    @admin.marshal_list_with(company_model, code=200)

    def get(self):

        return get_all_companies(), 200

@admin.route("/students")
class AdminStudentListResource(Resource):

    @role_required("Admin")
    @admin.marshal_list_with(student_model, code=200)

    def get(self):

        return get_all_students(), 200

@admin.route("/companies/<int:company_id>/drives")
class AdminCompanyDriveListResource(Resource):

    @role_required("Admin")
    @admin.marshal_list_with(drive_model, code=200)

    def get(self, company_id):

        return get_company_drives(company_id), 200

@admin.route("/companies/<int:company_id>/drives/<int:drive_id>/applications")
class AdminCompanyDriveApplicationListResource(Resource):

    @role_required("Admin")
    @admin.marshal_list_with(application_model, code=200)

    def get(self, company_id, drive_id):

        return get_drive_applications(company_id, drive_id), 200

@admin.route("/students/<int:student_id>/applications")
class AdminStudentApplicationListResource(Resource):

    @role_required("Admin")
    @admin.marshal_list_with(application_model, code=200)

    def get(self, student_id):

        return get_student_applications(student_id), 200

@admin.route("/applications/<int:application_id>")
class AdminApplicationDetailResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(application_detail_model, code=200)

    def get(self, application_id):

        return get_application_details(application_id), 200

@admin.route("/companies/<int:company_id>/approve")
class ApproveCompanyResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, company_id):

        return approve_company(company_id), 200

@admin.route("/companies/<int:company_id>/reject")
class RejectCompanyResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, company_id):
    
        return reject_company(company_id), 200

@admin.route("/companies/<int:company_id>/reapprove")
class ReapproveCompanyResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, company_id):

        return reapprove_company(company_id), 200

@admin.route("/companies/<int:company_id>/disable")
class DisableCompanyResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, company_id):

        return disable_company(company_id), 200

@admin.route("/companies/<int:company_id>/enable")
class EnableCompanyResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, company_id):

        return enable_company(company_id), 200

@admin.route("/companies/<int:company_id>/blacklist")
class BlacklistCompanyResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, company_id):

        return blacklist_company(company_id), 200

@admin.route("/companies/<int:company_id>/whitelist")
class WhitelistCompanyResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, company_id):

        return whitelist_company(company_id), 200

@admin.route("/companies/<int:company_id>/delete")
class DeleteCompanyResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def delete(self, company_id):

        return delete_company(company_id), 200

@admin.route("/students/<int:student_id>/disable")
class DisableStudentResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, student_id):

        return disable_student(student_id), 200

@admin.route("/students/<int:student_id>/enable")
class EnableStudentResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, student_id):

        return enable_student(student_id), 200

@admin.route("/students/<int:student_id>/blacklist")
class BlacklistStudentResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, student_id):

        return blacklist_student(student_id), 200

@admin.route("/students/<int:student_id>/whitelist")
class WhitelistStudentResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, student_id):

        return whitelist_student(student_id), 200

@admin.route("/students/<int:student_id>/delete")
class DeleteStudentResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def delete(self, student_id):

        return delete_student(student_id), 200

@admin.route("/drives/<int:drive_id>/approve")
class ApproveDriveResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, drive_id):

        return approve_drive(drive_id), 200

@admin.route("/drives/<int:drive_id>/reject")
class RejectDriveResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, drive_id):

        return reject_drive(drive_id), 200

@admin.route("/drives/<int:drive_id>/reapprove")
class ReapproveDriveResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=200)

    def post(self, drive_id):

        return reapprove_drive(drive_id), 200

@admin.route("/profile")
class AdminProfileResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(profile_model, code=200)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_admin_profile(user), 200

    @role_required("Admin")
    @admin.expect(profile_update_model)
    @admin.marshal_with(profile_model, code=200)

    def put(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        data = request.json

        return update_admin_profile(user, data), 200

@admin.route("/profile/export")
class AdminProfileExportResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(message_model, code=202)

    def post(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return start_admin_manual_export(user), 202

@admin.route("/inbox")
class AdminInboxResource(Resource):

    @role_required("Admin")
    @admin.marshal_list_with(notification_summary_model)

    def get(self):

        return get_admin_notification_summary(), 200

@admin.route("/inbox/notification/<string:notification_filename>")
class AdminInboxNotificationResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(notification_detail_model)

    def get(self, notification_filename):

        return get_admin_notification_detail(notification_filename), 200

@admin.route("/inbox/notification/<string:notification_filename>/attachment/<string:attachment_filename>")
class AdminInboxNotificationAttachmentResource(Resource):

    @role_required("Admin")

    def get(self, notification_filename, attachment_filename):

        return download_admin_notification_attachment(notification_filename, attachment_filename)

@admin.route("/inbox/status")
class AdminInboxStatusResource(Resource):

    @role_required("Admin")
    @admin.marshal_with(notification_status_model)

    def get(self):

        return get_admin_notification_status(), 200

from flask import session, request
from flask_restx import Namespace, Resource, fields
from app.database.models import User
from app.schemas.company import platform_fields, drive_approval_fields, placement_count_fields, placement_rate_fields, drive_fields, application_fields, create_or_update_drive_fields, update_application_fields, student_data_fields, drive_data_fields, application_data_fields, education_data_fields, experience_data_fields, project_data_fields, message_fields, profile_fields, profile_update_fields, notification_summary_fields, notification_detail_fields, notification_status_fields
from app.services.company import get_company_dashboard, get_drives, get_drive_applications, get_application_details, create_drive, update_drive, delete_drive, update_application, get_company_profile, update_company_profile, delete_company_profile, start_company_manual_export, get_company_notification_summary, get_company_notification_detail, download_company_notification_attachment, get_company_notification_status
from app.utils.decorators import role_required
from app.integrations.processing.cache.dashboard import get_company_dashboard_cache, set_company_dashboard_cache

company = Namespace("company", path="/company")

platform_model = company.model("Platform", platform_fields)

drive_approval_model = company.model("DriveApproval", drive_approval_fields)

placement_count_model = company.model("PlacementCount", placement_count_fields)
placement_rate_model = company.model("PlacementRate", placement_rate_fields)
placement_model = company.model(
    "Placement",
    {
        "count": fields.Nested(placement_count_model),
        "rate": fields.Nested(placement_rate_model)
    }
)

company_dashboard_model = company.model(
    "CompanyDashboard",
    {
        "platform": fields.Nested(platform_model),
        "drive_approval": fields.Nested(drive_approval_model),
        "placement": fields.Nested(placement_model)
    }
)

drive_model = company.model("Drive", drive_fields)
application_model = company.model("Application", application_fields)

create_or_update_drive_model = company.model("CreateOrUpdateDrive", create_or_update_drive_fields)
update_application_model = company.model("UpdateApplication", update_application_fields)

education_data_model = company.model("EducationData", education_data_fields)
experience_data_model = company.model("ExperienceData", experience_data_fields)
project_data_model = company.model("ProjectData", project_data_fields)

student_data_model = company.model(
    "StudentData",
    {
        **student_data_fields,
        "educations": fields.List(fields.Nested(education_data_model)),
        "experiences": fields.List(fields.Nested(experience_data_model)),
        "projects": fields.List(fields.Nested(project_data_model))
    }
)
drive_data_model = company.model("DriveData", drive_data_fields)
application_data_model = company.model("ApplicationData", application_data_fields)

application_detail_model = company.model(
    "ApplicationDetail",
    {
        "student": fields.Nested(student_data_model),
        "drive": fields.Nested(drive_data_model),
        "application": fields.Nested(application_data_model)
    }
)

message_model = company.model("Message", message_fields)

profile_model = company.model("Profile", profile_fields)
profile_update_model = company.model("ProfileUpdate", profile_update_fields)

notification_summary_model = company.model("NotificationSummary", notification_summary_fields)
notification_detail_model = company.model("NotificationDetail", notification_detail_fields)
notification_status_model = company.model("NotificationStatus", notification_status_fields)

@company.route("/dashboard")
class CompanyDashboardResource(Resource):

    @role_required("Company")
    @company.marshal_with(company_dashboard_model, code=200)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        cached = get_company_dashboard_cache(user.company.id)

        if cached is not None:
            return cached, 200

        data = get_company_dashboard(user.company)

        set_company_dashboard_cache(user.company.id, data)

        return data, 200

@company.route("/drives")
class CompanyDriveListResource(Resource):

    @role_required("Company")
    @company.marshal_list_with(drive_model, code=200)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_drives(user.company), 200

@company.route("/drives/<int:drive_id>/applications")
class CompanyDriveApplicationListResource(Resource):

    @role_required("Company")
    @company.marshal_list_with(application_model, code=200)

    def get(self, drive_id):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_drive_applications(user.company, drive_id), 200

@company.route("/drives/<int:drive_id>/applications/<int:application_id>")
class CompanyDriveApplicationDetailResource(Resource):

    @role_required("Company")
    @company.marshal_with(application_detail_model, code=200)

    def get(self, drive_id, application_id):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_application_details(user.company, drive_id, application_id), 200

@company.route("/drives/create")
class CreateDriveResource(Resource):

    @role_required("Company")
    @company.expect(create_or_update_drive_model)
    @company.marshal_with(message_model, code=201)

    def post(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        data = company.payload

        return create_drive(user.company, data), 201

@company.route("/drives/<int:drive_id>/update")
class UpdateDriveResource(Resource):

    @role_required("Company")
    @company.expect(create_or_update_drive_model)
    @company.marshal_with(message_model, code=200)

    def put(self, drive_id):

        user_id = session["user_id"]
        user = User.query.get(user_id)
        
        data = company.payload

        return update_drive(user.company, drive_id, data), 200

@company.route("/drives/<int:drive_id>/delete")
class DeleteDriveResource(Resource):

    @role_required("Company")
    @company.marshal_with(message_model, code=200)

    def delete(self, drive_id):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return delete_drive(user.company, drive_id), 200

@company.route("/applications/<int:application_id>/update")
class UpdateApplicationResource(Resource):

    @role_required("Company")
    @company.expect(update_application_model)
    @company.marshal_with(message_model, code=200)

    def put(self, application_id):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        data = company.payload

        return update_application(user.company, application_id, data), 200

@company.route("/profile")
class CompanyProfileResource(Resource):

    @role_required("Company")
    @company.marshal_with(profile_model, code=200)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_company_profile(user), 200

    @role_required("Company")
    @company.expect(profile_update_model)
    @company.marshal_with(profile_model, code=200)
    
    def put(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        data = request.json

        return update_company_profile(user, data), 200

    @role_required("Company")
    @company.marshal_with(message_model, code=200)

    def delete(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return delete_company_profile(user), 200

@company.route("/profile/export")
class CompanyProfileExportResource(Resource):

    @role_required("Company")
    @company.marshal_with(message_model, code=202)

    def post(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return start_company_manual_export(user), 202

@company.route("/inbox")
class CompanyInboxResource(Resource):

    @role_required("Company")
    @company.marshal_list_with(notification_summary_model)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_company_notification_summary(user.company.id), 200

@company.route("/inbox/notification/<string:notification_filename>")
class CompanyInboxNotificationResource(Resource):

    @role_required("Company")
    @company.marshal_with(notification_detail_model)

    def get(self, notification_filename):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_company_notification_detail(user.company.id, notification_filename), 200

@company.route("/inbox/notification/<string:notification_filename>/attachment/<string:attachment_filename>")
class CompanyInboxNotificationAttachmentResource(Resource):

    @role_required("Company")

    def get(self, notification_filename, attachment_filename):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return download_company_notification_attachment(user.company.id, notification_filename, attachment_filename)

@company.route("/inbox/status")
class CompanyInboxStatusResource(Resource):

    @role_required("Company")
    @company.marshal_with(notification_status_model)

    def get(self):

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return get_company_notification_status(user.company.id), 200

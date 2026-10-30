from flask_restx import fields

platform_fields = {
    "total_companies": fields.Integer,
    "total_students": fields.Integer,
    "total_drives": fields.Integer,
    "total_applications": fields.Integer
}

company_approval_fields = {
    "pending": fields.Integer,
    "approved": fields.Integer,
    "rejected": fields.Integer
}

drive_approval_fields = {
    "pending": fields.Integer,
    "approved": fields.Integer,
    "rejected": fields.Integer
}

company_user_fields = {
    "active": fields.Integer,
    "disabled": fields.Integer,
    "blacklisted": fields.Integer
}

student_user_fields = {
    "active": fields.Integer,
    "disabled": fields.Integer,
    "blacklisted": fields.Integer
}

placement_salary_fields = {
    "average": fields.Float,
    "median": fields.Float,
    "highest": fields.Float
}

placement_rate_fields = {
    "shortlist": fields.Float,
    "select": fields.Float,
    "accept": fields.Float
}

company_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "name": fields.String,
    "website": fields.String,
    "type": fields.String,    
    "industry": fields.String,
    "description": fields.String,
    "user_status": fields.String,
    "approval_status": fields.String
}

student_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "name": fields.String,
    "degree": fields.String,
    "department": fields.String,
    "graduation_year": fields.Integer,
    "cgpa": fields.Float,
    "linkedin": fields.String,
    "github": fields.String,
    "portfolio": fields.String,
    "resume": fields.String,
    "user_status": fields.String
}

drive_fields = {
    "id": fields.Integer,
    "job_title": fields.String,
    "job_location": fields.String,
    "job_type": fields.String,
    "job_mode": fields.String,
    "salary_package": fields.Float,
    "minimum_cgpa": fields.Float,
    "drive_status": fields.String,
    "approval_status": fields.String
}

application_fields = {
    "id": fields.Integer,
    "student_id": fields.Integer,
    "student_name": fields.String,
    "drive_id": fields.Integer,
    "job_title": fields.String,
    "company_id": fields.Integer,
    "company_name": fields.String,
    "application_status": fields.String,
    "interview_status": fields.String,
    "placement_status": fields.String
}

company_data_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "hr_contact_name": fields.String,
    "hr_contact_number": fields.String,
    "website": fields.String,
    "type": fields.String,
    "industry": fields.String,
    "description": fields.String,
    "user_status": fields.String,
    "approval_status": fields.String
}

student_data_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "contact_number": fields.String,
    "degree": fields.String,
    "department": fields.String,
    "graduation_year": fields.Integer,
    "cgpa": fields.Float,
    "linkedin": fields.String,
    "github": fields.String,
    "portfolio": fields.String,
    "resume": fields.String,
    "skills": fields.String,
    "certifications": fields.String,
    "achievements": fields.String,
    "educations": fields.List(fields.Raw),
    "experiences": fields.List(fields.Raw),
    "projects": fields.List(fields.Raw),
    "user_status": fields.String
}

drive_data_fields = {
    "id": fields.Integer,
    "job_title": fields.String,
    "job_description": fields.String,
    "job_location": fields.String,
    "job_type": fields.String,
    "job_mode": fields.String,
    "salary_package": fields.Float,
    "eligibility_criteria": fields.String,
    "minimum_cgpa": fields.Float,
    "drive_status": fields.String,
    "approval_status": fields.String
}

application_data_fields = {
    "id": fields.Integer,
    "application_status": fields.String,
    "interview_status": fields.String,
    "placement_status": fields.String,
    "interview_mode": fields.String,
    "interview_datetime": fields.String,
    "joining_datetime": fields.String
}

education_data_fields = {
    "id": fields.Integer,
    "degree": fields.String,
    "institution": fields.String,
    "duration": fields.String,
    "coursework": fields.String
}

experience_data_fields = {
    "id": fields.Integer,
    "role": fields.String,
    "organization": fields.String,
    "tenure": fields.String,
    "description": fields.String
}

project_data_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "link": fields.String,
    "description": fields.String
}

message_fields = {
    "message": fields.String
}

profile_fields = {
    "username": fields.String,
    "email": fields.String
}

profile_update_fields = {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
}

notification_summary_fields = {
    "notification_filename": fields.String,
    "notification_type": fields.String,
    "notification_subject": fields.String,
    "notification_sent": fields.String,
    "attachment_exists": fields.Boolean
}

notification_detail_fields = {
    "notification_body": fields.String,
    "attachment_filename": fields.String
}

notification_status_fields = {
    "task_completed": fields.Boolean,
    "message": fields.String
}

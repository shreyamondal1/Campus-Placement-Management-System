from flask_restx import fields

platform_fields = {
    "total_drives": fields.Integer,
    "eligible_drives": fields.Integer
}

drive_phase_fields = {
    "upcoming": fields.Integer,
    "ongoing": fields.Integer,
    "closed": fields.Integer
}

application_stage_fields = {
    "applied": fields.Integer,
    "shortlisted": fields.Integer,
    "rejected": fields.Integer,
    "scheduled": fields.Integer,
    "selected": fields.Integer,
    "not_selected": fields.Integer,
    "offered": fields.Integer,
    "accepted": fields.Integer,
    "declined": fields.Integer
}

application_performance_fields = {
    "shortlist": fields.Float,
    "selection": fields.Float,
    "acceptance": fields.Float
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

drive_fields = {
    "id": fields.Integer,
    "job_title": fields.String,
    "job_location": fields.String,
    "job_type": fields.String,
    "job_mode": fields.String,
    "salary_package": fields.Float,
    "minimum_cgpa": fields.Float,
    "eligible_status": fields.String,
    "drive_status": fields.String,
    "approval_status": fields.String,
    "application_exists": fields.Boolean
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
    "eligible_status": fields.String,
    "drive_status": fields.String
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

message_fields = {
    "message": fields.String
}

profile_fields = {
    "username": fields.String,
    "email": fields.String,
    "name": fields.String,
    "contact_number": fields.String,
    "degree": fields.String,
    "department": fields.String,
    "graduation_year": fields.Integer,
    "cgpa": fields.Float,
    "skills": fields.String,
    "certifications": fields.String,
    "achievements": fields.String,
    "linkedin": fields.String,
    "github": fields.String,
    "portfolio": fields.String,
    "resume": fields.String
}

profile_update_fields = {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
    "name": fields.String,
    "contact_number": fields.String,
    "degree": fields.String,
    "department": fields.String,
    "graduation_year": fields.Integer,
    "cgpa": fields.Float,
    "skills": fields.String,
    "certifications": fields.String,
    "achievements": fields.String,
    "linkedin": fields.String,
    "github": fields.String,
    "portfolio": fields.String,
    "resume": fields.String
}

education_fields = {
    "id": fields.Integer,
    "degree": fields.String,
    "institution": fields.String,
    "start_date": fields.String,
    "end_date": fields.String,
    "coursework": fields.String
}

experience_fields = {
    "id": fields.Integer,
    "role": fields.String,
    "organization": fields.String,
    "start_date": fields.String,
    "end_date": fields.String,
    "description": fields.String
}

project_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "link": fields.String,
    "description": fields.String
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

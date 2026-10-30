from app.utils.errors import ConversionError
from io import BytesIO
from openpyxl import Workbook

def build_manual_admin_export_mail():

    subject = "PlacementConnect | Manual Data Export"

    html = """

        <html>

            <body>

                <h2>PlacementConnect</h2>

                <p>Dear Administrator,</p>

                <p>Please find attached the PlacementConnect database export.</p>

                <p>
                    Regards,<br>
                    PlacementConnect
                </p>

            </body>

        </html>

    """

    return subject, html

def build_manual_admin_export(company_data, student_data, drive_application_data):

    workbook = Workbook()

    company_sheet = workbook.active
    company_sheet.title = "Company Database"

    company_sheet.append([
        "Company ID",
        "Username",
        "User Status",
        "Account Created At",
        "Name",
        "Email",
        "Website",
        "HR Contact Name",
        "HR Contact Number",
        "Approval Status",
        "Industry",
        "Type",
        "Drive Job Title",
        "Drive Job Location",
        "Drive Job Type",
        "Drive Job Mode",
        "Drive Salary Package",
        "Drive Application Start",
        "Drive Application Deadline",
        "Drive Approval Status"
    ])

    for company in company_data:

        company_sheet.append([
            company["company_id"],
            company["username"],
            company["user_status"],
            company["account_created_at"],
            company["name"],
            company["email"],
            company["website"],
            company["hr_contact_name"],
            company["hr_contact_number"],
            company["approval_status"],
            company["industry"],
            company["type"],
            company["drive_job_title"],
            company["drive_job_location"],
            company["drive_job_type"],
            company["drive_job_mode"],
            company["drive_salary_package"],
            company["drive_application_start"],
            company["drive_application_deadline"],
            company["drive_approval_status"]
        ])

    student_sheet = workbook.create_sheet("Student Database")

    student_sheet.append([
        "Student ID",
        "Username",
        "User Status",
        "Account Created At",
        "Name",
        "Email",
        "Contact Number",
        "Degree",
        "Department",
        "Graduation Year",
        "CGPA",
        "Skills",
        "Certifications",
        "Achievements",
        "LinkedIn",
        "GitHub",
        "Portfolio",
        "Resume",
        "Educations",
        "Experiences",
        "Projects"
    ])

    for student in student_data:

        educations = "| ".join(f"{education['degree']} , {education['institution']}" for education in student["educations"])
        experiences = "| ".join(f"{experience['role']} , {experience['organization']}" for experience in student["experiences"])
        projects = "| ".join(f"{project['name']} , {project['link']}" for project in student["projects"])

        student_sheet.append([
            student["student_id"],
            student["username"],
            student["user_status"],
            student["account_created_at"],
            student["name"],
            student["email"],
            student["contact_number"],
            student["degree"],
            student["department"],
            student["graduation_year"],
            student["cgpa"],
            student["skills"],
            student["certifications"],
            student["achievements"],
            student["linkedin"],
            student["github"],
            student["portfolio"],
            student["resume"],
            educations,
            experiences,
            projects
        ])

    drive_application_sheet = workbook.create_sheet("Drive Application Database")

    drive_application_sheet.append([
        "Company Name",
        "Drive Name",
        "Student Name",
        "Application Status",
        "Interview Status",
        "Placement Status"
    ])

    for drive_application in drive_application_data:

        drive_application_sheet.append([
            drive_application["company_name"],
            drive_application["drive_name"],
            drive_application["student_name"],
            drive_application["application_status"],
            drive_application["interview_status"],
            drive_application["placement_status"]
        ])

    return workbook

def build_manual_company_export_mail(company):

    subject = "PlacementConnect | Manual Data Export"

    html = f"""

        <html>

            <body>

                <h2>PlacementConnect</h2>

                <p>Dear {company.name},</p>

                <p>Please find attached your PlacementConnect data export.</p>

                <p>
                    Regards,<br>
                    PlacementConnect
                </p>

            </body>

        </html>

    """

    return subject, html

def build_manual_company_export(company_application_data):

    workbook = Workbook()

    company_sheet = workbook.active
    company_sheet.title = "Company Application Database"

    company_sheet.append([
        "Drive Name",
        "Student Name",
        "Application Status",
        "Interview Status",
        "Placement Status"
    ])

    for application in company_application_data:

        company_sheet.append([
            application["drive_name"],
            application["student_name"],
            application["application_status"],
            application["interview_status"],
            application["placement_status"]
        ])

    return workbook

def build_manual_student_export_mail(student):

    subject = "PlacementConnect | Manual Data Export"

    html = f"""

        <html>

            <body>

                <h2>PlacementConnect</h2>

                <p>Dear {student.name},</p>

                <p>Please find attached your PlacementConnect data export.</p>

                <p>
                    Regards,<br>
                    PlacementConnect
                </p>

            </body>

        </html>

    """

    return subject, html

def build_manual_student_export(student_application_data):

    workbook = Workbook()

    student_sheet = workbook.active
    student_sheet.title = "Student Application Database"

    student_sheet.append([
        "Company Name",
        "Drive Name",
        "Application Status",
        "Interview Status",
        "Placement Status"
    ])

    for application in student_application_data:

        student_sheet.append([
            application["company_name"],
            application["drive_name"],
            application["application_status"],
            application["interview_status"],
            application["placement_status"]
        ])

    return workbook

def build_xlsx_export(export):

    xlsx = BytesIO()

    try:
        export.save(xlsx)
    except Exception:
        raise ConversionError("Failed to generate XLSX export.")

    xlsx.seek(0)

    return xlsx.getvalue()

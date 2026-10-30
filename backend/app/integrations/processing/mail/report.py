from app.utils.helpers import format_datetime
from app.utils.errors import ConversionError
from io import BytesIO
from xhtml2pdf import pisa

def build_monthly_admin_report_mail():

    subject = "PlacementConnect | Monthly Placement Report"

    html = """

        <html>

            <body>

                <h2>PlacementConnect</h2>

                <p>Dear Administrator,</p>

                <p>Please find attached the monthly placement report.</p>

                <p>
                    Regards,<br>
                    PlacementConnect
                </p>

            </body>

        </html>

    """

    return subject, html

def build_monthly_admin_report(generated, summary, application_distribution, interview_distribution, placement_distribution, top_companies, top_drives):

    html = f"""

        <html>

            <body>

                <h1>PlacementConnect</h1>

                <h2>Monthly Placement Report : Administrator</h2>

                <p>Generated: {format_datetime(generated)}</p>

                <hr>

                <br>

                <h3>Summary</h3>

                <table border="1" cellspacing="0" cellpadding="8">

                    <tr>
                        <td style="font-weight:bold; text-align:center;">Total Companies</td>
                        <td style="text-align:center;">{summary["total_companies"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Total Students</td>
                        <td style="text-align:center;">{summary["total_students"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Total Drives</td>
                        <td style="text-align:center;">{summary["total_drives"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Total Applications</td>
                        <td style="text-align:center;">{summary["total_applications"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Pending Companies</td>
                        <td style="text-align:center;">{summary["pending_companies"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Approved Companies</td>
                        <td style="text-align:center;">{summary["approved_companies"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Rejected Companies</td>
                        <td style="text-align:center;">{summary["rejected_companies"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Pending Drives</td>
                        <td style="text-align:center;">{summary["pending_drives"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Approved Drives</td>
                        <td style="text-align:center;">{summary["approved_drives"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Rejected Drives</td>
                        <td style="text-align:center;">{summary["rejected_drives"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Average Salary</td>
                        <td style="text-align:center;">{summary["average_salary"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Median Salary</td>
                        <td style="text-align:center;">{summary["median_salary"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Highest Salary</td>
                        <td style="text-align:center;">{summary["highest_salary"]}</td>
                    </tr>

                </table>

                <br>

                <h3>Application Status Distribution</h3>

                <table border="1" cellspacing="0" cellpadding="8">

                    <tr>
                        <td style="font-weight:bold; text-align:center;">Applications</td>
                        <td style="font-weight:bold; text-align:center;">Count</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Applied</td>
                        <td style="text-align:center;">{application_distribution["applied"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Shortlisted</td>
                        <td style="text-align:center;">{application_distribution["shortlisted"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Rejected</td>
                        <td style="text-align:center;">{application_distribution["rejected"]}</td>
                    </tr>

                </table>

                <br>

                <table border="1" cellspacing="0" cellpadding="8">

                    <tr>
                        <td style="font-weight:bold; text-align:center;">Interviews</td>
                        <td style="font-weight:bold; text-align:center;">Count</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Scheduled</td>
                        <td style="text-align:center;">{interview_distribution["scheduled"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Selected</td>
                        <td style="text-align:center;">{interview_distribution["selected"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Not Selected</td>
                        <td style="text-align:center;">{interview_distribution["not_selected"]}</td>
                    </tr>

                </table>

                <br>

                <table border="1" cellspacing="0" cellpadding="8">

                    <tr>
                        <td style="font-weight:bold; text-align:center;">Placements</td>
                        <td style="font-weight:bold; text-align:center;">Count</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Offered</td>
                        <td style="text-align:center;">{placement_distribution["offered"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Accepted</td>
                        <td style="text-align:center;">{placement_distribution["accepted"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Declined</td>
                        <td style="text-align:center;">{placement_distribution["declined"]}</td>
                    </tr>

                </table>

                <br>

                <h3>Top Companies</h3>

                <table border="1" cellspacing="0" cellpadding="8">

                    <tr>
                        <td style="font-weight:bold; text-align:center;">Company</td>
                        <td style="font-weight:bold; text-align:center;">Applications</td>
                        <td style="font-weight:bold; text-align:center;">Interviews</td>
                        <td style="font-weight:bold; text-align:center;">Placements</td>
                    </tr>

    """

    for company in top_companies:

        html += f"""

            <tr>
                <td style="text-align:center;">{company["company"]}</td>
                <td style="text-align:center;">{company["applications"]}</td>
                <td style="text-align:center;">{company["interviews"]}</td>
                <td style="text-align:center;">{company["placements"]}</td>
            </tr>

        """

    html += """

        </table>

        <br>

        <h3>Top Drives</h3>

        <table border="1" cellspacing="0" cellpadding="8">

            <tr>
                <td style="font-weight:bold; text-align:center;">Company</td>
                <td style="font-weight:bold; text-align:center;">Drive</td>
                <td style="font-weight:bold; text-align:center;">Applications</td>
                <td style="font-weight:bold; text-align:center;">Interviews</td>
                <td style="font-weight:bold; text-align:center;">Placements</td>
            </tr>

    """

    for drive in top_drives:

        html += f"""

            <tr>
                <td style="text-align:center;">{drive["company"]}</td>
                <td style="text-align:center;">{drive["drive"]}</td>
                <td style="text-align:center;">{drive["applications"]}</td>
                <td style="text-align:center;">{drive["interviews"]}</td>
                <td style="text-align:center;">{drive["placements"]}</td>
            </tr>

        """

    html += """

            </table>

        </body>

    </html>

    """

    return html

def build_weekly_company_report_mail(company):

    subject = "PlacementConnect | Weekly Placement Report"

    html = f"""

        <html>

            <body>

                <h2>PlacementConnect</h2>

                <p>Dear {company.name},</p>

                <p>Please find attached your weekly placement report.</p>

                <p>
                    Regards,<br>
                    PlacementConnect
                </p>

            </body>

        </html>

    """

    return subject, html

def build_weekly_company_report(company, generated, summary, drive_breakdown, recent_applications):

    html = f"""

        <html>

            <body>

                <h1>PlacementConnect</h1>

                <h2>Weekly Placement Report : {company.name}</h2>

                <p>Generated: {format_datetime(generated)}</p>

                <hr>

                <br>

                <h3>Summary</h3>

                <table border="1" cellspacing="0" cellpadding="8">

                    <tr>
                        <td style="font-weight:bold; text-align:center;">Total Drives</td>
                        <td style="text-align:center;">{summary["total_drives"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Total Applications</td>
                        <td style="text-align:center;">{summary["total_applications"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Applied</td>
                        <td style="text-align:center;">{summary["applied"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Shortlisted</td>
                        <td style="text-align:center;">{summary["shortlisted"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Rejected</td>
                        <td style="text-align:center;">{summary["rejected"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Scheduled</td>
                        <td style="text-align:center;">{summary["scheduled"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Selected</td>
                        <td style="text-align:center;">{summary["selected"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Not Selected</td>
                        <td style="text-align:center;">{summary["not_selected"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Offered</td>
                        <td style="text-align:center;">{summary["offered"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Accepted</td>
                        <td style="text-align:center;">{summary["accepted"]}</td>
                    </tr>
                    <tr>
                        <td style="font-weight:bold; text-align:center;">Declined</td>
                        <td style="text-align:center;">{summary["declined"]}</td>
                    </tr>

                </table>

                <br>

                <h3>Drive-wise Breakdown</h3>

                <table border="1" cellspacing="0" cellpadding="8">

                    <tr>
                        <td style="font-weight:bold; text-align:center;">Drive</td>
                        <td style="font-weight:bold; text-align:center;">Applications</td>
                        <td style="font-weight:bold; text-align:center;">Applied</td>
                        <td style="font-weight:bold; text-align:center;">Shortlisted</td>
                        <td style="font-weight:bold; text-align:center;">Rejected</td>
                        <td style="font-weight:bold; text-align:center;">Scheduled</td>
                        <td style="font-weight:bold; text-align:center;">Selected</td>
                        <td style="font-weight:bold; text-align:center;">Not Selected</td>
                        <td style="font-weight:bold; text-align:center;">Offered</td>
                        <td style="font-weight:bold; text-align:center;">Accepted</td>
                        <td style="font-weight:bold; text-align:center;">Declined</td>
                    </tr>
    
    """

    for drive in drive_breakdown:

        html += f"""

            <tr>
                <td style="text-align:center;"">{drive["drive"]}</td>
                <td style="text-align:center;">{drive["applications"]}</td>
                <td style="text-align:center;">{drive["applied"]}</td>
                <td style="text-align:center;">{drive["shortlisted"]}</td>
                <td style="text-align:center;">{drive["rejected"]}</td>
                <td style="text-align:center;">{drive["scheduled"]}</td>
                <td style="text-align:center;">{drive["selected"]}</td>
                <td style="text-align:center;">{drive["not_selected"]}</td>
                <td style="text-align:center;">{drive["offered"]}</td>
                <td style="text-align:center;">{drive["accepted"]}</td>
                <td style="text-align:center;">{drive["declined"]}</td>
            </tr>
        
        """

    html += """

        </table>

        <br>

        <h3>Recent Applications</h3>

        <table border="1" cellspacing="0" cellpadding="8">

            <tr>
                <td style="font-weight:bold; text-align:center;">Student</td>
                <td style="font-weight:bold; text-align:center;">Drive</td>
                <td style="font-weight:bold; text-align:center;">Applied On</td>
                <td style="font-weight:bold; text-align:center;">Application Status</td>
                <td style="font-weight:bold; text-align:center;">Interview Status</td>
                <td style="font-weight:bold; text-align:center;">Placement Status</td>
            </tr>

    """

    for application in recent_applications:

        html += f"""

            <tr>
                <td style="text-align:center;">{application["student"]}</td>
                <td style="text-align:center;">{application["drive"]}</td>
                <td style="text-align:center;">{format_datetime(application["applied_on"])}</td>
                <td style="text-align:center;">{application["application_status"]}</td>
                <td style="text-align:center;">{application["interview_status"]}</td>
                <td style="text-align:center;">{application["placement_status"]}</td>
            </tr>
        
        """

    html += """

            </table>

        </body>

    </html>

    """

    return html

def build_pdf_report(report):

    pdf = BytesIO()

    result = pisa.CreatePDF(src=report, dest=pdf, encoding="utf-8")

    if result.err:
        raise ConversionError("Failed to generate PDF report.")

    pdf.seek(0)

    return pdf.getvalue()

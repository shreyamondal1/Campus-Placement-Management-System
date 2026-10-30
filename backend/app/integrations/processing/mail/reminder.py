from app.utils.helpers import format_datetime

def build_daily_student_reminder_mail(student, reminder_drives):

    subject = "PlacementConnect | Daily Deadline Reminder"

    html = f"""

        <html>

            <body>

                <h2>PlacementConnect</h2>

                <p>Dear {student.name},</p>
    
    """

    if reminder_drives:

        html += """

            <p>The following application deadlines are approaching within the next 24 hours.</p>

            <table border="1" cellspacing="0" cellpadding="8">

                <tr>
                    <td style="font-weight:bold; text-align:center;">Company</td>
                    <td style="font-weight:bold; text-align:center;">Drive</td>
                    <td style="font-weight:bold; text-align:center;">Application Deadline</td>
                </tr>
        
        """

        for drive in reminder_drives:

            html += f"""

                <tr>
                    <td style="text-align:center;">{drive.company.name}</td>
                    <td style="text-align:center;">{drive.job_title}</td>
                    <td style="text-align:center;">{format_datetime(drive.application_deadline)}</td>
                </tr>
            
            """

        html += """

            </table>

            <p>Please log in to PlacementConnect if you wish to apply before the deadline.</p>

        """

    else:

        html += """

            <p>You have no application deadlines within the next 24 hours.</p>
        
        """

    html += """

            <p>
                Regards,<br>
                PlacementConnect
            </p>

        </body>
    
    </html>

    """

    return subject, html

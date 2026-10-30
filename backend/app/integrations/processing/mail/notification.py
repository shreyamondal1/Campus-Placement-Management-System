from app.utils.helpers import get_current_ist, format_datetime
from pathlib import Path

def save_notification(user, notification_type, subject, html, attachment=None):

    NOTIFICATION_DIRECTORY = (Path(__file__).resolve().parents[2] / "storage" / "archived" / "notifications")

    NOTIFICATION_DIRECTORY.mkdir(parents=True, exist_ok=True)

    current_time = get_current_ist()

    sent = format_datetime(current_time)

    timestamp = current_time.strftime("%Y%m%d_%H%M%S")

    if user.role == "Student":
        recipient = f"student_{user.student.id}"

    elif user.role == "Company":
        recipient = f"company_{user.company.id}"

    else:
        recipient = "admin"

    filename = (f"{timestamp}_{recipient}_{notification_type}.html")

    file = NOTIFICATION_DIRECTORY / filename

    content = f"""

        <!DOCTYPE html>

        <html>

            <head>

                <title>{subject}</title>

            </head>

            <body>

                <table>

                    <tr>
                        <td><b>From:</b></td>
                        <td>info@placementconnect.com</td>
                    </tr>
                    <tr>
                        <td><b>To:</b></td>
                        <td>{user.email}</td>
                    </tr>
                    <tr>
                        <td><b>Subject:</b></td>
                        <td>{subject}</td>
                    </tr>
                    <tr>
                        <td><b>Sent:</b></td>
                        <td>{sent}</td>
                    </tr>

    """
    
    if attachment:

        content += f"""

            <tr>
                <td><b>Attachment:</b></td>
                <td>{attachment}</td>
            </tr>
        
        """

    content += f"""

            </table>

            <br>

            <hr>

            {html}

        </body>

    </html>

    """

    file.write_text(content, encoding="utf-8")

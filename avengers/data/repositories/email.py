from python_http_client.exceptions import BadRequestsError, UnauthorizedError
from sendgrid import Mail, SendGridAPIClient

from avengers.config import settings
from avengers.presentation.exceptions import FailedToSendEmail


def send_mail(address: str, title: str, content: str):
    message = Mail(
        from_email="entrydsm@dsm.hs.kr",
        to_emails=address,
        subject=title,
        html_content=content
    )

    try:
        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = client.send(message)

        return response.status_code

    except BadRequestsError or UnauthorizedError:
        raise FailedToSendEmail

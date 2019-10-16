import boto3
from botocore.exceptions import ClientError

from avengers.config import settings
from avengers.presentation.exceptions import EmailError


class EmailSenderRepository:
    CHARSET = 'UTF-8'
    CONFIGURATION_SET = "ConfigSet"
    SENDER = "Daedeok Software Meister High School <entrydsm@dsm.hs.kr>"

    @classmethod
    async def send_mail(cls, recipient: str, title: str, content: str):
        client = boto3.client('ses', region_name=settings.SES_REGION)

        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ]
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': cls.CHARSET,
                            'Data': content,
                        },
                    },
                    'Subject': {
                        'Charset': cls.CHARSET,
                        'Data': title,
                    },
                },
                Source=cls.SENDER,
            )

        except ClientError as e:
            raise EmailError(e.response['Error']['Message'])

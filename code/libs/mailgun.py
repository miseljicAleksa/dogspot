from typing import List
from requests import Response, post
import os

class MailgunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)



class Mailgun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

    FROM_TITLE = "DogSpot team"
    FROM_EMAIL = "postmaster@sandbox10b5144fca624707a8a6377021407201.mailgun.org"
    
    @classmethod
    def send_email(cls, email: List[str], subject:str, text:str, html:str) -> Response:
         if cls.MAILGUN_API_KEY is None:
             raise MailgunException("Failed to load maigun api key")

         if cls.MAILGUN_DOMAIN is None:
             raise MailgunException("Failed to load maigun domain")
         response = post( 
            "https://api.mailgun.net/v3/{}/messages".format(cls.MAILGUN_DOMAIN),
            auth=("api","{}".format(cls.MAILGUN_API_KEY)),
            data={
                "from": "DogSpot Team <{}>".format(cls.FROM_EMAIL),
                "to": email, 
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

         if response.status_code != 200:
           raise MailgunException("err in sending confirmation email, user registration failed ")

         return response     
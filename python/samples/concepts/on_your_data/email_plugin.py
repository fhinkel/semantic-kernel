from typing import List
from semantic_kernel.functions import kernel_function

class EmailPlugin:
    @kernel_function(
        name="send_email",
        description="Sends an email to a recipient."
    )
    def send_email(self, recipient_email: str|list[str], subject: str, body: str):
        # Add logic to send an email using the recipient_emails, subject, and body
        # For now, we'll just print out a success message to the console
        print("Email sent via email plugin!")

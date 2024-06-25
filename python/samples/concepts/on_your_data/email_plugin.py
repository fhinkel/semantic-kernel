from typing import List
from semantic_kernel.functions import kernel_function

class EmailPlugin:
    @kernel_function(
        name="send_email",
        description="Sends an email to a recipient."
    )
    # async def send_email(self, recipient_emails: List[str], subject: str, body: str):
    async def send_email(self):

        # Add logic to send an email using the recipient_emails, subject, and body
        # For now, we'll just print out a success message to the console
        print("Email sent!")
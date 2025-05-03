from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from packag.models.email_service import dtoSmtpService
from packag.utils.logger import get_logger

email_service_logger = get_logger('email_service')

class EmailBuilder:
    """
    EmailBuilder

    This class is responsible for constructing a complete email object (`MIMEMultipart`) 
    using the information provided in a `dtoSmtpService.Email` model.

    It prepares both:
    - The **body** (content) of the email (plain text or HTML format).
    - The **headers** (sender, recipients, subject).

    Attributes:
        email (dtoSmtpService.Email): The structured email data (sender, recipients, subject, body, and variables).
        email_object (MIMEMultipart): The final email object to be sent.

    Raises:
        ValueError: If the input is not a `dtoSmtpService.Email`.
        KeyError: If a variable required in the body content is missing from the provided variables dictionary.
        Exception: If an unexpected error occurs during body building.

    Methods:
        - update_body(): Builds and attaches the email body to the email object.
        - update_header(): Updates the email headers (From, To, Subject).
        - build_email_object() -> MIMEMultipart: Constructs the complete email and returns it.

    Example:
        >>> from modules.models import dtoSmtpService
        >>> from modules.utilities.smtp_email.smtp_client import EmailBuilder
        >>> from pathlib import Path

        >>> # Define the Email model
        >>> email = dtoSmtpService.Email(
        ...     header=dtoSmtpService.EmailHeader(
        ...         sender_email="sender@example.com",
        ...         recipient_email=["recipient@example.com"]
        ...     ),
        ...     content=dtoSmtpService.EmailContent(
        ...         subject="Test Email",
        ...         html_format=False,
        ...         body=dtoSmtpService.EmailBody(
        ...             variables={"name": "John"},
        ...             content="Hello, {name}! Welcome!"
        ...         )
        ...     )
        ... )

        >>> # Build the email object
        >>> builder = EmailBuilder(email)
        >>> email_object = builder.build_email_object()

        >>> # Now you can send 'email_object' using smtplib.SMTP().sendmail(...)
    """

    def __init__(self, email: dtoSmtpService.Email):
        if not isinstance(email, dtoSmtpService.Email):
            raise ValueError("Email must be an instance of dtoSmtpService.Email")
        
        self.email = email
        self.email_object = MIMEMultipart()

    def update_body(self) -> None:
        """
        Builds the email body based on the EmailBody content and attaches it
        to the MIMEMultipart email object.

        Raises:
            KeyError: If a required variable for content formatting is missing.
        """
        try:
            final_content = self.email.content.body.content.format(**self.email.content.body.variables)
        except KeyError as e:
            email_service_logger.error(f"Content variables not found: {e}")
            raise
        
        if self.email.content.html_format:
            self.email_object.attach(MIMEText(final_content, "html"))
        else:
            self.email_object.attach(MIMEText(final_content, "plain"))
    
    def update_header(self) -> None:
        """
        Sets the email headers (From, To, Subject) on the MIMEMultipart object.
        """
        self.email_object["From"] = self.email.header.sender_email
        self.email_object["To"] = ", ".join(self.email.header.recipient_email)
        self.email_object["Subject"] = self.email.content.subject
    
    def build_email_object(self) -> MIMEMultipart:
        """
        Constructs the complete email object.

        First updates the body, then the headers, and returns the ready-to-send email object.

        Returns:
            MIMEMultipart: The constructed email object.

        Raises:
            Exception: If any unexpected error occurs during body construction.
        """
        try:
            self.update_body()
        except Exception:
            email_service_logger.error(f"Error building email object")
            raise
        
        self.update_header()
        return self.email_object

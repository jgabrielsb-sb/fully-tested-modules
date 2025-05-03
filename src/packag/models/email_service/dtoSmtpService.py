from pydantic import (
    BaseModel,
    EmailStr,
)

from typing import Optional

class SMTPClientConfig(BaseModel):
    """
    SMTP Client Configuration
    Args:
        email_host: SMTP server host
        email_port: SMTP server port
        is_tls: Enable TLS encryption
        email_host_user: SMTP server username
        email_host_password: SMTP server password
    """
    email_host: str
    email_port: str
    is_tls: bool
    email_host_user: str
    email_host_password: str
    
class EmailBody(BaseModel):
    """
    Email Body
    Args:
        variables: variables to be replaced in content
        content: content of the email
        
    The intention is to use this model to send emails with variables in the content
    Example:
        variables = {"name": "John", "age": 30}
        content = "Hello, {{name}}! You are {{age}} years old."
    """
    variables: Optional[dict] = {}
    content: str 
    
class EmailHeader(BaseModel):
    """
    Email Header
    Args:
        recipient_email: recipient email
        sender_email: sender email
    The intention is to use this model to send emails.
    Can send emails to multiple recipients by passing a list of emails.
    Example:
        recipient_email = ["john@example.com", "jane@example.com"]
        sender_email = "noreply@example.com"
    """
    recipient_email: list[EmailStr]
    sender_email: EmailStr
    
class EmailContent(BaseModel):
    """
    Email Content
    Args:
        subject: subject of the email
        body: body of the email
        html_format: if the email is in html format
    """
    subject: str
    html_format: bool
    body: EmailBody
    
class Email(BaseModel):
    """
    Email
    Args:
        header: header of the email
        content: content of the email
    """
    header: EmailHeader
    content: EmailContent
    
    
    
    
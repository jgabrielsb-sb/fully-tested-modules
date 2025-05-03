from packag.models.email_service import dtoSmtpService
import pytest
from packag.modules.email_service import EmailBuilder

@pytest.fixture
def create_email_object():
    """
    Create an email object for testing.
    ONE SENDER
    PLAIN TEXT MESSAGE
    """
    email_header = dtoSmtpService.EmailHeader(
        sender_email="sender@example.com",
        recipient_email=["recipient@example.com"]
    )
    email_body = dtoSmtpService.EmailBody(
        content="This is a plain text message."
    )
    email_content = dtoSmtpService.EmailContent(
        subject="Test Subject",
        body=email_body,
        html_format=False
    )
    email = dtoSmtpService.Email(
        header=email_header,
        content=email_content
    )
    return email

@pytest.fixture
def create_email_object_with_variables_missing():
    email_header = dtoSmtpService.EmailHeader(
        sender_email="sender@example.com",
        recipient_email=["recipient@example.com"]
    )
    email_body = dtoSmtpService.EmailBody(
        variables={},
        content="Hello, {name}!"
    )
    email_content = dtoSmtpService.EmailContent(
        subject="Test Subject",
        body=email_body,
        html_format=False
    )
    email = dtoSmtpService.Email(
        header=email_header,
        content=email_content
    )
    return email

@pytest.fixture
def create_email_object_with_more_than_one_recipient():
    email_header = dtoSmtpService.EmailHeader(
        sender_email="sender@example.com",
        recipient_email=["recipient@example.com", "recipient2@example.com"]
    )
    email_body = dtoSmtpService.EmailBody(
        content="This is a plain text message."
    )
    email_content = dtoSmtpService.EmailContent(
        subject="Test Subject",
        body=email_body,
        html_format=False
    )
    email = dtoSmtpService.Email(
        header=email_header,
        content=email_content
    )
    return email

@pytest.fixture
def create_email_object_with_html_content():
    email_header = dtoSmtpService.EmailHeader(
        sender_email="sender@example.com",
        recipient_email=["recipient@example.com"]
    )
    email_body = dtoSmtpService.EmailBody(
        content="<h1>Hello</h1><p>This is an HTML message.</p>"
    )
    email_content = dtoSmtpService.EmailContent(
        subject="HTML Email",
        body=email_body,
        html_format=True
    )
    email = dtoSmtpService.Email(
        header=email_header,
        content=email_content
    )
    return email

@pytest.fixture
def create_email_object_with_plain_text_content():
    email_header = dtoSmtpService.EmailHeader(
        sender_email="sender@example.com",
        recipient_email=["recipient@example.com"]
    )
    email_body = dtoSmtpService.EmailBody(
        content="This is a plain text message."
    )
    email_content = dtoSmtpService.EmailContent(
        subject="Test Subject",
        body=email_body,
        html_format=False
    )
    email = dtoSmtpService.Email(
        header=email_header,
        content=email_content
    )
    return email
    

def test_init_email_builder_raises_value_error_when_email_is_not_instance_of_dtoSmtpService_Email():
    with pytest.raises(ValueError):
        EmailBuilder('invalid_email')

def test_update_body_raises_key_error_when_variables_are_missing(
    create_email_object_with_variables_missing
):
    email_builder = EmailBuilder(create_email_object_with_variables_missing)
    
    with pytest.raises(KeyError):
        email_builder.update_body()

def test_build_email_object_returns_plain_text_email(
    create_email_object_with_plain_text_content
):
    
    plain_text_email_builder = EmailBuilder(create_email_object_with_plain_text_content)
    email_obj = plain_text_email_builder.build_email_object()
    
    assert email_obj['From'] == "sender@example.com"
    assert email_obj['To'] == "recipient@example.com"
    assert email_obj['Subject'] == "Test Subject"
    assert "This is a plain text message." in email_obj.as_string()
    assert "Content-Type: text/plain" in email_obj.as_string()

def test_build_email_object_returns_html_email(
    create_email_object_with_html_content
):
    
    html_email_builder = EmailBuilder(create_email_object_with_html_content)
    email_obj = html_email_builder.build_email_object()
    
    assert email_obj['From'] == "sender@example.com"
    assert email_obj['To'] == "recipient@example.com"
    assert email_obj['Subject'] == "HTML Email"
    assert "<h1>Hello</h1>" in email_obj.as_string()
    assert "Content-Type: text/html" in email_obj.as_string()
    
def test_build_email_object_returns_email_with_multiple_recipients(
    create_email_object_with_more_than_one_recipient
):
    email_builder = EmailBuilder(create_email_object_with_more_than_one_recipient)
    email_obj = email_builder.build_email_object()
    
    assert email_obj['From'] == "sender@example.com"
    assert email_obj['To'] == "recipient@example.com, recipient2@example.com"
    assert email_obj['Subject'] == "Test Subject"
    assert "This is a plain text message." in email_obj.as_string()
    assert "Content-Type: text/plain" in email_obj.as_string()
    
def test_build_email_object_raises_exception_when_update_body_fails(
    create_email_object_with_variables_missing
):
    with pytest.raises(Exception):
        email_builder = EmailBuilder(create_email_object_with_variables_missing)
        email_builder.build_email_object()
    
    
    


    
    

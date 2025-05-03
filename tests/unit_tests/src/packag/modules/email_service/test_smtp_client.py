import pytest

from unittest.mock import patch, MagicMock

import smtplib

from packag.modules.email_service import SMTP
from packag.models.email_service import (
    dtoSmtpService
)

@pytest.fixture
def smtp_tls_config():
    return dtoSmtpService.SMTPClientConfig(
        email_host="smtp.example.com",
        email_port="587",
        email_host_user="user@example.com",
        email_host_password="correct_password",
        is_tls=True
    )

@pytest.fixture
def smtp_not_tls_config():
    return dtoSmtpService.SMTPClientConfig(
        email_host="smtp.example.com",
        email_port="587",
        email_host_user="user@example.com",
        email_host_password="correct_password",
        is_tls=False
    )

    
@pytest.fixture
def email_object():
    header = dtoSmtpService.EmailHeader(
        recipient_email=["user@example.com"],
        sender_email="user@example.com"
    )
    
    body = dtoSmtpService.EmailBody(
        content="This is a test email",
        variables={}
    )
    
    content = dtoSmtpService.EmailContent(
        subject="Test email",
        body=body,
        html_format=False
    )
    return dtoSmtpService.Email(
        header=header,
        content=content
    )
    
#### TEST IF raises VALUE ERROR WHEN config is not from type dtoSmtpService.SMTPClientConfig ####
def test_connect_smtp_raises_value_error_when_config_is_not_from_type_dtoSmtpService_SMTPClientConfig():
    with pytest.raises(ValueError):
        SMTP('invalid config')

#### TEST IF makes the right calls WHEN is TLS ####
@patch('smtplib.SMTP')
def test_connect_smtp_makes_right_calls_when_is_tls(
    mock_smtp_class,
    smtp_tls_config
    ):
    # arrange
    mock_smtp_instance = mock_smtp_class.return_value
    smtp_client = SMTP(smtp_tls_config)
    
    # act
    smtp = smtp_client.connect_smtp()
    
    # assert
    mock_smtp_class.assert_called_with( 
        host=smtp_tls_config.email_host,
        port=smtp_tls_config.email_port,
        timeout=5
    )
    
    mock_smtp_instance.starttls.assert_called_once()
    mock_smtp_instance.login.assert_called_once_with(
            smtp_tls_config.email_host_user, smtp_tls_config.email_host_password
        )
    
#### TEST IF makes the right calls WHEN is not TLS ####
@patch('smtplib.SMTP')
def test_connect_smtp_makes_right_calls_when_is_not_tls(
    mock_smtp_class,
    smtp_not_tls_config
):
    # arrange
    mock_smtp_instance = mock_smtp_class.return_value
    smtp_client = SMTP(smtp_not_tls_config)
    
    # act
    smtp = smtp_client.connect_smtp()
    
    # assert 
    mock_smtp_class.assert_called_with(
        host=smtp_not_tls_config.email_host,
        port=smtp_not_tls_config.email_port,
        timeout=5
    )
    
    mock_smtp_instance.starttls.assert_not_called()
    
    mock_smtp_instance.login.assert_called_once_with(
            smtp_not_tls_config.email_host_user, smtp_not_tls_config.email_host_password
        )
      
#### TEST IF RAISE smtplib.SMTPConnectError WHEN WRONG PORT or HOST####
@patch('smtplib.SMTP')
def test_connect_smtp_raises_connection_error_when_wrong_port_or_host(
    mock_smtp_class,
    smtp_tls_config,
    ):
    mock_smtp_class.side_effect = smtplib.SMTPConnectError(421, "Connection refused")
    smtp_client = SMTP(smtp_tls_config)
    
    with pytest.raises(smtplib.SMTPConnectError):
        smtp_client.connect_smtp()

#### TEST IF RAISE smtplib.SMTPServerDisconnected WHEN THE SERVER CLOSES CONNECTION UNEXPECTEDLY ####
@patch('smtplib.SMTP')
def test_connect_smtp_raises_server_disconnected_error_when_server_unexpectedly_disconnects(
    mock_smtp_class,
    smtp_tls_config
    ):
    mock_smtp_class.side_effect = smtplib.SMTPServerDisconnected("Server disconnected")  
    smtp_client = SMTP(smtp_tls_config)
        
    with pytest.raises(smtplib.SMTPServerDisconnected):
        smtp_client.connect_smtp()
            
#### TEST IF RAISE ValueError WHEN TRYING TO CONNECT BY TLS WHEN NOT SUPPORTED ####
@patch('smtplib.SMTP')
def test_connect_smtp_raises_value_error_when_tls_not_supported(
    mock_smtp_class, 
    smtp_tls_config
):
    mock_smtp_instance = mock_smtp_class.return_value
    mock_smtp_instance.starttls.side_effect = smtplib.SMTPNotSupportedError()

    smtp_client = SMTP(smtp_tls_config)

    with pytest.raises(smtplib.SMTPNotSupportedError):
        smtp_client.connect_smtp()
         
#### TEST IF RAISE smtplib.SMTPAuthenticationError WHEN WRONG USERNAME or PASSWORD ####
@pytest.mark.parametrize(
    "config_fixture_name",
    ["smtp_tls_config", "smtp_not_tls_config"]
)
@patch('smtplib.SMTP')
def test_connect_smtp_raises_authentication_error_when_wrong_username_or_password(
    mock_smtp_class,
    request,
    config_fixture_name
):
    # Arrange
    smtp_config = request.getfixturevalue(config_fixture_name)
    mock_smtp_instance = mock_smtp_class.return_value
    mock_smtp_instance.login.side_effect = smtplib.SMTPAuthenticationError(421, 'AUTH ERROR')

    smtp_client = SMTP(smtp_config)

    # Act + Assert
    with pytest.raises(smtplib.SMTPAuthenticationError):
        smtp_client.connect_smtp()
        
#### TEST IF RAISE ValueError WHEN EMAIL IS NOT INSTANCE OF dtoSmtpService.Email ####
@pytest.mark.parametrize(
    "config_fixture_name",
    ["smtp_tls_config", "smtp_not_tls_config"]
)
def test_send_email_raises_value_error_when_email_is_not_instance_of_dtoSmtpService_Email(
    request,
    config_fixture_name
):
    # Arrange
    smtp_config = request.getfixturevalue(config_fixture_name)
    smtp_client = SMTP(smtp_config)

    # Act + Assert
    with pytest.raises(ValueError):
        smtp_client.send_email('invalid email')
        
#### TEST IF RAISE Exception WHEN FAILED TO BUILD EMAIL OBJECT ####
@patch('packag.modules.email_service.EmailBuilder.build_email_object')
def test_send_email_raises_exception_when_failed_to_build_email_object(
    mock_build_email,
    smtp_tls_config,
    email_object
):
    mock_build_email.side_effect = Exception('Failed to build email object')
    smtp_client = SMTP(smtp_tls_config)
    
    with pytest.raises(Exception):
        smtp_client.send_email(email_object)
   
#### TEST IF RAISE smtplib.SMTPRecipientsRefused when sendmail raises smtplib.SMTPRecipientsRefused ####  
@pytest.mark.parametrize(
    "config_fixture_name",
    ["smtp_tls_config", "smtp_not_tls_config"]
)
@patch('packag.modules.email_service.SMTP.connect_smtp')  # patch your method
def test_send_email_raises_smtp_recipients_refused_when_send_mail_raises_smtp_recipients_refused(
    mock_connect_smtp,
    request,
    config_fixture_name,
    email_object
):
    # Arrange
    smtp_config = request.getfixturevalue(config_fixture_name)

    mock_smtp_instance = MagicMock()
    mock_connect_smtp.return_value.__enter__.return_value = mock_smtp_instance
    
    mock_smtp_instance.sendmail.side_effect = smtplib.SMTPRecipientsRefused({'recipient@example.com': (550, 'User unknown')})

    smtp_client = SMTP(smtp_config)

    # Act + Assert
    with pytest.raises(smtplib.SMTPRecipientsRefused):
        smtp_client.send_email(email_object)

@pytest.mark.parametrize(
    "config_fixture_name",
    ["smtp_tls_config", "smtp_not_tls_config"]
)
@patch('packag.modules.email_service.SMTP.connect_smtp')
def test_send_email_raises_smtp_recipientes_refused_when_send_mail_raises_smtp_sender_refused(
    mock_connect_smtp,
    request,
    config_fixture_name,
    email_object
):
    # Arrange
    smtp_config = request.getfixturevalue(config_fixture_name)
    
    mock_smtp_instance = MagicMock()
    mock_connect_smtp.return_value.__enter__.return_value = mock_smtp_instance
    mock_smtp_instance.sendmail.side_effect = smtplib.SMTPSenderRefused(
        554, 
        "Transaction failed",
        'Test Sender'
        )

    smtp_client = SMTP(smtp_config)

    # Act + Assert
    with pytest.raises(smtplib.SMTPSenderRefused):
        smtp_client.send_email(email_object)
    
@pytest.mark.parametrize(
    "config_fixture_name",
    ["smtp_tls_config", "smtp_not_tls_config"]
)
@patch('packag.modules.email_service.SMTP.connect_smtp')
def test_send_email_raises_smtp_data_error_when_sendmail_fails(
    mock_connect_smtp,
    request,
    config_fixture_name,
    email_object
):
    # Arrange
    smtp_config = request.getfixturevalue(config_fixture_name)
    
    mock_smtp_instance = MagicMock()
    mock_connect_smtp.return_value.__enter__.return_value = mock_smtp_instance
    mock_smtp_instance.sendmail.side_effect = smtplib.SMTPDataError(554, "Transaction failed")

    smtp_client = SMTP(smtp_config)

    # Act + Assert
    with pytest.raises(smtplib.SMTPDataError):
        smtp_client.send_email(email_object)
        
@pytest.mark.parametrize(
    "config_fixture_name",
    ["smtp_tls_config", "smtp_not_tls_config"]
)
@patch('packag.modules.email_service.SMTP.connect_smtp')  # patch your connect_smtp
def test_send_email_successfully(
    mock_connect_smtp,
    request,
    config_fixture_name,
    email_object
):
    # Arrange
    smtp_config = request.getfixturevalue(config_fixture_name)

    mock_smtp_instance = MagicMock()
    mock_connect_smtp.return_value.__enter__.return_value = mock_smtp_instance
    
    smtp_client = SMTP(smtp_config)

    # Act
    smtp_client.send_email(email_object)

    # Assert
    mock_smtp_instance.sendmail.assert_called_once()
    
    


    
    
    
    
    
    



















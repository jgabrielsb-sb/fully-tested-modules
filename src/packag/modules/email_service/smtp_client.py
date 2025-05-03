import smtplib
from packag.models.email_service import dtoSmtpService
from packag.utils.logger import get_logger
from packag.modules.email_service import EmailBuilder

email_service_logger = get_logger('email_service')
class SMTP:
    def __init__(self, config: dtoSmtpService.SMTPClientConfig) -> None:
        if not isinstance(config, dtoSmtpService.SMTPClientConfig):
            raise ValueError("Config must be a SMTPClientConfig")

        self.config = config

    def connect_smtp(self) -> smtplib.SMTP:
        """
        Connect to the email server.

        Returns:
            smtplib.SMTP: The SMTP connection object.

        Raises:
            ValueError: If TLS is required but not supported.
            ConnectionError: If the server cannot be reached.
            smtplib.SMTPAuthenticationError: If login fails.
        """
        
        # CONNECT TO SMTP SERVER
        try:
            smtp = smtplib.SMTP(
                host=self.config.email_host, port=self.config.email_port, timeout=5
            )
            email_service_logger.info(
                f"Connected to SMTP server {self.config.email_host}:{self.config.email_port}"
            )
        except (smtplib.SMTPConnectError) as e:
            email_service_logger.error(f"Connection to SMTP server failed: {e}")
            raise
        except smtplib.SMTPServerDisconnected as e:
            email_service_logger.error(f"SMTP server disconnected: {e}")
            raise
        
        # TLS CONNECTION
        if self.config.is_tls:
            try:
                smtp.starttls()
                email_service_logger.info("Started TLS connection.")
            except smtplib.SMTPNotSupportedError as e:
                email_service_logger.error("TLS not supported by server.")
                raise 

        # LOGIN TO SMTP SERVER
        try:
            smtp.login(self.config.email_host_user, self.config.email_host_password)
            email_service_logger.info(
                f"Logged in to SMTP server as {self.config.email_host_user}"
            )
        except smtplib.SMTPAuthenticationError as e:
            email_service_logger.error(f"SMTP login failed: {e}")
            raise
        
        return smtp
    
    def send_email(self, email: dtoSmtpService.Email) -> None:
        """
        Send an email.
        """
        if not isinstance(email, dtoSmtpService.Email):
            raise ValueError("Email must be an instance of dtoSmtpService.Email")

        try:
            email_builder = EmailBuilder(email)
            email_object = email_builder.build_email_object()
        except Exception as e:
            email_service_logger.error(f"Failed to build email object: {e}")
            raise
        
        with self.connect_smtp() as smtp:   # automatically closes the connection after the block is executed
            try:
                smtp.sendmail(
                    from_addr=email_object["From"],
                    to_addrs=email_object["To"],
                    msg=email_object.as_string(),
                )
                email_service_logger.info(f"Email sent from {email_object['From']} to {email_object['To']}")
            except smtplib.SMTPRecipientsRefused as e:
                email_service_logger.error(f"All recipients were refused: {e.recipients}")
                raise
            except smtplib.SMTPSenderRefused as e:
                email_service_logger.error(f"Sender address refused: {e}")
                raise
            except smtplib.SMTPDataError as e:
                email_service_logger.error(f"SMTP server responded with an error: {e}")
                raise
            
            

    

     
            
        

        

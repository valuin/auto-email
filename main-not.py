import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import csv

load_dotenv()

class EmailSender:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        # For Gmail
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_rejection_email(self, recipient: dict) -> bool:
        try:
            message = MIMEMultipart('related')
            message['Subject'] = "Application Result for Calon Pengurus KSM Android 2025"
            message['From'] = self.email
            message['To'] = recipient['email']

            # Create the HTML content part
            html_part = MIMEMultipart('alternative')
            message.attach(html_part)

            # Attach the HTML content
            html_content = self._create_email_content(name=recipient['name'])
            html_part.attach(MIMEText(html_content, 'html'))

            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable TLS
                server.login(self.email, self.password)
                server.send_message(message)
            
            return True
        except Exception as e:
            print(f"Error sending email to {recipient['email']}: {str(e)}")
            return False

    def test_email_template(self, name: str) -> None:
        """Save the rejection email template to a file for testing"""
        html_content = self._create_email_content(name=name)
        
        with open('test_rejection_email.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("Test rejection email template saved to 'test_rejection_email.html'")
    
    def _create_email_content(self, name: str) -> str:
        """Create HTML content for the rejection email"""
        return f"""
        <html>
            <head>
                <style>
                    .container {{
                        max-width: 1000px;
                        margin: 0 auto;
                        background-color: #f3f3f3;
                        padding: 20px;
                        font-family: Arial, sans-serif;
                    }}
                    img {{
                        width: 100%;
                        max-width: 1000px;
                        display: block;
                        margin: 0 auto;
                    }}
                </style>
            </head>
            <body style="margin: 0; padding: 0; background-color: #ffffff;">
                <div class="container">
                    <img src="https://i.imgur.com/e1mU9pN.jpeg" alt="Email Header">
                    <div style="padding: 20px;">
                        <h1>Thank You for Your Application, {name}</h1>
                        
                        <p>Kami menghargai minat Anda untuk bergabung sebagai Calon Pengurus KSM Android 2025.</p>

                        <p>Setelah pertimbangan yang cermat, dengan berat hati kami informasikan bahwa saat ini kami belum dapat melanjutkan proses aplikasi Anda.</p>

                        <p>Kami mendorong Anda untuk tetap terhubung dan mempertimbangkan untuk mendaftar kembali di masa mendatang atau mendaftar sebagai panitia di proker kami mendatang.</p>

                        <p>Terima kasih atas waktu dan usaha Anda.</p>
                        
                        <p>Jika Anda memilik pertanyaan, silahkan hubungi kontak di bawah:</p>
                        <ul>
                            <li>Rafa (rapaa / 081292859754)</li>
                            <li>Kela (kayylisha / 087811830315)</li>
                        </ul>

                        <p>Salam hangat,<br>
                        Kabinet Growth Catalyst</p>

                        <p>#BlossomTogether</p>
                    </div>
                </div>
            </body>
        </html>
        """

def main():
    # Get email credentials from environment variables
    EMAIL = os.getenv('EMAIL')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    
    if not EMAIL or not EMAIL_PASSWORD:
        raise ValueError("Please set EMAIL and EMAIL_PASSWORD environment variables")
    
    # Read recipients from CSV file
    recipients = []
    try:
        with open('auto-mail/anti-recipients.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            recipients = list(reader)
    except FileNotFoundError:
        print("Error: anti-recipients.csv not found!")
        return
    
    # Initialize email sender
    sender = EmailSender(EMAIL, EMAIL_PASSWORD)
    
    # Send emails to all recipients
    for recipient in recipients:
        success = sender.send_rejection_email(recipient)
        if success:
            print(f"✓ Email sent successfully to {recipient['email']} ({recipient['name']})")
        else:
            print(f"✗ Failed to send email to {recipient['email']} ({recipient['name']})")

if __name__ == "__main__":
    main()
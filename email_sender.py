import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_followup_email(sender_email, recipient_email, company_name, position, sender_password=None):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    if not sender_password:
        import os
        sender_password = os.environ.get('EMAIL_PASSWORD')
    
    if not sender_password:
        print("Error: Email password not set.")
        return False
    
    subject = f"Following Up - {position} Application"
    
    html_content = f'''
    <html>
    <body>
        <p>Dear Hiring Manager,</p>
        
        <p>I hope this email finds you well. I recently applied for the 
        <strong>{position}</strong> position at <strong>{company_name}</strong> 
        and wanted to follow up on my application.</p>
        
        <p>I am very enthusiastic about the opportunity to join your team and 
        would love to discuss how my skills align with your needs.</p>
        
        <p>Please let me know if you need any additional information from my side.</p>
        
        <p>Kind regards</p>
    </body>
    </html>
    '''
    
    email = MIMEMultipart()
    email['From'] = sender_email
    email['To'] = recipient_email
    email['Subject'] = subject
    email.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, email.as_string())
        server.quit()
        print(f"Follow-up email sent to {company_name}!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
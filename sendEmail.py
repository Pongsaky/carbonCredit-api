# Import smtplib, MIMEMultipart, MIMEText, and getpass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass

# Create a MIMEMultipart object
msg = MIMEMultipart()

# Set the sender, recipient, subject, and headers
sender = "sender@gmail.com"
recipient = "recipient@gmail.com"
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = "Test HTML Email"
msg['X-Mailer'] = "Python"

# Create a MIMEText object for plain text
plain_text = "Hi,\nThis is a test email.\nHere is the link you wanted:\nhttps://www.python.org"
part1 = MIMEText(plain_text, 'plain')

# Create a MIMEText object for HTML
html_text = """
<html>
  <head></head>
  <body>
    <h1>Hello My name is นายพงศกร แก้วใจดี</h1>
    <p>Hi,<br>
       This is a test email.<br>
       Here is the <a href="https://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""
part2 = MIMEText(html_text, 'html')

# Attach both parts to the message
msg.attach(part1)
msg.attach(part2)

# Create an SMTP object
smtp = smtplib.SMTP('smtp.gmail.com', 587)

# Start TLS encryption
smtp.starttls()

# Log in with your Gmail username and password
username = sender
# password = getpass("Enter your password: ")
password = "Your SMTP password"
smtp.login(username, password)

# Send the email message
smtp.sendmail(sender, recipient, msg.as_string())

# Close the SMTP connection
smtp.quit()

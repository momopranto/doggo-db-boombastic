''' The following script could be used to send a temporary new password
to a user if the user forgets their password.
A dummy Yahoo email was made, cs3083MRM@yahoo.com
The password for it is NYUcs3083.
STILL TO BE DONE: generate a random temp password and update the user's
password in the DB with the temp password '''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

username = 'cs3083MRM'
password = 'NYUcs3083'
print "connecting"
server = smtplib.SMTP('android.smtp.mail.yahoo.com', port=587)
print "connected"
server.starttls()
print "logging in"
server.login(username, password)
print "logged in, sending"

fromaddr = 'cs3803MRM@yahoo.com'
toaddr = 'cs3083MRM@yahoo.com'
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['Subject'] = "Your Secret Santa assignment has arrived!"
msg['To'] = toaddr
body = """
<h1> Forgot your password? Use this temporary password to log in. </h1>
<h3> Your temporary password is: </h3>
</body>
"""
msg.attach(MIMEText(body, 'html'))
server.sendmail(fromaddr, toaddr, msg.as_string())
    

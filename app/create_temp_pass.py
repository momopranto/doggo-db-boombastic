''' The following script could be used to send a temporary new password
to a user if the user forgets their password.
A dummy Yahoo email was made, cs3083MRM@yahoo.com
The password for it is NYUcs3083.
STILL TO BE DONE: generate a random temp password and update the user's
password in the DB with the temp password '''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

temporary = "new password goes here"

username = 'cs3083MRM@yahoo.com'
password = 'NYUcs3083'
print "connecting"
server = smtplib.SMTP('smtp.mail.yahoo.com', port=587)
print "connected"
server.starttls()
print "logging in"
server.login(username, password)
print "logged in, sending"

fromaddr = 'cs3083MRM@yahoo.com'
toaddr = 'mattr2496@yahoo.com'
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['Subject'] = "Findfolks - Requested a Password Change"
msg['To'] = toaddr
body = """
<h3> Forgot your password? Use this temporary password to log in. </h3>
<h2> Your temporary password is: %s</h2>
</body>
""" % temporary
msg.attach(MIMEText(body, 'html'))
server.sendmail(fromaddr, toaddr, msg.as_string())
    

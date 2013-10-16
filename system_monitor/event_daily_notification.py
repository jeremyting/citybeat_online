#!/usr/bin/python
import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_email():
    #user = "xieke.buaa"
    #pw = "yjxkk131415"
    sender = 'xieke.buaa@gmail.com'
    receivers = ['cx28@cs.rutgers.edu']

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receivers)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'event list'

    #message = msg
    msg.attach( MIMEText('Please see attachment') )

    file = 'monitor.sh'
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(file,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
    msg.attach(part)

    print 'ok'

    try:
    #smtpObj = smtplib.SMTP('localhost')
    #smtpObj.sendmail(sender, receivers, message)
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo
        smtp.login('oeddyo@gmail.com', 'yueyue-0105&love')
        smtp.sendmail(sender, receivers, msg.as_string())
        print "Successfully sent email"
    except Exception, e:
        print str(e)


send_email()
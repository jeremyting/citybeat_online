#!/usr/bin/python
import csv
import smtplib
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.event_interface import EventInterface
from utility.config import InstagramConfig
from utility.tool import getCurrentStampUTC

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

csv_file = 'all_classified_events.csv'

def findLast24HourEvents():
    ei = EventInterface()
    ei.setCollection(InstagramConfig.front_end_events)

    now = int(getCurrentStampUTC())
    # for merge reason, delay one hour
    offset = 60 * 60
    end_time = now - offset
    begin_time = end_time - 24 * 3600

    conditions = {'created_time':{'$gte':str(begin_time), '$lte':str(end_time)}}
    fields = ['_id']
    cur = ei.getAllFields(fields=fields, condition=conditions)

    event_count = 0
    with open(csv_file, 'wb') as csvfile:
        event_writer = csv.writer(csvfile, delimiter=',')
        events = []
        for event in cur:
            url = 'http://ec2-23-22-67-45.compute-1.amazonaws.com/cb/event/' + str(event['_id'])
            events.append([url])
            event_count += 1
        event_writer.writerows(events)

    return event_count

def send_email(count):
    #user = "xieke.buaa"
    #pw = "yjxkk131415"
    sender = 'xieke.buaa@gmail.com'
    receivers = ['cx28@cs.rutgers.edu', 'cx28@eden.rutgers.edu']# ., 'aak2128@columbia.edu', 'raz.schwartz@cornell.edu']

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receivers)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'event list'

    text = 'This is an automatic email, please do not reply. ' \
           'You may wish to contact cx28@eden.rutgers.edu for any issue. ' \
           'The attachment includes %d events during the past 24 hours.' % (count)
    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(csv_file,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(csv_file))
    msg.attach(part)

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
        print 'Unable to send this email' + str(e)


if __name__ == '__main__':
    count = findLast24HourEvents()
    send_email(count)
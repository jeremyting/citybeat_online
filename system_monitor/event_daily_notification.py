#!/usr/bin/python
import smtplib

def send_email(msg):
    user = "xieke.buaa"
    pw = "yjxkk131415"
    sender = 'xieke.buaa@gmail.com'
    receivers = ['cx28@cs.rutgers.edu']

    message = msg
    try:
    #smtpObj = smtplib.SMTP('localhost')
    #smtpObj.sendmail(sender, receivers, message)
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo
        smtp.login('oeddyo@gmail.com', 'yueyue-0105&love')
        smtp.sendmail(sender, receivers, message)
        print "Successfully sent email"
    except Exception, e:
        print str(e)


send_email('hi')
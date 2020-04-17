import smtplib
import threading


"""
This python file sends emails and works in the background. 
This is achieved through threads.
The mail is sent through a SMTP server hosted by google.
"""


# Sends the mail
def mail(msg, l):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("****", "****")

    # message to be sent
    message = msg

    # sending the mail
    for i in l:
        s.sendmail("anpmriet@gmail.com", i, message)

    print("Mails sent")

    # terminating the session
    s.quit()


# Creates a thread to run the process in the background
def send_email(msg, l):
    print("thread")
    thr = threading.Thread(target=mail, args=[msg, l])
    thr.start()


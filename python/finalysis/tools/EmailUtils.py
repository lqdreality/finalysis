import smtplib
import json

def send_gmail(subject,
               msg,
               param_file=None,
               sender=None,
               recipients=None,
               pw=None,
               ssl=True) :

    # if param file is supplied, load it
    if param_file is not None :
        pass #todo

    # Marshal over the inputs before connecting
    if sender is None :
        raise ValueError('sender cannot be None')
    if recipients is None :
        raise ValueError('recipients cannot be None')
    elif isinstance(recipients, str) :
        recipients = [recipients]
    message = ''

    # Instaniate the SMTP object
    if ssl :
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    else :
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # will run .ehlo

    # Login
    try :
        server.login(sender, pw)
    except smtplib.SMTPAuthenticationError as e :
        print(e)
        return None

    # Append the necessary From/To Headers to the message
    message += 'From: ' + sender + '\r\n'
    message += 'To: '
    for i in range(0, len(recipients)) :
        if i+1 < len(recipients) :
            message += recipients[i] + ', '
        else :
            message += recipients[i] + '\r\n'
    message += 'Content-type: text/html\r\n' # assumed for now
    message += 'Subject: ' + subject + '\r\n'

    message += msg

    # Send the message
    try :
        server.sendmail(sender, recipients, message)
    except smtplib.SMTPSenderRefused as e :
        print(e)
        return None
    except smtplib.SMTPRecipientsRefused as e :
        print(e)
        return None
    except smtplib.SMTPDataError as e :
        print(e)
        return None

    # Close the server
    server.close()

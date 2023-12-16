import smtplib, ssl
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication
import csv


def flatten(l):
    return [item for sublist in l for item in sublist]


email_csv = input("write the path of emails file: ")

recievers =[]

with open(email_csv) as file:
        reader = csv.reader(file)
        next(reader)
        for email in reader:
                recievers.append(email)
        recievers = flatten(recievers)

email = input("write your email address: ")
password =  input("write your password: ")

if email.split('@')[1].split('.')[0] in ['hotmail', 'live', 'outlook']:
    smtp_server = 'smtp-mail.outlook.com'
elif email.split('@')[1].split('.')[0] == 'gmail':
    smtp_server = 'smtp.gmail.com'
smtp_port = 587

attachmentPath = input("attachment path")

name = input('write your name in the From box')

for x in recievers:
        message = MIMEMultipart('mixed')
        message['From'] = f'{name.title()}  <{email}>'
        message['Subject'] = 'My CV'
        message['To'] = str(x)#.join(reciever)
        reciever = str(x)

        msg_content = f'<p>Hello Dear,<br> Kindly find my C.V. in attachments. <br>I hope to get an opportunity to work by your company.<br>Best Regards,<br> {name.split()[0].capitalize()}.</p>\n'
        body = MIMEText(msg_content, 'html')
        message.attach(body)

        try:
                with open(attachmentPath, "rb") as attachment:
                        p = MIMEApplication(attachment.read(),_subtype="pdf")	
                        p.add_header('Content-Disposition', "attachment; filename= %s" % 'My_CV.pdf') 
                        message.attach(p)
        except Exception as e:
                print(str(e))

        context = ssl.create_default_context()
        msg_full = message.as_string()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()  
                server.starttls(context=context)
                server.ehlo()
                server.login(email, password)
                server.sendmail(email, reciever, msg_full)
                server.quit()
        print(f"email sent out to {x} successfully")


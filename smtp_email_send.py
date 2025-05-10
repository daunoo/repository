import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

sender_email = "202211680150@stu.blcu.edu.cn"
recipient_email = "202311680374@stu.blcu.edu.cn"  # 收件人邮件地址
password = "Wu20040903"  # 如果是QQ邮箱，请使用授权码
smtp_server = "smtp.stu.blcu.edu.cn"  # SMTP服务器地址
smtp_port = 587  # SMTP服务器端口
subject = "SMTP实验邮件"
content = "这是一封通过SMTP协议发送的实验邮件。"

message = MIMEMultipart()
message['From'] = Header(sender_email, 'utf-8')
message['To'] = Header(recipient_email, 'utf-8')
message['Subject'] = Header(subject, 'utf-8')

message.attach(MIMEText(content, 'plain', 'utf-8'))

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # 启动TLS加密
    server.login(sender_email, password)
    server.sendmail(sender_email, recipient_email, message.as_string())  # 修正拼写错误
    print("邮件发送成功！")
    server.quit()
except smtplib.SMTPException as e:
    print(f"邮件发送失败，错误信息：{e}")
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv
# import os

# load_dotenv()

# class EmailSender:
#     def __init__(self):
#         self.sender_email = "nitish.vinove@gmail.com"
#         self.sender_password = os.getenv("EMAIL_APP_PASSWORD")
    
#     def send_email(self, receiver_email, subject, body):
#         try:
#             msg = MIMEMultipart()
#             msg['From'] = self.sender_email
#             msg['To'] = receiver_email
#             msg['Subject'] = subject
#             msg.attach(MIMEText(body, 'html'))
            
#             with smtplib.SMTP('smtp.gmail.com', 587) as server:
#                 server.starttls()
#                 server.login(self.sender_email, self.sender_password)
#                 server.sendmail(self.sender_email, receiver_email, msg.as_string())
#                 print("Email sent successfully!")
#         except Exception as e:
#             print(f"Error sending email: {e}")


# if __name__ == "__main__":
#     receiver_email = "nitish.kumar5@mail.vinove.com"
#     subject = "Event Booked2"
#     body = "Event Booked Successfully: Thank you for using Vinove Customer Support Chatbot."
    
#     email_sender = EmailSender()
#     email_sender.send_email(receiver_email, subject, body)
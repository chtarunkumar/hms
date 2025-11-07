from app.emailer import send_gmail
from app.config import to_address

send_gmail(to_address, "Testing Purpose", "Mail Sent Successfully")
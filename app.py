from flask import Flask, render_template, request
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env locally
load_dotenv()

app = Flask(__name__)

# -----------------------
# Routes
# -----------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    try:
        send_contact_email(name, email, message)
        feedback = "Thank you. We'll respond deliberately."
    except Exception as e:
        print(f"Email send failed: {e}")
        feedback = "Sorry, there was a problem sending your message."

    return feedback

# -----------------------
# Email Logic
# -----------------------

def send_contact_email(name, email, message):
    # Pull config from environment
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    receiver = os.getenv("CONTACT_RECEIVER")

    msg = EmailMessage()
    msg["Subject"] = "New Contact Request — Sigma14"
    msg["From"] = smtp_user
    msg["To"] = receiver
    msg["Reply-To"] = email

    msg.set_content(f"""
New contact submission received.

Name: {name}
Email: {email}
Message:
{message}
""")

    # Send via SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()              # Secure the connection
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

# -----------------------
# Entry Point
# -----------------------

#if __name__ == "__main__":
#    app.run(debug=True)

if __name__ == "__main__":
    import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False
    )

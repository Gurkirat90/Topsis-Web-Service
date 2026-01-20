from flask import Flask, render_template, request
import os
import re
import smtplib
from email.message import EmailMessage
from topsis import run_topsis

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

def is_valid_email(email):
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", email)

def send_email(to_email, attachment_path):
    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result File"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content("Please find attached the TOPSIS result file.")

    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="topsis_result.csv"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        weights = request.form.get("weights")
        impacts = request.form.get("impacts")
        email = request.form.get("email")

        if not all([file, weights, impacts, email]):
            return "All fields are required"

        if not is_valid_email(email):
            return "Invalid email format"

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(RESULT_FOLDER, "topsis_result.csv")

        file.save(input_path)

        run_topsis(input_path, weights, impacts, output_path)
        send_email(email, output_path)

        return "✅ Result has been sent to your email successfully!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

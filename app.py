from flask import Flask, render_template, request, send_file
import os
import re
from topsis import run_topsis   # make sure this function exists in topsis.py

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def is_valid_email(email):
    """Validate email format"""
    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    return re.match(pattern, email)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        weights = request.form.get("weights")
        impacts = request.form.get("impacts")
        email = request.form.get("email")

        if not file or not weights or not impacts or not email:
            return "All fields are required"

        if not is_valid_email(email):
            return "Invalid email format"

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(RESULT_FOLDER, "topsis_result.csv")

        file.save(input_path)

        # Run TOPSIS
        run_topsis(input_path, weights, impacts, output_path)

        # Return file for download
        return send_file(
            output_path,
            as_attachment=True,
            download_name="topsis_result.csv"
        )

    return render_template("index.html")


# REQUIRED FOR RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

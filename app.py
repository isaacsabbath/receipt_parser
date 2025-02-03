from flask import Flask, request, render_template, jsonify
import cv2
import os
from main import preprocess_image, extract_text, ai_extract

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        file = request.files["file"]
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Process receipt image
            processed_image = preprocess_image(file_path)
            text_content = extract_text(processed_image)
            json_data = ai_extract(text_content)

            # Return JSON response
            return jsonify({"parsed_receipt": json_data})
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

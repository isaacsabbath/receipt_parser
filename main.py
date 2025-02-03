import cv2
import pytesseract
import os
import google.generativeai as genai
from flask import Flask
from dotenv import load_dotenv
from PIL import Image

load_dotenv()


ai_client = genai.configure(api_key=os.environ["GEMINI_API_KEY"], transport='rest')

def preprocess_image(image):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return threshold


def extract_text(image):
	return pytesseract.image_to_string(image)


def ai_extract(text_content):

	prompt = """You are a receipt parser AI. I am going to provide tou with text extracted from an image of a store receipt.
	I need you to return a JSON  object wuth this structure:
	{"total", "business", "items":[{"title", "quantity", "price"}], "transcation_timestamp"}.
	Return the prices as integers that represent the number of shillings($1 = 100) Only return the JSON object.
	Do not return anything else.Here is the text extracted from the receipt: """

	generation_config = {
	"temperature": 1,
	"top_p": 0.95,
	"top_k": 40,
	"max_output_tokens": 8192,
	"response_mime_type": "text/plain",
	}

	model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config,)

	chat_session = model.start_chat(history = [
		])

	response = chat_session.send_message({"parts": [{"text":prompt}]})

	return response.text.strip()
   

	if __name__ == '__main__':
		image_path = "receipt.jpg"

		preprocess_image = preprocess_image(image_path)

		text_content = extract_text(preprocess_image)
		json_data = ai_extract(text_content)

		with open('receipt.json', 'w') as f:
			f.write(json_data)
The project is a Flask-based web application that allows users to upload a receipt image (in JPG format). It then processes the image, extracts text from it, and uses Google's Gemini API to generate structured data in JSON format, including:
- Business Name
- Total Amount
- Transaction Timestamp
- Itemized Purchase List (with item names, quantities, and prices)

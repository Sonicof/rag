from google.cloud import vision
import io

# Initialize client using the service account JSON key directly
client = vision.ImageAnnotatorClient.from_service_account_file('firebaseSecretKey.json')

# Load image file
with io.open("screenshots/dr-arunkumar.png", 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Perform text detection
response = client.text_detection(image=image)
texts = response.text_annotations

# Print extracted text
if texts:
    print("🔍 Extracted Text:\n")
    print(texts[0].description)
else:
    print("No text found.")

# Handle errors
if response.error.message:
    raise Exception(f'{response.error.message}')

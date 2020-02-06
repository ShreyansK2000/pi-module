import requests
import os

subscription_key = "4de40c2867a54d2381f77ac810c2035f"
analyze_url = "https://7bvision.cognitiveservices.azure.com/vision/v2.1/detect"

# Set image_path to the local path of an image that you want to analyze.
image_path = "object-detection/image_input.png"

# Read the image into a byte array
image_data = open(image_path, "rb").read()
headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
params = {'visualFeatures': 'Categories,Description,Color'}
response = requests.post(
    analyze_url, headers=headers, params=params, data=image_data)
response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
print(analysis)

f = open("object-detection/image_response.txt","w+")
f.write(str(response.json()))
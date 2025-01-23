import requests

url = "http://127.0.0.1:8000/api/v1/process-images"

payload = {
    "input_type": "local_folder",
    "path": "C:/Users/91830/Documents/image_analysis/images",  # Use forward slashes
    # OR "path": "C:\\Users\\91830\\Documents\\image_analysis\\images",  # Use double backslashes
    "api_key": "app-53gFeCZttFUyoMs0HuL0eNyc"  # Your Dify AI API key
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    result = response.json()
    print("Success!")
    print(f"Excel file: {result['excel_path']}")
    print(f"PDF file: {result['pdf_path']}")
    print(f"Message: {result['message']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
import requests, os
from dotenv import load_dotenv
load_dotenv()

url = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
r = requests.post(url, headers=headers, json={"inputs": "hola"})
print(r.status_code)
print(r.text)
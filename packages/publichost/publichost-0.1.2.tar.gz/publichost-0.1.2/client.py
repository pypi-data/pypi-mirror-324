# backend/client.py
from flask import Flask
from publichost import Tunnel
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add basic logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    # Ensure proper env variables are set
    tunnel = Tunnel(port=5000)
    print(f"Public URL: {tunnel}")
    app.run(port=5000)
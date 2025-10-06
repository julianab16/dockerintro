from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)
student = os.getenv("STUDENT_NAME", "Anon")
hood = os.getenv("BARRIO", "Unknown")

@app.get("/")
def home():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"Hola, I am {student} and I live in {hood}"
    
    # Log the visit to the shared volume
    try:
        with open("/var/log/app/visitas.log", "a") as f:
            f.write(f"[{timestamp}] {msg}\n")
    except Exception as e:
        print(f"Error writing to log: {e}")
    
    return msg

@app.get("/health")
def health():
    return {"ok": True, "student": student, "barrio": hood}, 200

if __name__ == "__main__":
    print(f"Starting service for {student} in {hood}")
    app.run(host="0.0.0.0", port=8080, debug=False)
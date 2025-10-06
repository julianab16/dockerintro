# 📘 README: *Cali Container City Lab*

## 🎯 Objective
In this lab, every student will design and **build their own Docker image**, publish it to **Docker Hub or GitHub Packages**, and then run a container from that image.  
Each container will live in a **neighborhood (Docker network)** and will log its activity into the shared **La Biblioteca del Pueblo** volume.  
Additionally, students must collaborate using **Git trunk-based development** with a shared repository, where each student contributes their own component inside a dedicated folder.

The goal is to learn **networks**, **volumes**, **image publishing**, and **team collaboration with Git**, while being creative with your container design.

---

## 🏙️ The Cali Neighborhoods & La Biblioteca
- Each **network** will represent a **neighborhood in Cali** (e.g., *San Antonio*, *Granada*, *Ciudad Jardín*, *San Fernando*).  
- There will be a **shared volume** called **“La Biblioteca del Pueblo”** where all services will log their visits.  
- Just like in real Cali, services from one neighborhood cannot directly reach another neighborhood unless explicitly connected.  
- **Note:** These names are suggestions. You are free to use **any names** for your networks, containers, or images.  

---

## 🛠️ Lab Setup (leader)
Create networks and the shared volume once:

```bash
docker network create san-antonio
docker network create granada
docker network create ciudad-jardin
docker volume create biblioteca-del-pueblo
```

---

## 👩‍💻 Student Task

### Step 1: Repository structure with Git trunk strategy
- The team will work on **one shared Git repository** using **trunk-based development**.  
- Students will create **short-lived branches from `main`** and merge back quickly with small, tested contributions (via Pull Requests).  
- Each student must create a folder under `/students/<your-name>/` with their component definition (Dockerfile, code, dependencies). Example:

```
/students/
  ├── ana/
  │    ├── Dockerfile
  │    ├── app.py
  │    └── requirements.txt
  ├── carlos/
  │    ├── Dockerfile
  │    └── index.html
  └── diana/
       ├── Dockerfile
       ├── server.js
       └── package.json
```

This ensures clear ownership, easy reviews, and modular design.

---

### Step 2: Build your own service
Each student must create a **simple service** that:
1. Listens on port `8080`.  
2. Responds with a message like:  
   ```
   Hola, I am <YourName> and I live in <Neighborhood>
   ```  
3. Logs every request into `/var/log/app/visitas.log` (mounted from the shared volume).  

---

### Step 3: Choose your tech stack (examples to keep)
You can use any language or server. **Keep these examples in the repo** so students can start faster or compare approaches.

#### 🔹 Python (Flask)
`/students/<your-name>/app.py`
```python
from flask import Flask
import os

app = Flask(__name__)
student = os.getenv("STUDENT_NAME", "Anon")
hood = os.getenv("BARRIO", "Unknown")

@app.get("/")
def home():
    msg = f"Hola, I am {student} and I live in {hood}"
    with open("/var/log/app/visitas.log", "a") as f:
        f.write(msg + "\n")
    return msg

@app.get("/health")
def health():
    return {"ok": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```
`/students/<your-name>/requirements.txt`
```
flask==3.0.3
```
`/students/<your-name>/Dockerfile`
```Dockerfile
FROM python:3.12-alpine
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN mkdir -p /var/log/app && chown -R app:app /var/log/app
USER app
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
  CMD wget -qO- http://localhost:8080/health >/dev/null || exit 1
CMD ["python","/app/app.py"]
```

#### 🔹 Node.js (Express)
`/students/<your-name>/server.js`
```javascript
const express = require('express');
const fs = require('fs');
const app = express();

const student = process.env.STUDENT_NAME || "Anon";
const hood = process.env.BARRIO || "Unknown";

app.get('/', (req, res) => {
  const msg = `Hola, I am ${student} and I live in ${hood}`;
  fs.appendFileSync('/var/log/app/visitas.log', msg + '\n');
  res.type('text/plain').send(msg);
});

app.get('/health', (req, res) => res.json({ ok: true }));

app.listen(8080, () => console.log("Server running on 8080"));
```
`/students/<your-name>/package.json`
```json
{
  "name": "cali-service",
  "private": true,
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.19.2"
  }
}
```
`/students/<your-name>/Dockerfile`
```Dockerfile
FROM node:20-alpine
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app
COPY package.json ./
RUN npm ci --omit=dev
COPY server.js ./
RUN mkdir -p /var/log/app && chown -R app:app /var/log/app
USER app
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
  CMD wget -qO- http://localhost:8080/health >/dev/null || exit 1
CMD ["node","server.js"]
```

#### 🔹 Nginx (Static HTML)
`/students/<your-name>/index.html`
```html
<h1>Hola, I am Ana and I live in San Antonio</h1>
```
`/students/<your-name>/Dockerfile`
```Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
# (Static example: no custom log writes; OK for the message demo)
```

---

### Step 4: Build and publish your image
Students must tag and push their images under their account:

```bash
# Docker Hub example
docker build -t your-dockerhub-username/cali-service:v1 ./students/<your-name>
docker push your-dockerhub-username/cali-service:v1

# GitHub Packages example
from flask import Flask
import os

app = Flask(__name__)
student = os.getenv("STUDENT_NAME", "Anon")
hood = os.getenv("BARRIO", "Unknown")

@app.get("/")
def home():
    msg = f"Hola, I am {student} and I live in {hood}"
    with open("/var/log/app/visitas.log", "a") as f:
        f.write(msg + "\n")
    return msg

@app.get("/health")
def health():
    return {"ok": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)docker push ghcr.io/your-username/cali-service:v1
```
*(For GitHub Packages, ensure you’re logged in with a PAT and `docker login ghcr.io`.)*

---

### Step 5: Run your service in your neighborhood
Each student runs a container from their **published image** (names below are examples; feel free to customize):

```bash
docker run -d --name svc-ana \
  --network san-antonio \
  -e STUDENT_NAME="Ana" \
  -e BARRIO="San Antonio" \
  -v biblioteca-del-pueblo:/var/log/app \
  -p 0:8080 your-dockerhub-username/cali-service:v1
```

---

### Step 6: Test connectivity
```bash
# From host
curl http://localhost:<port>

# From another container in the same neighborhood
docker run --rm --network san-antonio curlimages/curl -s http://svc-ana:8080/
```

---

### Step 7: Check “La Biblioteca del Pueblo”
Verify that logs are being written:

```bash
docker run --rm -v biblioteca-del-pueblo:/data alpine \
  sh -c "tail -n 20 /data/visitas.log"
```

Or enter the volume:
```bash
docker run --rm -it -v biblioteca-del-pueblo:/data alpine sh
```

---

## ✅ What you will learn
- How to **collaborate as a team using trunk-based Git strategy**.  
- How to **build and publish Docker images** to Docker Hub or GitHub Packages.  
- How **Docker networks** isolate and connect services.  
- How **volumes** allow sharing and persistence of data.  
- How collaboration looks when multiple services write to the same shared space.  

---

# 📌 Deliverables
- A folder in the shared repo `/students/<your-name>/` with Dockerfile, code, and dependencies.  
- A published Docker image (Docker Hub or GitHub Packages).  
- A working container in your chosen neighborhood.  
- Evidence that your service wrote to **La Biblioteca del Pueblo**.  
- Short explanation of your design choice (Python, Node.js, Nginx, etc).  
- Optional: use your **own names** for networks, images, and containers to make the demo personal.  

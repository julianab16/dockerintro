# 📘 README: *Cali Container City Lab*

## 🎯 Objective
In this lab, every student will design their own **Docker container service**, place it in a **neighborhood (Docker network)**, and write their activity logs into a **shared library (Docker volume)**.

The goal is to understand how to use **Docker networks** (for communication and isolation) and **Docker volumes** (for persistence and sharing) while being creative with your container design.

---

## 🏙️ The Cali Neighborhoods & La Biblioteca
- Each **network** will represent a **neighborhood in Cali** (e.g., *San Antonio*, *Granada*, *Ciudad Jardín*, *San Fernando*).
- There will be a **shared volume** called **“La Biblioteca del Pueblo”** where all services will log their visits.
- Just like in real Cali, services from one neighborhood cannot directly reach another neighborhood unless explicitly connected.

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

### Step 1: Build your own service
Each student must create a **simple service** that:
1. Listens on port `8080`.
2. Responds with a message like:
   ```
   Hola, I am <YourName> and I live in <Neighborhood>
   ```
3. Logs every request into `/var/log/app/visitas.log` (mounted from the shared volume).

---

### Step 2: Choose your tech stack
You are free to use **different languages or servers**. Here are examples:

#### 🔹 Python (Flask)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

#### 🔹 Node.js (Express)
```javascript
const express = require('express');
const fs = require('fs');
const app = express();

const student = process.env.STUDENT_NAME || "Anon";
const hood = process.env.BARRIO || "Unknown";

app.get('/', (req, res) => {
  const msg = `Hola, I am ${student} and I live in ${hood}`;
  fs.appendFileSync('/var/log/app/visitas.log', msg + '\n');
  res.send(msg);
});

app.listen(8080, () => console.log("Server running on 8080"));
```

#### 🔹 Nginx (Static HTML)
1. Create an `index.html`:
   ```html
   <h1>Hola, I am Ana and I live in San Antonio</h1>
   ```
2. Dockerfile:
   ```Dockerfile
   FROM nginx:alpine
   COPY index.html /usr/share/nginx/html/index.html
   ```
*(Nginx won’t log custom messages to the volume by default, but it’s great for static responses.)*

---

### Step 3: Run your service in your neighborhood
Example:

```bash
docker build -t alumno-fredy:v1 .
docker run -d --name svc-fredy   --network san-antonio   -e STUDENT_NAME="Fredy"   -e BARRIO="San Antonio"   -v biblioteca-del-pueblo:/var/log/app   -p 0:8080 alumno-fredy:v1
```

---

### Step 4: Test connectivity
- From your host:
  ```bash
  curl http://localhost:<port>
  ```
- From another container in the same neighborhood:
  ```bash
  docker run --rm --network san-antonio curlimages/curl     -s http://svc-fredy:8080/
  ```

---

### Step 5: Check “La Biblioteca del Pueblo”
See everyone’s logs:
```bash
docker run --rm -v biblioteca-del-pueblo:/data alpine   sh -c "tail -n 20 /data/visitas.log"
```

---

## ✅ What you will learn
- How **Docker networks** isolate and connect services.
- How **volumes** allow sharing and persistence of data.
- How to build containers in **different tech stacks**.
- How collaboration looks when multiple services write to the same shared space.

---

# 📌 Deliverables
- A working container in your chosen neighborhood.
- Evidence that your service wrote to **La Biblioteca del Pueblo**.
- Short explanation of your design choice (Python, Node.js, Nginx, etc).

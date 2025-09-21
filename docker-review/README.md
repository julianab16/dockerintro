# 📘 README — *Cali NGINX Log Demo*

Learn Docker **networks** and **volumes** with a tiny NGINX image that writes **real files** into a shared volume (no bind mounts for config). Perfect for live classes: you can show container IPs, network isolation, and persistent logs in minutes.

---

## 🎯 What you’ll demonstrate
- Run a **prebuilt container image** that you extend via a **Dockerfile** .
- Use a **Docker network** to isolate/enable container-to-container traffic.
- Use a **Docker volume** to persist and share **real log files** .
- Inspect **JSON metadata** of containers, networks, and volumes from the CLI.

---

## 🧱 Project layout
```
docker-review/
├─ Dockerfile
└─ nginx.conf
```

## 🚀 Step‑by‑step demo

### 0) Build the image
```bash
docker build -t nginx-demo:v1 .
```

### 1) Create a network and a volume
```bash
docker network create demo-net
docker volume create demo-logs
```

### 2) Run the container (no ports exposed yet)
```bash
docker rm -f web 2>/dev/null || true
docker run -d --name web \
  --network demo-net \
  -v demo-logs:/var/log/nginx-files \
  nginx-demo:v1
```

### 3) Generate traffic (from another container on the same network)
```bash
docker run --rm --network demo-net curlimages/curl -s http://web/
docker run --rm --network demo-net curlimages/curl -s http://web/
```

### 4) Read the **real** log files from the volume
```bash
docker run --rm -v demo-logs:/v alpine sh -c "ls -l /v && tail -n 50 /v/access.log"
```

### 5) (Optional) Expose to host for browser testing
```bash
docker rm -f web
docker run -d --name web \
  --network demo-net \
  -v demo-logs:/var/log/nginx-files \
  -p 8080:80 \
  nginx-demo:v1

curl -s http://localhost:8080/
docker run --rm -v demo-logs:/v alpine tail -n 20 /v/access.log
```

---

## 🔎 Inspect like a pro (JSON & filters)

### Container metadata (full JSON)
```bash
docker inspect web | jq .
```

### Container IP on `demo-net`
```bash
docker inspect -f '{{ (index .NetworkSettings.Networks "demo-net").IPAddress }}' web
```

### All networks & IPs for this container
```bash
docker inspect -f '{{range $k,$v := .NetworkSettings.Networks}}{{printf "%s\t%s\n" $k $v.IPAddress}}{{end}}' web
```

### Live stats, processes, ports
```bash
docker stats web            # CPU/MEM/NET IO live
docker top web              # processes inside the container
docker port web             # published ports (none if you didn't use -p)
docker logs -f web          # stdout/stderr from NGINX
```

---

## 🌐 Network commands you’ll use in class
```bash
docker network ls
docker network inspect demo-net | jq .
docker network inspect demo-net \
  | jq -r '.Containers | to_entries[] | "\(.value.Name)\t\(.value.IPv4Address)"'

# connect/disconnect existing containers
docker network connect demo-net some-container
docker network disconnect demo-net some-container
```

> Key idea: containers **see each other by name** only if they are on the **same network** (built‑in DNS). Networks isolate services by default.

---

## 💾 Volume commands (persistence & backup)
```bash
docker volume ls
docker volume inspect demo-logs | jq .

# Read files from the volume using a throwaway container
docker run --rm -v demo-logs:/v alpine ls -l /v

# Quick backup/restore of the volume
docker run --rm -v demo-logs:/data -v "$PWD":/backup busybox \
  sh -c 'tar czf /backup/demo-logs.tgz -C /data .'

docker run --rm -v demo-logs:/data -v "$PWD":/backup busybox \
  sh -c 'cd /data && tar xzf /backup/demo-logs.tgz'
```

> Volumes are **managed by Docker** (portable and decoupled from host paths), making demos predictable across machines.

---

## 💡 Talking points & benefits of Docker (for your slide)
- **Isolation by default**: networks create safe “neighborhoods”; only what you expose is reachable.
- **Reproducibility**: the same image runs the same way everywhere (classroom, CI, prod).
- **Fast iteration**: spin up clean environments in seconds; no host pollution.
- **Portability of data**: volumes keep logs and state outside container lifecycles.
- **Observability**: simple CLI gives you JSON metadata and live stats (`inspect`, `logs`, `stats`).
- **Security knobs**: run as non‑root, read‑only mounts (`:ro`), resource limits (`--cpus`, `--memory`).

---

## 🧹 Cleanup
```bash
docker rm -f web
docker network rm demo-net
docker volume rm demo-logs
```

# FastAPI Blog DevOps Project

A beginner-friendly FastAPI blog application with PostgreSQL, Docker, Kubernetes, GitHub Actions, and monitoring support.

## Project Overview

This project contains:
- `backend/`: FastAPI application with models, authentication, routes, and tests.
- `frontend/`: Static HTML, CSS, and JavaScript to call the API.
- `Dockerfile`: Container image for FastAPI.
- `docker-compose.yml`: Local stack with FastAPI, PostgreSQL, and Nginx.
- `nginx.conf`: Reverse proxy configuration.
- `k8s/`: Kubernetes manifests for deployment.
- `.github/workflows/`: CI and CD workflow files.

## Folder Structure

```
backend/
  app/
    main.py
    database.py
    models.py
    schemas.py
    auth.py
    dependencies.py
    config.py
    routes/
      posts.py
      comments.py
      users.py
  tests/
    test_api.py
  requirements.txt
  Dockerfile
frontend/
  index.html
  style.css
  app.js
docker-compose.yml
nginx.conf
k8s/
  deployment.yaml
  service.yaml
  ingress.yaml
.github/workflows/
  ci.yml
  cd.yml
README.md
```

## Local Setup

1. Install Python 3.11.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Start PostgreSQL locally and set `DATABASE_URL` if needed.
4. Run the app:
   ```bash
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Open `frontend/index.html` in a browser or serve it from a simple static server.

## Docker Setup

Build and run locally:
```bash
docker compose up --build
```

This creates:
- `postgres` database service
- `fastapi` app service
- `nginx` reverse proxy service

## Kubernetes Deployment

Apply the manifests:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## AWS Deployment

1. Launch an EC2 instance (Ubuntu).
2. SSH into the instance.
3. Install Docker:
   ```bash
   sudo apt update
   sudo apt install -y docker.io
   sudo systemctl enable --now docker
   sudo usermod -aG docker $USER
   ```
4. Install k3s:
   ```bash
   curl -sfL https://get.k3s.io | sh -
   ```
5. Install kubectl locally:
   ```bash
   sudo snap install kubectl --classic
   ```
6. Install Nginx ingress on k3s:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.1/deploy/static/provider/cloud/deploy.yaml
   ```
7. Deploy manifests with kubectl.

## CI/CD Workflow

- `ci.yml`: runs on GitHub pushes and pull requests.
  - `flake8`
  - `pytest`
  - `docker build`
  - `docker push`
- `cd.yml`: runs on `main` branch using a self-hosted runner.
  - applies Kubernetes manifests with `kubectl`

## Monitoring Setup

This project uses `prometheus-fastapi-instrumentator` to expose metrics.
Prometheus, Grafana, and Loki can be installed with Helm on your cluster.

## API Endpoints

- `POST /register`
- `POST /api/token`
- `GET /posts`
- `POST /posts`
- `GET /posts/{id}`
- `DELETE /posts/{id}`
- `GET /posts/{id}/comments`
- `POST /posts/{id}/comments`
- `GET /health`
- `GET /readiness`

## Screenshots

Add screenshots here:
- `C:\MRsoftware\data\image.png`
- `C:\MRsoftware\data\image1.png`

# Docker Project 2 — Multi-Container Application

## Objective

Build and run a multi-container application using Docker networking and Docker Compose.

The application contains:

- Flask — backend application
- Redis — data store used for the visitor counter

The main Docker concepts demonstrated are:

- Docker images
- Docker containers
- Docker networks
- Container-to-container communication
- Port mapping
- Docker Compose

---

## Architecture

The project demonstrates two approaches for running the same multi-container application:

1. Manual Docker networking
2. Docker Compose

![Docker Project 2 Architecture](./architecture-diagram.png)

### Application Flow

```text
Browser
   ↓
localhost:5000
   ↓
Flask Container
   ↓
Docker Network
   ↓
Redis Container
   ↓
Visitor Count Response

---

## Project Structure

```text
docker-project-2/
├── Dockerfile
├── app.py
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

# Method 1 — Manual Docker

In the first approach, the containers were created and connected manually.

## Step 1 — Build Flask Image

### Generic Syntax

```bash
docker build -t <image-name>:<tag> <build-context>
```

### Command Used

```bash
docker build -t docker-project-2:v1 .
```

---

## Step 2 — Create Docker Network

### Generic Syntax

```bash
docker network create <network-name>
```

### Command Used

```bash
docker network create docker-project-2-network
```

This creates a custom Docker bridge network for communication between the containers.

---

## Step 3 — Run Redis Container

### Generic Syntax

```bash
docker run -d --name <container-name> --network <network-name> <image-name>
```

### Command Used

```bash
docker run -d --name redis --network docker-project-2-network redis
```

Redis was attached to the custom Docker network.

Redis did not need to be exposed to the host because it only needed to communicate with the Flask container.

---

## Step 4 — Run Flask Container

### Generic Syntax

```bash
docker run -d --name <container-name> --network <network-name> -p <host-port>:<container-port> <image-name>:<tag>
```

### Command Used

```bash
docker run -d --name flask-app --network docker-project-2-network -p 5000:5000 docker-project-2:v1
```

This maps:

```text
Host Port 5000 → Container Port 5000
```

---

## Step 5 — Verify Containers

### Generic Syntax

```bash
docker ps
```

### Command Used

```bash
docker ps
```

Both containers should be running:

```text
flask-app
redis
```

---

## Step 6 — Verify Docker Network

### Generic Syntax

```bash
docker network inspect <network-name>
```

### Command Used

```bash
docker network inspect docker-project-2-network
```

The network should contain:

```text
flask-app
redis
```

This confirms that both containers are connected to the same Docker network.

---

## Step 7 — Test Application

Open:

```text
http://localhost:5000
```

The application displays the visitor count.

Refreshing the page increases the visitor count because Flask communicates with Redis through the Docker network.

---

# Method 2 — Docker Compose

After understanding the manual approach, Docker Compose was used to manage the same multi-container application.

Instead of manually creating the network and starting each container, the configuration is defined in:

```text
docker-compose.yml
```

---

## Docker Compose Configuration

```yaml
services:

  flask-app:
    build: .
    container_name: flask-app
    ports:
      - "5000:5000"
    depends_on:
      - redis

  redis:
    image: redis:latest
    container_name: redis
```

---

## Start Application with Compose

### Generic Syntax

```bash
docker compose up -d
```

### Command Used

```bash
docker compose up -d
```

Docker Compose:

1. Builds the Flask image
2. Pulls the Redis image
3. Creates the application network
4. Creates the Flask container
5. Creates the Redis container
6. Connects both services to the Compose network

---

## Verify Compose Services

### Generic Syntax

```bash
docker compose ps
```

### Command Used

```bash
docker compose ps
```

The expected services are:

```text
flask-app
redis
```

---

## Test Application

Open:

```text
http://localhost:5000
```

The application should display the visitor count.

---

# Manual Docker vs Docker Compose

| Manual Docker | Docker Compose |
|---|---|
| Network created manually | Network managed by Compose |
| Containers started manually | Services started together |
| Multiple commands required | Single Compose command |
| Configuration spread across commands | Configuration stored in YAML |
| Useful for understanding Docker fundamentals | Useful for managing multi-container applications |

---

# Important Docker Concepts Learned

## Docker Network

A Docker network allows containers to communicate with each other.

### Manual Approach

```text
docker-project-2-network
        ↓
Flask Container
        ↕
Redis Container
```

### Compose Approach

Docker Compose automatically creates a network for the application.

---

## Container-to-Container Communication

Flask communicates with Redis using:

```text
redis:6379
```

The Flask container does not need to know the Redis container's IP address.

Docker's internal networking and DNS allow the service/container name to be used.

---

## Port Mapping

Flask uses:

```text
5000:5000
```

Meaning:

```text
Host Port 5000 → Container Port 5000
```

The application is accessed through:

```text
http://localhost:5000
```

Redis does not need host port mapping because it is only accessed by the Flask container through the Docker network.

---

# Useful Commands

### List Docker images

```bash
docker images
```

### List running containers

```bash
docker ps
```

### List all containers

```bash
docker ps -a
```

### List Docker networks

```bash
docker network ls
```

### Inspect a network

```bash
docker network inspect <network-name>
```

### Stop a container

```bash
docker stop <container-name>
```

### Remove a container

```bash
docker rm <container-name>
```

### Start Compose application

```bash
docker compose up -d
```

### Check Compose services

```bash
docker compose ps
```

### Stop Compose application

```bash
docker compose down
```

---

# Complete Docker Workflow

## Manual Approach

```text
Application
    ↓
Dockerfile
    ↓
Docker Image
    ↓
Create Docker Network
    ↓
Run Redis Container
    ↓
Run Flask Container
    ↓
Connect Containers
    ↓
Test Application
```

## Docker Compose Approach

```text
Application
    ↓
Dockerfile + docker-compose.yml
    ↓
docker compose up -d
    ↓
Flask Container + Redis Container
    ↓
Compose Network
    ↓
Test Application
```

---

# Skills Learned

- Docker image creation
- Docker containers
- Dockerfile
- Docker bridge networks
- Container-to-container communication
- Port mapping
- Redis container
- Flask application container
- Docker Compose
- Multi-container application management
- Docker troubleshooting

---

# Project Result

A multi-container application was successfully deployed using two approaches:

1. Manual Docker networking and container management
2. Docker Compose

The Flask application successfully communicated with the Redis container through a Docker network.

## Project Status

Completed ✅

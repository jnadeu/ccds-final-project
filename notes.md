# NOTES TO DO THE PROJECT

To implement the project outlined in the document, here's a step-by-step plan to help you build the required infrastructure and deliver the expected results.

---

### **1. Understanding the Requirements**
You need to containerize and deploy a company’s digital infrastructure into microservices using Docker. The project involves three main stacks:
- **Basic services** (shared infrastructure components)
- **App** (a core microservices application)
- **Atenea** (a Learning Management System, specifically Moodle)

Deployment must support **local development** and **production** environments, leveraging **Docker Swarm** for scaling and high availability.

---

### **2. Tools and Environment Setup**
#### **Required Tools:**
- **Docker:** For building and running containers.
- **Docker Compose:** To define multi-container applications.
- **Docker Swarm:** For clustering and orchestration.
- **Volume Sharing Technology:** For shared storage between nodes (e.g., NFS).

#### **Infrastructure Requirements:**
- At least three nodes for Docker Swarm.
- Shared storage mechanism (e.g., NFS, GlusterFS).
- Basic Linux/UNIX environment (can be virtualized).

#### **Environment Options:**
- Local deployment (laptop/PC with VMs or Docker Desktop).
- On-premises (e.g., Raspberry Pi cluster).
- Cloud provider (e.g., AWS, Google Cloud, Azure).

---

### **3. Implementation Plan**
#### **Step 1: Setup the Development Environment**
- Install Docker and Docker Compose on your local machine.
- Set up a minimal Docker Swarm cluster for local testing:
  ```bash
  docker swarm init
  docker swarm join-token worker
  ```
- Define a **basic compose.yml** for local development:
  - No TLS.
  - Simple volume mapping.
  - Use local Docker registry or Docker Hub.

#### **Step 2: Configure Basic Stack**
1. **Frontend/Proxy:** 
   - Use **nginx** or **Apache** for reverse proxy.
   - Integrate with Let’s Encrypt for TLS in production (`letsencrypt` service).
2. **Container Registry:** 
   - Use Docker’s own registry or a cloud-based alternative.
3. **NFS/Shared Storage:** 
   - Use a shared filesystem to persist application data across nodes.

Create `docker-compose.basic.yml`:
```yaml
version: '3.8'
services:
  proxy:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
  letsencrypt:
    image: certbot/certbot
  registry:
    image: registry:2
    ports:
      - "5000:5000"
  nfs:
    image: itsthenetwork/nfs-server-alpine
    volumes:
      - ./shared:/nfsshare
```

---

#### **Step 3: Configure App Stack**
1. **Core Application:**
   - Use a Python application (Flask/Django) as the core service.
   - Include necessary Dockerfile.
2. **Database Cluster:**
   - Deploy a clustered DBMS (e.g., PostgreSQL or MariaDB Galera Cluster).
3. **Static Files:** 
   - Serve static content using Apache or Nginx.
4. **Cache Layer:** 
   - Integrate Redis.
5. **SMTP Service:**
   - Forward emails using a lightweight SMTP server (e.g., `msmtp-mta`).

Create `docker-compose.app.yml`:
```yaml
version: '3.8'
services:
  core-app:
    build: ./core-app
    ports:
      - "8000:8000"
  db-cluster:
    image: mariadb:latest
    environment:
      - MYSQL_ROOT_PASSWORD=example
    deploy:
      replicas: 3
  redis:
    image: redis:latest
  smtp:
    image: bytemark/smtp
```

---

#### **Step 4: Configure Atenea Stack**
1. **Moodle LMS:**
   - Deploy the Moodle application with its database.
   - Use MySQL/MariaDB for the database.
2. **Volumes:**
   - Use volumes to persist data.

Create `docker-compose.atenea.yml`:
```yaml
version: '3.8'
services:
  moodle:
    image: moodle:latest
    ports:
      - "8080:80"
    volumes:
      - ./moodledata:/var/www/moodledata
  moodle-db:
    image: mariadb:latest
    environment:
      - MYSQL_ROOT_PASSWORD=moodlepass
```

---

#### **Step 5: Prepare Production Deployment**
- Create `production.yml`:
  - Add TLS configurations (e.g., Let’s Encrypt).
  - Use external storage for persistence.
  - Define scaling for Docker Swarm.
- Example for Swarm deployment:
  ```bash
  docker stack deploy -c production.yml my-infrastructure
  ```

---

### **4. Documentation**
1. **How-to Guide:**
   - Describe steps to deploy and manage the services.
   - Include commands for building and deploying containers.
2. **Backup Management:**
   - Define a strategy for backing up critical data (e.g., DB backups, Moodle data).
3. **Scalability Considerations:**
   - Highlight limitations and scaling strategies for specific services.
4. **Additional Notes:**
   - Explain any decisions (e.g., why Redis for caching, MariaDB for Moodle).

---

### **5. Testing and Delivery**
- Validate both local and production deployments.
- Ensure services are scalable and fault-tolerant.
- Deliver the following:
  - `compose.yml` and `production.yml` files.
  - Dockerfiles for custom services.
  - Backup and operational documentation.

This structure should help you implement and deliver the project effectively!


-----------

# Step 1

Here’s how to install **Docker** and **Docker Compose** on your local machine. The steps depend on your operating system:

---

### **For Linux (Ubuntu/Debian)**

#### **Step 1: Install Docker**
1. **Update your package list**:
   ```bash
   sudo apt update
   ```
2. **Install required dependencies**:
   ```bash
   sudo apt install -y ca-certificates curl gnupg
   ```
3. **Add Docker’s GPG key**:
   ```bash
   sudo mkdir -m 0755 -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   ```
4. **Set up the Docker repository**:
   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
5. **Install Docker Engine**:
   ```bash
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
6. **Verify the installation**:
   ```bash
   docker --version
   ```

#### **Step 2: Install Docker Compose**
Docker Compose is now included in Docker’s installation as a plugin. You can verify it with:
```bash
docker compose version
```

---

### **For Windows**

1. **Download Docker Desktop**:
   - Go to [Docker Desktop](https://www.docker.com/products/docker-desktop) and download the installer for Windows.
2. **Install Docker Desktop**:
   - Run the installer and follow the instructions.
3. **Enable WSL2 Backend**:
   - Ensure that WSL2 is enabled for better performance.
   - If not installed, download and install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install).
4. **Verify Docker and Docker Compose**:
   Open a terminal and run:
   ```bash
   docker --version
   docker compose version
   ```

---

### **For macOS**

1. **Download Docker Desktop**:
   - Go to [Docker Desktop](https://www.docker.com/products/docker-desktop) and download the macOS installer.
2. **Install Docker Desktop**:
   - Open the `.dmg` file and drag Docker to the Applications folder.
3. **Run Docker Desktop**:
   - Start Docker Desktop from your Applications folder.
4. **Verify Docker and Docker Compose**:
   Open a terminal and run:
   ```bash
   docker --version
   docker compose version
   ```

---

### **Post-Installation Steps**

#### **Add Current User to Docker Group (Linux only)**:
This allows you to run Docker without `sudo`:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

#### **Test Docker Installation**:
Run a test container:
```bash
docker run hello-world
```

#### **Test Docker Compose**:
Create a simple `docker-compose.yml`:
```yaml
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```
Run:
```bash
docker compose up
```
Access `http://localhost:8080` to confirm it works.

---

Let me know if you encounter any issues during installation!

-----------

# Step 2

-----------

Here’s an example of a **basic `compose.yml`** for local development that meets your requirements:

---

### **`compose.yml`**
```yaml
version: '3.8'

services:
  # Frontend service using Nginx
  proxy:
    image: nginx:latest
    ports:
      - "8080:80"  # Expose port 8080 for local development
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf  # Mount local config file
    depends_on:
      - app

  # Core application service
  app:
    image: my-core-app:latest  # Replace with your app image
    build:
      context: ./app  # Dockerfile location for your core app
    environment:
      - ENV=development  # Local development environment
    volumes:
      - ./app:/app  # Mount app code for development
    ports:
      - "8000:8000"  # App port exposed for debugging

  # Database service
  db:
    image: mariadb:latest  # Use MariaDB for development
    environment:
      - MYSQL_ROOT_PASSWORD=example
      - MYSQL_DATABASE=dev_db
      - MYSQL_USER=dev_user
      - MYSQL_PASSWORD=dev_password
    volumes:
      - db_data:/var/lib/mysql  # Persist database data

  # Redis cache
  redis:
    image: redis:latest
    ports:
      - "6379:6379"  # Default Redis port for local use

volumes:
  db_data:
    driver: local  # Local volume for DB persistence
```

---

### **Features of This Compose File**
1. **No TLS**:
   - The Nginx proxy does not use HTTPS/TLS in this setup, simplifying local development.

2. **Volume Mapping**:
   - Static files and application code are mounted from the host using `volumes` for easy local edits.
   - A persistent local volume (`db_data`) is used for the database.

3. **Local Registry**:
   - The `image` fields reference either:
     - **Local Docker images** (e.g., `my-core-app:latest`) built from a `Dockerfile` in the specified directory.
     - **Public images** from Docker Hub (e.g., `mariadb:latest`, `redis:latest`).

---

### **Local Development Steps**

#### 1. Build and Run
Run the following commands to set up and start the environment:
```bash
# Build all services
docker-compose build

# Start the services
docker-compose up
```

#### 2. Verify the Services
- **Proxy (Nginx)**: Open `http://localhost:8080` in your browser.
- **Core App**: Access the app directly on `http://localhost:8000`.
- **Database**: Use any MySQL client to connect to `localhost:3306`.
- **Redis**: Test connectivity on `localhost:6379`.

#### 3. Stop the Environment
Shut down all services:
```bash
docker-compose down
```

---

This setup provides a clean, functional environment for local development without the complexities of TLS or external dependencies. Let me know if you need help customizing it further!

-----------

# Step Create production.yml stack

-----------

Here’s a **`production.yml`** file that includes **TLS via Let’s Encrypt**, **external storage**, and is optimized for deployment on a **Docker Swarm** cluster with scaling.

---

### **`production.yml`**
```yaml
version: '3.8'

services:
  # Frontend/Reverse Proxy with TLS
  proxy:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    deploy:
      replicas: 3  # Scale proxy to 3 instances
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    volumes:
      - /etc/letsencrypt:/etc/letsencrypt  # Let’s Encrypt TLS certificates
      - ./nginx.conf:/etc/nginx/nginx.conf  # Custom Nginx config
    networks:
      - frontend
    depends_on:
      - app

  # Core Application
  app:
    image: my-core-app:latest
    build:
      context: ./app  # Use Dockerfile in ./app directory
    deploy:
      replicas: 5  # Scale app to 5 instances
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
    environment:
      - ENV=production
    volumes:
      - /data/app:/app  # External persistent storage for app data
    networks:
      - backend

  # Database Cluster
  db:
    image: mariadb:latest
    environment:
      - MYSQL_ROOT_PASSWORD=securepassword
      - MYSQL_DATABASE=prod_db
      - MYSQL_USER=prod_user
      - MYSQL_PASSWORD=prod_password
    deploy:
      replicas: 3  # Clustered database nodes
      placement:
        constraints:
          - node.role == manager  # Run DB on manager nodes
    volumes:
      - db_data:/var/lib/mysql  # Persistent data storage
    networks:
      - backend

  # Redis Cache
  redis:
    image: redis:latest
    deploy:
      replicas: 2  # Scale cache service
    volumes:
      - redis_data:/data  # Persistent Redis storage
    networks:
      - backend

  # Let’s Encrypt TLS Certificate Manager
  certbot:
    image: certbot/certbot
    command: renew
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
    volumes:
      - /etc/letsencrypt:/etc/letsencrypt
      - /var/log/letsencrypt:/var/log/letsencrypt
    networks:
      - frontend

volumes:
  db_data:
    driver: nfs
    driver_opts:
      share: nfs-server:/mnt/db_data  # NFS mount for database
  redis_data:
    driver: nfs
    driver_opts:
      share: nfs-server:/mnt/redis_data  # NFS mount for Redis
  app_data:
    driver: nfs
    driver_opts:
      share: nfs-server:/mnt/app_data  # NFS mount for app

networks:
  frontend:
    driver: overlay  # Overlay network for external access
  backend:
    driver: overlay  # Overlay network for internal communication
```

---

### **Features of This `production.yml`**

#### 1. **TLS with Let’s Encrypt**
- TLS certificates are stored in `/etc/letsencrypt`, and the **certbot** service periodically renews them.
- The Nginx proxy is configured to serve HTTPS traffic on port `443`.

#### 2. **External Storage for Persistence**
- **NFS** (Network File System) is used for persistent storage to ensure data consistency across the swarm nodes.
- Volumes (`db_data`, `redis_data`, `app_data`) are mounted using an external NFS server.

#### 3. **Scaling for Docker Swarm**
- Services like the **proxy**, **app**, and **redis** are scaled using the `replicas` field.
- Database replicas are constrained to **manager nodes** for reliability.

#### 4. **Swarm Networks**
- **Overlay networks** (`frontend` and `backend`) are used for communication:
  - `frontend` for public-facing services (e.g., proxy, certbot).
  - `backend` for internal services (e.g., app, db, redis).

#### 5. **Service Resilience**
- Deploy strategies like `restart_policy` and `update_config` ensure zero-downtime upgrades and recovery from failures.

---

### **Deployment Steps**

1. **Initialize Docker Swarm**:
   ```bash
   docker swarm init
   ```

2. **Deploy the Stack**:
   ```bash
   docker stack deploy -c production.yml my-stack
   ```

3. **Verify the Services**:
   - Check running services:
     ```bash
     docker service ls
     ```
   - Verify containers:
     ```bash
     docker ps
     ```

4. **Access Services**:
   - Use a browser to visit `https://your-domain` to verify the HTTPS setup.

---

This configuration ensures secure, scalable, and persistent production deployment on Docker Swarm. Let me know if you need further details!
Creating a Docker container with an **NFS shared disk** involves deploying a container that exports a directory over NFS, making it accessible to other systems or containers. Here's how to set up an **NFS server** using Docker.

---

### **Steps to Create an NFS Server in a Docker Container**

#### **1. Pull the `openebs/nfs-server-alpine` Image**
This is a lightweight and efficient NFS server image:
```bash
docker pull openebs/nfs-server-alpine
```

#### **2. Create a Directory for the Shared Disk**
On your host machine, create a directory that will be shared via NFS:
```bash
mkdir -p /path/to/shared/disk
```

#### **3. Run the NFS Server Container**
Start the NFS server container, binding the shared directory to `/nfsshare` inside the container:
```bash
docker run -d \
  --name nfs-server \
  -p 2049:2049 \
  -v /path/to/shared/disk:/nfsshare \
  openebs/nfs-server-alpine
```

- `-p 2049:2049`: Maps the NFS port from the container to the host.
- `-v /path/to/shared/disk:/nfsshare`: Mounts the host directory into the container as the shared NFS directory.

#### **4. Verify the NFS Server**
Check if the container is running:
```bash
docker ps
```

You should see `nfs-server` in the list of running containers.

---

### **Testing the NFS Server**

#### **1. Mount the NFS Share on the Host**
On a system that supports NFS (your host or another machine), mount the NFS share:
```bash
sudo mount -t nfs localhost:/nfsshare /mnt
```

- Replace `localhost` with the IP address of the host running the NFS server if testing from another machine.
- `/mnt` is the local mount point on the client.

#### **2. Verify File Access**
Navigate to `/mnt` and try creating a test file:
```bash
cd /mnt
touch testfile
ls -l
```
This verifies that the shared directory is accessible and writable.

---

### **Using Docker Compose to Deploy NFS Server**

If you prefer Docker Compose, here's how you can define it:

#### **docker-compose.yml**
```yaml
version: "3.8"

services:
  nfs-server:
    image: openebs/nfs-server-alpine
    container_name: nfs-server
    ports:
      - "2049:2049"  # NFS port
    volumes:
      - /path/to/shared/disk:/nfsshare
```

#### **Steps to Deploy**
1. Create the `docker-compose.yml` file.
2. Start the service:
   ```bash
   docker-compose up -d
   ```

---

### **Tips and Considerations**

1. **Firewall Configuration**:
   Ensure that the NFS port (2049) is open on the host firewall if accessing the share from external machines:
   ```bash
   sudo ufw allow 2049
   ```

2. **Persistent Data**:
   The `/path/to/shared/disk` directory on the host ensures that NFS data persists beyond the lifecycle of the container.

3. **Access Control**:
   Configure appropriate permissions for the `/path/to/shared/disk` directory to control access for clients.

4. **Testing Client Access in Another Container**:
   Run a container to act as a client and mount the NFS share:
   ```bash
   docker run -it --rm --privileged --mount type=volume,src=nfs-share,dst=/mnt alpine sh
   ```

This setup is a simple, robust way to provide a shared NFS disk using Docker. Let me know if you need additional help!
docker inspect --format '{{ .NetworkSettings.IPAddress }}' container


server {
    listen 80;
    server_name your_domain.com;  # Change this to your domain or IP address

    # Serve static files
    location /static/ {
        alias /usr/share/nginx/html/static/;  # Path to your static files
    }

    # Proxy to Core Application
    location /core/ {
        proxy_pass http://core_app:5000;  # Change the port based on your core app
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Proxy to Moodle Application
    location /moodle/ {
        proxy_pass http://moodle:80;  # Assuming Moodle is running on port 80
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Redirect all other requests to the frontend
    location / {
        proxy_pass http://frontend:80;  # Frontend service
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


project/
├── docker-compose.yml
├── frontend/
│   ├── nginx.conf  # Your Nginx configuration file
│   └── static/     # Directory for static files
├── core_app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
└── letsencrypt/
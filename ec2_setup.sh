#!/bin/bash

# Update system packages
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-dev nginx git

# Clone your repository (replace with your actual repo URL)
# git clone https://github.com/yourusername/your-repo.git
# cd your-repo

# Create and activate virtual environment
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-local.txt
pip install gunicorn

# Configure Gunicorn
sudo bash -c 'cat > /etc/systemd/system/gunicorn.service << EOL
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/WEBSITE/movies
ExecStart=/home/ubuntu/WEBSITE/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/WEBSITE/movies/movies.sock movies.wsgi:application

[Install]
WantedBy=multi-user.target
EOL'

# Configure Nginx
sudo bash -c 'cat > /etc/nginx/sites-available/movies << EOL
server {
    listen 80;
    server_name your_domain_or_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/WEBSITE/movies;
    }
    
    location /media/ {
        root /home/ubuntu/WEBSITE/movies;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/WEBSITE/movies/movies.sock;
    }
}
EOL'

# Enable the Nginx configuration
sudo ln -s /etc/nginx/sites-available/movies /etc/nginx/sites-enabled

# Collect static files
cd movies
python manage.py collectstatic --noinput

# Start services
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx

echo "Setup complete! Your website should be running now."